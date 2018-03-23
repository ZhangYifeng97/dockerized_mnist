from flask import Flask, request, jsonify
from werkzeug import secure_filename
from PIL import Image, ImageFilter
from cassandra.cluster import Cluster


import time

import tensorflow as tf





app = Flask(__name__)







@app.route("/", methods = ["POST"])
def main():
    cluster = Cluster(contact_points = ["172.18.0.2"], port = 9042)
    session = cluster.connect()

    if request.method == "POST" and request.files["image"]:
        image = request.files["image"]
        file_name = secure_filename(image.filename)
        identified_digit = getImageAndClassify(image)
        time_stamp = time.time()
        session.execute(
        """
            INSERT INTO mykeyspace.ImgCls (file_name, posted_time, identified_digit)
            VALUES (%s, %s, %s)
        """,
            (file_name, time_stamp, identified_digit)
        )

        response = {"Identified Number": identified_digit, "Time": time_stamp}
        return jsonify(**response)
    else:
    	return "No image uploaded."






def imageResize(argv):

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






def getImageAndClassify(file_name):

    def identifyThis(sess, x, y_conv, keep_prob, image):
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
        data = imageResize(file_name)
        identified_digit = identifyThis(sess, x, y_conv, keep_prob, data)


        return identified_digit




if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 80)
