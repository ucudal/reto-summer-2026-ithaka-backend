"""Utilidades de auditoria para entidades vinculadas a caso."""

from __future__ import annotations

import json
from typing import Any, Optional

from sqlalchemy.orm import Session

from app.models.auditoria import Auditoria


def _serializar_valor(valor: Any) -> Optional[str]:
    """Serializa valores a texto para almacenarlos en auditoria."""
    if valor is None:
        return None

    if isinstance(valor, str):
        return valor

    try:
        return json.dumps(valor, default=str, ensure_ascii=False)
    except (TypeError, ValueError):
        return str(valor)


def registrar_auditoria_caso(
    db: Session,
    *,
    accion: str,
    id_usuario: int,
    id_caso: int,
    valor_anterior: Any = None,
    valor_nuevo: Any = None,
) -> Auditoria:
    """
    Registra un evento de auditoria para una entidad ligada a un caso.

    Importante:
    - No hace commit.
    - Debe llamarse dentro de la misma transaccion de negocio.
    """
    registro = Auditoria(
        accion=accion,
        valor_anterior=_serializar_valor(valor_anterior),
        valor_nuevo=_serializar_valor(valor_nuevo),
        id_usuario=id_usuario,
        id_caso=id_caso,
    )
    db.add(registro)
    return registro
