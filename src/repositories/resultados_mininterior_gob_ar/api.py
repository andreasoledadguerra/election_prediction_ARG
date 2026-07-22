import os
import asyncio
import httpx
from pydantic import BaseModel, ConfigDict, Field

class ResultsParams(BaseModel):
    category_id: int = Field(..., alias="categoriaId")
    election_year: Optional[str] = Field(None, alias="anioEleccion")    
    election_type: Optional[str] = Field(None, alias="tipoEleccion")
    count_type: Optional[str] = Field(None, alias="tipoRecuento")
    district_id: Optional[str] = Field(None, alias="distritoId")
    provincial_section_id: Optional[str] = Field(None, alias="seccionProvincialId") 
    section_id: Optional[str] = Field(None, alias="seccionId")
    circuit_id: Optional[str] = Field(None, alias="circuitoId")
    polling_station_id: Optional[str] = Field(None, alias="mesaId")

    model_config = ConfigDict(populate_by_name=True)


class APIDatosGobArRepository:

    BASE_URL = "https://resultados.mininterior.gob.ar/api/resultados/getResultados"
    MAX_CONCURRENT = 2  # Número máximo de solicitudes concurrentes
    TIMEOUT = 30.0 # segundos

    def __init__(self):
        token = os.getenv("MININTERIOR_TOKEN")
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}

    async def get_results(self, params: ResultsParams) -> dict:
        async with httpx.AsyncClient(
            headers=self.headers,
            timeout=self.TIMEOUT
            ) as client:
                return await self._fetch_result(client, params)
        
    async def get_results_bulk(self, list_params: list[ResultsParams]) -> list[dict]:
        semaphore = asyncio.Semaphore(self.MAX_CONCURRENT)

        async def fetch_with_limit(params:ResultsParams) -> dict:
            async with semaphore:
                return await self._fetch_result(client, params) 

        async with httpx.AsyncClient(
            headers=self.headers,
            timeout=self.TIMEOUT
            ) as client:
            tasks = [fetch_with_limit(params) for params in list_params]        
            results = await asyncio.gather(*tasks)
        return results
    
    async def _fetch_result(
        self, client: httpx.AsyncClient, params: ResultsParams
        ) -> dict:
        response = await client.get(
            self.BASE_URL, params=params.model_dump(by_alias=True, exclude_none=True)
        )
        response.raise_for_status()
        return response.json()
        