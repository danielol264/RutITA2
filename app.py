from flask import Flask, request, url_for, render_template,redirect, flash, jsonify
import geocoder
from User import User
from ModelUser import ModelUser
from geopy.geocoders import Nominatim
import osmnx as ox
import networkx as nx
import folium
import math
from shapely.geometry import Point, Polygon

app = Flask(__name__)

app.secret_key="mysecretkey"
@app.route('/')
def Index():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        usuario=User(request.form['usuario'],request.form['contraseña'])    
        usuario_logeado=ModelUser.login(usuario)
        if usuario_logeado != None:
            if usuario_logeado.contraseña:
                return redirect(url_for('home')) 
            else:
                flash('error!!! contraseña incorrecta')
                return render_template('login.html')
        else:
            flash('error!!! usuario no enncontrado')    
            return render_template('login.html')
    else:
        return render_template('login.html')
@app.route('/home')
def home():
    
    return render_template('kevin.html')


punto_inicio = (21.876615, -102.2590349)  

distancia_red = 8000 
G = ox.graph_from_point(punto_inicio, dist=distancia_red, network_type='drive')

def obtener_ubicacion(latitud, longitud):
    geolocalizador = Nominatim(user_agent="my_geolocation_app")
    
    try:
        ubicacion = geolocalizador.reverse((latitud, longitud), exactly_one=True)
        if ubicacion:
            direccion = ubicacion.raw['address']
            calle = direccion.get('road', 'Calle no encontrada')
            ciudad = direccion.get('city', 'Ciudad no encontrada')
            estado = direccion.get('state', 'Estado no encontrado')
            pais = direccion.get('country', 'País no encontrado')
            codigo_postal = direccion.get('postcode', 'Código postal no encontrado')
            return f"Calle: {calle}, Ciudad: {ciudad}, Estado: {estado}, País: {pais}, Código Postal: {codigo_postal}"
        else:
            return "Ubicación no encontrada."
    except Exception as e:
        return f"Error al obtener la ubicación: {str(e)}"

def calcular_poligono_circulo(centro, radio, num_puntos=30):
    puntos = []
    for i in range(num_puntos):
        angulo = 2 * math.pi * i / num_puntos
        dx = radio * math.cos(angulo)
        dy = radio * math.sin(angulo)
        punto = (centro[0] + (dy / 111320), centro[1] + (dx / (111320 * math.cos(math.radians(centro[0])))))
        puntos.append(punto)
    return puntos

def calcular_ruta_extendida(G, nodo_A, nodo_B, punto_inicio, distancia_colonias=2000):
   
    G_colonias = ox.graph_from_point(punto_inicio, dist=distancia_colonias, network_type='drive')
   
    nodos_intermedios = list(G_colonias.nodes)
    nodo_intermedio = nodos_intermedios[len(nodos_intermedios) // 2] 

    ruta_1 = nx.shortest_path(G, nodo_A, nodo_intermedio, weight='length')
    ruta_2 = nx.shortest_path(G, nodo_intermedio, nodo_B, weight='length')

    ruta_extendida = ruta_1 + ruta_2[1:]  
    return ruta_extendida

def generar_mapa(latitud, longitud):
    mapa = folium.Map(location=[latitud, longitud], zoom_start=15)

    folium.Marker(
        [latitud, longitud],
        popup="Ayuda",
        icon=folium.Icon(color='red', icon='info-sign') 
    ).add_to(mapa)

    folium.Marker(
        punto_inicio,
        popup="C4 Aguascalientes",
        icon=folium.Icon(color='blue', icon='info-sign') 
    ).add_to(mapa)

    poligono_area = calcular_poligono_circulo(punto_inicio, 1000) 
    folium.Polygon(
        locations=poligono_area,
        color='red',
        fill=True,
        fill_opacity=0.3
    ).add_to(mapa)

    poligono_shapely = Polygon(poligono_area)

    for u, v, data in G.edges(data=True):
  
        x_u, y_u = G.nodes[u]['x'], G.nodes[u]['y']
        x_v, y_v = G.nodes[v]['x'], G.nodes[v]['y']

        punto_u = Point(y_u, x_u)
        punto_v = Point(y_v, x_v)

        if poligono_shapely.contains(punto_u) and poligono_shapely.contains(punto_v):

            folium.PolyLine([(y_u, x_u), (y_v, x_v)], color="red", weight=2.5, opacity=0.8).add_to(mapa)


    try:
        nodo_A = ox.distance.nearest_nodes(G, longitud, latitud) 
        nodo_B = ox.distance.nearest_nodes(G, punto_inicio[1], punto_inicio[0])

        ruta_extendida = calcular_ruta_extendida(G, nodo_A, nodo_B, punto_inicio)

        ruta_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in ruta_extendida]

        folium.PolyLine(ruta_coords, color="red", weight=5, opacity=0.8).add_to(mapa)
    except Exception as e:
        print(f"Error calculando la ruta: {str(e)}")

    return mapa._repr_html_()

@app.route('/')
def index():
    return render_template('kevin.html')

@app.route('/obtener_coordenadas', methods=['GET'])
def obtener_coordenadas():
    g = geocoder.ip('me')
    if g.latlng is not None:
        lat = g.latlng[0]
        lon = g.latlng[1]
        direccion = obtener_ubicacion(lat, lon)
        mapa_html = generar_mapa(lat, lon)
        return jsonify({'latitud': lat, 'longitud': lon, 'direccion': direccion, 'mapa': mapa_html})
    else:
        return jsonify({'latitud': None, 'longitud': None}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)