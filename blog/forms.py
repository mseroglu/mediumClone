from django import forms
from django.core import validators
from .models import BlogPost, Tag
from tinymce.widgets import TinyMCE


# my validator
from config.validators import max_length_10_validator


class BlogPostModelForm(forms.ModelForm):
    tag = forms.CharField()
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 40, 'rows': 10}))
    title = forms.CharField(validators=[validators.MinLengthValidator(3, message="Oops.. En az 3 karakter!"), max_length_10_validator])



    class Meta:
        model = BlogPost
        fields = [
            "tag",
            "title",
            "cover_image",
            "content",
            "category",

        ]


    # 3. Validator tipi
    # def clean_title(self):
    #     title = self.cleaned_data.get("title")
    #     if len(title)<3:
    #         raise forms.ValidationError("Ooo  Başlık en az 3 karakter olmalı!!")
    #     return title

