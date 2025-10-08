FROM python:3.6

WORKDIR /application

# Installer les dépendances système nécessaires à Fiona / GeoPandas
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    libproj-dev \
    libgeos-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

ADD requirements.txt /application/

RUN pip install -r /application/requirements.txt

CMD [ "python", "main.py" ]

