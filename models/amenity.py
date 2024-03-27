#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from os import getenv
from models.review import Review
from models import storage


class Amenity(BaseModel, Base):
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place",
                                   secondary="place_amenity",
                                   viewonly=False,
                                   overlaps="place_amenities")
