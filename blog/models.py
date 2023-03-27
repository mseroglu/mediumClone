from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from autoslug import AutoSlugField
from tinymce.models import HTMLField


class BaseModel(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="title", unique=True)
    is_active = models.BooleanField(default=True)
    at_created = models.DateTimeField(auto_now_add=True)
    at_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ("title",)


class Category(BaseModel):

    def get_absolute_url(self):
        return reverse(
            "blog:category_view",
            kwargs={"category_slug": self.slug}
        )


class Tag(BaseModel):

    def get_absolute_url(self):
        return reverse(
            "blog:tag_view",
            kwargs={"tag_slug": self.slug}
        )


class BlogPost(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag)
    cover_image = models.ImageField(upload_to="post")
    content = HTMLField(blank=True, null=True)
    view_count = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ("-at_created",)

    def get_absolute_url(self):
        return reverse(
            "read:post_detail_view",
            kwargs={
                "user_slug": self.user.profile.slug,
                "post_slug": self.slug},
        )

    def get_post_edit_url(self):
        return reverse(
            "blog:post_edit_view",
            kwargs={
                "post_slug": self.slug},
        )


class UserPostFav(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    at_updated = models.DateTimeField(auto_now=True)

