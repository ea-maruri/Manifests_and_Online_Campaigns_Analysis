from os import name
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.deletion import PROTECT

# Create your models here.

class Campaign(models.Model):
  name = models.CharField(max_length=25)
  start_date = models.DateField()
  end_date = models.DateField()
  description = models.CharField(max_length=50, blank=True)

  def __str__(self):
    return "Campaign\n\tname: %s, start_date: %s, end_date: %s, description: %s." % (self.name, self.start_date, self.end_date, self.description)


class Candidate(models.Model):
  campaign_id = models.ForeignKey(Campaign, on_delete=models.PROTECT)
  name = models.CharField(max_length=20)
  lastname = models.CharField(max_length=20)
  type = models.CharField(max_length=20, blank=True)  # candidate of what? Can be blank
  party = models.CharField(max_length=20, blank=True)

  def __str__(self):
    return "Candidate\n\tname: %s, lastname: %s, campaign, %s, type: %s, party: %s" %(self.name, self.lastname, self.campaign_id, self.type, self.party)


class Manifest(models.Model):
  candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)
  collect_date = models.DateField()
  release_date = models.DateField()
  provider = models.CharField(max_length=40, blank=True)
  type = models.CharField(max_length=10)
  # Maybe a path for the document location

  def __str__(self):
    return "Manifest\n\tcandidate: %s, collect_date: %s, release_date: %s, provider: %s, type: %s" %(self.candidate_id, self.collect_date, self.release_date, self.provider, self.type)


class SocialMediaAccount(models.Model):
  candidate_id = models.ForeignKey(Candidate, on_delete=models.PROTECT)
  screen_name = models.CharField(max_length=20)
  created_date = models.DateField()
  description = models.CharField(max_length=50, blank=True)
  followers = models.JSONField(encoder=DjangoJSONEncoder)
  mentions = models.JSONField(encoder=DjangoJSONEncoder)

  def __str__(self):
    return "Social Media Account\n\tcandidate: %s, screen_name: %s, creation_date: %s, description: %s" %(self.candidate_id, self.screen_name, self.created_date, self.description)

class TimeLine(models.Model):
  social_media_id = models.ForeignKey(SocialMediaAccount, on_delete=models.CASCADE)
  # maybe a DateRangeField()
  collect_date = models.DateField()
  end_date = models.DateField()

  def __str__(self):
    return "Timeline\n\tsocial_medio: %s, collect_date: %s, end_date: %s" %(self.social_media_id, self.collect_date, self.end_date)


class Post(models.Model):
  timeline_id = models.ForeignKey(TimeLine, on_delete=models.CASCADE)
  
  # Must point to Post
  # Reverse query name for 'Post.parent_id' clashes with field name 'Post.post'
  # HINT: Rename field 'Post.post', or add/change a related_name argument to the definition for field 'Post.parent_id'.
  parent_id = models.ForeignKey('self', on_delete=models.PROTECT, related_name='+') 
  post_date = models.DateField()
  post_text = models.CharField(max_length=100)
  post = models.JSONField(encoder=DjangoJSONEncoder)

  def __str__(self):
    return "Post\n\tparent: %s, post_date: %s, text: %s" %(self.parent_id, self.post_date, self.post_text)

