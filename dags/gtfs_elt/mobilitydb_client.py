import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

import os

def is_docker():
    '''
    Checks whether the script is running in docker container or in local environment
    '''
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))

    )

if is_docker():
    postgres_url = 'postgresql+psycopg2://docker:docker@host.docker.internal:25434/'
else:
    postgres_url =   'postgresql+psycopg2://docker:docker@localhost:25434/'


class MobilityDBClient:
    '''
    This Class allow us to interact with the MobilityDB Client through Python
    '''
    def __init__(self, db):
        self.dialect =  postgres_url
        self.db = db
        self._engine = None
        self._session = None

    def _get_engine(self):
        db_uri = f'{self.dialect}{self.db}'
        if not self._engine:
            self._engine = create_engine(db_uri)
        return self._engine

    def _connect(self):
        return self._get_engine().connect()
    
    def _get_session(self):
        if not self._engine:
            self._engine = self._get_engine()

        Session = sessionmaker(bind=self._engine)
        self._session = Session()

        return self._session

    @staticmethod
    def _cursor_columns(cursor):
        if hasattr(cursor, 'keys'):
            return cursor.keys()
        else:
            return [c[0] for c in cursor.description]

    def execute(self, sql, connection=None):
        if connection is None:
            connection = self._connect()
        return connection.execute(sql)

    def insert_from_frame(self, df, table, if_exists='append', index=False, **kwargs):
        connection = self._connect()
        with connection:
            df.to_sql(table, connection, if_exists=if_exists, index=index, **kwargs)

    def to_frame(self, *args, **kwargs):
        cursor = self.execute(*args, **kwargs)
        if not cursor:
            return
        data = cursor.fetchall()
        if data:
            df = pd.DataFrame(data, columns=self._cursor_columns(cursor))
        else:
            df = pd.DataFrame()
        return df
    
    def insert_from_declarative_base(self, data):
        engine = self._get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(data)
        session.commit()



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