from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from vectordb import vectordb

from .filters import PersonFilter
from .models import Person
from .search_backend import elasticsearch_persons
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

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def vector_search(self, request):
        """
        Endpoint to query Person model instances from the vectorized database from the given query string.
        """
        query = request.query_params.get('q', None)
        if not query:
            return Response({"error": "Query parameter 'q' is required."}, status=status.HTTP_400_BAD_REQUEST)

        results = vectordb.search(query, k=5).unwrap()

        # An exension example to query through specific meta data
        # results = vectordb.filter(text__icontains=query).search('ell', k=5).unwrap()

        serializer = PersonSerializer(results, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def elastic_search(self, request):
        """
        Endpoint to fizzy search Person model instances from the Elasticsearch's Person Document
        using the given query string.
        """
        query = request.query_params.get('q', None)
        if not query:
            return Response({"error": "Query parameter 'q' is required."}, status=status.HTTP_400_BAD_REQUEST)
        results = elasticsearch_persons(query)
        serializer = PersonSearchSerializer(results, many=True)
        return Response(serializer.data)
