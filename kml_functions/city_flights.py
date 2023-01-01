import linecache
from statistics import median
import kml_functions.constants as c
import pandas as pd
import geopy.distance
from math import radians, cos, sin, asin, sqrt  # Used to calculate distance from GPS points


def read_cities_csv(file):
    df_csv = pd.read_csv(f'{file}')
    df_csv = df_csv[['City', 'Country', 'Arrive', 'Depart', 'Coordinates']]
    df_csv['Coordinates'] = df_csv['Coordinates'].str.replace('°', '', regex=True)
    df_csv[['Latitude', 'Longitude']] = df_csv.Coordinates.str.split(", ", expand=True)
    return df_csv


def coordinate_to_distance(lat1, lat2, lon1, lon2):
    # Python 3 program to calculate Distance Between Two Points on Earth
    # The math module contains a function named radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    distance_between_points_tmp = c * r

    # calculate the result
    return distance_between_points_tmp


def clean_cities_csv(df_csv):
    df_csv['ns_hemisphere'] = df_csv['Latitude'].str[-1:]
    df_csv['ns_hemisphere'] = df_csv['ns_hemisphere'].apply(lambda x: '' if x == 'N' else '-')
    df_csv['Latitude'] = df_csv[['ns_hemisphere', 'Latitude']].apply("".join, axis=1)
    df_csv['Latitude'] = df_csv['Latitude'].str[:-2]

    df_csv['ew_hemisphere'] = df_csv['Longitude'].str[-1:]
    df_csv['ew_hemisphere'] = df_csv['ew_hemisphere'].apply(lambda x: '' if x == 'E' else '-')
    df_csv['Longitude'] = df_csv[['ew_hemisphere', 'Longitude']].apply("".join, axis=1)
    df_csv['Longitude'] = df_csv['Longitude'].str[:-2]

    columns = ['Longitude', 'Latitude']
    df_csv['Coordinates_Clean'] = df_csv[columns].apply(lambda row_temp: ','.join(row_temp.values.astype(str)), axis=1)
    df_csv['Coordinates_Next'] = df_csv['Coordinates_Clean'].shift(-1).fillna(str('0,0'))
    df_csv[['Latitude_Next', 'Longitude_Next']] = df_csv['Coordinates_Next'].str.split(",", expand=True)

    df_csv = df_csv.astype(
        {'Latitude': 'float', 'Longitude': 'float', 'Latitude_Next': 'float',
         'Longitude_Next': 'float'})

    df_csv['Distance to Next'] = df_csv.apply(
        lambda row_temp2: coordinate_to_distance(
            row_temp2['Latitude'], row_temp2['Latitude_Next'],
            row_temp2['Longitude'], row_temp2['Longitude_Next']),  axis=1)

    df_csv.drop(columns=['Coordinates', 'ns_hemisphere', 'ew_hemisphere'], inplace=True)
    return df_csv


def flight_path(df_cities_temp, flight_duration_temp_seconds):
    number_of_line_segments_temp = flight_duration_temp_seconds * 30
    #df_cities_temp['Line_Length'] = df_cities_temp['Distance to Next']/(flight_duration_temp * 30)

    df_cities_temp['Latitude'] = df_cities_temp['Latitude'].astype(float)
    df_cities_temp['Latitude_Next'] = df_cities_temp['Latitude_Next'].astype(float)
    df_cities_temp['Longitude'] = df_cities_temp['Longitude'].astype(float)
    df_cities_temp['Longitude_Next'] = df_cities_temp['Longitude_Next'].astype(float)
    df_cities_temp['Latitude Delta'] = \
        (df_cities_temp['Latitude'] - df_cities_temp['Latitude_Next']) / number_of_line_segments_temp
    df_cities_temp['Longitude Delta'] = \
        (df_cities_temp['Longitude'] - df_cities_temp['Longitude_Next']) / number_of_line_segments_temp
    return df_cities_temp


def header_temp(h_name):
    head_temp = [f'<?xml version="1.0" encoding="UTF-8"?>\n',
                 f'<kml xmlns="http://www.opengis.net/kml/2.2"\n  xmlns:gx="http://www.google.com/kml/ext/2.2">\n\n',
                 f'<Document>\n',
                 f'    <name>{h_name}</name>\n\n']
    return head_temp


def line_style_temp(l_color, l_width):
    l_style_temp = [f'    <Style id="line-style">\n',
                    f'        <LineStyle>\n',
                    f'            <color>{l_color}</color>\n',
                    f'            <width>{l_width}</width>\n',
                    f'        </LineStyle>\n',
                    f'    </Style>\n\n']
    return l_style_temp


