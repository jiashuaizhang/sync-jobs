FROM debian:stable

COPY redis-shake /usr/local/bin
COPY shake.toml /etc
WORKDIR /

ENTRYPOINT ["redis-shake", "/etc/shake.toml"]




