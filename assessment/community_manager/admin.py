from django.contrib import admin
from .models import CommunityPost, CommunityReply

admin.site.register(CommunityPost)
admin.site.register(CommunityReply)
