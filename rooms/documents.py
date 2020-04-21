from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Room

@registry.register_document
class RoomDocument(Document):
    class Index:
        name='rooms'
        settings= {'number_of_shards':1,'number_of_replicas':0}
    
    class Django:
        model = Room
        fields = [
            'title',
            'description',
        ]