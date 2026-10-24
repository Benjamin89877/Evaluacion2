import os
import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
idioma = "es"
# La clave se lee desde una variable de entorno para no publicarla en GitHub.
key = os.environ.get("GRAPHHOPPER_KEY") or input("Ingrese su API key de GraphHopper: ").strip()


def geocoding(location, key):
    while location == "":
        location = input("Ingrese la ubicación nuevamente: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "locale": idioma, "key": key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country = ""

        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state = ""

        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) != 0:
            new_loc = name + ", " + state
        elif len(country) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name

        print("URL de la API de geocodificación para " + new_loc + " (Tipo de ubicación: " + value + ")\n" + url.replace(key, "***"))
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status == 200:
            json_status = 404
    return json_status, lat, lng, new_loc


while True:
    loc1 = input("Ubicación de origen (escriba 's' o 'salir' para terminar): ")
    if loc1.lower() == "salir" or loc1.lower() == "s":
        break
    orig = geocoding(loc1, key)

    loc2 = input("Ubicación de destino (escriba 's' o 'salir' para terminar): ")
    if loc2.lower() == "salir" or loc2.lower() == "s":
        break
    dest = geocoding(loc2, key)

    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "locale": idioma}) + op + dp
        respuesta = requests.get(paths_url)
        paths_status = respuesta.status_code
        paths_data = respuesta.json()
        print("Estado de la API de rutas: " + str(paths_status) + "\nURL de la API de rutas:\n" + paths_url.replace(key, "***"))

        print("=================================================")
        print("Indicaciones desde " + orig[3] + " hasta " + dest[3])
        print("=================================================")
        if paths_status == 200:
            millas = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km = (paths_data["paths"][0]["distance"]) / 1000
            seg = int(paths_data["paths"][0]["time"] / 1000 % 60)
            minutos = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print("Distancia recorrida: {0:.2f} millas / {1:.2f} km".format(millas, km))
            print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, minutos, seg))
            print("=================================================")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.2f} km / {2:.2f} millas )".format(path, distance / 1000, distance / 1000 / 1.61))
            print("=============================================")
        else:
            print("Error al calcular la ruta. Código de estado: " + str(paths_status))
    else:
        print("No se pudo encontrar una de las ubicaciones. Intente de nuevo.")

print("Programa finalizado. ¡Hasta luego!")