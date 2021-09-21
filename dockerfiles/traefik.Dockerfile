FROM traefik:v2.5.3

COPY applications/traefik/conf/traefik-tls.yaml /etc/traefik/

