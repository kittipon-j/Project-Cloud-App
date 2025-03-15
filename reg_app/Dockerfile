FROM python:3.10.11
EXPOSE 3000

WORKDIR /reg_app
COPY register_service.py /reg_app
COPY requirements.txt /reg_app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt

COPY ./common /reg_app/common
CMD python register_service.py