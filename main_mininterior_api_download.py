import requests

BASE_URL = "https://resultados.mininterior.gob.ar/api/resultados/getResultados"

params = {
    "categoriaId": 1,
    "anioEleccion": "2023",
    "tipoEleccion": "2",
    "tipoRecuento": "1",
}

response = requests.get(BASE_URL, params=params)

print(f"Status code: {response.status_code}")
print(f"Respuesta: response.text")