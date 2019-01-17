import googlemaps
import pickle

from app import db, app
from app.models import Route, Invoice
from datetime import datetime


def decode_polyline(polyline_str):
    '''Pass a Google Maps encoded polyline string; returns list of lat/lon pairs'''
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}

    # Coordinates have variable length when encoded, so just keep
    # track of whether we've hit the end of the string. In each
    # while loop iteration, a single coordinate is decoded.
    while index < len(polyline_str):
        # Gather lat/lon changes, store them in a dictionary to apply them later
        for unit in ['latitude', 'longitude']:
            shift, result = 0, 0

            while True:
                byte = ord(polyline_str[index]) - 63
                index += 1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break

            if (result & 1):
                changes[unit] = ~(result >> 1)
            else:
                changes[unit] = (result >> 1)

        lat += changes['latitude']
        lng += changes['longitude']

        coordinates.append((lat / 100000.0, lng / 100000.0))

    return coordinates


def invoice_processing(data):
    id = data.get('id', False)
    invoice = Invoice.query.get(id)

    method = data.get('method', False)
    if method == 'update':
        if not invoice:
            invoice = Invoice(id=id)
            invoice.order = 0
            invoice.route_id = None
            invoice.route_date = None

        invoice.date = data.get('date')
        invoice.manadger = data.get('manadger')
        invoice.client_nickname = data.get('client_nickname')
        invoice.client_name = data.get('client_name')
        invoice.volume = data.get('volume')
        invoice.lon = data.get('lon')
        invoice.lat = data.get('lat')
        invoice.city = data.get('city')
        invoice.city_lon = data.get('city_lon')
        invoice.city_lat = data.get('city_lat')
        db.session.add(invoice)
        # print('update', invoice)

    elif method == 'route':
        if not invoice:
            invoice = Invoice(id=id)

        invoice.order = data.get('order', 0)
        invoice.route_id = data.get('route_id', None)
        invoice.route_date = data.get('route_date', None)
        db.session.add(invoice)

    elif method == 'delete' and invoice:
        # print('delete', invoice)
        db.session.delete(invoice)

    db.session.commit()


def route_processing(data):
    # get route
    id = data.get('id', False)
    route = Route.query.get(id)

    method = data.get('method', False)
    if method == 'update':
        if not route:
            # make new if absent
            route = Route(id=id)

        route.date = data.get('date')
        route.car = data.get('car')
        route.car_volume = data.get('car_volume')
        db.session.add(route)

        volume = 0
        invoices = data.get('invoices', list())
        for invoice in invoices:
            invoice['method'] = 'route'
            invoice['route_id'] = id
            invoice['route_date'] = route.date
            invoice_processing(invoice)

        # calculate additional data for route
        route = Route.query.get(id)

        volume = 0
        route_points = dict()
        number = 1
        points = [(49.443813, 26.936749)]
        for invoice in route.invoices_by_order():

            volume += invoice.volume

            point = (invoice.lat, invoice.lon)
            if points[-1] != point:
                points.append(point)
                route_points[point] = number
                number += 1
                if len(points) == 25:
                    points.append(point)

        route.volume = round(volume, 2)
        points.append((49.443813, 26.936749))

        route.points = pickle.dumps(route_points)

        gm = googlemaps.Client(key=app.config['GOOGLE_KEY'])

        # path by manadger
        distance = 0
        duration = 0
        polyline = list()
        waypoint_order = list()

        for i in range((24 + len(points)) // 25):
            step = points[(i * 25):(i * 25 + 25)]
            # print(step)

            path = gm.directions(step[0], step[-1], waypoints=step[1:-1],
                                 optimize_waypoints=False, mode="driving",
                                 language='uk')[0]

            waypoint_order += path['waypoint_order']
            polyline += decode_polyline(path['overview_polyline']['points'])

            for i in range(len(path['legs'])):
                distance += path['legs'][i]['distance']['value']
                duration += path['legs'][i]['duration']['value']
                # print('distance=', path['legs'][i]['distance']['value'],
                # 'duration=', path['legs'][i]['duration']['value'])

        route.manadger_waypoint_order = pickle.dumps(waypoint_order)
        route.manadger_polyline = pickle.dumps(polyline)
        route.manadger_popup = 'popup'
        route.manadger_distance = distance / 1000.

        if len(points) > 25:
            route.google_waypoint_order = route.manadger_waypoint_order
            route.google_polyline = route.manadger_polyline
            route.google_popup = 'popup'
            route.google_distance = route.manadger_distance

        else:
            # path by GOOGLE
            path = gm.directions(points[0], points[-1], waypoints=points[1:-1],
                                 optimize_waypoints=True, mode="driving",
                                 language='uk')[0]

            route.google_waypoint_order = pickle.dumps(path['waypoint_order'])
            route.google_polyline = pickle.dumps(
                decode_polyline(path['overview_polyline']['points']))

            distance, duration = 0, 0
            for i in range(len(path['legs'])):
                distance += path['legs'][i]['distance']['value']
                duration += path['legs'][i]['duration']['value']

            route.google_popup = 'popup'
            route.google_distance = distance / 1000.

        # print('update', route)

        db.session.add(route)

    elif method == 'delete' and route:
        for invoice in route.invoices:
            invoice.order = 0
            invoice.route_id = None
            invoice.route_date = None
            db.session.add(invoice)

        # print('delete', route)

        db.session.delete(route)

    db.session.commit()
