# This function returns a list which was converted from a png file
# This list is suitable for tensorflow classification


def resize(argv):
    from PIL import Image, ImageFilter

    # argv must be the path to a png file
    image = Image.open(argv).convert("L")
    width = float(image.size[0])
    height = float(image.size[1])

    # Create a white canvas of 28x28 pixels
    new_image = Image.new("L", (28, 28), (255))


    # Check if the original picture is a "fat" one or "thin" one

    # Fat
    if width > height:

        # Width becomes 20 pixels.
        # Resize height according to ratio width
        new_height = int( round( (20.0/width*height), 0 ) )

        # Resize and sharpen
        image = image.resize( (20, new_height), Image.ANTIALIAS ).filter(ImageFilter.SHARPEN)

        # Caculate the horizontal pozition
        width_top = int( round( ( (28 - new_height)/2 ), 0 ) )

        # Paste resized image on white canvas
        new_image.paste( image, (4, width_top) )

    # Thin
    else:
        # Heigth becomes 20 pixels.
        new_width = int( round( (20.0/height*width), 0 ) )
        image = image.resize( (new_width, 20), Image.ANTIALIAS ).filter(ImageFilter.SHARPEN)
        width_left = int( round( ( (28 - new_width)/2 ), 0 ) )
        new_image.paste( image, (width_left, 4) )


    # Get the pixel values
    pv = list(new_image.getdata())

    # Normalize the pixels
    pvn = [ (255-x)*1.0/255.0 for x in pv]
    return pvn
