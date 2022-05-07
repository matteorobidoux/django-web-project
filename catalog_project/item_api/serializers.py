from rest_framework import serializers
from django.contrib.auth.models import User
from item_catalog.models import TYPE_CHOICES, STATUS_CHOICES, Item

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', )

class ItemSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        result = super().to_representation(instance)
        liked_users = len(result['likes'])
        result['likes'] = liked_users
        return result
    class Meta:
        model = Item
        fields = ('id', 'name', 'owner', 'type', 'field', 'keyword_list', 'content', 'likes', 'url', 'status', 'date_posted', )
    """"
    name = serializers.CharField(max_length=100)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    type = serializers.CharField(max_length=30, default='practical')
    field = serializers.CharField(max_length=100)
    keyword_list = serializers.CharField(max_length=200)
    content = serializers.CharField()
    url = serializers.URLField()
    status = serializers.CharField(max_length=30, default='planned')
    snapshot = serializers.ImageField(default='default.jpg')
    likes = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    date_posted = serializers.DateTimeField()
    """