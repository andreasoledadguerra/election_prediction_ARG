import asyncio

from src.repositories.resultados_mininterior_gob_ar.api import (
    APIDatosGobArRepository,
    ResultsParams,
)

from src.repositories.mongo.repository import MongoRepository

async def main():
    repo = APIDatosGobArRepository()
    mongo_repo = MongoRepository()

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

    inserted = 0
    skipped = 0

    for params, response_json in zip(comb_params, results):
        was_inserted = await mongo_repo.insert_if_not_exists(
            params=params.model_dump(by_alias=True, exclude_none=True),  # Convert to dict with alias names
            response_json=response_json,
        )
        if was_inserted:
            inserted += 1
        else:
            skipped += 1


    print(f"Insertados: {inserted}, Ya existentes: {skipped}")

    #print(json.dumps(results[0], indent=2, ensure_ascii=False))
    #output_path = Path("data/results.json")
    #output_path.parent.mkdir(parents=True, exist_ok=True)
    #output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    #print(f"Resultados guardados en {output_path}")

if __name__ == "__main__":
    asyncio.run(main())