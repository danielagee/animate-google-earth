# Breaking the link to the header.kml file and inputting it here as hard code for now.

header1 = ['<?xml version="1.0" encoding="UTF-8"?>\n',
           '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:'
           'kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n',
           '<Document>\n',
           '    <name> Line Animation</name>\n',
           '    <open>1</open>\n\n',
           '    <Style id="line-style">\n',
           '        <LineStyle>\n',
           '            <color>']

header2 = ['</color><!-- this is the color of your path -->\n',
           '            <width>']

header3 = ['</width><!-- this is the width of your path -->\n',
           '        </LineStyle>\n',
           '    </Style>\n\n',
           '    <!-- this is the camera view -->\n\n',
           '        <LookAt>\n',
           '            <longitude>']

header4 = ['</longitude>\n',
           '            <latitude>']

header5 = ['</latitude>\n',
           '            <altitude>']

header6 = ['</altitude>\n',
           '            <heading>']

header7 = ['</heading>\n',
           '            <tilt>']

header8 = ['</tilt>\n',
           '            <range>']

header9 = ['</range>\n',
           '            <gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>\n',
           '        </LookAt>\n\n',
           '<gx:Tour>\n',
           '    <name>Double-click here to start tour</name>\n',
           '    <gx:Playlist>\n\n',
           '         <gx:Wait> <gx:duration>1</gx:duration></gx:Wait> <!-- short pause at the beginning -->\n\n',
           '<!-- line animation -->\n\n',
           '        <gx:AnimatedUpdate>\n',
           '            <Update>\n',
           '                <Change><Placemark targetId="0"><visibility>1</visibility> </Placemark> </Change>\n',
           '            </Update>\n',
           '        </gx:AnimatedUpdate>\n\n']

