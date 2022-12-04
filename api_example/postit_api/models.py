from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# Create your models here.

User = get_user_model()

class Post(models.Model):
    title = models.CharField('title', max_length=150)
    body = models.TextField('body')
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE, related_name='posts')

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
   
    def __str__(self) -> str:
        return _("{title} by {user} posted at {created_at}").format(
            title=self.title,
            user=self.user,
            created_at=self.created_at,)

    class Meta:
        ordering = ('-created_at',)

class Comment(models.Model):
    body = models.TextField(_('body'), max_length=10000)
    post = models.ForeignKey(Post, verbose_name='post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE, related_name='comments')

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)


    def __str__(self) -> str:
        return _("Comment on {post_id} by {user} at {created_at}").format(
            post_id=self.post.id,
            user=self.user,
            created_at=self.created_at,)
        
    class Meta:
        ordering = ('-created_at',)

class PostLike(models.Model):
    post = models.ForeignKey(Post, verbose_name=('post'), on_delete=models.CASCADE, related_name='likes')
