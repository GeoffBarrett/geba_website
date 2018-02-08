from rest_framework import serializers
from .models import ModelName


class ModelNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModelName
        fields = ('')  # can include all fields, but if you want to only have certain ones...
        # fields = '__all__'
