from django.contrib import admin

from src.django_project.task_app.models import Task

class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Task, UserAdmin)