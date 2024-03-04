from django.db import models
from django.utils.translation import gettext as _


# Create your models here.
def get_image_filepath(self, filename):
    return f"/media/posts/{self.owner.id}/{self.pk}.png"
    # return f'static/posts/{self.owner.id}/{self.pk}.png'


class Post(models.Model):
    owner = models.ForeignKey(
        "user.MyUserModel", verbose_name=_("Właściciel"), on_delete=models.DO_NOTHING
    )
    # animal = modelf.models.ForeignKey(
    #     "app.Model", verbose_name=_(""), on_delete=models.CASCADE
    # )
    description = models.CharField(
        _("Tytuł char"), max_length=1024, blank=True, null=True
    )
    content = models.TextField(_("Zawartość text"), blank=True, null=True)
    image = models.ImageField(
        upload_to=get_image_filepath, max_length=255, null=True, blank=True
    )
    added = models.DateTimeField(auto_now_add=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-added"]
