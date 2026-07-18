"""Namespace-independent XML helpers."""

from xml.etree.ElementTree import Element


class Datex2Parser:
    @staticmethod
    def text(parent: Element, tag_name: str) -> str:
        for element in parent.iter():
            if element.tag.endswith(tag_name):
                return element.text or ""
        return ""

    @staticmethod
    def element(parent: Element, tag_name: str) -> Element | None:
        for element in parent.iter():
            if element.tag.endswith(tag_name):
                return element
        return None

    @staticmethod
    def optional_float(value: str) -> float | None:
        try:
            return float(value) if value else None
        except ValueError:
            return None