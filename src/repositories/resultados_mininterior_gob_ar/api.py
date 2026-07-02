import os
import requests


class APIDatosGobArRepository:

    BASE_URL = "https://resultados.mininterior.gob.ar/api/resultados/getResultados"

    def __init__(self):
        token = os.getenv("MININTERIOR_TOKEN")
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}

    def get_resultados(
        self,
        categoria_id: int,               # 1=Presidente, 2=Diputado Nacional, 3=Intendente
        anio_eleccion: str = None,
        tipo_eleccion: str = None,      # "1"=PASO, "2"=Generales, "3"=Segunda Vuelta
        tipo_recuento: str = None,      # "1" (único valor documentado)
        distrito_id: str = None,
        seccion_provincial_id: str = None,
        seccion_id: str = None,
        circuito_id: str = None,
        mesa_id: str = None,
    ) -> dict:

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
        params = {k: v for k, v in params.items() if v is not None}

        response = requests.get(self.BASE_URL, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()