from rest_framework import serializers

from tts.models import Project, Audio
from tts.utils import get_validate_sentence, sentence2texts, texts2audio


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ['id', 'project', 'index', 'update_time', 'text', 'speed', 'file']
        read_only_fields = ['update_time', 'file']


class ProjectSerializer(serializers.ModelSerializer):
    audios = AudioSerializer(read_only=True, many=True)
    title = serializers.CharField()
    sentence = serializers.CharField(max_length=1024, write_only=True)  # sentence 는 전처리 과정을 거쳐 Audio Model에 데이터를 넣게 된다.

    def create(self, validated_data):
        sentence = validated_data.pop('sentence')
        instance = super().create(validated_data)
        if sentence:
            valid_sentence = get_validate_sentence(sentence)
            results = sentence2texts(valid_sentence)
            texts2audio(instance.user.id, instance, results)

        return instance

    class Meta:
        model = Project
        fields = ['id', 'index', 'title', 'user', 'update_time', 'create_time', 'audios', 'sentence', 'audio_count']
        read_only_fields = ['update_time', 'create_time']
