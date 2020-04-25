from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Course
from django.conf import settings
User = settings.AUTH_USER_MODEL
from users.models import CustomUser
from django.shortcuts import get_object_or_404


@registry.register_document
class CourseDocument(Document):
    # tutor = fields.ObjectField(properties={
    #     'description':fields.TextField(),
    #     'title':fields.TextField(),
    #     'pk':fields.IntegerField(),
    # })
    class Index:
        name='courses'
        settings= {'number_of_shards':1,'number_of_replicas':0}
    
    class Django:
        model = Course
        fields = [
            'title',
            'description',
        ]
        # related_models = [User]
