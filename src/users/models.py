from PIL import Image
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def upload_location(instance, filename):
    file_path = f'users/{instance.user.id}/{instance.user.username}-{filename}'
    return file_path

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_pics = models.ImageField(default="user_logo.png", upload_to=upload_location)

    def save(self, *arg, **kwargs):
        super().save()

        img = Image.open(self.user_pics.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.user_pics.path)

    def __str__(self):
        return f'{self.user.username} Profile'
