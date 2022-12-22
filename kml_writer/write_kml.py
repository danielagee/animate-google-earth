class KmlWriter:
    import kml_writer.constants as writer_constants
    from kml_writer.read_kml import gps_coordinates_raw
    from kml_writer.read_kml import gps_points
    from kml_writer.read_kml import camera_latitude
    from kml_writer.read_kml import camera_longitude
    from kml_writer.read_kml import camera_altitude

    def header_temp(h_name):
        head_temp = ['<?xml version="1.0" encoding="UTF-8"?>\n',
                     '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:'
                     'kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n',
                     '<Document>\n',
                     f'    <name>{h_name}</name>\n',
                     '    <open>1</open>\n\n']
        return head_temp

    def line_style_temp(l_color, l_width):
        l_style_temp = ['    <Style id="line-style">\n',
                        '        <LineStyle>\n',
                        f'            <color>{l_color}</color><!-- this is the color of your path -->\n',
                        f'            <width>{l_width}</width><!-- this is the width of your path -->\n',
                        '        </LineStyle>\n',
                        '    </Style>\n\n']
        return l_style_temp

    def camera_temp(c_long, c_lat, c_alt, c_head, c_tilt, c_range):
        cam_temp = ['    <!-- this is the camera view -->\n\n',
                    '        <LookAt>\n',
                    f'            <longitude>{c_long}</longitude>\n',
                    f'            <latitude>{c_lat}</latitude>\n',
                    f'            <altitude>{c_alt}</altitude>\n',
                    f'            <heading>{c_head}</heading>\n',
                    f'            <tilt>{c_tilt}</tilt>\n',
                    f'            <range>{c_range}</range>\n',
                    '            <gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>\n',
                    '        </LookAt>\n\n',
                    '<gx:Tour>\n',
                    '    <name>Double-click here to start tour</name>\n',
                    '    <gx:Playlist>\n\n',
                    '         <gx:Wait> <gx:duration>1</gx:duration></gx:Wait>\n\n',  # Short pause at start.
                    '<!-- line animation -->\n\n',
                    '        <gx:AnimatedUpdate>\n',
                    '            <Update>\n',
                    '                <Change><Placemark targetId="0">'
                    '<visibility>1</visibility> </Placemark> </Change>\n',
                    '            </Update>\n',
                    '        </gx:AnimatedUpdate>\n\n']
        return cam_temp

    def animation_temp(dur, id):  # Template for the animation loop
        an_temp = [f'<gx:Wait><gx:duration>{dur}</gx:duration></gx:Wait>\n',
                   '		<gx:AnimatedUpdate>\n',
                   '			<Update>\n',
                   f'				<Change><Placemark targetId="{id}"><visibility>1</visibility></Placemark></Change>\n',
                   '			</Update>\n',
                   '		</gx:AnimatedUpdate>\n\n']
        return an_temp

    def body_temp(dur):  # Fixed body template
        bod_temp = [f'<gx:Wait> <gx:duration>{dur}</gx:duration></gx:Wait>\n\n',
                    '	</gx:Playlist>\n',
                    '</gx:Tour>\n\n',
                    '<!-- the tour ends here and the following is the line information -->\n\n',
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

    #output_file = input('What is the GPS file to output?\n'
    #                    'Example: Example: c:\\MyFolder\\track.kml\n')

    output_file = 'C:\\Python\\GPS-files\\output_animation.kml'

    # Create the Google Earth input file
    new_animation = open(output_file, 'w')

    # Add the header to the file
    new_animation.writelines(
        header_temp(str(writer_constants.NAME)))

    # Describe the line
    new_animation.writelines(
        line_style_temp(
            str(writer_constants.PATH_COLOR),
            writer_constants.LINE_WIDTH))

    # Set up camera start point
    new_animation.writelines(
        camera_temp(
            str(camera_longitude),
            str(camera_latitude),
            str(camera_altitude),
            str(writer_constants.CAMERA_HEADING),
            str(writer_constants.CAMERA_TILT),
            str(writer_constants.CAMERA_RANGE)))

    # Write the animation loops for targetId (data point ID number in the .kml file)
    for target_id in range(1, gps_points):
        new_animation.writelines(
            animation_temp(str(writer_constants.ANIMATION_DELAY),
                           str(target_id)))

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
