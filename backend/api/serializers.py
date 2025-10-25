from rest_framework import serializers
from .models import User, WubiDict, WubiCategory, WubiWord

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nickname', 'email', 'password', 'invitation_code')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            password=validated_data['password'],
            invitation_code=validated_data.get('invitation_code', '')
        )
        return user

class WubiDictSerializer(serializers.ModelSerializer):
    contentSize = serializers.IntegerField(source='content_size')
    wordCount = serializers.IntegerField(source='word_count')
    dateUpdate = serializers.DateTimeField(source='date_update', read_only=True)

    class Meta:
        model = WubiDict
        fields = ('id', 'title', 'content', 'contentSize', 'wordCount', 'dateUpdate')

class WubiCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WubiCategory
        fields = '__all__'

class WubiWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WubiWord
        fields = '__all__'
