from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Course
from django.conf import settings
User = settings.AUTH_USER_MODEL


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
        # def get_queryset(self):
        #     return super(CourseDocument, self).get_queryset().select_related(
        #         'tutor'
        #     )
        # def get_instances_from_related(self, related_instance):
        #     if isinstance(related_instance, User):
        #         return related_instance.course_set.all()


 