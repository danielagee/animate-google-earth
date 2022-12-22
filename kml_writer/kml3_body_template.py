

# body text which fills the transition from animation loops to GPS coordinates
body = ['<gx:Wait> <gx:duration>1</gx:duration></gx:Wait>\n\n',
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

# Template for looped GPS coordinates
placemark_loop1 = ['<Placemark id="']
placemark_loop2 = ['">\n',
                   '		<name>']
placemark_loop3 = ['</name>\n',
                   '		<visibility>0</visibility>\n',
                   '		<styleUrl>#line-style</styleUrl>\n',
                   '		<LineString>\n',
                   '			<tessellate>1</tessellate>\n',
                   '			<coordinates>']
placemark_loop4 = ['\n',
                   '			</coordinates>\n',
                   '		</LineString>\n',
                   '    </Placemark>\n']


