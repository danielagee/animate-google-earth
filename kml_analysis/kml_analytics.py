from kml_writer.read_kml import gps_coordinates_raw

#Counts the number of GPS points by counting the ',' between lat-lon pairs.
gps_points = gps_coordinates_raw.count(',')

latitude = []
longitude = []

for placemarkId in range(1, gps_points):
    comma_index = gps_coordinates_raw.find(',')
    longitude_string = gps_coordinates_raw[0:comma_index]
    gps_coordinates_raw = gps_coordinates_raw.removeprefix(longitude_string + ',')
    longitude_float = float(longitude_string)
    longitude.append(longitude_float)

    space_index = gps_coordinates_raw.find(' ')
    latitude_string = gps_coordinates_raw[0:space_index]
    gps_coordinates_raw = gps_coordinates_raw.removeprefix(latitude_string + ' ')
    latitude_float = float(latitude_string)
    latitude.append(latitude_float)

from statistics import median

camera_latitude = median(latitude)
camera_longitude = median(longitude)

max_latitude = max(latitude)
min_latitude = min(latitude)
max_longitude = max(longitude)
min_longitude = min(longitude)
latitude_distance = max_latitude-min_latitude
longitude_distance = max_longitude-min_longitude
camera_altitude = max(latitude_distance, longitude_distance)*110*1000*2
