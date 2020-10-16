from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.deletion import PROTECT

import datetime

# Models for Database are created here as Python classes.
class Campaign(models.Model):
  name = models.CharField(max_length=50, unique=True)  # verbose_name="something" to change the output in admin panel
  start_date = models.DateField()
  end_date = models.DateField()
  description = models.CharField(max_length=50, blank=True, null=True)
  
  def __str__(self):
    return "%s" % self.name


class Candidate(models.Model):
  campaign_id = models.ForeignKey(Campaign, on_delete=models.CASCADE, verbose_name="Campaign")
  name = models.CharField(max_length=20)
  lastname = models.CharField(max_length=20)
  type = models.CharField(max_length=20, blank=True, null=True)  # candidate of what? Can be blank
  party = models.CharField(max_length=20, blank=True, null=True)

  def __str__(self):
    return "%s %s. In campaign: %s" %(self.name, self.lastname, self.campaign_id)


# class CandidatesCampaigns(models.Model):
#   campaign_id = models.ForeignKey(Campaign, on_delete=models.CASCADE, verbose_name="Campaign")
#   candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name="Candidate")

#   def __str__(self):
#     return "%s in %s"  % (self.candidate_id, self.campaign_id)


class Manifest(models.Model):
  candidate_id = models.OneToOneField(Candidate, on_delete=models.CASCADE, verbose_name="Candidate", primary_key=True)
  name = models.CharField(max_length=45, blank=True, null=True)
  document = models.FileField(max_length=400, upload_to="StudyCasesManage/uploads/manifests/%Y/%m/%d")
  collect_date = models.DateField(blank=True, default=datetime.date.today)
  release_date = models.DateField(blank=True, null=True)
  provider = models.CharField(max_length=40, blank=True, null=True)
  type = models.CharField(max_length=10, blank=True, null=True)
  # Maybe a path for the document location

  def __str__(self):
    return "candidate: %s, collect_date: %s, release_date: %s, provider: %s, type: %s" %(self.candidate_id, self.collect_date, self.release_date, self.provider, self.type)


class SocialMediaAccount(models.Model):
  candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name="Candidate")
  screen_name = models.CharField(max_length=20)
  account = models.CharField(max_length=40, default='Twitter')
  created_date = models.DateField(blank=True, null=True)
  followers = models.JSONField(encoder=DjangoJSONEncoder, blank=True, null=True)
  mentions = models.JSONField(encoder=DjangoJSONEncoder, blank=True, null=True)

  def __str__(self):
    return "Account: %s of candidate: %s" %(self.screen_name, self.candidate_id)


class Timeline(models.Model):
  social_media_id = models.ForeignKey(SocialMediaAccount, on_delete=models.CASCADE, verbose_name="Timeline")
  # maybe a DateRangeField()
  collect_date = models.DateField(default=datetime.date.today)
  end_date = models.DateField(blank=True, null=True)

  def __str__(self):
    return "social_media_account: %s, collect_date: %s, end_date: %s" %(self.social_media_id, self.collect_date, self.end_date)


class Post(models.Model):
  timeline_id = models.ForeignKey(Timeline, on_delete=models.CASCADE)
  
  # Must point to Post
  # Reverse query name for 'Post.parent_id' clashes with field name 'Post.post'
  # HINT: Rename field 'Post.post', or add/change a related_name argument to the definition for field 'Post.parent_id'.
  # HINT: Rename field 'Post.post', or add/change a related_name argument to the definition for field 'Post.parent_id'.
  parent_id = models.ForeignKey('self', on_delete=models.CASCADE, related_name='+', blank=True, null=True) 
  post_date = models.DateField()
  post_text = models.CharField(max_length=500)
  post_as_json = models.JSONField(encoder=DjangoJSONEncoder, blank=True, null=True)


  def __str__(self):
    return "parent: %s, post_date: %s, text: %s" %(self.parent_id, self.post_date, self.post_text)



## TEST MODELS

