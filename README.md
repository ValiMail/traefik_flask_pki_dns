# traefik_flask__pki_dns

PKI + DNS client authentication using Traefik and Flask.

## What it does

The client attempts to POST to the API endpoint with `dane_id` and `message` fields populated.

The API endpoint requires any client certificate for mutual authentication.

After successful mTLS authentication, Traefik forwards the `HTTP_X_FORWARDED_TLS_CLIENT_CERT` header to uwsgi, together with the POST data.

Flask (sitting behind uwsgi) compares the `dane_id` name against a list of allowed host names and domains.

Next, flask parses the `HTTP_X_FORWARDED_TLS_CLIENT_CERT` field into an x.509 certificate and attempts to authenticate the presented certificate against the TLSA record for `dane_id`.

If the checks pass, the identity is validated. DANE validation happens live. No certs are cached in the application itself. Revocation happens at the speed of TTL.

## Setup

* Clone this repository on a system with a public IP address.
* Copy the `.env.example` file to `.env` and complete the settings.
  * Note: `BASE_DNS_NAME` is a DNS name under your control. Create an A record to point to the instance hosting this application. Create two CNAME records, one for `api.${BASE_DNS_NAME}` and another for `portal.${BASE_DNS_NAME}`, and point them both to `${BASE_DNS_NAME}`
* Install `docker-compose` and all dependencies.
* run `docker-compose up -d && docker-compose logs-f`

## Operation

### Post a message

```bash
curl -X POST \
    -d "dane_id=${VALID_DANE_ID}&message=${SOME_MESSAGE}" \
    --cert cert.pem \
    --key privkey.pem \
    https://api.${BASE_DNS_NAME}/new`

```

### Confirmation

```bash
curl https://portal.${BASE_DNS_NAME}/messages

```

## TODO

* [ ] Set smart TLS options (versions, cipher suites, etc)