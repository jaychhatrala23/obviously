from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import PersonFilter
from .models import Person
from .serializers import PersonSerializer, PersonSearchSerializer
from .permissions import IsAdminRole


class PersonViewSet(viewsets.ModelViewSet):
    # Efficient db querying by joining on role in single call, reduces number of db queries
    queryset = Person.objects.all().select_related('role')
    permission_classes = [IsAdminRole]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PersonFilter
    search_fields = ['first_name', 'last_name']

    def get_serializer_class(self):
        """
        Serializer class to handle various actions
        """
        if self.action in ["search"]:
            return PersonSearchSerializer
        else:
            return PersonSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def search(self, request):
        """
        Endpoint to filter persons by first_name, last_name, and age.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
