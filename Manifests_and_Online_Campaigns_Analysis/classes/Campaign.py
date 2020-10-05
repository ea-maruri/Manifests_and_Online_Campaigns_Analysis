"""Class that represents a case study (campaign)"""
from datetime import datetime

class Campaign(object):
  def __init__(self, id: str, start_date: datetime, end_date: datetime, desc: str):
    self.id = id
    self.start_date = start_date
    self.end_date = end_date
    self.description = desc

    self.candidates_list = list()

  def add_candidate(self, name: str):
    self.candidates_list.append(name)
