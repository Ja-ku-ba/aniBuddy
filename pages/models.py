from django.db import models

# Create your models here.
def get_image_filepath(self, filename):
    return f'static/posts/{self.owner.id}/{self.pk}.png'
                                                                                                

class Post(models.Model):
    # owner = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    description_char = models.CharField(max_length=1024)
    content_text = models.TextField()
    image = models.ImageField(upload_to=get_image_filepath, max_length=255, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=False)
    deleted = models.BooleanField(default=False)
