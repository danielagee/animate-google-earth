class KmlWriter:
    import kml_writer.constants as writer_constants
    import kml_writer.kml_header_template as header_template
    import kml_writer.kml_animation_template as animation_template

    # Create the Google Earth input file "new_animation.kml"
    new_animation = open(writer_constants.OUTPUT_PATH + writer_constants.OUTPUT_NAME, 'w')

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

    new_animation.close()
