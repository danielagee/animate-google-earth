import linecache

input_file = input('What is the GPS file to analyze?\n'
                   'Example: c:\\MyFolder\\track.kml\n')

# extracts the data I need from line 19 of the recorded GPS file.
gps_coordinates_raw = linecache.getline(input_file, 19)
# removes the fixed prefix from the front of the data.
gps_coordinates_raw = gps_coordinates_raw.removeprefix('        <coordinates>')
# removes the fixed suffix from the end of the data.
gps_coordinates_raw = gps_coordinates_raw.removesuffix('</coordinates>\n')
