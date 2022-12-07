from rest_framework import serializers

from tts.models import Project, Audio
from tts.utils import sentence2texts


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ['id', 'project', 'index', 'update_time', 'text', 'speed', 'file']
        read_only_fields = ['update_time', 'file']


class ProjectSerializer(serializers.ModelSerializer):
    audios = AudioSerializer(read_only=True, many=True)
    sentence = serializers.CharField(write_only=True)  # sentence 는 전처리 과정을 거쳐 Audio Model에 데이터를 넣게 된다.

    # 이곳에서 sentence 를 전처리과정을 거치고 Audio 모델에 데이터가 들어가도록
    # def create(self, validated_data):
    #     sentence = validated_data.pop('validate_data')
    #     if sentence:
    #         sentence = sentence2texts(sentence)
    #     return

    class Meta:
        model = Project
        fields = ['id', 'index', 'title', 'user', 'update_time', 'create_time', 'audios', 'sentence']
        read_only_fields = ['update_time', 'create_time']
