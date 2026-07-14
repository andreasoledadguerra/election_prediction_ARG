import os
import asyncio
import httpx

from src.repositories.resultados_mininterior_gob_ar.models import ResultsParams


class APIDatosGobArRepository:

    BASE_URL = "https://resultados.mininterior.gob.ar/api/resultados/getResultados"
    MAX_CONCURRENT = 2  # Número máximo de solicitudes concurrentes
    TIMEOUT = 30.0 # segundos

    def __init__(self):
        token = os.getenv("MININTERIOR_TOKEN")
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}

        async def get_results(
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

            params = ResultsParams(
                category_id=category_id,
                election_year=election_year,
                election_type=election_type,
                count_type=count_type,
                district_id=district_id,
                provincial_section_id=provincial_section_id,
                section_id=section_id,
                circuit_id=circuit_id,
                polling_station_id=polling_station_id,
            ).to_query_params() 

            async with httpx.AsyncClient(headers=self.headers, timeout=self.TIMEOUT) as client:
                response = await client.get(self.BASE_URL, params=params)
                response.raise_for_status()
                return response.json()


    # Método asíncrono para obtener resultados
    async def get_results_bulk(self, list_params: list[ResultsParams]) -> list[dict]:
        semaphore = asyncio.Semaphore(self.MAX_CONCURRENT)
        async with httpx.AsyncClient(
            headers=self.headers,
            timeout=self.TIMEOUT
            ) as client:
            tasks = [
                self._fetch_result(client, params, semaphore)
                for params in list_params
            ]
            results = await asyncio.gather(*tasks)
        return results
    

    # Método privado para realizar la solicitud asíncrona
    async def _fetch_result(
        self, client: httpx.AsyncClient, params: ResultsParams, semaphore: asyncio.Semaphore
        ) -> dict:

        query_params = params.to_query_params()
        
        async with semaphore: # Pide permiso para ejecutar la solicitud, espera si ya hay 2 corriendo
            response = await client.get(self.BASE_URL, params=query_params) # Al salir del async with, libera el permiso para que otra solicitud pueda ejecutarse
            response.raise_for_status()
            return response.json()
        