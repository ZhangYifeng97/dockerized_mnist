
Dockerized application for classifying handwritten numbers
====================
This application uses mnist_deep model from the examples of *tensorflow*.

When running it, follow the following steps:

* Create a docker network
* Start a Cassandra container, and initialize it using cass_init.py
* Run the app image (which I call "one") in a container, and connect it to the network
* Use "curl" to post a png file to the app, and get a JSON containing the number, and the time stamp
* Use cqlsh in cassandra to check the history of posted files

