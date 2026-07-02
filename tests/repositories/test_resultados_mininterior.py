from src.repositories.resultados_mininterior_gob_ar.api import APIDatosGobArRepository


def test_get_resultados():
    """Prueba que la clase instancia correctamente y el método get_resultados funciona."""

    repository = APIDatosGobArRepository()
    resultado = repository.get_resultados(
        categoria_id=1,
        anio_eleccion="2019",
        tipo_eleccion="2",
        tipo_recuento="1"
    )

    assert isinstance(resultado, dict)
    assert "valoresTotalizadosPositivos" in resultado
    assert "estadoRecuento" in resultado
    assert len(resultado["valoresTotalizadosPositivos"]) > 0
