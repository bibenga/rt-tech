from rest_framework import serializers

from company.models import Person, Department


class DepartmentSerializer(serializers.ModelSerializer):
    total_persons = serializers.IntegerField()
    total_salary = serializers.FloatField()

    class Meta:
        model = Department
        fields = ('id', 'name', 'head', 'total_persons', 'total_salary')


class DepartmentRelatedField(serializers.StringRelatedField):

    def to_representation(self, value):
        return value.id

    def to_internal_value(self, data):
        try:
            obj = Department.objects.get(id=data)
        except Department.DoesNotExist:
            raise serializers.ValidationError(f'Department {data} does not exists.')
        return obj


class PersonSerializer(serializers.ModelSerializer):
    department = DepartmentRelatedField(many=True, read_only=False)

    class Meta:
        model = Person
        fields = ('id', 'fullname', 'salary', 'age', 'position', 'department')
