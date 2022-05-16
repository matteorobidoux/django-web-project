from rest_framework import serializers
from django.contrib.auth.models import User
from item_catalog.models import TYPE_CHOICES, STATUS_CHOICES, Item
from rest_framework.fields import CurrentUserDefault


# A serializer for the likes class
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', )


# A serializer for items only
class ItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    owner = serializers.CharField(read_only=True)

    # Only display a select few fields
    class Meta:
        model = Item
        fields = ('id', 'name', 'owner', 'type', 'field', 'keyword_list', 'content', 'likes', 'url', 'status', 'date_posted', 'snapshot')

    # Likes and rate have to represent numbers, not the foreign keys
    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['likes'] = instance.total_likes()
        result['rate'] = instance.avg_rating()

        return result