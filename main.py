import asyncio
from src.repositories.resultados_mininterior_gob_ar.api import APIDatosGobArRepository

async def main():
    repo = APIDatosGobArRepository()

    #ejemplo de parámetros para obtener resultados
    comb_params = [
        {
            "category_id": 1,
            "election_year": "2019",
            "election_type": "2",
            "count_type": "1",
            "district_id": str(d)}
        for d in range(1, 25)
    ]

    results = await repo.get_results_async(comb_params)
    print(f"Resultados obtenidos: {len(results)}")

if __name__ == "__main__":
    asyncio.run(main())