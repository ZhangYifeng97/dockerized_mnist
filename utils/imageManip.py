from PIL import Image, ImageFilter
import time
import tensorflow as tf


def classifyThis(file_name):

    def maxPossibility(sess, x, y_conv, keep_prob, image):
        # Apply the model and return the number with maximum possibility
        result = list(sess.run(y_conv, {x:[image], keep_prob: 1.0})[0])
        return result.index(max(result))

    with tf.Session() as sess:

        # Restoring the previously trained model
        saver = tf.train.import_meta_graph("./model/mnist_deep.meta")
        saver.restore(sess, tf.train.latest_checkpoint("./model/"))

        # and some tensorflow variables needed for classification
        graph = tf.get_default_graph()
        x = graph.get_tensor_by_name("x:0")
        keep_prob = graph.get_tensor_by_name("dropout/keep_prob:0")
        y_conv = graph.get_tensor_by_name("fc2/y_conv:0")


        # Get the picture file and identify it
        data = png2data(file_name)
        identified_digit = maxPossibility(sess, x, y_conv, keep_prob, data)
        time_stamp = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

        return identified_digit, time_stamp




def png2data(file_name):

    # Reference:
    # https://stackoverflow.com/questions/44972395/python-converting-png-jpg-image-to-best-form-for-mnist-digit-classification

    # If I remove any step of the code (eg. paste it starting from (0, 0)), the classification result will become terrible...

    # I modified the variable names and comments to make them more readable (which used to be terribie, as is in the url)



    # argv must be the path to a png file
    raw_image = Image.open(file_name).convert("L")
    width = float(raw_image.size[0])
    height = float(raw_image.size[1])




    # Create a white canvas of 28x28 pixels
    new_image = Image.new("L", (28, 28), (255))


    # Check if the original picture is a "fat" one or "thin" one

    # Fat
    if width > height:

        # Width becomes 20 pixels.
        # Resize height according to ratio width
        new_height = int( 20.0/width*height )

        # Resize and sharpen
        resized_image = raw_image.resize( (20, new_height), Image.ANTIALIAS ).filter(ImageFilter.SHARPEN)

        # Caculate the horizontal pozition
        width_top = int( (28 - new_height)/2 )

        # Paste resized image on white canvas
        new_image.paste( resized_image, (4, width_top) )

    # Thin
    else:

        # Heigth becomes 20 pixels.
        new_width = int( 20.0/height*width )
        resized_image = raw_image.resize( (new_width, 20), Image.ANTIALIAS ).filter(ImageFilter.SHARPEN)
        width_left = int( (28 - new_width)/2 )
        new_image.paste( resized_image, (width_left, 4) )


    # Get the pixel values
    pv = list(new_image.getdata())

    # Normalize the pixels
    pvn = [ (255-x)*1.0/255.0 for x in pv]
    return pvn
