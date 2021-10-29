"""App models go here."""
import datetime

from . import db


class Entry(db.Model):
    """Entry abstraction."""

    __tablename__ = "entry"
    id = db.Column(db.Integer, primary_key=True)
    tstamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    source = db.Column(db.String(128))
    body = db.Column(db.String(2048))

    def __repr__(self):
        """Pretty printer."""
        return "<Source {} posted \"{}\">".format(self.source, self.body)
