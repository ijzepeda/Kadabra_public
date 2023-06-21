from overrides import override
import face_recognition
from apps.celebrity.document.schema import Faces
from apps.celebrity.models import ElasticSearchActorImage
from ms_data_mining.inteface import InterfaceJob


class ElasticsearchJob(InterfaceJob):
    JOB_MODEL = ElasticSearchActorImage

    @staticmethod
    def get_encoding(obj_actor_image):
        image = face_recognition.load_image_file(obj_actor_image.path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        return face_encodings

    @override
    def internal_process(self, item_id: str) -> bool:
        obj_elasticsearch = self.JOB_MODEL.objects.get(id=item_id)
        faces = Faces()
        face_encodings = self.get_encoding(obj_elasticsearch.actor_image)

        for face_encoding in face_encodings:
            data_dict = {
                "id": str(obj_elasticsearch.id),
                "name": obj_elasticsearch.actor_image.actor.name,
                "image_id": str(obj_elasticsearch.actor_image.id),
                "actor_id": str(obj_elasticsearch.actor_image.actor.id),
                "face_encoding": face_encoding.tolist()
            }

            if faces.check_by_document_id(item_id):
                faces.update_one(data_dict)
            else:
                faces.insert_one(data_dict)

            return True
        return False
