
Dockerized Single-digit Number Classification
====================
This application uses:
* Docker CE
* A deep net model trained by MNIST with tensorflow
* Flask
* Cassandra


When running it, follow the following steps:

* Create a docker network (in my case, "some-net")
* Start a Cassandra container, and initialize it using cass_init.py
* Run the app image (in my case, "one:latest") in a container, and connect it to the network
* Use "curl" to post a *png* file to the app, getting a JSON containing the number identified by the model and the time stamp as return
* Use cqlsh in cassandra to check the history of posted files (time stamp, file name, identified digit)

