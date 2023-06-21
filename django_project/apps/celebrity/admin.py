from django.contrib import admin, messages
from constance import config
from rangefilter.filters import DateRangeFilter
from django.utils.translation import ngettext
from apps.celebrity.jobs.ActorImageJob import ActorImageJob
from apps.celebrity.jobs.ActorJob import ActorJob
from apps.celebrity.jobs.ElasticsearchJob import ElasticsearchJob
from apps.celebrity.models import Actor, ActorImage, ElasticSearchActorImage
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django_admin_inline_paginator.admin import TabularInlinePaginated


def get_picture_preview(obj):
    if obj.pk:
        return format_html(
            f'<img src="{obj.url}" height="{config.CONFIG_ADMIN_LISTING_IMAGE_HEIGHT}"/>'
        )
    return "(No image)"


get_picture_preview.short_description = "Image"


class ActorImageAdminInline(admin.TabularInline):
    model = ActorImage
    raw_id_fields = ("actor",)
    show_change_link = True
    readonly_fields = ["path", "keyword", "attempt", get_picture_preview]
    classes = [
        "collapse",
    ]
    fields = [get_picture_preview, "keyword", "is_valid"]
    extra = 0

    def get_queryset(self, request):
        qs = super(ActorImageAdminInline, self).get_queryset(request)
        return qs.filter(is_valid=True)


class ActorResource(resources.ModelResource):
    class Meta:
        model = Actor


class ActorImageResource(resources.ModelResource):
    class Meta:
        model = ActorImage


@admin.register(Actor)
class ActorAdmin(ImportExportModelAdmin):
    list_per_page = config.CONFIG_ADMIN_LIMIT
    readonly_fields = (
        "created",
        "updated",
        "id",
    )
    list_display = (
        "id",
        "name",
        "slug",
        "status",
        "attempt",
        "created",
    )
    search_fields = (
        "id",
        "name",
        "slug",
    )
    list_filter = (("created", DateRangeFilter), "status")
    inlines = (ActorImageAdminInline,)
    resource_class = ActorResource
    actions = [
        "process",
    ]

    def process(self, request, queryset):
        count = queryset.count()
        for item in queryset:
            ActorJob(0, 1, item.id).process()

        self.message_user(
            request,
            ngettext(
                "%d celebrity was successfully executed.",
                "%d celebrities were successfully executed.",
                count,
            )
            % count,
            messages.SUCCESS,
        )

    process.allowed_permissions = ["view"]
    process.short_description = "Process"


@admin.register(ActorImage)
class ActorImageAdmin(ImportExportModelAdmin):
    list_per_page = config.CONFIG_ADMIN_LIMIT
    readonly_fields = (
        "created",
        "updated",
        "id",
        "thumbnail",
    )
    list_display = (
        "id",
        "thumbnail",
        "is_valid",
        "actor",
        "keyword",
        "status",
        "attempt",
        "created",
    )
    search_fields = (
        "id",
    )
    list_filter = (("created", DateRangeFilter), "keyword", "status", "is_valid")
    resource_class = ActorImageResource
    actions = [
        "process",
    ]

    @staticmethod
    def thumbnail(obj):
        return format_html(
            f'<img src="{obj.url}" height="{config.CONFIG_ADMIN_LISTING_IMAGE_HEIGHT}"/>'
        )

    def process(self, request, queryset):
        count = queryset.count()
        for item in queryset:
            ActorImageJob(0, 1, item.id).process()

        self.message_user(
            request,
            ngettext(
                "%d image was successfully executed.",
                "%d images were successfully executed.",
                count,
            )
            % count,
            messages.SUCCESS,
        )

    process.allowed_permissions = ["view"]
    process.short_description = "Process"


@admin.register(ElasticSearchActorImage)
class ElasticSearchActorImageAdmin(ImportExportModelAdmin):
    list_per_page = config.CONFIG_ADMIN_LIMIT
    readonly_fields = (
        "created",
        "updated",
        "id",
    )
    list_display = (
        "id",
        "status",
        "attempt",
        "created",
        "updated",
    )
    search_fields = (
        "id",
    )
    list_filter = (("created", DateRangeFilter), "status")
    actions = [
        "process",
    ]

    def process(self, request, queryset):
        count = queryset.count()
        for item in queryset:
            ElasticsearchJob(0, 1, item.id).process()

        self.message_user(
            request,
            ngettext(
                "%d document was successfully executed.",
                "%d documents were successfully executed.",
                count,
            )
            % count,
            messages.SUCCESS,
        )

    process.allowed_permissions = ["view"]
    process.short_description = "Process"
