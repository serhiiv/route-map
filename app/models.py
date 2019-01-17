from app import db


class Route(db.Model):

    id = db.Column(db.String(15), primary_key=True)
    invoices = db.relationship('Invoice', backref='route', lazy=True)
    date = db.Column(db.String(10))
    car = db.Column(db.String(50))
    car_volume = db.Column(db.Float)
    volume = db.Column(db.Float)
    points = db.Column(db.PickleType)
    manadger_waypoint_order = db.Column(db.PickleType)
    manadger_polyline = db.Column(db.PickleType)
    manadger_popup = db.Column(db.Text)
    manadger_distance = db.Column(db.Float)
    google_waypoint_order = db.Column(db.PickleType)
    google_polyline = db.Column(db.PickleType)
    google_popup = db.Column(db.Text)
    google_distance = db.Column(db.Float)

    def invoices_by_order(self):
        out = [''] * len(self.invoices)
        for invoice in self.invoices:
            out[invoice.order - 1] = invoice
        return out

    def __repr__(self):
        return f'<Route: {self.id[:10]} from {date}>'


class Invoice(db.Model):

    id = db.Column(db.String(15), primary_key=True)
    order = db.Column(db.Integer)
    manadger = db.Column(db.String(250))
    date = db.Column(db.String(10))
    route_date = db.Column(db.String(10))
    client_nickname = db.Column(db.String(32))
    client_name = db.Column(db.String(250))
    volume = db.Column(db.Float, default=0)
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)
    city = db.Column(db.String(40))
    city_lon = db.Column(db.Float)
    city_lat = db.Column(db.Float)
    route_id = db.Column(
        db.String(15), db.ForeignKey('route.id'), nullable=True)

    def __repr__(self):
        return f'<Invoice: {self.id[:10]} from {date}>'
