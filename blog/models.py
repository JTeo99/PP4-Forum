from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS = ((0, "Draft"), (1, "Published"))

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Blogpost titles have unique names to prevent having the same name to confuse users
class Post(models.Model):
    title = models.CharField(max_length = 200, unique=True)
    slug = models.SlugField(max_length = 200, unique = True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="blog_posts"
    )
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', blank=True, null=True)


    class Comment(models.Model):
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)
    level = models.PositiveIntegerField(default=0)
    edited_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
    
    def like(self, user):
        self.likes.add(user)

    def unlike(self, user):
        self.likes.remove(user)

    def dislike(self, user):
        self.dislikes.add(user)

    def undislike(self, user):
        self.dislikes.remove(user)

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def dislikes_count(self):
        return self.dislikes.count()
    
    def edit(self, body):
        self.body = body
        self.edited_on = timezone.now()
        self.save()

    def delete(self):
        self.is_deleted = True
        self.save()