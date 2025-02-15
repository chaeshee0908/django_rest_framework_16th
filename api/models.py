from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(BaseModel, AbstractUser):
    email = models.EmailField(max_length=250, unique=True)
    password = models.CharField(max_length=150)

    def __str__(self):
        return self.username


class Todo(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='todo')
    contents = models.TextField(max_length=30)
    date = models.DateField()
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.contents

class Diary(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='diary')
    emoji = models.CharField(max_length=15)
    mood_temperature = models.IntegerField(default=25)
    date = models.DateField()
    contents = models.TextField(max_length=200)
    background_color = models.CharField(max_length=15)
    private = models.BooleanField(default=False)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return '{} 일기'.format(self.user.name)


class Likes(BaseModel):
    # 좋아요를 누른 유저
    click_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user')
    todo = models.ForeignKey('Todo', on_delete=models.CASCADE, related_name='todo')
    diary = models.ForeignKey('Diary', on_delete=models.CASCADE, related_name='diary')

    def __str__(self):
        return '{}가 {}의 글을 좋아합니다.'.format(self.click_user.name, self.todo.user.name)


class Follows(BaseModel):
    # 팔로우를 건 유저
    click_user = models.ManyToManyField(User, related_name='click_user')
    # 팔로우 타겟
    target = models.ManyToManyField(User, related_name='target_user')

    def __str__(self):
        return '{}가 {}를 팔로우합니다.'.format(self.click_user.name, self.target.name)