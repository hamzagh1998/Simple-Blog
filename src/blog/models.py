from PIL import Image
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_delete

#Create your models here.
def upload_location(instance, filename):
	file_path = 'blog/{author_id}/{title}-{filename}'.format(
				author_id=str(instance.author.id),title=str(instance.title), filename=filename)
	return file_path

class Post(models.Model):
	title = models.CharField(max_length=60)
	body = models.TextField(max_length=6000)
	post_pic = models.ImageField(upload_to=upload_location, blank=True, null=True)
	date_posted = models.DateTimeField(verbose_name="Date Posted", default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def save(self):
	    super().save()

	    img = Image.open(self.post_pic.path)
	    if img.height > 900 or img.width > 900:
	        output_size = (900, 900)
	        img.thumbnail(output_size)
	        img.save(self.post_pic.path)

	def get_absolute_url(self):
		return reverse('blog:post-detail', kwargs={'pk':self.pk})

	def __str__(self):
	    return "{} - {}".format(self.title, self.author)

@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.post_pic.delete(False)
