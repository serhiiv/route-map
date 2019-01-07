from app import db


class Route(db.Model):

    id = db.Column(db.String(15), primary_key=True)
    invoices = db.relationship('Invoice', backref='route', lazy=True)
    date = db.Column(db.DateTime)
    car = db.Column(db.String(50))
    car_volume = db.Column(db.Float)

    def __repr__(self):
        out = list()
        out.append(f'<Route: {self.id[:10]}')
        out.append(f'Date: {self.date}')
        out.append(f'Car: {self.car}')
        out.append(f'Volume: {self.car_volume}')
        out.append('Invoices: [' + ', '.join([i.id[:10]
                                              for i in self.invoices]) + ']>')
        return ', '.join(out)


class Invoice(db.Model):

    id = db.Column(db.String(15), primary_key=True)
    order = db.Column(db.Integer)
    date = db.Column(db.DateTime)
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
        out = list()
        out.append(f'<Invoice: {self.id[:10]}')
        out.append(f'Order: {self.order}')
        if self.route_id:
            out.append(f'Route: {self.route_id[:10]}')
        else:
            out.append(f'Route: {self.route_id}')

        out.append(f'Date: {self.date}')
        out.append(f'Nickname: {self.client_nickname}')
        out.append(f'Name: {self.client_name}')
        out.append(f'Volume: {self.volume}')
        out.append(f'Lon: {self.lon}')
        out.append(f'Lat: {self.lat}')
        out.append(f'City: {self.city}')
        out.append(f'City_lon: {self.city_lon}')
        out.append(f'City_lat: {self.city_lat}>')
        return ', '.join(out)
