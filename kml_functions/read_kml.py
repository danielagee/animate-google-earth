import linecache
from statistics import median
import kml_functions.constants as c

#input_file = input('What is the GPS file to analyze?\n'
#                   'Example: c:\\MyFolder\\track.kml\n')

input_file = 'C:\\Python\\GPS\\kyiv_track.kml'

# extracts the data I need from line 19 of the recorded GPS file.
gps_coordinates_raw = linecache.getline(input_file, 19)
# removes the fixed prefix from the front of the data.
gps_coordinates_raw = gps_coordinates_raw.removeprefix('        <coordinates>')
# removes the fixed suffix from the end of the data.
gps_coordinates_raw = gps_coordinates_raw.removesuffix('</coordinates>\n')

#Counts the number of GPS points by counting the ',' between lat-lon pairs.
gps_points = gps_coordinates_raw.count(',')

latitude = []
longitude = []

gps_coordinates_temp = gps_coordinates_raw

for placemarkId in range(1, gps_points):
    comma_index = gps_coordinates_temp.find(',')
    longitude_string = gps_coordinates_temp[0:comma_index]
    gps_coordinates_temp = gps_coordinates_temp.removeprefix(longitude_string + ',')
    longitude_float = float(longitude_string)
    longitude.append(longitude_float)

    space_index = gps_coordinates_temp.find(' ')
    latitude_string = gps_coordinates_temp[0:space_index]
    gps_coordinates_temp = gps_coordinates_temp.removeprefix(latitude_string + ' ')
    latitude_float = float(latitude_string)
    latitude.append(latitude_float)

camera_latitude = median(latitude)
camera_longitude = median(longitude)

max_latitude = max(latitude)
min_latitude = min(latitude)
max_longitude = max(longitude)
min_longitude = min(longitude)
latitude_distance = max_latitude-min_latitude
longitude_distance = max_longitude-min_longitude
#camera_altitude = max(latitude_distance, longitude_distance)*110*1000*2
camera_altitude = c.ALTITUDE
