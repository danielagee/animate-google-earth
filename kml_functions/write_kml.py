class KmlWriter:
    import kml_functions.constants as c
    from kml_functions.read_kml import gps_coordinates_raw
    from kml_functions.read_kml import gps_points
    from kml_functions.read_kml import camera_latitude
    from kml_functions.read_kml import camera_longitude
    from kml_functions.read_kml import camera_altitude

    #output_file = input('What is the GPS file to output?\n'
    #                    'Example: Example: c:\\MyFolder\\track.kml\n')

    output_file = 'C:\\Python\\GPS-files\\output_animation.kml'

    def header_temp(h_name):
        head_temp = [f'<?xml version="1.0" encoding="UTF-8"?>\n',
                     f'<kml xmlns="http://www.opengis.net/kml/2.2"\n  xmlns:gx="http://www.google.com/kml/ext/2.2">\n\n',
                     f'<Document>\n',
                     f' <name>{h_name}</name>\n',
                     f' <open>1</open>\n\n']
        return head_temp

    def line_style_temp(l_color, l_width):
        l_style_temp = [f'  <Style id="line-style">\n',
                        f'      <LineStyle>\n',
                        f'          <color>{l_color}</color>\n',
                        f'          <width>{l_width}</width>\n',
                        f'      </LineStyle>\n',
                        f'  </Style>\n\n']
        return l_style_temp

    def camera_temp(c_long, c_lat, c_alt, c_head, c_tilt, c_range, c_alt_mode):
        cam_temp = [f'  <LookAt>\n',
                    f'      <longitude>{c_long}</longitude>\n',
                    f'      <latitude>{c_lat}</latitude>\n',
                    f'      <altitude>{c_alt}</altitude>\n',
                    f'      <heading>{c_head}</heading>\n',
                    f'      <tilt>{c_tilt}</tilt>\n',
                    f'      <range>{c_range}</range>\n',
                    f'      <gx:altitudeMode>{c_alt_mode}</gx:altitudeMode>\n',
                    f'  </LookAt>\n\n',
                    f'<gx:Tour>\n',
                    f'  <name>Double-click here to start tour</name>\n',
                    f'  <gx:Playlist>\n\n',
                    f'      <gx:Wait> <gx:duration>1</gx:duration></gx:Wait>\n\n',  # Short pause at start.
                    f'      <gx:AnimatedUpdate>\n',
                    f'          <Update>\n',
                    f'              <Change><Placemark targetId="0">'
                    f'<visibility>1</visibility> </Placemark> </Change>\n',
                    f'          </Update>\n',
                    f'      </gx:AnimatedUpdate>\n\n']
        return cam_temp

    def animation_temp(dur, id):  # Template for the animation loop
        an_temp = [f'<gx:Wait><gx:duration>{dur}</gx:duration></gx:Wait>\n',
                   f'<gx:AnimatedUpdate>\n',
                   f'   <Update>\n',
                   f'       <Change><Placemark targetId="{id}"><visibility>1</visibility></Placemark></Change>\n',
                   f'   </Update>\n',
                   f'</gx:AnimatedUpdate>\n\n']
        return an_temp

    def fly_to_temp(dur, c_long, c_lat, c_alt, c_head, c_tilt, c_range, c_alt_mode):
        fly_temp = [f'<gx:FlyTo>\n',
                    f'  <gx:duration> {dur} </gx:duration>\n',
                    f'  <gx:flyToMode> smooth </gx:flyToMode>\n',
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

    # Create the Google Earth input file
    new_animation = open(output_file, 'w')

    # Add the header to the file
    new_animation.writelines(
        header_temp(str(c.CITIES_NAME)))

    # Describe the line
    new_animation.writelines(
        line_style_temp(
            str(c.PATH_COLOR),
            c.LINE_WIDTH))

    # Set up camera start point
    new_animation.writelines(
        camera_temp(
            str(camera_longitude),
            str(camera_latitude),
            str(camera_altitude),
            str(c.CAMERA_HEADING),
            str(c.CAMERA_TILT),
            str(c.CAMERA_RANGE),
            str(c.ALTITUDE_MODE)))

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

    # Write the footer
    new_animation.writelines(['    </Folder >\n','  </Document >\n','</kml >'])

    new_animation.close()
