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
    

    # Método asíncrono para obtener resultados
    async def get_results_async(self, list_params: list[dict]) -> list[dict]:

        semaphore = asyncio.Semaphore(self.MAX_CONCURRENT)

        async with httpx.AsyncClient(
            headers=self.headers,
            timeout=30.0
            ) as client:
            tasks = [
                self._fetch_result(client, params, semaphore)
                for params in list_params
            ]
            results = await asyncio.gather(*tasks)
        
        return results
    

    # Método privado para realizar la solicitud asíncrona
    async def _fetch_result(
        self, client: httpx.AsyncClient, params: dict, semaphore: asyncio.Semaphore
        ) -> dict:

        async with semaphore: # Pide permiso para ejecutar la solicitud, espera si ya hay 2 corriendo
            response = await client.get(self.BASE_URL, params=params) # Al salir del async with, libera el permiso para que otra solicitud pueda ejecutarse
            response.raise_for_status()
            return response.json()
        

    # Método privado para construir los parámetros de la solicitud
    def _build_params(
        self,
        category_id: int,
        election_year: str = None,
        election_type: str = None,
        count_type: str = None,
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

        return {k: v for k, v in params.items() if v is not None}