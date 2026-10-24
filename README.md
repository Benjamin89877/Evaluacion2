# Evaluacion2 - Planificador de rutas con GraphHopper

Script en Python que consulta la API de GraphHopper (geocodificación y rutas)
y muestra distancia, duración y la narrativa del viaje en español.

## Cómo ejecutarlo
1. Tener Python 3 y la librería requests: `pip3 install requests`
2. Obtener una API key en https://www.graphhopper.com
3. Definir la clave: `export GRAPHHOPPER_KEY="su_clave"`
4. Ejecutar: `python3 graphhopper_es.py`
5. Ingresar medio de transporte, origen y destino. Para salir, escribir `s` o `salir`.