FROM wgzhao/addax:4.1.6-lite AS addax
FROM openjdk:11 AS openjdk

FROM python:3.12.7
COPY --from=addax /opt/addax /opt/addax
COPY --from=openjdk /usr/local/openjdk-11 /opt/openjdk
ENV PATH=$PATH:/opt/openjdk/bin:/opt/addax/bin

COPY *.py /tmp/sync-jobs/
COPY config /tmp/sync-jobs/config
COPY mysql /tmp/sync-jobs/mysql
COPY logs /tmp/sync-jobs/logs
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN ["chmod", "+x", "/usr/local/bin/entrypoint.sh"]

ENTRYPOINT ["entrypoint.sh"]