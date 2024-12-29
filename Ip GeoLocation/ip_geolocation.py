import ipinfo
from dotenv import load_dotenv
import os
import sys
import folium
import argparse




def draw_map(latitude, longitude, location, filename="map.html"):
    """Esto dibuja un mapa basandose en lso detalles de una ip"""
    my_map = folium.Map(location=[latitude, longitude], zoom_start=9)
    folium.Marker([latitude, longitude], popup=location).add_to(my_map)
    my_map.save(filename)
    return os.path.abspath(filename)
def get_ip_details(ip_addr,access_token):
    """Obtiene detalles de Geolocalizacion de una IP utilizando ip info"""
    try:
        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails(ip_addr)
        return details.all
    except Exception as e:
        print(f"Error al obtener los detalles de la ip: {ip_addr}")
        sys.exit(1)
        

if __name__ == "__main__":
    #Configuracion
    load_dotenv()

    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    
    parser = argparse.ArgumentParser(description="Herramienta para geolocalizar IP")
    parser.add_argument("-i","--ip", type=str, required=True, help="Introduzca la ip target, ejemplo: -i 'xxx.xxx.xx.xxx'")
    
    args = parser.parse_args()
    
    details = get_ip_details(ip_addr=args.ip, access_token=ACCESS_TOKEN)

    
    #Mostramos los detalles de la Ip
    
    for key, value in details.items():
        print(f"{key}:{value}")
        
    #Obtenemos los valores de latitud, longitud y geolocalitation
    
    latitude = details["latitude"]
    longitude = details["longitude"]
    location = details.get("region", "Ubicacion desconocida")
    
    #Dibujamos el mapa
    
    map_file_path = draw_map(latitude, longitude,location)
    print(f"Mapa guardado en : {map_file_path}")
