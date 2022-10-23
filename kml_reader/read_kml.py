class KmlReader:
    import linecache
    import kml_reader.constants as reader_constants

    # extracts the data I need from line 19 of the recorded GPS file.
    gps_coordinates_raw = linecache.getline(reader_constants.INPUT_FILE, 19)
    # removes the fixed prefix from the front of the data.
    gps_coordinates_raw = gps_coordinates_raw.removeprefix('        <coordinates>')
    # removes the fixed suffix from the end of the data.
    gps_coordinates_raw = gps_coordinates_raw.removesuffix('</coordinates>\n')
    # Finds the position of the delimitor ' ' which differentiates the GPS coordinates.
    space_index = gps_coordinates_raw.find(' ')
    # Extracts the first GPS coordinate as gps_temp.
    gps_temp = gps_coordinates_raw[0:space_index]
    # Adds the mandatory suffix and stores the result as GPS coordinate 1.
    gps1 = gps_temp + ',0'
    # Test print to check formatting.
    print(gps1)
    print(gps_coordinates_raw)

    # Removes the already captured GPS coordinate and remaining " " delimiter
    gps_coordinates_raw = gps_coordinates_raw.removeprefix(gps_temp + ' ')

    # Repeats the process built for GPS coordinate 1 to extract GPS coordinate 2.
    space_index = gps_coordinates_raw.find(' ')
    gps_temp = gps_coordinates_raw[0:space_index]
    gps2 = gps_temp + ',0'
    print(gps2)
    gps_coordinates_raw = gps_coordinates_raw.removeprefix(gps_temp + ' ')

    # Combines GPS coordinate 1 and 2 to make the GPS pair required for the path.
    print(gps1 + ' ' + gps2)
