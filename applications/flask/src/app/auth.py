"""Authentication-related routes."""
import base64
import datetime
import pprint
from urllib.parse import unquote

from flask import Blueprint
from flask import abort
# from flask import flash
# from flask import redirect
from flask import render_template
from flask import request
# from flask import url_for
# from flask_login import login_user
# from flask_login import logout_user
# from flask_login import login_required
from werkzeug.security import check_password_hash
from dane_discovery.identity import Identity
from dane_discovery.pki import PKI

# from .models import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET"])
def login():
    """Log in."""
    cert = request.environ["HTTP_X_FORWARDED_TLS_CLIENT_CERT"]
    cert_valid = does_certificate_dane(cert)
    if not cert_valid:
        return abort(403)
    return render_template("x5response.html", id_name=cert_valid)


def does_certificate_dane(cert):
    """Return first valid client name if certificate is valid, else empty string."""
    # This is the DNS-based ACL! Replace this with a proper 
    # ORM User or policy lookup feature
    allowed_ids = {"laptop1._device.universalauth.com"}
    clean_cert = unquote(cert)
    der_cert = base64.b64decode(clean_cert)
    try:
        x509_obj = PKI.build_x509_object(der_cert)
    except ValueError:
        print(clean_cert)
        return ""
    valid_dnsnames = [x for x in PKI.get_dnsnames_from_cert(x509_obj) if x in allowed_ids]
    for dnsname in valid_dnsnames:
        identity = Identity(dnsname)
        status, reason = identity.validate_certificate(der_cert)
        if status is True:
            return dnsname
        print("Not valid: {}".format(reason))
    return ""
    


    