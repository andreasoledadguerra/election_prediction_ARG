import os
import asyncio
import httpx
import requests


class APIDatosGobArRepository:

    BASE_URL = "https://resultados.mininterior.gob.ar/api/resultados/getResultados"
    MAX_CONCURRENT = 2  # Número máximo de solicitudes concurrentes

    def __init__(self):
        token = os.getenv("MININTERIOR_TOKEN")
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}

    # Método síncrono para obtener resultados
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

        params = self._build_params(
            category_id,
            election_year,
            election_type,
            count_type,
            district_id,
            provincial_section_id,
            section_id,
            circuit_id,
            polling_station_id,
        )

        response = requests.get(self.BASE_URL, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()