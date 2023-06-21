import os
import errno
import random
import time
from overrides import override
from apps.celebrity.enums import StatusEnum
from ms_data_mining.get_html import download_page
from ms_data_mining.inteface import InterfaceJob
from apps.celebrity.models import Actor, ActorImage
from django.conf import settings
from apps.celebrity.enums import KeywordsEnum
import cv2
import urllib.request
import numpy as np
import re
import emoji


class ActorJob(InterfaceJob):
    JOB_MODEL = Actor
    HAARCASCADE = ["haarcascade_frontalface_alt_tree.xml", "haarcascade_frontalface_alt.xml",
                   "haarcascade_frontalface_alt2.xml", "haarcascade_frontalface_default.xml"]

    @override
    def internal_process(self, item_id: str) -> bool:
        is_completed = True
        obj_actor = self.JOB_MODEL.objects.get(id=item_id)
        self.__get_massive_images(obj_actor)
        self.__get_complementary_information(obj_actor)
        return is_completed

    def __get_massive_images(self, actor: JOB_MODEL):
        search = actor.name.strip().replace(" ", "%20")

        try:
            os.makedirs(
                f"{settings.STATIC_ROOT}/images/celebrities/{actor.name.strip()}/IMDB")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            pass

        downloaded = self.__image_from_imdb(actor, 1)
        if not downloaded:
            self.__image_from_google(actor, search)

    def __identify_image(self, url):
        url = re.sub("V1_.+\.jpg", "V1_FMjpg_UX710_.jpg", url)

        req = urllib.request.urlopen(url)
        print("VALIDATE IMAGE: ", url, end=" ")
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)

        number_faces = []
        for item in self.HAARCASCADE:
            cascade = cv2.CascadeClassifier(f'apps/celebrity/jobs/haarcascade/{item}')
            img = cv2.imdecode(arr, -1)
            faces = cascade.detectMultiScale(image=img, scaleFactor=1.1,
                                             minNeighbors=5,
                                             minSize=(30, 30),
                                             flags=cv2.CASCADE_SCALE_IMAGE)
            number_faces.append(len(faces))

        if number_faces == [0, 1, 1, 1] or number_faces == [1, 1, 1, 1]:
            return True, [url]

        return False, None

    @staticmethod
    def __get_image(content):
        grid = content.find_all("div", class_="media_index_thumb_list")
        if grid:
            grid = grid[0]
        else:
            return []

        return [image[r'\nsrc'] for item in grid.find_all("a") for image in item.find_all('img')]

    def __image_from_imdb(self, actor, page):
        webpage = f"https://www.imdb.com/name/{actor.imdb_id}/mediaindex?page={page}"
        print("GET IMAGES IMDB:", webpage)

        content = download_page(webpage)
        images = self.__get_image(content)
        if not images:
            return []

        result = []

        for image in images:
            is_valid, _image = self.__identify_image(image)
            if is_valid:
                result += _image

                ActorImage.objects.update_or_create(
                    actor=actor,
                    keyword="IMDB",
                    url=_image[0],
                    defaults={"status": StatusEnum.READY},
                )
            print(emoji.emojize(":thumbs_up:") if is_valid else emoji.emojize(":collision:"))
        return result + self.__image_from_imdb(actor, page + 1)

    def __image_from_google(self, actor, search):
        for keyword in KeywordsEnum:
            try:
                os.makedirs(
                    f"{settings.STATIC_ROOT}/images/celebrities/{actor.name.strip()}/{keyword.replace(' ', '')}")
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                pass

            pure_keyword = keyword.replace(" ", "%20")
            url = f"https://www.google.com/search?q={search}{pure_keyword}&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg"
            print("GET IMAGES GOOGLE:", url)
            raw_html = download_page(url)
            time.sleep(random.randint(1, 4))
            items = self.__images_get_all_items(raw_html)

            for item in items:
                is_valid, _image = self.__identify_image(item)
                if is_valid:
                    ActorImage.objects.update_or_create(
                        actor=actor,
                        keyword=keyword,
                        url=_image[0],
                        defaults={"status": StatusEnum.READY},
                    )
                print(emoji.emojize(":thumbs_up:") if is_valid else emoji.emojize(":collision:"))

    @staticmethod
    def __images_get_all_items(page):
        return [content["src"] for content in page.find_all("img", class_="yWs4tf")]

    @staticmethod
    def __get_complementary_information(obj_actor):
        try:
            url = f"https://www.imdb.com/name/{obj_actor.imdb_id.replace(' ', '%20')}"
            raw_html = download_page(url)
            time.sleep(random.randint(1, 4))
            items = list(set([content.text for content in raw_html.find_all("span", class_="sc-dec7a8b-2 haviXP") if
                              content.text != "Born"]))

            for item in items:
                obj_actor.birthday = item
                obj_actor.save()
        except Exception as ex:
            print(ex)
