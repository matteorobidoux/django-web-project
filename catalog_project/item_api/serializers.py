from rest_framework import serializers
from django.contrib.auth.models import User
from item_catalog.models import TYPE_CHOICES, STATUS_CHOICES, Item
from rest_framework.fields import CurrentUserDefault

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', )

class ItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    owner = serializers.CharField(read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'owner', 'type', 'field', 'keyword_list', 'content', 'likes', 'url', 'status', 'date_posted', 'snapshot')

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['likes'] = instance.total_likes()
        result['rate'] = instance.avg_rating()

        return result