from django.contrib import admin, messages
from constance import config
from rangefilter.filters import DateRangeFilter
from django.utils.translation import ngettext
from apps.movies.jobs.MovieJob import MovieJob
from apps.movies.models import Movie, MovieActor
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class MovieResource(resources.ModelResource):
    class Meta:
        model = Movie


class MovieActorAdminInline(admin.TabularInline):
    model = MovieActor
    raw_id_fields = ("actor",)
    show_change_link = True
    classes = [
        "collapse",
    ]
    fields = ["actor", ]
    extra = 0


@admin.register(Movie)
class MovieAdmin(ImportExportModelAdmin):
    list_per_page = config.CONFIG_ADMIN_LIMIT
    readonly_fields = (
        "created",
        "updated",
        "id",
    )
    list_display = (
        "id",
        "name",
        "starts_name",
        "status",
        "genre",
        "created",
    )
    search_fields = (
        "id",
        "name",
        "description",
        "imdb_id",
    )
    list_filter = (("created", DateRangeFilter), "status")
    resource_class = MovieResource
    inlines = (MovieActorAdminInline,)
    actions = [
        "process",
    ]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def process(self, request, queryset):
        count = queryset.count()
        for item in queryset:
            MovieJob(0, 1, item.id).process()

        self.message_user(
            request,
            ngettext(
                "%d movie was successfully executed.",
                "%d movies were successfully executed.",
                count,
            )
            % count,
            messages.SUCCESS,
        )

    process.allowed_permissions = ["view"]
    process.short_description = "Process"
