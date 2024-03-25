from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.translation import gettext as _
from filetype import guess


# Create your models here.
def get_image_filepath(self, filename):
    file_extension = filename[filename.rfind(".") :]
    return f"posts/{self.post.owner.id}/{self.post.id}/{self.pk}{file_extension}"

    # formImages.is_valid() checks if there is extension to file
    # if file_extension != -1:
    #     return f"posts/{self.post.owner.id}/{self.post.id}/{self.pk}{file_extension}"
    # return f"posts/{self.post.owner.id}/{self.post.id}/{self.pk}.webp"


class Post(models.Model):
    owner = models.ForeignKey(
        "user.MyUserModel", verbose_name=_("Właściciel"), on_delete=models.DO_NOTHING
    )
    description = models.CharField(
        _("Tytuł char"), max_length=1024, blank=True, null=True
    )
    content = models.TextField(_("Zawartość text"), blank=True, null=True)
    added = models.DateTimeField(auto_now_add=False)
    deleted = models.BooleanField(default=False)


def convert_to_webp(image):
    img = Image.open(image)
    output = BytesIO()
    img.save(output, format="WEBP")

    # Przenieś wskaźnik pliku na początek
    output.seek(0)
    # Utwórz obiekt InMemoryUploadedFile z obrazem w formacie WebP
    webp_image = InMemoryUploadedFile(
        output,
        "ImageField",
        "%s.webp" % image.name.split(".")[0],
        "image/webp",
        output.tell(),
        None,
    )
    return webp_image


class PostImage(models.Model):
    # post to which image was added
    post = models.ForeignKey("POST", on_delete=models.DO_NOTHING)
    image = models.ImageField(
        upload_to=get_image_filepath, max_length=255, null=True, blank=True
    )
    deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.image:
            if not guess(self.image).mime.startswith("image/gif"):
                self.image = convert_to_webp(self.image)
        super().save(*args, **kwargs)


class Coment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.DO_NOTHING)
    coment = models.CharField(max_length=1023)
    added = models.DateTimeField(auto_now_add=False)
    owner = models.ForeignKey(
        "user.MyUserModel", verbose_name=_("Właściciel"), on_delete=models.DO_NOTHING
    )
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-added"]


class Reaction(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey("user.MyUserModel", on_delete=models.CASCADE)
    # reaction = 1, means that user liked post. reaction = -1 means dislike
    reaction = models.IntegerField(default=0)
