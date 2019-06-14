FROM balenalib/rpi-raspbian

RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    git

WORKDIR /app
RUN git clone https://github.com/hassiweb/mitemp-sender.git & cd mitemp-sender
RUN pip3 install -r requirements.txt

CMD ["bash"]
