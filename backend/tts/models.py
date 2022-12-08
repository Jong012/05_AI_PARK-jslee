from django.contrib.auth.models import User
from django.db import models
from django.db.models import Manager


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    index = models.IntegerField(help_text='순서')
    title = models.CharField(max_length=128, help_text='프로젝트의 제목')
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    objects = Manager()

    class Meta:
        db_table = 'project'

    def __str__(self):
        return self.title


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'


class Audio(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='audios')
    index = models.IntegerField(help_text='텍스트의 순서를 뜻함')
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1024, help_text='오디오로 변환될 텍스트')
    speed = models.FloatField(help_text='오디오의 스피드', default=1.0)
    # file = models.FileField(upload_to=user_directory_path)
    file = models.URLField()  # S3 bucket 으로 하기 위해 url field 로 일단은 구성
    objects = Manager()

    def __str__(self):
        return f'{self.project.title}(Audio - {self.index}번째 텍스트)'

    class Meta:
        db_table = 'audio'
