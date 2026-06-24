# Resultados_mininiterior.gob.ar

>  Plataforma de búsqueda avanzada y generación de informes con los resultados provisionales de la elecciones de los últimos años publicado por la Dirección Nacional Electoral.

---

## Información general

| Campo | Detalle |
|---|---|
| **Organismo** | Ministerio del Interior  / Dirección Nacional Electoral|
| **Tipo** | `Dataset descargable`|
| **Formato** | CSV |
| **Actualización** | Por elección |
| **Cobertura temporal** | Desde 2023 hasta 2025|
| **Cobertura geográfica** | Provincial |
| **Licencia** | Datos abiertos |

---

## Links de interés

- [Documentación oficial](https://resultados.mininterior.gob.ar/)
- [Portal de datos / descarga](https://resultados.mininterior.gob.ar/categorias)
- [Página del organismo](https://www.argentina.gob.ar/interior)

---

## Autenticación


La documentación oficial indica que esta API requiere Bearer Token.
En la práctica, el endpoint `/resultados/getResultados` responde con `200`
sin autenticación. Se recomienda igual solicitar el token a
`soportedine@mininterior.gob.ar` para uso en producción.

### Cómo obtenerlo

1. Enviar un mail a `soportedine@mininterior.gob.ar` solicitando acceso.
2. Indicar: finalidad del proyecto, datos a consultar, volumen estimado de uso.
3. El organismo evalúa la solicitud y responde con el token.

