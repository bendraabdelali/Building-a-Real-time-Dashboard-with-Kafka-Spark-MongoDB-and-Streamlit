FROM python:3.8-slim-buster

WORKDIR /app

RUN pip install numpy kafka-python Faker

COPY ./Stream/streamAddUsers.py ./streamAddUsers.py

CMD [ "python3", "streamAddUsers.py"]