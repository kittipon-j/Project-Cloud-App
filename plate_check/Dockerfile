FROM python:3.10.11
EXPOSE 5555

WORKDIR /plate_app

COPY plate_service.py /plate_app
COPY requirements.txt /plate_app
COPY ./common /plate_app/common
COPY ./model /plate_app/model

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0
RUN pip install -r requirements.txt

CMD python plate_service.py
