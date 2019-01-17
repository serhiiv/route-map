import folium
import pickle
from folium.plugins import MarkerCluster
from flask import render_template

from app import db
from app.models import Route, Invoice
from datetime import datetime


def popup_invoice(invoice):
    if invoice.order == 0:
        return render_template('popup_invoice.html', invoice=invoice)

    route = Route.query.get(invoice.route_id)
    google_waypoint_order = pickle.loads(route.google_waypoint_order)
    points = pickle.loads(route.points)

    length = len(set(points))
    m_order = points.get((invoice.lat, invoice.lon), 1)

    diff, g_order = False, 0
    if route.manadger_distance - route.google_distance > 10:
        diff = round(route.google_distance - route.manadger_distance, 1)
        g_order = google_waypoint_order.index(m_order - 1) + 1

    return render_template('popup_invoice.html', invoice=invoice, route=route,
                           length=length, g_order=g_order, m_order=m_order,
                           diff=diff)


# def get_icon(invoice, colors):
def get_icon(invoice):
    #     вибір іконки залежно від об'єму завантаження
    bats = ('battery-empty', 'battery-quarter', 'battery-half',
            'battery-three-quarters', 'battery-full')
    icon = bats[min(int(invoice.volume), 4) % 5]
    if invoice.order != 0:
        color = 'lightgray'
        # icon_color = colors.get(invoice.manadger, 'pink')
    else:
        color = 'red'
        # color = colors.get(invoice.manadger, 'pink')
    icon_color = 'white'

    return folium.Icon(icon=icon, prefix='fa', color=color, icon_color=icon_color)


# def get_colors(day):
    # NOT_COLORS = ['lightgray', 'black', 'white', 'gray']
    # COLOR_NEW = 'lightgray'
#     COLORS = ['red', 'blue', 'green', 'purple',
#               'darkred', 'darkblue', 'darkgreen', 'darkpurple',
#               'lightred', 'lightblue', 'lightgreen',
#               'cadetblue', 'orange', 'beige']

#     manadgers = set()
#     for invoice in Invoice.query.filter_by(route_date=day):
#         manadgers.add(invoice.manadger)

#     for invoice in Invoice.query.filter_by(order=0):
#         manadgers.add(invoice.manadger)

#     lencol = len(COLORS)
#     colors = dict()
#     for i, manadger in enumerate(sorted(manadgers)):
#         colors[manadger] = COLORS[i % lencol]

#     return colors


def get_map(day):

    # colors = get_colors(day)

    # init map
    # start poin TODO: remove from sourse
    HOME = (49.443813, 26.936749)
    m = folium.Map(location=HOME, zoom_start=7, tiles=None)

    folium.raster_layers.TileLayer('Cartodb Positron', name='Сіра').add_to(m)
    folium.raster_layers.TileLayer('OpenStreetMap', name='Кольорова').add_to(m)

    # add HOME marker TODO: remove from sourse
    COLOR_HOME = 'black'
    folium.Marker(
        location=HOME,
        icon=folium.Icon(icon='home', prefix='fa', color=COLOR_HOME)
    ).add_to(m)

    # add markers for clients
    marker_layer = MarkerCluster(name='markers',
                                 options={'maxClusterRadius': 2}).add_to(m)

    for invoice in Invoice.query.filter_by(order=0, date=day):
        folium.Marker(
            location=[invoice.lat, invoice.lon],
            popup=popup_invoice(invoice),
            icon=get_icon(invoice)
            # icon=get_icon(invoice, colors)
        ).add_to(marker_layer)

    for route in Route.query.filter_by(date=day):
        route_layer = folium.FeatureGroup(
            name=route.id[:10] + ' - ' + route.car).add_to(m)

        marker_layer = MarkerCluster(
            options={'maxClusterRadius': 2}).add_to(route_layer)

        for invoice in route.invoices:
            folium.Marker(
                location=[invoice.lat, invoice.lon],
                popup=popup_invoice(invoice),
                # icon=get_icon(invoice, colors)
                icon=get_icon(invoice)
            ).add_to(marker_layer)

        # add pathes from google
        if route.manadger_distance - route.google_distance > 10:
            path = pickle.loads(route.google_polyline)
            folium.PolyLine(path, weight=5, color='pink').add_to(route_layer)

        # add pathes from manadgers
        path = pickle.loads(route.manadger_polyline)
        folium.PolyLine(path, weight=1, color='black').add_to(route_layer)

    folium.LayerControl().add_to(m)

    return m._repr_html_()
