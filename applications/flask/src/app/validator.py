"""Validation functions."""

import base64

from dane_discovery.identity import Identity
from dane_discovery.pki import PKI


class Validator:
    """Validation happens here."""

    @classmethod
    def is_a_valid_domain_name(cls, domain_name):
        """Return True if domain is valid.

        We check that all labels are 63 characters or less, and
        the entire domain name is no more than 253 characters.
        """
        label_representation = cls.domain_str_to_labels(domain_name)
        for label in label_representation:
            if len(label) >= 63:
                return False
        if len(domain_name) > 253:
            return False
        for unallowed in ["/", "\\", ":"]:
            if unallowed in domain_name:
                return False
        return True

    @classmethod
    def domain_str_to_labels_reverse(cls, domain_name):
        """Return a list of domain name labels, in reverse-DNS order."""
        labels = domain_name.rstrip(".").split(".")
        labels.reverse()
        return labels

    @classmethod
    def domain_str_to_labels(cls, domain_name):
        """Return a list of domain name labels, in reverse-DNS order."""
        labels = domain_name.rstrip(".").split(".")
        return labels

    @classmethod
    def dnsname_in_domain(cls, dns_name, domain_name):
        """Return True if dns_name falls under domain_name, else False.
        
        Forces to lowercase for comparison, since DNS is case-insensitive"""
        dns_name_parts = cls.domain_str_to_labels_reverse(dns_name.lower())
        domain_name_parts = cls.domain_str_to_labels_reverse(domain_name.lower())
        if len(dns_name_parts) <= len(domain_name_parts):
            # Not enough labels to be a subdomain
            return False
        for domain_label in domain_name_parts:
            # Walk down the hierarchy, matching labels
            dns_label = dns_name_parts.pop(0)
            if dns_label != domain_label:
                return False
        return True

    @classmethod
    def does_it_dane(cls, dane_identifier, cert):
        """Return None if cert is valid for identity_name, else raise ValueError."""
        # clean_cert = unquote(cert)
        der_cert = base64.b64decode(cert)
        try:
            PKI.build_x509_object(der_cert)
        except ValueError as err:
            msg = "Unable to parse {} into an x509 object ({})".format(cert, err)
            raise ValueError(msg)
        identity = Identity(dane_identifier)
        status, reason = identity.validate_certificate(der_cert)
        if status is True:
            return None
        msg = "Not valid: {}".format(reason)
        raise ValueError(msg)
        
