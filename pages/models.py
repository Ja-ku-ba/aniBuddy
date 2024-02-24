from django.db import models

# Create your models here.
class Post(models.Model):
    # owner = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    description = models.CharField(max_length=1024)
    content = models.TextField()
    # image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    added = models.DateTimeField(auto_now_add=False)
