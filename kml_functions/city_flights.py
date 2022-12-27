import linecache
from statistics import median
import kml_functions.constants as c
import pandas as pd


def read_cities_csv(file):
    df_csv = pd.read_csv(f'{file}')
    df_csv = df_csv[['City', 'Country', 'Arrive', 'Depart', 'Coordinates']]
    df_csv['Coordinates'] = df_csv['Coordinates'].str.replace('°', '', regex=True)
    df_csv[['Latitude', 'Longitude']] = df_csv.Coordinates.str.split(", ", expand=True)
    return df_csv


def clean_cities_csv(df_csv):
    df_csv['ns_hemisphere'] = df_csv['Latitude'].str[-1:]
    df_csv['ns_hemisphere'] = df_csv['ns_hemisphere'].apply(lambda x: '' if x == 'N' else '-')
    df_csv['Latitude'] = df_csv[['ns_hemisphere', 'Latitude']].apply("".join, axis=1)
    df_csv['Latitude'] = df_csv['Latitude'].str[:-2]

    df_csv['ew_hemisphere'] = df_csv['Longitude'].str[-1:]
    df_csv['ew_hemisphere'] = df_csv['ew_hemisphere'].apply(lambda x: '' if x == 'E' else '-')
    df_csv['Longitude'] = df_csv[['ew_hemisphere', 'Longitude']].apply("".join, axis=1)
    df_csv['Longitude'] = df_csv['Longitude'].str[:-2]

    df_csv = df_csv.astype({'Latitude': 'float', 'Longitude': 'float'})
    df_csv.drop(columns=['Coordinates', 'ns_hemisphere', 'ew_hemisphere'], inplace=True)
    return df_csv


def header_temp(h_name):
    head_temp = [f'<?xml version="1.0" encoding="UTF-8"?>\n',
                 f'<kml xmlns="http://www.opengis.net/kml/2.2"\n  xmlns:gx="http://www.google.com/kml/ext/2.2">\n\n',
                 f'<Document>\n',
                 f' <name>{h_name}</name>\n']
    return head_temp


def line_style_temp(l_color, l_width):
    l_style_temp = [f'  <Style id="line-style">\n',
                    f'      <LineStyle>\n',
                    f'          <color>{l_color}</color>\n',
                    f'          <width>{l_width}</width>\n',
                    f'      </LineStyle>\n',
                    f'  </Style>\n\n']
    return l_style_temp


def look_temp(c_long, c_lat, c_alt, c_head, c_tilt, c_range, c_alt_mode):
    cam_temp = [f'  <LookAt>\n',
                f'      <longitude>{c_long}</longitude>\n',
                f'      <latitude>{c_lat}</latitude>\n',
                f'      <altitude>{c_alt}</altitude>\n',
                f'      <heading>{c_head}</heading>\n',
                f'      <tilt>{c_tilt}</tilt>\n',
                f'      <range>{c_range}</range>\n',
                f'      <gx:altitudeMode>{c_alt_mode}</gx:altitudeMode>\n',
                f'  </LookAt>\n\n',
                f'<gx:Tour>\n']
    return cam_temp


def tour_temp(dur_temp):
    tour_head_temp = [f'  <name>Double-click here to start tour</name>\n',
                      f'  <gx:Playlist>\n\n',
                      f'      <gx:Wait> <gx:duration>{dur_temp}</gx:duration></gx:Wait>\n\n']  # Short pause at start.
    return tour_head_temp


def animation_temp(dur, id_temp):  # Template for the animation loop
    an_temp = [f'<gx:Wait><gx:duration>{dur}</gx:duration></gx:Wait>\n',
               f'<gx:AnimatedUpdate>\n',
               f'   <Update>\n',
               f'       <Change><Placemark targetId="{id_temp}"><visibility>1</visibility></Placemark></Change>\n',
               f'   </Update>\n',
               f'</gx:AnimatedUpdate>\n\n']
    return an_temp


def fly_to_temp(dur, c_mode, c_long, c_lat, c_alt, c_head, c_tilt, c_range, c_alt_mode):
    fly_temp = [f'<gx:FlyTo>\n',
                f'  <gx:duration> {dur} </gx:duration>\n',
                f'  <gx:flyToMode> {c_mode} </gx:flyToMode>\n',
                f'  <LookAt>\n',
                f'      <longitude> {c_long} </longitude>\n',
                f'      <latitude> {c_lat} </latitude>\n',
                f'      <altitude> {c_alt} </altitude>\n',
                f'      <heading> {c_head} </heading>\n',
                f'      <tilt> {c_tilt} </tilt>\n',
                f'      <range> {c_range} </range>\n',
                f'      <altitudeMode> {c_alt_mode} </altitudeMode>\n',
                f'  </LookAt>\n',
                f'</gx:FlyTo>\n\n']
    return fly_temp


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


