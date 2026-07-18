"""Parser for DGT SituationPublication documents."""

import xml.etree.ElementTree as ET

from dgt_monitor.core.exceptions import DgtParseError
from dgt_monitor.core.localization import Translator
from dgt_monitor.core.models import Incident
from dgt_monitor.core.text import TextCleaner
from dgt_monitor.infrastructure.parsers.base import Datex2Parser


class IncidentParser(Datex2Parser):
    def __init__(self, translator: Translator | None = None, cleaner: TextCleaner | None = None) -> None:
        self._translator = translator or Translator()
        self._cleaner = cleaner or TextCleaner()

    def parse(self, xml_content: str) -> list[Incident]:
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as exc:
            raise DgtParseError(f"XML de incidentes no válido: {exc}") from exc
        return [incident for node in root.iter() if node.tag.endswith("situation") if (incident := self._parse_one(node))]

    def _parse_one(self, situation: ET.Element) -> Incident | None:
        record = self.element(situation, "situationRecord")
        if record is None:
            return None
        get = lambda tag: self.text(record, tag)
        raw_type = record.get("{http://www.w3.org/2001/XMLSchema-instance}type", "")
        incident_type = raw_type.split(":")[-1] if raw_type else "Unknown"
        cause = self._cleaner.clean(get("causeType"))
        detailed = self.element(record, "detailedCauseType")
        if detailed is not None:
            detail = next((self._cleaner.clean(child.text) for child in detailed if child.text), "")
            cause = f"{cause} - {detail}" if cause and detail else cause or detail
        cause = cause or "Unknown"
        latitude = self.optional_float(get("latitude"))
        longitude = self.optional_float(get("longitude"))
        return Incident(
            id=situation.get("id", ""), record_id=record.get("id", ""), version=record.get("version", ""),
            creation_time=get("situationRecordCreationTime"), source=get("sourceIdentification") or "DGT",
            start_time=get("overallStartTime"), end_time=get("overallEndTime"),
            severity=get("severity") or self.text(situation, "overallSeverity"), type=incident_type,
            type_label=self._translator.translate(incident_type), cause=cause,
            cause_label=" - ".join(self._translator.translate(part.strip()) for part in cause.split(" - ")),
            road=self._cleaner.clean(get("roadName")) or "Desconocida", destination=self._cleaner.clean(get("roadDestination")),
            municipality=self._cleaner.clean(get("municipality")), province=self._cleaner.clean(get("province")),
            community=self._cleaner.clean(get("autonomousCommunity")), km=get("kilometerPoint"),
            direction=get("tpegDirection"), direction_label=self._translator.translate(get("tpegDirection")),
            direction_road=get("tpegDirectionRoad"), latitude=latitude, longitude=longitude,
            lane_usage=get("laneUsage"), management_type=get("roadOrCarriagewayOrLaneManagementType"),
            maintenance_type=get("roadMaintenanceType"), information_status=self.text(situation, "informationStatus"),
            probability=get("probabilityOfOccurrence"), compliance=get("complianceOption"), vehicle_type=get("vehicleType"),
            temp_speed_limit=get("temporarySpeedLimit"), environment_type=get("poorEnvironmentType"),
            road_condition_type=get("nonWeatherRelatedRoadConditionType"),
            location_description=self._cleaner.clean(get("locationDescription")),
            geographic_descriptor=self._cleaner.clean(get("geographicDescriptor")),
        )