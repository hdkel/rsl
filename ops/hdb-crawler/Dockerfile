FROM python:3.7.6 as hdb-crawler

WORKDIR /hdb_crawler
RUN pip3 install --no-cache-dir Scrapy

# This is to keep container alive
CMD ["tail", "-f", "/dev/null"]