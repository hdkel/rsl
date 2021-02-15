FROM python:3.7.6 as hdb-crawler

WORKDIR /usr/src/hdb_api
RUN pip3 install --no-cache-dir Scrapy

# Install node
RUN apt-get update && apt-get -y install curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_14.x  | bash -
RUN apt-get -y install nodejs

# NPM install and run!
RUN npm install
CMD [ "node", "server.js" ]