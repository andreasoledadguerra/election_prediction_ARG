
from pydantic import BaseModel, Field
from typing import Optional

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

    def to_query_params(self) -> dict:
        return {k: v for k, v in 
                self.model_dump(by_alias=True).items() 
                if v is not None
        }