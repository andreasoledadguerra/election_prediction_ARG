import os
import requests

BASE_URL = "https://resultados.mininterior.gob.ar/api/resultados/getResultados"


def get_resultados(
    categoria_id: int,              # 1=Presidente, 2=Diputado Nacional, 3=Intendente
    anio_eleccion: str = None,
    tipo_eleccion: str = None,      # "1"=PASO, "2"=Generales, "3"=Segunda Vuelta
    tipo_recuento: str = None,      #"1" (único)
    distrito_id: str = None,        # datos geográficos: si no se especifican la API devuelve resultadps nacionales agregados
    seccion_provincial_id: str = None,
    seccion_id: str = None,
    circuito_id: str = None,
    mesa_id: str = None,
) -> dict:

    # token opcional: la API responde 200 sin auth, pero podríarequerirlo en el futuro
    token = os.getenv("MININTERIOR_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    params = {
        "categoriaId": categoria_id,
        "anioEleccion": anio_eleccion,
        "tipoEleccion": tipo_eleccion,
        "tipoRecuento": tipo_recuento,
        "distritoId": distrito_id,
        "seccionProvincialId": seccion_provincial_id,
        "seccionId": seccion_id,
        "circuitoId": circuito_id,
        "mesaId": mesa_id,
    }
    # saca los None para no mandar parámetros vacíos
    params = {k: v for k, v in params.items() if v is not None}

    response = requests.get(BASE_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json() # dict con la respuesta JSON de la API