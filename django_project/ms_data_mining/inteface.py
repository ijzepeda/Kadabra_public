import uuid
from django.utils import timezone
from django.db.models import F, Q
from apps.celebrity.enums import StatusEnum


class InterfaceJob:
    JOB_MODEL = None

    def __init__(self, size: int, attempt: int, job_id: uuid = None):
        self.size = size
        self.attempt = attempt
        self.job_id = str(job_id) if job_id else None
        self.lst_items = []
        if not self.JOB_MODEL:
            raise Exception("JOB_MODEL is missing")

    def process(self):
        if self.job_id is not None:
            query = Q(id=self.job_id)
        else:
            query = Q(status=StatusEnum.READY) & Q(attempt__lte=self.attempt)

        if self.size == 0:
            lst_prop = self.JOB_MODEL.objects.filter(query).order_by(
                "attempt", "created"
            )
        else:
            lst_prop = self.JOB_MODEL.objects.filter(query).order_by(
                "attempt", "created"
            )[: self.size]
        [self.lst_items.append({"id": str(item.id)}) for item in lst_prop]

        self.JOB_MODEL.objects.filter(
            id__in=list(map(lambda x: x["id"], self.lst_items))
        ).update(status=StatusEnum.RUNNING, updated=timezone.now())

        self.__process_item()

    def __process_item(self):
        for item in self.lst_items:
            try:
                is_completed = self.internal_process(item["id"])

                if is_completed:
                    self.JOB_MODEL.objects.filter(id=item["id"]).update(
                        status=StatusEnum.COMPLETED,
                        updated=timezone.now(),
                    )
            except Exception as ex:
                print(ex)
                self.JOB_MODEL.objects.filter(id=item["id"]).update(
                    status=StatusEnum.ERROR,
                    updated=timezone.now(),
                )

            self.update_task(item["id"])

    def internal_process(self, item_id: str) -> bool:
        pass

    def update_task(self, item_id: str):
        pass

    def __updated_item(self) -> None:
        for item in self.lst_items:
            self.update_task(item["id"])

    def process_expired(self):
        self.lst_items = []
        query = Q(status=StatusEnum.ERROR) & Q(attempt__gte=self.attempt)

        lst_prop = self.JOB_MODEL.objects.filter(query).order_by("created")

        [self.lst_items.append({"id": str(item.id)}) for item in lst_prop]

        self.JOB_MODEL.objects.filter(
            id__in=list(map(lambda x: x["id"], self.lst_items))
        ).update(
            status=StatusEnum.EXPIRED,
            updated=timezone.now(),
        )

    def process_error(self):
        if self.job_id is not None:
            query = Q(id=self.job_id)
        else:
            query = Q(status=StatusEnum.ERROR) & Q(attempt__lt=self.attempt)

        if self.size == 0:
            lst_prop = self.JOB_MODEL.objects.filter(query).order_by("created")
        else:
            lst_prop = self.JOB_MODEL.objects.filter(query).order_by("created")[
                : self.size
            ]

        [self.lst_items.append({"id": str(item.id)}) for item in lst_prop]

        self.JOB_MODEL.objects.filter(
            id__in=list(map(lambda x: x["id"], self.lst_items))
        ).update(
            status=StatusEnum.READY,
            attempt=F("attempt") + 1,
            updated=timezone.now(),
        )

        self.process_expired()
        self.__updated_item()

    def process_long_task(self):
        if self.job_id is not None:
            query = Q(id=self.job_id)
        else:
            query = Q(status=StatusEnum.RUNNING) & Q(
                updated__lte=(timezone.now() + timezone.timedelta(days=-1))
            )

        if self.size == 0:
            lst_prop = self.JOB_MODEL.objects.filter(query).order_by("created")
        else:
            lst_prop = self.JOB_MODEL.objects.filter(query).order_by("created")[
                : self.size
            ]

        [self.lst_items.append({"id": str(item.id)}) for item in lst_prop]

        self.JOB_MODEL.objects.filter(
            id__in=list(map(lambda x: x["id"], self.lst_items))
        ).update(
            status=StatusEnum.READY,
            attempt=0,
            updated=timezone.now(),
        )
        self.__updated_item()
