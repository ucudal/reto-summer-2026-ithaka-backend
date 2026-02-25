"""
Tests para exportación de casos en CSV.
"""
import csv
from io import StringIO

from app.models.asignacion import Asignacion
from app.models.caso import Caso
from app.models.catalogo_estados import CatalogoEstados
from app.models.convocatoria import Convocatoria


def _leer_csv_response(response):
    contenido = response.content.decode("utf-8")
    return list(csv.reader(StringIO(contenido)))


def test_exportar_casos_csv_basico(client, headers_admin, caso_test):
    response = client.get("/api/v1/casos/export", headers=headers_admin)

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "attachment;" in response.headers.get("content-disposition", "")

    filas = _leer_csv_response(response)
    assert len(filas) >= 2

    encabezado = filas[0]
    idx_id_caso = encabezado.index("ID Caso")
    ids = {fila[idx_id_caso] for fila in filas[1:]}
    assert str(caso_test.id_caso) in ids


def test_exportar_casos_filtra_por_estado(
    client,
    db,
    headers_admin,
    emprendedor_test,
    caso_test
):
    estado_postulado = db.query(CatalogoEstados).filter(
        CatalogoEstados.nombre_estado == "Postulado"
    ).first()
    convocatoria = db.query(Convocatoria).first()

    estado_proyecto = CatalogoEstados(
        nombre_estado="En Desarrollo",
        tipo_caso="Proyecto"
    )
    db.add(estado_proyecto)
    db.commit()
    db.refresh(estado_proyecto)

    caso_proyecto = Caso(
        nombre_caso="Caso proyecto",
        descripcion="Caso para validar filtro por estado",
        id_emprendedor=emprendedor_test.id_emprendedor,
        id_estado=estado_proyecto.id_estado,
        id_convocatoria=convocatoria.id_convocatoria
    )
    db.add(caso_proyecto)
    db.commit()

    response = client.get(
        "/api/v1/casos/export",
        params={"id_estado": estado_postulado.id_estado},
        headers=headers_admin
    )

    assert response.status_code == 200

    filas = _leer_csv_response(response)
    assert len(filas) >= 2

    encabezado = filas[0]
    idx_estado = encabezado.index("Estado del Caso")
    idx_id_caso = encabezado.index("ID Caso")
    ids_exportados = {fila[idx_id_caso] for fila in filas[1:]}

    assert str(caso_test.id_caso) in ids_exportados
    assert str(caso_proyecto.id_caso) not in ids_exportados
    for fila in filas[1:]:
        assert fila[idx_estado] == "Postulado"


def test_exportar_casos_con_tutores_filtra_por_tutor(
    client,
    db,
    headers_admin,
    caso_test,
    usuario_tutor
):
    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()

    response = client.get(
        "/api/v1/casos/export",
        params={
            "con_tutores": True,
            "id_tutor": usuario_tutor.id_usuario
        },
        headers=headers_admin
    )

    assert response.status_code == 200

    filas = _leer_csv_response(response)
    assert len(filas) >= 2

    encabezado = filas[0]
    idx_email_tutor = encabezado.index("Email del Tutor")
    for fila in filas[1:]:
        assert fila[idx_email_tutor] == usuario_tutor.email


def test_tutor_exporta_solo_casos_asignados(
    client,
    db,
    headers_tutor,
    emprendedor_test,
    caso_test,
    usuario_tutor
):
    convocatoria = db.query(Convocatoria).first()
    estado = db.query(CatalogoEstados).first()

    caso_no_asignado = Caso(
        nombre_caso="Caso no asignado",
        descripcion="No debería aparecer para el tutor",
        id_emprendedor=emprendedor_test.id_emprendedor,
        id_estado=estado.id_estado,
        id_convocatoria=convocatoria.id_convocatoria
    )
    db.add(caso_no_asignado)

    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()
    db.refresh(caso_no_asignado)

    response = client.get("/api/v1/casos/export", headers=headers_tutor)

    assert response.status_code == 200

    filas = _leer_csv_response(response)
    encabezado = filas[0]
    idx_id_caso = encabezado.index("ID Caso")
    ids_exportados = {fila[idx_id_caso] for fila in filas[1:]}

    assert str(caso_test.id_caso) in ids_exportados
    assert str(caso_no_asignado.id_caso) not in ids_exportados
