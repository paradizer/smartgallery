from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)
def user_directory_path2(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/_{1}'.format(instance.user.id, filename)
'''
class Images(models.Model):
    imgfile = models.ImageField(upload_to='images/%Y/%m/%d')
    #imgfile = models.ImageField(upload_to=user_directory_path)
    upload_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User')
    description = models.CharField(max_length=200, default="")
'''
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


class Images(models.Model):
    imgfile = models.FileField(upload_to=user_directory_path)
    imgfile_mini = models.FileField(upload_to=user_directory_path2, blank=True)
    user = models.ForeignKey('auth.User')
    upload_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        pil_image_obj = Image.open(self.imgfile)
        w, h = pil_image_obj.size
        new_h = 200
        new_w = w * new_h // h
        new_image = pil_image_obj.resize((new_w, new_h), Image.ANTIALIAS)

        new_image_io = BytesIO()
        new_image.save(new_image_io, format='JPEG')

        temp_name = '_'+self.imgfile.name
        #self.imgfile_mini.delete(save=False)

        self.imgfile_mini.save(
            temp_name,
            content=ContentFile(new_image_io.getvalue()),
            save=False
        )

        super(Images, self).save(*args, **kwargs)

