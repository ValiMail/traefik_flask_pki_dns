FROM traefik:v2.4.11

COPY applications/traefik/conf/traefik-tls.yaml /etc/traefik/

