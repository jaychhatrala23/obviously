from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Person


@registry.register_document
class PersonDocument(Document):
    """
    Elasticsearch document mapping for the Person model.
    """
    full_name = fields.TextField(attr='full_name', fields={
        'raw': fields.KeywordField(),
        'suggest': fields.CompletionField(),
    })

    class Index:
        name = 'persons'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Person
        fields = []

    def prepare_full_name(self, instance):
        """Prepare the full name by combining first and last names."""
        return f"{instance.first_name} {instance.last_name}"
