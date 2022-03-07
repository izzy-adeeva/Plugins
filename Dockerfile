FROM teamvaders/hellbot:latest

RUN git clone https://github.com/izzy-adeeva/Plugins.git /root/ramext

WORKDIR /root/ramext

RUN pip3 install -U -r requirements.txt

ENV PATH="/home/hellbot/bin:$PATH"

CMD ["python3", "-m", "ramext"]
