class KmlHeader:
    import kml_writer.constants as writer_constants
    import kml_writer.kml_header_template as template

    # Create the Google Earth input file "new_animation.kml"
    new_animation = open(writer_constants.OUTPUT_PATH + writer_constants.OUTPUT_NAME, 'w')

    # Add the header to the file
    new_animation.writelines(template.header1)
    new_animation.writelines(str(writer_constants.PATH_COLOR))
    new_animation.writelines(template.header2)
    new_animation.writelines(str(writer_constants.LINE_WIDTH))
    new_animation.writelines(template.header3)
    new_animation.writelines(str(writer_constants.CAMERA_LONGITUDE))
    new_animation.writelines(template.header4)
    new_animation.writelines(str(writer_constants.CAMERA_LATITUDE))
    new_animation.writelines(template.header5)
    new_animation.writelines(str(writer_constants.CAMERA_ALTITUDE))
    new_animation.writelines(template.header6)
    new_animation.writelines(str(writer_constants.CAMERA_HEADING))
    new_animation.writelines(template.header7)
    new_animation.writelines(str(writer_constants.CAMERA_TILT))
    new_animation.writelines(template.header8)
    new_animation.writelines(str(writer_constants.CAMERA_RANGE))
    new_animation.writelines(template.header9)

    # Close the Google Earth animation file.
    new_animation.close()