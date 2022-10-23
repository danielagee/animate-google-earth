class KmlWriter:
    import kml_writer.constants as writer_constants
    import kml_writer.kml_header_template as header_template
    import kml_writer.kml_animation_template as animation_template
    import kml_writer.kml_body_template as body_template
    import kml_writer.kml_footer_template as footer_template
    from kml_writer.read_kml import gps_coordinates_raw

    # Create the Google Earth input file "new_animation.kml"
    new_animation = open(writer_constants.OUTPUT_FILE, 'w')

    # Add the header to the file
    new_animation.writelines(header_template.header1)
    new_animation.writelines(str(writer_constants.PATH_COLOR))
    new_animation.writelines(header_template.header2)
    new_animation.writelines(str(writer_constants.LINE_WIDTH))
    new_animation.writelines(header_template.header3)
    new_animation.writelines(str(writer_constants.CAMERA_LONGITUDE))
    new_animation.writelines(header_template.header4)
    new_animation.writelines(str(writer_constants.CAMERA_LATITUDE))
    new_animation.writelines(header_template.header5)
    new_animation.writelines(str(writer_constants.CAMERA_ALTITUDE))
    new_animation.writelines(header_template.header6)
    new_animation.writelines(str(writer_constants.CAMERA_HEADING))
    new_animation.writelines(header_template.header7)
    new_animation.writelines(str(writer_constants.CAMERA_TILT))
    new_animation.writelines(header_template.header8)
    new_animation.writelines(str(writer_constants.CAMERA_RANGE))
    new_animation.writelines(header_template.header9)

    # write the animation loops for targetId in the .kml file
    # targetId is the data point ID number in the .kml file
    # As I need to write the same formatting over and over with only a change in
    # the targetId, I can achieve this with a for loop on target_id.
    for target_id in range(1, 5):  # repeating 5 times only just as a test.
        new_animation.writelines(animation_template.animation_loop1)
        new_animation.write(str(writer_constants.ANIMATION_DELAY))
        new_animation.writelines(animation_template.animation_loop2)
        new_animation.write(str(target_id))
        new_animation.writelines(animation_template.animation_loop3)

    # Add the body transition to the file
    new_animation.writelines(body_template.body)

    # for loops for GPS coordinates and counting of placemark id.
    # Placemark id is the data point ID number in the .kml file which aligns with
    # targetId written before. For this, we have to use 4 sets of strings plus the
    # Placemark id twice and the GPS coordinates. Templates for this are stored in
    # kml_body_template.py

    # Temporarily hard code the number of loops as the target_id for loop
    for placemark_id in range(1, 5):
        new_animation.writelines(body_template.placemark_loop1)
        new_animation.write(str(placemark_id))
        new_animation.writelines(body_template.placemark_loop2)
        new_animation.write(str(placemark_id))
        new_animation.writelines(body_template.placemark_loop3)

        # Test print to check formatting and proper import of gps_coordinates_raw
        print(gps_coordinates_raw)

        # Finds the position of the delimiter ' ' which differentiates the GPS coordinates.
        space_index = gps_coordinates_raw.find(' ')
        # Extracts the first GPS coordinate as gps_temp.
        gps_temp = gps_coordinates_raw[0:space_index]
        # Adds the mandatory suffix and stores the result as GPS coordinate 1.
        gps1 = gps_temp + ',0'
        # Test print to check formatting.
        print(gps1)

        # Removes the already captured GPS coordinate and remaining " " delimiter
        gps_coordinates_raw = gps_coordinates_raw.removeprefix(gps_temp + ' ')

        # Repeats the process built for GPS coordinate 1 to extract GPS coordinate 2.
        space_index = gps_coordinates_raw.find(' ')
        gps_temp = gps_coordinates_raw[0:space_index]
        gps2 = gps_temp + ',0'
        print(gps2)

        # Combines GPS coordinate 1 and 2 to make the GPS pair required for the path.
        print(str(gps1 + ' ' + gps2))
        new_animation.write(str(gps1 + ' ' + gps2))

        new_animation.writelines(body_template.placemark_loop4)

    # Write the footer
    new_animation.writelines(footer_template.footer)

    new_animation.close()
