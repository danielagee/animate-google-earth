class KmlHeader:
    # Create the Google Earth input file "new_animation.kml"
    new_animation = open(r'C:\Python\Google_Earth_Animator\new_animation.kml', 'w')

    # Basic test to see if I can write to the file I just created.
    test = ['test1\n', 'test2\n', 'test3\n']
    new_animation.writelines(test)

    # Close the Google Earth animation file.
    new_animation.close()