def look_temp(c_long, c_lat, c_alt, c_head, c_tilt, c_range, c_alt_mode):
    cam_temp = [f'    <LookAt>\n',
                f'        <longitude>{c_long}</longitude>\n',
                f'        <latitude>{c_lat}</latitude>\n',
                f'        <altitude>{c_alt}</altitude>\n',
                f'        <heading>{c_head}</heading>\n',
                f'        <tilt>{c_tilt}</tilt>\n',
                f'        <range>{c_range}</range>\n',
                f'        <gx:altitudeMode>{c_alt_mode}</gx:altitudeMode>\n',
                f'    </LookAt>\n\n']
    return cam_temp


def tour_temp(dur_temp):
    tour_head_temp = [f'    <gx:Tour>\n'
                      f'        <name>Double-click here to start tour</name>\n',
                      f'        <gx:Playlist>\n\n',
                      f'            <gx:Wait><gx:duration>{dur_temp}</gx:duration></gx:Wait>\n\n']  # Short pause at start.
    return tour_head_temp


def fly_to_temp(dur, c_mode, c_long, c_lat, c_alt, c_head, c_tilt, c_range, c_alt_mode, pause_temp):
    fly_temp = [f'            <gx:FlyTo>\n',
                f'                <gx:duration> {dur} </gx:duration>\n',
                f'                <gx:flyToMode> {c_mode} </gx:flyToMode>\n',
                f'                <LookAt>\n',
                f'                    <longitude> {c_long} </longitude>\n',
                f'                    <latitude> {c_lat} </latitude>\n',
                f'                    <altitude> {c_alt} </altitude>\n',
                f'                    <heading> {c_head} </heading>\n',
                f'                    <tilt> {c_tilt} </tilt>\n',
                f'                    <range> {c_range} </range>\n',
                f'                    <altitudeMode> {c_alt_mode} </altitudeMode>\n',
                f'                </LookAt>\n',
                f'            </gx:FlyTo>\n\n',
                f'            <gx:Wait><gx:duration>{pause_temp}</gx:duration></gx:Wait>\n\n']
    return fly_temp


def animation_temp(id_temp):  # Template for the animation loop
    an_temp = [f'            <gx:AnimatedUpdate>\n',
               f'                <Update>\n',
               f'                    <Change><Placemark targetId="{id_temp}"><visibility>1</visibility></Placemark></Change>\n',
               f'                </Update>\n',
               f'            </gx:AnimatedUpdate>\n\n']
    return an_temp


def line_header_temp():
    line_head_temp = [f'    <Folder>\n',
                      f'        <name>Path Lines</name>\n\n',
                      f'        <Style>\n',
                      f'            <ListStyle>\n',
                      f'                <listItemType>checkHideChildren</listItemType>\n',
                      f'            </ListStyle>\n',
                      f'        </Style>\n\n']
    return line_head_temp


def placemark_line_temp(pm_id, pm_name, gps1_tmp, gps2_tmp):  # Template for looped GPS coordinates
    pml_tmp = [f'        <Placemark id="{pm_id}">\n',
               f'            <name>{pm_name}</name>\n',
               f'            <visibility>0</visibility>\n',
               f'            <styleUrl>#line-style</styleUrl>\n',
               f'            <LineString>\n',
               f'                <tessellate>1</tessellate>\n',
               f'                <coordinates>{gps1_tmp},0 {gps2_tmp},0</coordinates>\n',
               f'            </LineString>\n',
               f'        </Placemark>\n\n']
    return pml_tmp


def line_footer_temp():
    line_foot_temp = [f'    </Folder>\n\n']
    return line_foot_temp


def pin_header_temp():
    pin_head_temp = [f'    <Folder>\n',
                     f'        <name>Pins</name>\n\n',
                     f'        <Style id="pushpin">\n',
                     f'            <IconStyle>\n',
                     f'                <Icon>\n',
                     f'                    <href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n',
                     f'                </Icon>\n',
                     f'            </IconStyle>\n',
                     f'        </Style>\n\n']
    return pin_head_temp


def pin_temp(pin_id_temp, pin_name_temp, pin_long_temp, pin_lat_temp):
    p_temp = [f'    <Placemark id="{pin_id_temp}">\n',
              f'        <name>{pin_name_temp}</name>\n',
              f'        <styleUrl>#pushpin</styleUrl>\n',
              f'        <Point>\n',
              f'            <coordinates>{pin_long_temp},{pin_lat_temp},0</coordinates>\n',
              f'        </Point>\n',
              f'    </Placemark>\n\n']
    return p_temp


