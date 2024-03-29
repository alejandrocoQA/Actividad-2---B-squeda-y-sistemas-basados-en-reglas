import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt

# Cargar datos GeoJSON
gdf = gpd.read_file('C:\\Users\\Usuario\\Desktop\\proyecto\\Estaciones_Troncales_de_TRANSMILENIO.geojson') # Asegúrate de usar la ruta correcta

# Crear el grafo
G = nx.Graph()

# Añadir nodos (estaciones) al grafo basado en los datos GeoJSON
for index, row in gdf.iterrows():
    G.add_node(row['nombre_estacion'], pos=(row['coordenada_x_estacion'], row['coordenada_y_estacion']))

# Suposición inicial de conexiones secuenciales dentro de las troncales
troncales = gdf.groupby('troncal_estacion')
for troncal, frame in troncales:
    estaciones_ordenadas = frame.sort_values('objectid')
    for i in range(len(estaciones_ordenadas) - 1):
        estacion_actual = estaciones_ordenadas.iloc[i]
        estacion_siguiente = estaciones_ordenadas.iloc[i + 1]
        G.add_edge(estacion_actual['nombre_estacion'], estacion_siguiente['nombre_estacion'])

# Añadir manualmente conexiones específicas entre estaciones, si se conocen
# G.add_edge('NombreEstacion1', 'NombreEstacion2')

# Función para encontrar la ruta más corta usando Dijkstra
def encontrar_ruta_mas_corta(origen, destino):
    try:
        ruta = nx.shortest_path(G, source=origen, target=destino)
        return ruta
    except nx.NetworkXNoPath:
        return "No hay ruta disponible entre las estaciones seleccionadas."

# Usar la función para encontrar una ruta
origen = 'Alcalá'  # Sustituir con el nombre exacto de la estación de origen
destino = 'Portal Norte'  # Sustituir con el nombre exacto de la estación de destino
ruta = encontrar_ruta_mas_corta(origen, destino)
print("Ruta más corta encontrada:", ruta)

# Opcional: Visualización básica del grafo
# Esto puede ayudar a visualizar cómo están conectadas las estaciones en tu grafo
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, pos, with_labels=True, node_size=50, font_size=8)
plt.show()