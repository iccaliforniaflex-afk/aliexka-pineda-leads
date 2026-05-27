# agent/tools.py — Herramientas del agente Aliexka Pineda Leads
# Generado por AgentKit

import os
import yaml
import logging
from datetime import datetime

logger = logging.getLogger("agentkit")


def cargar_info_negocio() -> dict:
    """Carga la información del negocio desde business.yaml."""
    try:
        with open("config/business.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error("config/business.yaml no encontrado")
        return {}


def obtener_horario() -> dict:
    """Retorna el horario de atención y si el negocio está abierto ahora."""
    ahora = datetime.now()
    dia_semana = ahora.weekday()  # 0=Lunes, 6=Domingo
    hora_actual = ahora.hour + ahora.minute / 60

    # Lunes a Sábado (0-5): 10am–7pm. Domingo (6): cerrado.
    esta_abierto = (
        dia_semana <= 5 and
        10.0 <= hora_actual < 19.0
    )

    return {
        "horario": "Lunes a Sábado 10am–7pm. Domingos cerrado.",
        "esta_abierto": esta_abierto,
        "mensaje": (
            "Estamos disponibles ahora mismo. 😊"
            if esta_abierto else
            "En este momento estamos fuera de horario. Nuestro horario es Lunes a Sábado 10am–7pm."
        )
    }


def buscar_en_knowledge(consulta: str) -> str:
    """
    Busca información relevante en los archivos de /knowledge.
    Retorna el contenido más relevante encontrado.
    """
    resultados = []
    knowledge_dir = "knowledge"

    if not os.path.exists(knowledge_dir):
        return "No hay archivos de conocimiento disponibles."

    for archivo in os.listdir(knowledge_dir):
        ruta = os.path.join(knowledge_dir, archivo)
        if archivo.startswith(".") or not os.path.isfile(ruta):
            continue
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
                if consulta.lower() in contenido.lower():
                    resultados.append(f"[{archivo}]: {contenido[:800]}")
        except (UnicodeDecodeError, IOError):
            continue

    if resultados:
        return "\n---\n".join(resultados)
    return "No encontré información específica sobre eso en mis archivos."


def calificar_lead(tiene_banco: bool, tiene_id: bool, presupuesto: float = 0) -> dict:
    """
    Evalúa si un cliente potencial califica para adquirir un vehículo.

    Args:
        tiene_banco: Si el cliente tiene cuenta de banco con más de 3 meses
        tiene_id: Si el cliente tiene identificación vigente
        presupuesto: Presupuesto disponible del cliente (0 = no especificado)

    Returns:
        Diccionario con resultado y mensaje para el cliente
    """
    califica = tiene_banco and tiene_id

    if califica:
        return {
            "califica": True,
            "mensaje": (
                "¡Excelente! Tienes todo lo que necesitas para avanzar. ✅\n"
                "¿Te agendamos una cita con el dealer más cercano a ti?"
            )
        }
    else:
        faltantes = []
        if not tiene_banco:
            faltantes.append("cuenta de banco con más de 3 meses de uso")
        if not tiene_id:
            faltantes.append("identificación vigente")

        return {
            "califica": False,
            "mensaje": (
                f"Para poder ayudarte, necesitarías: {', '.join(faltantes)}. "
                "Cuando los tengas listos, con gusto te orientamos. 😊"
            )
        }


def registrar_lead(telefono: str, nombre: str, vehiculo: str, ubicacion: str, forma_pago: str) -> dict:
    """
    Registra la información de un lead calificado para enviarlo al dealer.

    Args:
        telefono: Número de teléfono del cliente
        nombre: Nombre del cliente
        vehiculo: Vehículo de interés
        ubicacion: Área del Metroplex donde está el cliente
        forma_pago: cash o financiamiento

    Returns:
        Confirmación del registro
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    logger.info(
        f"[LEAD REGISTRADO] {timestamp} | "
        f"Nombre: {nombre} | Tel: {telefono} | "
        f"Vehículo: {vehiculo} | Ubicación: {ubicacion} | Pago: {forma_pago}"
    )

    return {
        "registrado": True,
        "mensaje": (
            f"¡Perfecto, {nombre}! Ya registré tu información. 🚗\n"
            "En breve te contactaremos para coordinar los detalles con el dealer.\n"
            "¿Tienes alguna pregunta adicional?"
        )
    }


def agendar_cita(telefono: str, nombre: str, fecha_preferida: str, ubicacion: str) -> dict:
    """
    Agenda (o solicita agendar) una cita con el dealer según la ubicación del cliente.

    Args:
        telefono: Número de teléfono del cliente
        nombre: Nombre del cliente
        fecha_preferida: Fecha/hora que le viene bien al cliente
        ubicacion: Área del Metroplex donde está el cliente

    Returns:
        Confirmación de la solicitud de cita
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    logger.info(
        f"[CITA SOLICITADA] {timestamp} | "
        f"Nombre: {nombre} | Tel: {telefono} | "
        f"Fecha preferida: {fecha_preferida} | Ubicación: {ubicacion}"
    )

    return {
        "agendado": True,
        "mensaje": (
            f"¡Listo, {nombre}! Tomé nota de tu solicitud de cita para {fecha_preferida} "
            f"en el área de {ubicacion}. 📅\n"
            "Te confirmaremos los detalles del dealer y la dirección exacta en breve.\n"
            "¿Hay algo más en que pueda ayudarte?"
        )
    }
