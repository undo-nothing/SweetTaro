from rest_framework import serializers

from apps.bing_wapper.models import BingWapper


class BingWapperSerializer(serializers.ModelSerializer):

    class Meta:
        model = BingWapper
        fields = ['id', 'filename', 'title', 'description', 'date',
                  'url', 'location', 'keyword', 'author']


class BingWapperCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BingWapper
        fields = ['id', 'filename', 'title', 'description', 'date',
                  'url', 'location', 'keyword', 'author']


class BingWapperUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BingWapper
        fields = ['id', 'filename', 'title', 'description', 'date',
                  'url', 'location', 'keyword', 'author']
