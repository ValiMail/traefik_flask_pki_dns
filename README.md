# traefik_flask__pki_dns

PKI + DNS client authentication using Traefik and Flask.

## What it does

Traefik supports mutual TLS authentication, with no binding to a particular CA. 

If the client can prove possession of the private key, the TLS client will be authenticated by Traefik.

Traefik forwards the `HTTP_X_FORWARDED_TLS_CLIENT_CERT` header to uwsgi, which fronts the Flask application.

The `HTTP_X_FORWARDED_TLS_CLIENT_CERT` header is decoded and parsed into a certificate, which is then parsed by the application, which checks the following:

* Does the certificate have at least one dNSName in the subjectAltName of the certificate?
* Does one of the dNSName values align with a user in the client ACL? (auth.py, line 39)
* Does the presented certificate match the DANE record for the aligned dNSName?

If all three checks pass, the identity is validated. DANE(ish) validation happens live. No certs are cached in the application itself. Revocation happens at the speed of TTL.

## Opportunities for improvement

* [ ] When dealing with the potential multiplicity of dNSName members of the subjectAltName, we could have a dNSName that is DANE-valid for an identity right next to one that is not. We could also have multiple valid names, and only the first one would be authenticated. It would be better to have a POST URL for authentication which accepts a DANE DNS name from the client, which is then used as the anchoring name for the certificate that we wish to verify, which gets validated by Traefik and passed through in the `HTTP_X_FORWARDED_TLS_CLIENT_CERT` header.
* [ ] Integrate with the Validev policy engine for representing roles and members.
* [ ] Establish a client session and sort out different routing rules (in Traefik) for TLS auth. Should not need TLS authentication for every page. This is for client browsers.
* [ ] Establish an API interaction pattern, with one auth per interaction.
* [ ] Establish an API interaction pattern for bearer token issuance.