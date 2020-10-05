from django.contrib import admin

# Register your models here.
from StudyCasesManage.models import Campaign, Candidate, Manifest, SocialMediaAccount, TimeLine, Post

admin.site.register(Campaign)
admin.site.register(Candidate)
admin.site.register(Manifest)
admin.site.register(SocialMediaAccount)
admin.site.register(TimeLine)
admin.site.register(Post)
