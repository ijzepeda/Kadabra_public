from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from apps.celebrity.document.schema import Faces
from apps.celebrity.models import ElasticSearchActorImage


def delete_index_actor_image(elastic_image):
    try:
        Faces().delete_by_document_id(str(elastic_image.id))
        if os.path.exists(elastic_image.actor_image.path):
            os.remove(elastic_image.actor_image.path)
    except ElasticSearchActorImage.DoesNotExist:
        pass


@receiver(post_delete, sender=ElasticSearchActorImage)
def actor_image_post_delete(sender, instance, **kwargs):
    delete_index_actor_image(instance)
