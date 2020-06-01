from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=20)
    adds = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Source(models.Model):
    name = models.CharField(max_length=50)
    # thumbnail_image = models.ImageField(upload_to='thumbnail_images', blank=True)
    find_all_tag = models.CharField(max_length=100)
    find_ind_tag = models.CharField(max_length=100)
    home_link = models.URLField()
    redir_link = models.URLField()
    implemented = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    # linkes UserProfile to User model instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # other attributes
    sources_list = models.ManyToManyField(Source ,blank=True)
    tags_list = models.ManyToManyField(Tag ,blank=True)

    def __str__(self):
        return self.user.username
