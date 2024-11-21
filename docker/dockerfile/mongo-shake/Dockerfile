FROM python:2

COPY mongo-shake-v2.8.4 /opt/mongo-shake
WORKDIR /

EXPOSE 9100 9101 9200
ENV PATH=$PATH:/opt/mongo-shake
WORKDIR /opt/mongo-shake
ENTRYPOINT ["collector.linux", "-conf=collector.conf"]




