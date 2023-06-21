from celery import shared_task
from constance import config
import memory_profiler as mem_profile
from apps.movies.jobs.MovieJob import MovieJob


@shared_task(bind=True, name="movie_process")
def movie_process(self, size=100, attempts=config.CONFIG_ACTOR_ATTEMPTS, movie_id=None):
    print(
        f"{self.__class__.__name__} Memory (Before) : {mem_profile.memory_usage()} Mb"
    )

    MovieJob(size, attempts, movie_id).process()

    print(f"{self.__class__.__name__} Memory (After) : {mem_profile.memory_usage()} Mb")


@shared_task(bind=True, name="movie_process_long_task")
def movie_process_long_task(
    self, size=0, attempts=config.CONFIG_ACTOR_ATTEMPTS, movie_id=None
):
    print(
        f"{self.__class__.__name__} Memory (Before) : {mem_profile.memory_usage()} Mb"
    )

    MovieJob(size, attempts, movie_id).process_long_task()

    print(f"{self.__class__.__name__} Memory (After) : {mem_profile.memory_usage()} Mb")


@shared_task(bind=True, name="movie_process_error")
def movie_process_error(
    self, size=0, attempts=config.CONFIG_ACTOR_ATTEMPTS, movie_id=None
):
    print(
        f"{self.__class__.__name__} Memory (Before) : {mem_profile.memory_usage()} Mb"
    )

    MovieJob(size, attempts, movie_id).process_error()

    print(f"{self.__class__.__name__} Memory (After) : {mem_profile.memory_usage()} Mb")
