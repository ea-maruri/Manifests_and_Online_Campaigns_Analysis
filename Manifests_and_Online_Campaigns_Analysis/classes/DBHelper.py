"""Class that provides DB assistance"""
from .Campaign import Campaign
from datetime import datetime

class DBHelper(object):
  def __init__(self):
    # # (self, id:str, start_date:date, end_date:date, campaign_desc:str)
    a = datetime(2020, 10, 1)
    b = datetime(2020, 12, 31)
    camp0 = Campaign("1", a, b, "Case Study 1")
    camp1 = Campaign("2", a, b, "Case Study 2")
    camp2 = Campaign("3", a, b, "Case Study 3")
    camp3 = Campaign("4", a, b, "Case Study 4")

    self.campaigns = [camp0, camp1, camp2, camp3]

