from django import forms
from django.forms import ModelForm

from .models import Post, PostImage


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        exclude = ["added", "deleted", "owner"]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in ["description", "content"]:
            self.fields[field].required = False

    # def clean(self):
    #     cleaned_data = super().clean()
    #     description = cleaned_data.get("description")
    #     content = cleaned_data.get("content")

    #     if not any([description, content]):
    #         raise forms.ValidationError("Przynajmniej jedno pole musi zawierać treść.")

    #     return cleaned_data


class PostImageForm(ModelForm):
    class Meta:
        model = PostImage
        fields = ["image"]

        def __init__(self, *args, **kwargs):
            super(PostForm, self).__init__(*args, **kwargs)
            self.fields["image"].required = False

    def clean(self):
        pass