def placemark_temp(pm_id, pm_name, gps1_tmp, gps2_tmp):  # Template for looped GPS coordinates
    pm_tmp = [f'<Placemark id="{pm_id}">\n',
              f'		<name>{pm_name}</name>\n',
              '		<visibility>0</visibility>\n',
              '		<styleUrl>#line-style</styleUrl>\n',
              '		<LineString>\n',
              '			<tessellate>1</tessellate>\n',
              f'			<coordinates>{gps1_tmp} {gps2_tmp}\n',
              '			</coordinates>\n',
              '		</LineString>\n',
              '    </Placemark>\n']
    return pm_tmp


def gps_temp(gps_coord_raw_temp):  # Template for looped GPS coordinates
    # Finds the position of the delimiter ' ' which differentiates the GPS coordinates.
    space_index = gps_coord_raw_temp.find(' ')
    # Extracts the GPS coordinate as gps_temp.
    gps_temp = gps_coord_raw_temp[0:space_index]
    return gps_temp


#input_file = input('What is the GPS file to analyze?\n'
#                   'Example: c:\\MyFolder\\track.kml\n')

#output_file = input('What is the GPS file to output?\n'
#                    'Example: Example: c:\\MyFolder\\track.kml\n')

input_file = 'C:\\Python\\GPS\\cities.csv'
output_file = 'C:\\Python\\GPS-Files\\city_output_animation.kml'
output_cities = 'C:\\Python\\GPS-Files\\output_cities_list.csv'
df_cities = read_cities_csv(input_file)
df_cities = clean_cities_csv(df_cities)
df_cities.to_csv(f'{output_cities}')
city_count = len(df_cities.City)+1

# Build KML Animation File

# Create the Google Earth input file
new_animation = open(output_file, 'w')

# Add the header to the file
new_animation.writelines(header_temp(str(c.NAME)))

# Describe the line ----- Not needed until lines are added
# new_animation.writelines(line_style_temp(str(c.PATH_COLOR),c.LINE_WIDTH))

# Set initial camera position based on first point.
new_animation.writelines(
    look_temp(
        str(df_cities.at[0, 'Longitude']),
        str(df_cities.at[0, 'Latitude']),
        str(c.LOOK_ALTITUDE_CITIES),
        str(c.CAMERA_HEADING_CITIES),
        str(c.CAMERA_TILT_CITIES),
        str(c.CAMERA_RANGE_CITIES),
        str(c.ALTITUDE_MODE_CITIES)))

new_animation.writelines(tour_temp(c.CITY_DELAY))

for i, row in df_cities.iterrows():
    # Set up camera start point
    new_animation.writelines(
        fly_to_temp(
            c.CITY_FLY_DURATION,
            c.CITY_FLY_MODE,
            str(row['Longitude']),
            str(row['Latitude']),
            str(c.LOOK_ALTITUDE_CITIES),
            str(c.CAMERA_HEADING_CITIES),
            str(c.CAMERA_TILT_CITIES),
            str(c.CAMERA_RANGE_CITIES),
            str(c.ALTITUDE_MODE_CITIES)))

# Write the footer

new_animation.writelines(['	</gx:Playlist>',
                          '</gx:Tour>',
                          '<Folder>',
                          '<name>Path segments</name>'])

new_animation.writelines(['    </Folder >\n','  </Document >\n','</kml >'])

new_animation.close()
#gps_coordinates_raw = read_kml_track(input_file)

"""
# Counts the number of GPS points.
gps_points = len(df. index)

!!!!!!!!!!!!!!!!!Iterate to extract GPS points from DF and merge them with template


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













# Write the animation loops for targetId (data point ID number in the .kml file)
for target_id in range(1, gps_points):
    new_animation.writelines(
        animation_temp(str(c.ANIMATION_DELAY),
                       str(target_id)))
    new_animation.writelines(
        fly_to_temp(
            str(c.ANIMATION_DELAY),
            str(camera_longitude),
            str(camera_latitude),
            str(camera_altitude),
            str(c.CAMERA_HEADING + target_id / gps_points * c.TOTAL_ROTATION),
            str(c.CAMERA_TILT),
            str(c.CAMERA_RANGE),
            str(c.ALTITUDE_MODE))
    )

# Add the body transition to the file
new_animation.writelines(
    body_temp(1))

# Extracts individual GPS pairs from the GPS coordinates list. Placemark id aligns with targetId written before.
for placemark_id in range(1, gps_points):
    gps1 = gps_temp(gps_coordinates_raw)  # Extracts GPS1
    gps_coordinates_raw = gps_coordinates_raw.removeprefix(gps1 + " ")  # Trims GPS1 out of the GPS list.
    gps2 = gps_temp(gps_coordinates_raw)  # Extracts GPS2
    gps1 = gps1 + ',0'  # Adds mandatory suffix
    gps2 = gps2 + ',0'  # Adds mandatory suffix
    new_animation.writelines(
        placemark_temp(placemark_id, placemark_id, gps1, gps2))



"""
