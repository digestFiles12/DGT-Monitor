"""Parser for DGT camera DevicePublication documents."""

import xml.etree.ElementTree as ET

from dgt_monitor.core.exceptions import DgtParseError
from dgt_monitor.core.models import Camera
from dgt_monitor.core.text import TextCleaner
from dgt_monitor.infrastructure.parsers.base import Datex2Parser


class CameraParser(Datex2Parser):
    def __init__(self, cleaner: TextCleaner | None = None) -> None:
        self._cleaner = cleaner or TextCleaner()

    def parse(self, xml_content: str) -> list[Camera]:
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as exc:
            raise DgtParseError(f"XML de cámaras no válido: {exc}") from exc
        cameras: list[Camera] = []
        for node in root.iter():
            xsi_type = node.get("{http://www.w3.org/2001/XMLSchema-instance}type", "")
            if "device" not in node.tag or not xsi_type.endswith("ExtendedDevice") or self.text(node, "typeOfDevice") != "camera":
                continue
            image_url = self.text(node, "deviceUrl")
            if image_url:
                cameras.append(Camera(
                    id=node.get("id", ""), road=self._cleaner.clean(self.text(node, "roadName")),
                    province=self._cleaner.clean(self.text(node, "province")), km=self.text(node, "kilometerPoint"),
                    latitude=self.optional_float(self.text(node, "latitude")),
                    longitude=self.optional_float(self.text(node, "longitude")), image_url=image_url,
                ))
        return cameras