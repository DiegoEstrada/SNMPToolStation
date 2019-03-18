from monitor.models import Image, Agent
from rest_framework import serializers

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="Image:agent-detail")
    class Meta:
        model = Image
        fields = ('url', 'location')