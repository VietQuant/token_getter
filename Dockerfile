FROM ubuntu:18.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN apt-get install -y curl
RUN apt-get install -y net-tools
RUN apt-get install -y vim
RUN apt-get install -y nano
RUN apt-get install -y gcc gcc+
RUN apt install -y python3.7
RUN apt install -y python3-pip
USER root
RUN echo 'Asia/Ho_Chi_Minh' > /etc/timezone
RUN rm -f /etc/localtime
RUN apt update -y
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN pip3 install python-dotenv
RUN pip3 install kafka-python
RUN apt-get install -y chromium-browser --fix-missing
RUN curl -L "https://github.com/docker/compose/releases/download/1.28.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose
RUN ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
RUN pip3 install retrying
RUN pip3 install lxml
RUN pip3 install selenium
WORKDIR /DataCollector
COPY . .