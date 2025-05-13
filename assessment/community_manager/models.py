from django.db import models
from django.contrib.auth.models import User

class CommunityPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # Optionally, you can add a title or tags

    def __str__(self):
        return f"{self.author.username}: {self.content[:30]}"

class CommunityReply(models.Model):
    post = models.ForeignKey(CommunityPost, related_name='replies', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author.username} on {self.post.id}"
