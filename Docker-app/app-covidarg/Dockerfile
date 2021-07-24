# We simply inherit the Python 3 image. This image does
# not particularly care what OS runs underneath
FROM python:3.6

# Set an environment variable with the directory
# where we'll be running the app
ENV APP2 /app-covidarg

# Create the directory and instruct Docker to operate
# from there from now on
RUN mkdir $APP2
WORKDIR $APP2

# Expose the port uWSGI will listen on
EXPOSE 5002

# Copy the requirements file in order to install
# Python dependencies
COPY . .

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements-covidarg.txt

# Finally, we run uWSGI with the ini file we
# created earlier
CMD [ "uwsgi", "--ini", "app.ini" ]
#CMD ["python3", "void.py"]
