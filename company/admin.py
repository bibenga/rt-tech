from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet

from .models import Person, PersonDepartment, Department


class PersonDepartmentInline(admin.TabularInline):
    model = PersonDepartment
    extra = 0

    def get_queryset(self, request: Any) -> QuerySet[Any]:
        return super().get_queryset(request).select_related('department', 'person')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    inlines = [
        PersonDepartmentInline
    ]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('fullname',)
    list_display = ('fullname', 'salary', 'age', 'position', 'foto')
    list_filter = ('position', 'department')
    fields = (
        'fullname', 'salary', 'age', 'position', 'foto'
    )

    inlines = [
        PersonDepartmentInline
    ]
    exclude = ('department', 'person')
