import asyncio
import json
from itertools import product
from pathlib import Path

from src.repositories.resultados_mininterior_gob_ar.api import (
    APIDatosGobArRepository,
    ResultsParams,
)

from src.repositories.mongo.repository import MongoRepository

ELECTION_YEARS = ["2011", "2013", "2015", "2017", "2019", "2021", "2023"]
ELECTION_TYPES = ["1", "2", "3"] # PASO, Generales, Segunda vuelta
CATEGORY_IDS = 1 # Presidente
DISTRICT_IDS = [str(d) for d in range(1, 25)] # filtrar distritos válidos
COUNT_TYPES = "1" # único valor documentado

async def main():
    repo = APIDatosGobArRepository()
    mongo_repo = MongoRepository()

    comb_params = [
        ResultsParams(
            category_id=category_id,
            election_year=year,
            election_type=election_type,
            count_type=COUNT_TYPES,
            district_id=district,
        )
        for category_id, year, election_type, district in product(
            [CATEGORY_IDS], ELECTION_YEARS, ELECTION_TYPES, DISTRICT_IDS
        )
    ]

    print(f"Total combinaciones a consultar: {len(comb_params)}")

    inserted = 0
    skipped = 0 
    errors = 0

    # Procesamos de a 50
    BATCH_SIZE = 50

    for i in range(0, len(comb_params), BATCH_SIZE):
        batch = comb_params[i:i + BATCH_SIZE]
        print(f"Procesando batch {i // BATCH_SIZE + 1} de {len(comb_params) // BATCH_SIZE + 1}...")
        results = await repo.get_results_bulk(batch)

        for params, response_json in zip(batch, results):
            if response_json is None:
                errors += 1
                print(f"Error en la consulta para {params.model_dump(by_alias=True, exclude_none=True)}")
                continue

            was_inserted = await mongo_repo.insert_if_not_exists(
                params=params.model_dump(by_alias=True, exclude_none=True),  # Convert to dict with alias names
                response_json=response_json,
            )
            if was_inserted:
                inserted += 1
            else:
                skipped += 1
        print(f"Progreso: {min(i + BATCH_SIZE, len(comb_params))}/{len(comb_params)} | Insertados: {inserted} | Errores: {errors}")

    print(f"\nFinal — Insertados: {inserted} | Ya existían: {skipped} | Errores: {errors}")

    results = await repo.get_results_bulk(comb_params)


    for params, response_json in zip(comb_params, results):
        if response_json is None:
            errors += 1
            print(f"Error en la consulta para {params.model_dump(by_alias=True, exclude_none=True)}")
            continue

        was_inserted = await mongo_repo.insert_if_not_exists(
            params=params.model_dump(by_alias=True, exclude_none=True),  # Convert to dict with alias names
            response_json=response_json,
        )
        if was_inserted:
            inserted += 1
        else:
            skipped += 1


    print(f"Insertados: {inserted}, Ya existentes: {skipped}, Errores: {errors}")

if __name__ == "__main__":
    asyncio.run(main())