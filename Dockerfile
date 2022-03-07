# slim-buster is significantly smaller, but to compensate excludes certain tools such as gcc (which may be needed to build certain dependencies)
# For now will use buster image until discover valid ways of reducing both image size and build time

FROM python:3.9.7-buster

RUN apt-get -y update

RUN apt-get -y install git

WORKDIR /home

RUN git clone https://github.com/lukadd16/NBC-Boterator.git

WORKDIR /home/NBC-Boterator

RUN pip install -r requirements.txt

COPY config.py .

CMD [ "python3", "main.py"]
