"""Translation of DATEX2 values used by the presentation layers."""

TRANSLATIONS = {
    "accident": "Accidente",
    "Accident": "Accidente",
    "vehicleObstruction": "Obstrucción de vehículo",
    "vehicleStuck": "Vehículo averiado",
    "vehicleBreakdown": "Avería de vehículo",
    "roadworks": "Obras",
    "roadMaintenance": "Mantenimiento",
    "weatherRelatedRoadConditions": "Condiciones meteorológicas",
    "poorRoadConditions": "Mal estado de la carretera",
    "poorEnvironment": "Condiciones ambientales adversas",
    "poorEnvironmentConditions": "Condiciones ambientales adversas",
    "fog": "Niebla",
    "snow": "Nieve",
    "rain": "Lluvia",
    "ice": "Hielo",
    "flooding": "Inundación",
    "obstruction": "Obstrucción",
    "animalPresenceObstruction": "Presencia de animales",
    "peopleOnRoadway": "Personas en la calzada",
    "abnormalTraffic": "Tráfico anómalo",
    "slowTraffic": "Tráfico lento",
    "heavyTraffic": "Tráfico denso",
    "stationaryTraffic": "Tráfico detenido",
    "trafficCongestion": "Congestión de tráfico",
    "highest": "Crítica",
    "high": "Alta",
    "medium": "Media",
    "low": "Baja",
    "northBound": "Dirección Norte",
    "southBound": "Dirección Sur",
    "eastBound": "Dirección Este",
    "westBound": "Dirección Oeste",
    "both": "Ambos sentidos",
    "unknown": "Desconocida",
}


class Translator:
    def __init__(self, translations: dict[str, str] | None = None) -> None:
        self._translations = translations or TRANSLATIONS

    def translate(self, value: str | None) -> str:
        if not value:
            return "N/A"
        return self._translations.get(value, value)