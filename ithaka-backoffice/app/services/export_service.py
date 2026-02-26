import csv
import json
from datetime import datetime
from io import StringIO
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.models.asignacion import Asignacion
from app.models.caso import Caso
from app.models.catalogo_estados import CatalogoEstados
from app.models.emprendedor import Emprendedor
from app.models.usuario import Usuario


class ExportService:
    @staticmethod
    def construir_query_casos(
        db: Session,
        current_user: Optional[Usuario] = None,
        id_estado: Optional[int] = None,
        tipo_caso: Optional[str] = None,
        nombre_estado: Optional[str] = None,
        id_emprendedor: Optional[int] = None,
        id_convocatoria: Optional[int] = None,
        id_tutor: Optional[int] = None,
        incluir_relaciones: bool = True
    ):
        """
        Construye el query base de casos reutilizable para listados y exportaciones.
        """
        query = db.query(Caso)

        if incluir_relaciones:
            query = query.options(
                joinedload(Caso.estado),
                joinedload(Caso.emprendedor),
                joinedload(Caso.convocatoria),
                joinedload(Caso.asignaciones).joinedload(Asignacion.usuario)
            )

        es_tutor = bool(
            current_user
            and current_user.rol
            and current_user.rol.nombre_rol == "Tutor"
        )
        necesita_join_asignacion = es_tutor or id_tutor is not None
        necesita_join_estado = tipo_caso is not None or nombre_estado is not None

        if necesita_join_asignacion:
            query = query.join(Asignacion)
        if necesita_join_estado:
            query = query.join(Caso.estado)

        if es_tutor:
            query = query.filter(Asignacion.id_usuario == current_user.id_usuario)
        if id_tutor is not None:
            query = query.filter(Asignacion.id_usuario == id_tutor)
        if id_estado is not None:
            query = query.filter(Caso.id_estado == id_estado)
        if id_emprendedor is not None:
            query = query.filter(Caso.id_emprendedor == id_emprendedor)
        if id_convocatoria is not None:
            query = query.filter(Caso.id_convocatoria == id_convocatoria)
        if tipo_caso is not None:
            query = query.filter(CatalogoEstados.tipo_caso == tipo_caso)
        if nombre_estado is not None:
            query = query.filter(CatalogoEstados.nombre_estado == nombre_estado)

        if necesita_join_asignacion:
            query = query.distinct()

        return query

    @staticmethod
    def exportar_casos_csv(
        db: Session,
        current_user: Optional[Usuario] = None,
        id_estado: Optional[int] = None,
        tipo_caso: Optional[str] = None,
        nombre_estado: Optional[str] = None,
        id_emprendedor: Optional[int] = None,
        id_convocatoria: Optional[int] = None,
        id_tutor: Optional[int] = None
    ) -> StringIO:
        """
        Exportar casos a CSV con filtros opcionales.
        """
        casos = ExportService.construir_query_casos(
            db=db,
            current_user=current_user,
            id_estado=id_estado,
            tipo_caso=tipo_caso,
            nombre_estado=nombre_estado,
            id_emprendedor=id_emprendedor,
            id_convocatoria=id_convocatoria,
            id_tutor=id_tutor
        ).order_by(Caso.id_caso.asc()).all()

        # Crea archivo CSV en memoria
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_ALL)

        # Encabezados
        writer.writerow([
            "ID Caso",
            "Nombre del Caso",
            "Descripción",
            "Fecha de Creación",
            "Nombre Emprendedor",
            "Apellido Emprendedor",
            "Email Emprendedor",
            "Teléfono",
            "Documento de Identidad",
            "País de Residencia",
            "Ciudad de Residencia",
            "Campus UCU",
            "Relación con UCU",
            "Facultad",
            "Canal de Llegada",
            "Motivación",
            "Convocatoria",
            "Estado del Caso",
            "Datos del Chatbot (JSON)"
        ])

        # Filas de datos
        for caso in casos:
            emprendedor = caso.emprendedor or Emprendedor()

            writer.writerow([
                caso.id_caso or "",
                caso.nombre_caso or "",
                caso.descripcion or "",
                caso.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S") if caso.fecha_creacion else "",
                emprendedor.nombre or "",
                emprendedor.apellido or "",
                emprendedor.email or "",
                emprendedor.telefono or "",
                emprendedor.documento_identidad or "",
                emprendedor.pais_residencia or "",
                emprendedor.ciudad_residencia or "",
                emprendedor.campus_ucu or "",
                emprendedor.relacion_ucu or "",
                emprendedor.facultad_ucu or "",
                emprendedor.canal_llegada or "",
                emprendedor.motivacion or "",
                caso.convocatoria.nombre if caso.convocatoria else "",
                caso.estado.nombre_estado if caso.estado else "",
                json.dumps(caso.datos_chatbot) if caso.datos_chatbot else "",
            ])

        output.seek(0)
        return output

    @staticmethod
    def exportar_casos_con_tutores_csv(
        db: Session,
        current_user: Optional[Usuario] = None,
        id_estado: Optional[int] = None,
        tipo_caso: Optional[str] = None,
        nombre_estado: Optional[str] = None,
        id_emprendedor: Optional[int] = None,
        id_convocatoria: Optional[int] = None,
        id_tutor: Optional[int] = None
    ) -> StringIO:
        """
        Exporta casos con información de tutores asignados
        """
        casos = ExportService.construir_query_casos(
            db=db,
            current_user=current_user,
            id_estado=id_estado,
            tipo_caso=tipo_caso,
            nombre_estado=nombre_estado,
            id_emprendedor=id_emprendedor,
            id_convocatoria=id_convocatoria,
            id_tutor=id_tutor
        ).order_by(Caso.id_caso.asc()).all()

        # Crea archivo CSV
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_ALL)

        # Encabezados
        writer.writerow([
            "ID Caso",
            "Nombre del Caso",
            "Email Emprendedor",
            "Tutor Asignado",
            "Email del Tutor",
            "Fecha de Asignación",
            "Estado del Caso"
        ])

        # Filas de datos
        for caso in casos:
            asignaciones = caso.asignaciones

            if id_tutor is not None:
                asignaciones = [
                    asignacion
                    for asignacion in asignaciones
                    if asignacion.id_usuario == id_tutor
                ]

            if asignaciones:
                for asignacion in asignaciones:
                    tutor = asignacion.usuario
                    writer.writerow([
                        caso.id_caso or "",
                        caso.nombre_caso or "",
                        caso.emprendedor.email if caso.emprendedor else "",
                        tutor.nombre if tutor else "",
                        tutor.email if tutor else "",
                        asignacion.fecha_asignacion.strftime("%Y-%m-%d") if asignacion.fecha_asignacion else "",
                        caso.estado.nombre_estado if caso.estado else "",
                    ])
            elif id_tutor is None:
                # Mostrar casos sin tutor asignado
                writer.writerow([
                    caso.id_caso or "",
                    caso.nombre_caso or "",
                    caso.emprendedor.email if caso.emprendedor else "",
                    "Sin asignar",
                    "",
                    "",
                    caso.estado.nombre_estado if caso.estado else "",
                ])

        output.seek(0)
        return output

    @staticmethod
    def generar_nombre_archivo(tipo_reporte: str = "postulaciones") -> str:
        """
        Generar nombre de archivo con timestamp
        
            tipo_reporte: Tipo de reporte para el nombre
        
            Nombre de archivo con timestamp
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{tipo_reporte}_{timestamp}.csv"
