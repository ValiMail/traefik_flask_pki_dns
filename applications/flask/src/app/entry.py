"""Routes for entry-related pages."""
import base64
import os

from flask import Blueprint
from flask import request
from flask import abort
from flask import render_template
from flask.wrappers import Response
from urllib.parse import unquote
from dane_discovery.identity import Identity
from dane_discovery.pki import PKI

from .models import Entry
from .validator import Validator

from . import db

entry = Blueprint("entry", __name__)

@entry.route("/new", methods=["POST"])
def entries_new_post():
    """Create new entry."""
    if not request.headers['Host'] == "api.{}".format(os.getenv("BASE_DNS_NAME")):
        return abort(404, "A whole bunch of nope for you. ({} is not {})".format(
                         request.headers['Host'], 
                         "api.{}".format(os.getenv("BASE_DNS_NAME"))))
    cert = request.environ["HTTP_X_FORWARDED_TLS_CLIENT_CERT"]
    dane_id = request.form.get("dane_id").strip(".")
    message = request.form.get("message")
    authenticated, reason = authenticate_dane(dane_id, cert)
    if not authenticated:
        return abort(403, reason)
    new_content = Entry(source=dane_id, body=message)
    db.session.add(new_content)
    total_rows = Entry.query.count()
    print("Total rows: {}".format(total_rows))
    if total_rows > 1000:
        try:
            entry_ids = [e.id for e in Entry.query.all()]
            entry_ids.sort()
            delete_me = Entry.__table__.delete().where(
                                    Entry.id.in_(entry_ids[:20]))
            print(delete_me)
            db.session.execute(delete_me)
            print("Trimming table...")
        except Exception as err:
            print("ERROR: {}".format(err))
    db.session.commit()
    return "Thank you, {}, for your message.".format(dane_id), 202


@entry.route("/messages", methods=["GET"])
def entries_read():
    """Read all entries."""
    if not request.headers['Host'] == "portal.{}".format(os.getenv("BASE_DNS_NAME")):
        return abort(404, "Sorry, buddy. You're not in the list. ({})".format(request.headers['Host']))
    messages = Entry.query.all()
    return render_template("all_messages.html", messages=messages)


def authenticate_dane(dane_id, cert):
    """Return True if the cert is valid for dane_id, else False."""
    if not Validator.is_a_valid_domain_name(dane_id):
        reason = "Invalid DANE id: {}".format(dane_id)
        return False, reason
    domains, hosts = get_policy()
    if dane_id not in hosts and not [x for x in domains if Validator.dnsname_in_domain(dane_id, x)]:
        reason = ("ID {} not allowed.".format(dane_id))
        return False, reason
    clean_cert = unquote(cert)
    der_cert = base64.b64decode(clean_cert)
    try:
        PKI.build_x509_object(der_cert)
    except ValueError:
        reason = "Can't parse x509: {}".format(clean_cert)
        return False, reason
    resolver_override = os.getenv("RESOLVER_OVERRIDE", "1.1.1.1")
    identity = Identity(dane_id, None, resolver_override)
    status, reason = identity.validate_certificate(der_cert)
    if status is True:
        return True, ""
    reason = "DANE match for {} failed: {}!".format(dane_id, reason)
    return False, reason


def get_policy():
    """Return a two lists, one for wildcards and one for direct matches."""
    domains_from_env = os.getenv("ALLOW_DOMAINS", "").split(",")
    hostnames_from_env = os.getenv("ALLOW_HOSTS", "").split(",")
    domains = [x.strip() for x in domains_from_env if Validator.is_a_valid_domain_name(x)]
    hosts = [x.strip() for x in hostnames_from_env if Validator.is_a_valid_domain_name(x)]
    return domains, hosts
