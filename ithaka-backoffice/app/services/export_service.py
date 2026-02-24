import csv
from io import StringIO, BytesIO
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.caso import Caso
from app.models.emprendedor import Emprendedor


class ExportService:
    @staticmethod
    def exportar_casos_csv(
        db: Session,
        filtro_estado: Optional[int] = None,
        filtro_convocatoria: Optional[int] = None
    ) -> StringIO:
        """
            Exportar casos a CSV con filtros opcionales
        
            db: Sesión de base de datos
            filtro_estado: ID del estado para filtrar (opcional)
            filtro_convocatoria: ID de la convocatoria para filtrar (opcional)
        
        """
        query = db.query(Caso)
        
        # Aplica filtros
        if filtro_estado:
            query = query.filter(Caso.id_estado == filtro_estado)
        if filtro_convocatoria:
            query = query.filter(Caso.id_convocatoria == filtro_convocatoria)
        
        casos = query.all()
        
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
                str(caso.datos_chatbot) if caso.datos_chatbot else "",
            ])
        
        output.seek(0)
        return output
    
    @staticmethod
    def exportar_casos_con_tutores_csv(db: Session) -> StringIO:
        """
        Exporta casos con información de tutores asignados
                
        """
        from app.models.asignacion import Asignacion
        
        # Casos con sus asignaciones
        query = db.query(Caso).all()
        
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
        for caso in query:
            asignaciones = db.query(Asignacion).filter(
                Asignacion.id_caso == caso.id_caso
            ).all()
            
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
            else:
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