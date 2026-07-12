import asyncio
import json
from src.repositories.resultados_mininterior_gob_ar.api import APIDatosGobArRepository

async def main():
    repo = APIDatosGobArRepository()

    #ejemplo de parámetros para obtener resultados
    comb_params = [
        {
            "categoriaId": 1,
            "anioEleccion": "2019",
            "tipoEleccion": "2",
            "tipoRecuento": "1",
            "distritoId": str(d)}
        for d in range(1, 25)
    ]

    results = await repo.get_results_bulk(comb_params)
    print(f"Resultados obtenidos: {len(results)}")

    # Imprimir el primer resultado de manera legible (se puede borrar)
    print(json.dumps(results[0], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())