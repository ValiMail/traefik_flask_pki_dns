# traefik_flask_pki_dns

PKI + DNS client authentication using Traefik and Flask.

## What it does

The client attempts to POST to the API endpoint with `dane_id` and `message` fields populated.

The API endpoint requires any client certificate for mutual authentication.

After successful mTLS authentication, Traefik forwards the `HTTP_X_FORWARDED_TLS_CLIENT_CERT` header to uwsgi, together with the POST data.

Flask (sitting behind uwsgi) compares the `dane_id` name against a list of allowed host names and domains.

Next, flask parses the `HTTP_X_FORWARDED_TLS_CLIENT_CERT` field into an x.509 certificate and attempts to authenticate the presented certificate against the TLSA record for `dane_id`.

If DANE checks pass, the identity is validated. DANE validation happens live. No certificates are cached in the application itself. Revocation happens at the speed of TTL.

## Setup

* Clone this repository on a system with a public IP address.
* Install `docker-compose` and all dependencies.
* Copy the `.env.example` file to `.env` and complete the settings therein.
  * Policy for allowing clients to post data to the system are defined using two environment variables:
    * `ALLOW_DOMAINS` is a comma-separated list of domains which should be permitted to post messages to the application.
    * `ALLOW_HOSTS` is a comma-separated list of DNS names which are allowed to post messages to the API.
  * `BASE_DNS_NAME` is a DNS name under your control. Create an A record to point to the instance hosting this application. Create two `CNAME` records, one for `api.${BASE_DNS_NAME}` and another for `portal.${BASE_DNS_NAME}`, and point them both to `${BASE_DNS_NAME}`. For instance:
    * If your `BASE_DNS_NAME` is `machine.mydomain.example`:
      * Provision an A record for `machine.mydomain.example`
      * Provision a CNAME record for `api.machine.mydomain.example`, which points to `machine.mydomain.example`
      * Provision a CNAME record for `portal.machine.mydomain.example`, which points to `machine.mydomain.example`
* run `docker-compose up -d && docker-compose logs -f`
* Open a browser and navigate to <https://portal.${BASE_DNS_NAME}/messages>. Authenticated messages will appear on this page.

## Operation

### Post a message

```bash
curl -X POST \
    -d "dane_id=${CLIENT_DANE_ID}" \
    --data-urlencode "message=${SOME_MESSAGE}" \
    --cert cert.pem \
    --key privkey.pem \
    https://api.${BASE_DNS_NAME}/new`

```

The `CLIENT_DANE_ID` variable is a DNS name where a correctly-configured TLSA record can be found, corresponding to the private key being used for client identification.

`SOME_MESSAGE` is just a plaintext message.

### Confirmation

```bash
curl https://portal.${BASE_DNS_NAME}/messages

```

Or browse to <https://portal.${BASE_DNS_NAME}/messages>

## TODO

* [ ] Set ideal TLS options (versions, cipher suites, etc)
