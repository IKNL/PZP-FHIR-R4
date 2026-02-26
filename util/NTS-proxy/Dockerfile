FROM debian:bookworm
RUN apt-get update
RUN apt-get -y install mitmproxy
RUN apt-get -y install python3-requests
COPY NTS-proxy.py /NTS-proxy.py
ENTRYPOINT ["mitmdump", "-s", "/NTS-proxy.py"]