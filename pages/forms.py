from django.forms import ModelForm

from .models import Coment, Post, PostImage, UserMessage


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        exclude = ["added", "deleted", "owner"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ["description", "content"]:
            self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("description")
        content = cleaned_data.get("content")

        if not any([description, content]):
            return None

        return cleaned_data


class PostImageForm(ModelForm):
    class Meta:
        model = PostImage
        fields = ["image"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["image"].required = False

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("image")

        if not any([image]):
            return None

        return cleaned_data


class ComentForm(ModelForm):
    class Meta:
        model = Coment
        fields = ["coment"]


class MessageForm(ModelForm):

    class Meta:
        model = UserMessage
        fields = ["message"]

    # allows to send an empty messages
    # try to create random gif when empty message is send
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["message"].required = False
