FROM zero:latest

# "zero" is the image I build with all the packages needed for this app


# Copy the current directory contents into the container at /app
ADD . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World


# Run app.py when the container launches
CMD ["python3", "app.py"]
