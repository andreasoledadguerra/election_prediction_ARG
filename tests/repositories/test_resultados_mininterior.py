from src.repositories.resultados_mininterior_gob_ar.api import get_resultados


def test_get_resultados_presidente_2019():
    """Prueba que el endpoint devuelve datos reales para Presidente 2019 Generales."""
    resultado = get_resultados(
        categoria_id=1,
        anio_eleccion="2019",
        tipo_eleccion="2",
        tipo_recuento="1"
    )

    assert isinstance(resultado, dict)
    assert "valoresTotalizadosPositivos" in resultado
    assert "estadoRecuento" in resultado
    assert len(resultado["valoresTotalizadosPositivos"]) > 0
