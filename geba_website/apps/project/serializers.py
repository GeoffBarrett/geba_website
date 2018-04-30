from .models import Project
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('title',
                  'image',
                  'image_caption',
                  'publish_date',
                  'draft')