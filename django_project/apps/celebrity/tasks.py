from celery import shared_task
from constance import config
import memory_profiler as mem_profile

from apps.celebrity.jobs.ActorImageJob import ActorImageJob
from apps.celebrity.jobs.ActorJob import ActorJob
from apps.celebrity.jobs.ElasticsearchJob import ElasticsearchJob


@shared_task(bind=True, name="actor_process")
def actor_process(self, size=100, attempts=config.CONFIG_ACTOR_ATTEMPTS, actor_id=None):
    print(
        f"{self.__class__.__name__} Memory (Before) : {mem_profile.memory_usage()} Mb"
    )

    ActorJob(size, attempts, actor_id).process()

    print(f"{self.__class__.__name__} Memory (After) : {mem_profile.memory_usage()} Mb")


@shared_task(bind=True, name="actor_process_long_task")
def actor_process_long_task(
        self, size=0, attempts=config.CONFIG_ACTOR_ATTEMPTS, actor_id=None
):
    print(
        f"{self.__class__.__name__} Memory (Before) : {mem_profile.memory_usage()} Mb"
    )

    ActorJob(size, attempts, actor_id).process_long_task()

    print(f"{self.__class__.__name__} Memory (After) : {mem_profile.memory_usage()} Mb")


@shared_task(bind=True, name="actor_process_error")
def actor_process_error(
        self, size=0, attempts=config.CONFIG_ACTOR_ATTEMPTS, actor_id=None
):
    print(
        f"{self.__class__.__name__} Memory (Before) : {mem_profile.memory_usage()} Mb"
    )

    ActorJob(size, attempts, actor_id).process_error()

    print(f"{self.__class__.__name__} Memory (After) : {mem_profile.memory_usage()} Mb")


@shared_task(bind=True, name="actor_image_process")
def actor_image_process(
        self, size=100, attempts=config.CONFIG_ACTOR_ATTEMPTS, actor_image_id=None
):
    print(
        f"{self.__class__.__name__} Memory (Before) : {mem_profile.memory_usage()} Mb"
    )

    ActorImageJob(size, attempts, actor_image_id).process()

    print(f"{self.__class__.__name__} Memory (After) : {mem_profile.memory_usage()} Mb")


@shared_task(bind=True, name="actor_image_process_long_task")
def actor_image_process_long_task(
        self, size=0, attempts=config.CONFIG_ACTOR_ATTEMPTS, actor_image_id=None
):
    print(
        f"{self.__class__.__name__} Memory (Before) : {mem_profile.memory_usage()} Mb"
    )

    ActorImageJob(size, attempts, actor_image_id).process_long_task()

    print(f"{self.__class__.__name__} Memory (After) : {mem_profile.memory_usage()} Mb")


@shared_task(bind=True, name="actor_image_process_error")
def actor_image_process_error(
        self, size=0, attempts=config.CONFIG_ACTOR_ATTEMPTS, actor_image_id=None
):
    print(
        f"{self.__class__.__name__} Memory (Before) : {mem_profile.memory_usage()} Mb"
    )

    ActorImageJob(size, attempts, actor_image_id).process_error()

    print(f"{self.__class__.__name__} Memory (After) : {mem_profile.memory_usage()} Mb")


@shared_task(bind=True, name="elasticsearch_process")
def elasticsearch_process(
        self, size=100, attempts=config.CONFIG_ACTOR_ATTEMPTS, document_id=None
):
    print(
        f"{self.__class__.__name__} Memory (Before) : {mem_profile.memory_usage()} Mb"
    )

    ElasticsearchJob(size, attempts, document_id).process()

    print(f"{self.__class__.__name__} Memory (After) : {mem_profile.memory_usage()} Mb")


@shared_task(bind=True, name="elasticsearch_process_long_task")
def elasticsearch_process_long_task(
        self, size=0, attempts=config.CONFIG_ACTOR_ATTEMPTS, document_id=None
):
    print(
        f"{self.__class__.__name__} Memory (Before) : {mem_profile.memory_usage()} Mb"
    )

    ElasticsearchJob(size, attempts, document_id).process_long_task()

    print(f"{self.__class__.__name__} Memory (After) : {mem_profile.memory_usage()} Mb")


@shared_task(bind=True, name="elasticsearch_process_error")
def elasticsearch_process_error(
        self, size=0, attempts=config.CONFIG_ACTOR_ATTEMPTS, document_id=None
):
    print(
        f"{self.__class__.__name__} Memory (Before) : {mem_profile.memory_usage()} Mb"
    )

    ElasticsearchJob(size, attempts, document_id).process_error()

    print(f"{self.__class__.__name__} Memory (After) : {mem_profile.memory_usage()} Mb")
