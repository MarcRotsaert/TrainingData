# Debian Base Image with Python 3.11
# LABEL version="1.0"
# LABEL description="Alleen maar testen van Docker"
# ADD src /app
FROM python:bullseye

ADD . /mnt/Polar
ADD requirements.txt  /mnt/Polar/python/requirements.txt
ADD data/polar-user-data-export /mnt/Polar/looptracks/polar-user-data-export

# Install Pyton libraries
RUN python -m pip install --no-cache-dir -r /mnt/Polar/python/requirements.txt 

# Environment variables
ENV PYTHONBUFFERED=1
ENV DJANGO_SETTINGS_MODULE="myfirstdjango.settings"

# Filepath location in Docker container
WORKDIR /mnt/Polar

CMD ["python","python/main_polar_analyzer.py"]