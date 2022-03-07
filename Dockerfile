FROM teamvaders/hellbot:latest

RUN git clone https://github.com/izzy-adeeva/Plugins.git /root/userbot

WORKDIR /root/userbot

RUN pip3 install -U -r requirements.txt

ENV PATH="/home/hellbot/bin:$PATH"

CMD ["python3", "-m", "userbot"]