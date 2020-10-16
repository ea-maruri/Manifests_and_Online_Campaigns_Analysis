from django.contrib import admin

# Register your models here.
from StudyCasesManage.models import Campaign, Candidate, Manifest, SocialMediaAccount, Timeline, Post


# Classes that allows to show the fields on admin panel, criteria for search fields, and filters
class CampaignAdmin(admin.ModelAdmin):
  list_display = ("name", "start_date", "end_date", "description")
  search_fields = ("name", "start_date", "end_date")
  list_filter = ("start_date", "end_date")
  date_hierarchy = "start_date"  # Top date menu

class CandidateAdmin(admin.ModelAdmin):
  list_display = ("name", "lastname", "campaign_id", "type", "party")
  search_fields = ("name", "lastname", "type")
  list_filter = ("campaign_id", "type", "party")

class ManifestAdmin(admin.ModelAdmin):
  list_display = ("candidate_id", "manifest", "name", "type", "collect_date", "release_date", "provider")
  search_fields = ("name", "candidate_id", "type")
  list_filter = ("name", "type", "candidate_id")
  date_hierarchy = "collect_date"

class SocialMediaAccountAdmin(admin.ModelAdmin):
  list_display = ("candidate_id", "screen_name", "created_date", "account", "followers", "mentions")
  search_fields = ("candidate_id", "screen_name")
  list_filter = ("candidate_id", "screen_name")

class TimelineAdmin(admin.ModelAdmin):
  list_display = ("social_media_id", "collect_date", "end_date")
  search_fields = ("social_media_id",)
  list_filter = ("social_media_id", "collect_date", "end_date")
  date_hierarchy="collect_date"

class PostAdmin(admin.ModelAdmin):
  list_display = ("timeline_id", "parent_id", "post_date", "post_text")  # "post_as_json" # is too big
  search_fields = ("timeline_id", "parent_id", "post_date")
  list_filter = ("timeline_id", "parent_id", "post_date")
  date_hierarchy = "post_date"



# Registering Models
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Manifest, ManifestAdmin)
admin.site.register(SocialMediaAccount, SocialMediaAccountAdmin)
admin.site.register(Timeline, TimelineAdmin)
admin.site.register(Post, PostAdmin)
