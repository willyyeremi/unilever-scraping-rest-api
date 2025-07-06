from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import declarative_base

##############################
# common used variable
##############################

base = declarative_base()


##############################
# table on schema: public
##############################

class tr_raw_scrap_data(base):
    __tablename__ = 'tr_raw_scrap_data'
    __table_args__ = {'schema': 'main'}
    id = Column(Integer, primary_key = True)
    name = Column(String)
    detail = Column(String)
    price = Column(Integer)
    originalprice = Column(Integer)
    discountpercentage = Column(Float)
    platform = Column(String)
    createdate = Column(Date)