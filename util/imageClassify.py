



def classify(file_name):
    import os
    import time
    import tensorflow as tf
    from util import imageManip

    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

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
        data = imageManip.resize(file_name)
        identified_digit = identifyThis(sess, x, y_conv, keep_prob, data)
        time_stamp = time.time()

        return (identified_digit, time_stamp)
