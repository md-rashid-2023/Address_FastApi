from sqlalchemy import Column, Integer, String, Float

from database import Base


class Address(Base):

    '''
        A model for address
    '''

    __tablename__ = "address"
    id = Column(Integer, primary_key=True, index=True)
    street = Column(String)
    city = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)