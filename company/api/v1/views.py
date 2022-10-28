from django.db.models import Sum, Count

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from company.models import Person, Department
from .serializers import PersonSerializer, DepartmentSerializer
from ..validators import uuid_valid


class DepartmentViewSet(ReadOnlyModelViewSet):
    queryset = Department.objects.prefetch_related('persons')\
        .annotate(total_salary=Sum('persons__salary'), total_persons=Count('persons'))
    serializer_class = DepartmentSerializer
    pagination_class = None


class PersonViewSet(GenericViewSet):
    queryset = Person.objects.prefetch_related('department')
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        family_name = self.request.query_params.get('family_name', None)
        department_id = self.request.query_params.get('department_id', None)
        queryset = self.queryset
        if department_id:
            if uuid_valid(department_id):
                queryset = self.queryset.filter(department=department_id)
            else:
                queryset = Person.objects.none()
        if family_name:
            queryset = self.queryset.filter(fullname__icontains=family_name)
        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
