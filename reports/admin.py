from django.contrib import admin
from django.core.files.uploadedfile import UploadedFile

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "date", "owner")
    fields = ("name", "file", "date")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(owner=request.user)

        return qs

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if request.user.is_superuser:
            fields += ("owner",)

        return fields

    def save_model(self, request, obj, form, change):
        # set default owner upon creation
        if not change and obj.owner is None:
            obj.owner = request.user

        # update metatada fields on file change
        if issubclass(obj.file.file.__class__, UploadedFile):
            file = obj.file.file
            obj.file_content_type = file.content_type
            obj.file_size = file.size

        return super().save_model(request, obj, form, change)
