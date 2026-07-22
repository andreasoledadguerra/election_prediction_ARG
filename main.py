import asyncio
import json
from pathlib import Path

from src.repositories.resultados_mininterior_gob_ar.api import (
    APIDatosGobArRepository,
    ResultsParams,
)


async def main():
    repo = APIDatosGobArRepository()

    # ejemplo de parámetros para obtener resultados
    comb_params = [
        ResultsParams(
            category_id=1,
            election_year="2019",
            election_type="2",
            count_type="1",
            district_id=str(d),
        )
        for d in range(1, 25)
    ]

    results = await repo.get_results_bulk(comb_params)

    print(f"Resultados obtenidos: {len(results)}")
    print(json.dumps(results[0], indent=2, ensure_ascii=False))

    output_path = Path("data/results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"Resultados guardados en {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
