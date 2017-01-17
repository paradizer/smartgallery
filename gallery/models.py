from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)
'''
class Images(models.Model):
    imgfile = models.ImageField(upload_to='images/%Y/%m/%d')
    #imgfile = models.ImageField(upload_to=user_directory_path)
    upload_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User')
    description = models.CharField(max_length=200, default="")
'''

class Images(models.Model):
    imgfile = models.FileField(upload_to=user_directory_path)
    user = models.ForeignKey('auth.User')


