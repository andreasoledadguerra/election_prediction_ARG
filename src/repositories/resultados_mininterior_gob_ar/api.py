import os
import requests


class APIDatosGobArRepository:

    BASE_URL = "https://resultados.mininterior.gob.ar/api/resultados/getResultados"

    def __init__(self):
        token = os.getenv("MININTERIOR_TOKEN")
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}

    def get_results(
        self,
        category_id: int,               # 1=Presidente, 2=Diputado Nacional, 3=Intendente
        election_year: str = None,
        election_type: str = None,      # "1"=PASO, "2"=Generales, "3"=Segunda Vuelta
        count_type: str = None,      # "1" (único valor documentado)
        district_id: str = None,
        provincial_section_id: str = None,
        section_id: str = None,
        circuit_id: str = None,
        polling_station_id: str = None,
    ) -> dict:

        params = {
            "categoriaId": category_id,
            "anioEleccion": election_year,
            "tipoEleccion": election_type,
            "tipoRecuento": count_type,
            "distritoId": district_id,
            "seccionProvincialId": provincial_section_id,
            "seccionId": section_id,
            "circuitoId": circuit_id,
            "mesaId": polling_station_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = requests.get(self.BASE_URL, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()