FROM python:3.10.11
EXPOSE 5000

WORKDIR /check_app
COPY recognition_service.py /check_app
COPY requirements.txt /check_app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
COPY ./common /check_app/common
CMD python recognition_service.py
