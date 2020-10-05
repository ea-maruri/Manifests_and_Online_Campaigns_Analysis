from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.deletion import PROTECT

# Create your models here.

class Campaign(models.Model):
  name = models.CharField(max_length=25)
  start_date = models.DateField()
  end_date = models.DateField()
  description = models.CharField(max_length=50)

class Candidate(models.Model):
  campaign_id = models.ForeignKey(Campaign, on_delete=models.PROTECT)
  name = models.CharField(max_length=20)
  lastname = models.CharField(max_length=20)
  type = models.CharField(max_length=20)  # candidate of what?
  party = models.CharField(max_length=20)

class Manifest(models.Model):
  candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)
  collect_date = models.DateField()
  release_date = models.DateField()
  provider = models.CharField(max_length=40)
  type = models.CharField(max_length=10)

class SocialMediaAccount(models.Model):
  candidate_id = models.ForeignKey(Candidate, on_delete=models.PROTECT)
  screen_name = models.CharField(max_length=20)
  created_date = models.DateField()
  description = models.CharField(max_length=50)
  followers = models.JSONField(encoder=DjangoJSONEncoder)
  mentions = models.JSONField(encoder=DjangoJSONEncoder)

class TimeLine(models.Model):
  social_media_id = models.ForeignKey(SocialMediaAccount, on_delete=models.CASCADE)
  # maybe a DateRangeField()
  collect_date = models.DateField()
  end_date = models.DateField()

class Post(models.Model):
  timeline_id = models.ForeignKey(TimeLine, on_delete=models.CASCADE)
  
  # Must point to Post
  # Reverse query name for 'Post.parent_id' clashes with field name 'Post.post'
  # HINT: Rename field 'Post.post', or add/change a related_name argument to the definition for field 'Post.parent_id'.
  parent_id = models.ForeignKey('self', on_delete=models.PROTECT, related_name='+') 
  post_date = models.DateField()
  post_text = models.CharField(max_length=100)
  post = models.JSONField(encoder=DjangoJSONEncoder)


