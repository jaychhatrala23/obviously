from django.apps import AppConfig


class PersonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "person"

    def ready(self):
        """
        Automates the syncing of Django Models with Vector db everytime data is created, updated or deleted
        """
        from .models import Person
        from vectordb.shortcuts import autosync_model_to_vectordb
        autosync_model_to_vectordb(Person)
