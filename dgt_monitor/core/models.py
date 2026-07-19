"""Typed domain models shared by the desktop and web applications."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class Incident:
    id: str = ""
    record_id: str = ""
    version: str = ""
    creation_time: str = ""
    source: str = "DGT"
    start_time: str = ""
    end_time: str = ""
    severity: str = ""
    type: str = "Unknown"
    type_label: str = "Unknown"
    cause: str = "Unknown"
    cause_label: str = "Unknown"
    road: str = "Desconocida"
    destination: str = ""
    municipality: str = ""
    province: str = ""
    community: str = ""
    km: str = ""
    direction: str = ""
    direction_label: str = "N/A"
    direction_road: str = ""
    latitude: float | None = None
    longitude: float | None = None
    lane_usage: str = ""
    management_type: str = ""
    maintenance_type: str = ""
    information_status: str = ""
    probability: str = ""
    compliance: str = ""
    vehicle_type: str = ""
    temp_speed_limit: str = ""
    environment_type: str = ""
    road_condition_type: str = ""
    location_description: str = ""
    geographic_descriptor: str = ""
    has_camera_coverage: bool = False
    camera_coverage_count: int = 0
    nearest_camera_km_delta: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Camera:
    id: str = ""
    road: str = ""
    province: str = ""
    km: str = ""
    image_url: str = ""
    latitude: float | None = None
    longitude: float | None = None
    distance_km: float | None = None
    km_delta: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class IncidentStats:
    total: int = 0
    accidents: int = 0
    roadworks: int = 0
    stuck: int = 0
    obstructions: int = 0
    weather: int = 0

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class IncidentFilters:
    province: str | None = None
    municipality: str | None = None
    road: str | None = None
    severity: str | None = None
    kind: str | None = None
    camera: str | None = None


@dataclass(frozen=True, slots=True)
class CameraFilters:
    province: str | None = None
    road: str | None = None
    kilometer: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    limit: int | None = 12
    max_km_delta: float = 1.0
    max_distance_km: float | None = None