def body_temp(dur):  # Fixed body template
    bod_temp = [f'<gx:Wait> <gx:duration>{dur}</gx:duration></gx:Wait>\n\n',
                '	</gx:Playlist>\n',
                '</gx:Tour>\n\n',
                '	<Folder>\n',
                '		<name>Path segments</name>\n\n',
                '		<Style>\n',
                '			<ListStyle>\n',
                '				<listItemType>checkHideChildren</listItemType>\n',
                '			</ListStyle>\n',
                '		</Style>\n\n']
    return bod_temp


def gps_temp(gps_coord_raw_temp):  # Template for looped GPS coordinates
    # Finds the position of the delimiter ' ' which differentiates the GPS coordinates.
    space_index = gps_coord_raw_temp.find(' ')
    # Extracts the GPS coordinate as gps_temp.
    gps_tmp = gps_coord_raw_temp[0:space_index]
    return gps_tmp


input_file = input('What is the city list file to analyze?\n'
                   'Example: c:\\MyFolder\\track.kml\n')

output_file = input('What is the GPS file to output?\n'
                    'Example: Example: c:\\MyFolder\\track.kml\n')

output_cities = input('What is the city flight tour file to output?\n'
                    'Example: Example: c:\\MyFolder\\track.kml\n')

#input_file = 'C:\\NotBackedUp\\PythonProjects\\animate-google-earth\\csv_files\\cities_trimmed.csv'
#output_file = 'C:\\Python\\GPS-Files\\city_output_animation.kml'
#output_cities = 'C:\\Python\\GPS-Files\\output_cities_list.csv'

df_cities = \
    read_cities_csv(input_file)
df_cities = \
    clean_cities_csv(df_cities)
df_cities = \
    flight_path(df_cities, c.CITY_FLIGHT_DURATION)

df_cities.to_csv(f'{output_cities}')
city_count = len(df_cities.City)-1
total_stops_count = len(df_cities.index)
print(total_stops_count)

# Create the Google Earth input file
new_animation = open(output_file, 'w')
new_animation.writelines(
    header_temp(str(c.CITY_NAME)))
new_animation.writelines(
    line_style_temp(c.PATH_COLOR, c.LINE_WIDTH))

# Set initial camera position based on first point.
new_animation.writelines(
    look_temp(
        str(df_cities.at[0, 'Longitude']),
        str(df_cities.at[0, 'Latitude']),
        str(c.START_ALTITUDE_CITIES),
        str(c.CAMERA_HEADING_CITIES),
        str(c.CAMERA_TILT_CITIES),
        str(c.CAMERA_RANGE_CITIES),
        str(c.ALTITUDE_MODE_CITIES)))

new_animation.writelines(
    tour_temp(c.CITY_TOUR_INITIAL_DELAY))

for i, row in df_cities.iterrows():
    # Set up camera start point
    new_animation.writelines(
        fly_to_temp(
            c.CITY_FLIGHT_DURATION,
            c.CITY_FLY_MODE,
            str(row['Longitude']),
            str(row['Latitude']),
            str(c.LOOK_ALTITUDE_CITIES),
            str(c.CAMERA_HEADING_CITIES),
            str(c.CAMERA_TILT_CITIES),
            str(c.CAMERA_RANGE_CITIES),
            str(c.ALTITUDE_MODE_CITIES),
            c.CITY_PAUSE_DURATION))
    new_animation.writelines(
        animation_temp(i))

new_animation.writelines([f'        </gx:Playlist>\n    </gx:Tour>\n\n'])

new_animation.writelines(
    line_header_temp())

for i, row in df_cities.iterrows():
    new_animation.writelines(
        placemark_line_temp(
            i,
            str(row['City']),
            str(row['Coordinates_Clean']),
            str(row['Coordinates_Next']),))

new_animation.writelines(
    line_footer_temp())

new_animation.writelines(
    pin_header_temp())

df_cities_unique = df_cities.drop_duplicates(['City'])

for i, row in df_cities_unique.iterrows():
    new_animation.writelines(
        pin_temp(
            i+total_stops_count,
            str(row['City']),
            str(row['Longitude']),
            str(row['Latitude'])))

# Write the footer

new_animation.writelines(['    </Folder >\n', '</Document >\n', '</kml >'])

new_animation.close()
