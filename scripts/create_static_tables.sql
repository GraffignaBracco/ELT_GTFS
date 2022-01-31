CREATE SCHEMA gtfs 
CREATE TABLE agency (
  agency_id text default '',
  agency_name text default null,
  agency_url text default null,
  agency_timezone text default null,
  agency_lang text default null,
  agency_phone text default null,

  CONSTRAINT agency_pkey PRIMARY KEY (agency_id)
)

CREATE TABLE calendar_dates (
  service_id text,
  date date not null,
  exception_type int 
)

CREATE TABLE routes (
  route_id text,
  agency_id text,
  route_short_name text default '',
  route_long_name text default '',
  route_desc text default '',
  route_type int,
  CONSTRAINT routes_pkey PRIMARY KEY ( route_id)
)

CREATE TABLE shapes (
  shape_id text not null,
  shape_pt_lat double precision not null,
  shape_pt_lon double precision not null,
  shape_pt_sequence int not null,
  -- optional
  shape_dist_traveled double precision default null
)

CREATE TABLE trips (
  route_id text not null,
  service_id text not null,
  trip_id text not null,
  trip_headsign text,
  trip_short_name text,
  direction_id int,
  block_id text,
  shape_id text,
  exceptional int default null,
  CONSTRAINT trips_pkey PRIMARY KEY (trip_id)
)
    
    
CREATE TABLE stop_times (
  trip_id text not null,
  arrival_time text,
  departure_time text,
  stop_id text,
  stop_sequence int not null,
  timepoint int,
  shape_dist_traveled numeric(10, 2)
)


CREATE TABLE stops (
  stop_id text,
  stop_name text default null,
  stop_desc text default null,
  stop_lat double precision,
  stop_lon double precision,
  CONSTRAINT stops_pkey PRIMARY KEY (stop_id)
);

COPY gtfs.agency(agency_id, agency_name, agency_url, agency_timezone,  agency_lang, agency_phone) FROM '/gtfs-static/agency.txt' DELIMITER ',' CSV HEADER;
COPY gtfs.calendar_dates(service_id,date, exception_type) FROM '/gtfs-static/calendar_dates.txt' DELIMITER ',' CSV HEADER;
COPY gtfs.routes (route_id,  agency_id, route_short_name, route_long_name, route_desc, route_type) FROM '/gtfs-static/routes.txt' DELIMITER ',' CSV HEADER;
COPY gtfs.shapes(shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence, shape_dist_traveled) FROM '/gtfs-static/shapes.txt' DELIMITER ',' CSV HEADER;
COPY gtfs.stop_times(trip_id, arrival_time, departure_time, stop_id, stop_sequence, timepoint, shape_dist_traveled) FROM '/gtfs-static/stop_times.txt' DELIMITER ',' CSV HEADER;
COPY gtfs.stops(stop_id, stop_name, stop_desc, stop_lat, stop_lon) FROM '/gtfs-static/stops.txt' DELIMITER ',' CSV HEADER;
COPY gtfs.trips(route_id, service_id, trip_id, trip_headsign, trip_short_name, direction_id, block_id, shape_id, exceptional) FROM '/gtfs-static/trips.txt' DELIMITER ',' CSV HEADER;
