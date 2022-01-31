from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Float, DateTime

from mobilitydb_client import MobilityDBClient

import os


postgres_client = MobilityDBClient('mobilitydb')

postgres_client._get_session()

Base = declarative_base()

class VehiclePositions(Base):
    '''Declarative base for Vehicle Positions'''
    __tablename__ = 'vehicle_positions'
    id = Column(String, primary_key=True)
    trip_id = Column(String)
    vehicle_id = Column(String)
    feed_timestamp = Column(Integer, primary_key=True)
    vehicle_timestamp = Column(Integer)
    schedule_relationship = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    bearing = Column(Float)
    speed = Column(Float)

    def __init__(self, id, trip_id, vehicle_id, feed_timestamp, vehicle_timestamp, schedule_relationship, latitude, longitude, bearing, speed):
        self.id = id
        self.trip_id = trip_id
        self.vehicle_id = vehicle_id
        self.feed_timestamp = feed_timestamp
        self.vehicle_timestamp = vehicle_timestamp
        self.schedule_relationship = schedule_relationship
        self.latitude = latitude
        self.longitude = longitude
        self.bearing = bearing
        self.speed = speed

if __name__ == '__main__':

    Base.metadata.create_all(postgres_client._engine)
