
import requests
from datetime import datetime
from google.transit import gtfs_realtime_pb2
import pytz
import os
import logging
from gtfs_elt.mobilitydb_client import MobilityDBClient, VehiclePositions

from gtfs_elt.api_credentials import credentials

'''
logging.basicConfig(level=logging.INFO,
                    handlers=[logging.StreamHandler(), logging.FileHandler('../logs/extract_gtfs.log')],
                    format='%(asctime)s:%(message)s')
'''

def extract_gtfs(endpoint):

    #Import API credentials
    client_id = credentials['CLIENT_ID']
    client_secret = credentials['CLIENT_SECRET']
    url = 'https://apitransporte.buenosaires.gob.ar/colectivos/'
    
    #Make a GET Requests to get the RealTime Data
    gtfs_requests = requests.get(url + endpoint, params ={'client_id': client_id, 'client_secret' : client_secret, 'json': 0})   

    #Save the current timestamp
    date_now = datetime.now(pytz.timezone('America/Argentina/Buenos_Aires'))

    #Create a sub-path for VehiclePositions or TripUpdates if they don't exist
    data_path = '/opt/airflow/data/gtfs-realtime/'
    os.chdir(data_path)

    if not os.path.isdir(endpoint):
        os.mkdir(endpoint)

    #Create a SUB - Path for every day of data if it doesn't exists
    dir_path = endpoint + '/' + date_now.strftime('%Y-%m-%d')
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    #If the request gets a 200 status code, the file will be saved for the next process to read it
    if gtfs_requests.status_code == 200:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(gtfs_requests.content)

        file_name = endpoint + '_' + feed.header.timestamp.__str__() 
        file_path = dir_path + '/' + file_name
        
        #If the file does not exist, it is saved in binary format and the path is returned  for the next process
        #to load it in the database
        if not os.path.isfile(file_path):
            '''logging.info(date_now.strftime('%Y-%m-%d %H:%M:%S'), str(gtfs_requests.status_code), file_name)'''
            with open(file_path, 'wb') as f:
                f.write(gtfs_requests.content)
                f.close()

            return data_path + file_path   
    else:
        '''logging.info(date_now.strftime('%Y-%m-%d %H:%M:%S'), str(gtfs_requests.status_code))'''
    



def load_gtfs(path):
    '''This function loads a single feed message into the database'''

    postgres_client = MobilityDBClient('mobilitydb')

    postgres_client._get_session()

    with open(path, 'rb') as f:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(f.read())

    for i in range(len(feed.entity)):
        id = feed.entity[i].id
        trip_id = feed.entity[i].vehicle.trip.trip_id
        vehicle_id = feed.entity[i].vehicle.vehicle.id
        feed_timestamp = feed.header.timestamp
        vehicle_timestamp = feed.entity[i].vehicle.timestamp
        schedule_relationship = feed.entity[i].vehicle.trip.schedule_relationship
        latitude = feed.entity[i].vehicle.position.latitude
        longitude = feed.entity[i].vehicle.position.longitude
        bearing = feed.entity[i].vehicle.position.bearing
        speed = feed.entity[i].vehicle.position.speed
        
        check_duplicados = postgres_client._session.query(VehiclePositions).filter_by(id=id,feed_timestamp=feed_timestamp).first()
        
        if not check_duplicados:
            vehicle_position = VehiclePositions(id, trip_id, vehicle_id, feed_timestamp, vehicle_timestamp, schedule_relationship, latitude, longitude, bearing, speed)
            postgres_client.insert_from_declarative_base(vehicle_position)    
        

 
if __name__ == '__main__':
    endpoint ='vehiclePositions'
    path = extract_gtfs(endpoint)
    print(path)
    load_feed_to_db(path)
    