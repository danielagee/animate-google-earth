import linecache
import kml_writer.constants as constants

# extracts the data I need from line 19 of the recorded GPS file.
gps_coordinates_raw = linecache.getline(constants.INPUT_FILE, 19)
# removes the fixed prefix from the front of the data.
gps_coordinates_raw = gps_coordinates_raw.removeprefix('        <coordinates>')
# removes the fixed suffix from the end of the data.
gps_coordinates_raw = gps_coordinates_raw.removesuffix('</coordinates>\n')

