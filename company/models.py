from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class TimeStampedModel(models.Model):  # опционально, для поддержания истории изменений
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):  # во имя производительности возможно отказаться там, где это излишне
    id = models.UUIDField(db_column='id', primary_key=True, default=uuid4, editable=False, unique=True, blank=True)

    class Meta:
        abstract = True


class Department(UUIDModel, TimeStampedModel):
    name = models.CharField(_('name'), max_length=255)
    head = models.ForeignKey('Person', db_column='head_id', on_delete=models.PROTECT, related_name='hdepartment')

    class Meta:
        verbose_name = _('department')
        verbose_name_plural = _('departments')
        db_table = 'company\".\"department'

    def __str__(self):
        return self.name


class PersonDepartment(UUIDModel):
    person = models.ForeignKey('Person', db_column='person_id', on_delete=models.CASCADE)
    department = models.ForeignKey('Department', db_column='department_id', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'company\".\"person_department'
        constraints = [
            models.UniqueConstraint(fields=['person', 'department'], name='unique_person_department')
        ]


class Position(models.TextChoices):  # в зависимости от размера и частоты обновления мб Модель
    ARCHITECT = 'architect', _('architect')
    LEAD = 'lead', _('lead')
    DEVELOPER = 'developer', _('developer')
    MANAGER = 'manager', _('manager')


class Person(UUIDModel, TimeStampedModel):
    fullname = models.CharField(_('fullname'), max_length=511)
    foto = models.FileField(_('foto'), upload_to='persons/', null=True, blank=True)
    salary = models.FloatField(_('salary'), validators=[MinValueValidator(0)], null=True, blank=True)
    age = models.IntegerField(_('age'), validators=[MinValueValidator(16)], null=True, blank=True)
    position = models.CharField(_('position'), max_length=30, choices=Position.choices)
    department = models.ManyToManyField(Department, through='PersonDepartment', related_name='persons')

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        db_table = 'company\".\"person'

    def __str__(self):
        return self.fullname
