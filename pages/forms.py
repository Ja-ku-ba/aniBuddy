from django import forms
from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        exclude = ["added", "deleted"]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in ["description", "content", "image"]:
            self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("description")
        content = cleaned_data.get("content")
        image = cleaned_data.get("image")

        if not any([description, content, image]):
            raise forms.ValidationError("Przynajmniej jedno pole musi zawierać treść.")

        return cleaned_data
