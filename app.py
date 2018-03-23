from flask import Flask, request, jsonify
from werkzeug import secure_filename
from cassandra.cluster import Cluster
from utils import imageManip

app = Flask(__name__)


@app.route("/", methods = ["POST"])
def main():
    cluster = Cluster(contact_points = ["172.18.0.2"], port = 9042)
    session = cluster.connect()

    if request.method == "POST" and request.files["image"]:
        image = request.files["image"]
        file_name = secure_filename(image.filename)
        identified_digit, time_stamp = imageManip.classifyThis(image)

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



if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 80)
