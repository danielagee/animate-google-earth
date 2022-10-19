# template for animation loops
animation_loop1 = ['<gx:Wait><gx:duration>']

animation_loop2 = ['</gx:duration></gx:Wait>\n',
                   '		<gx:AnimatedUpdate>\n',
                   '			<Update>\n',
                   '				<Change><Placemark targetId="']

animation_loop3 = ['"><visibility>1</visibility></Placemark></Change>\n',
                   '			</Update>\n',
                   '		</gx:AnimatedUpdate>\n\n']