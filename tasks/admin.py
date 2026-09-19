from django.contrib import admin

from .models import (
    Task,
    Category
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
    )



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'user',
        'category',
        'priority',
        'completed',
        'due_date',
    )


    list_filter = (
        'priority',
        'completed',
        'category',
    )


    search_fields = (
        'title',
        'description',
    )