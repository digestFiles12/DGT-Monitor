"""Shared PyQt6 theme styles."""

from typing import Literal

ThemeName = Literal["light", "dark"]


def normalize_theme(theme: str | None) -> ThemeName:
    return "dark" if theme == "dark" else "light"


def next_theme(theme: ThemeName) -> ThemeName:
    return "light" if theme == "dark" else "dark"


def main_window_stylesheet(theme: ThemeName) -> str:
    palette = _palette(theme)
    return f"""
        QMainWindow, QWidget {{ background: {palette['paper']}; color: {palette['ink']}; font-family: 'Segoe UI'; font-size: 13px; }}
        QLabel#eyebrow {{ color: {palette['accent']}; font-size: 11px; font-weight: 700; }}
        QLabel#title {{ font-size: 30px; font-weight: 700; }}
        QLabel#sectionTitle {{ font-size: 18px; font-weight: 700; }}
        QLabel#connectionStatus {{ color: {palette['muted']}; font-weight: 600; padding: 0 10px; }}
        QFrame#panel {{ background: {palette['panel']}; border: 1px solid {palette['line']}; border-radius: 3px; }}
        QPushButton#statCard {{ min-height: 74px; background: {palette['panel']}; border: 1px solid {palette['line']}; border-radius: 3px; padding: 8px; text-align: center; }}
        QPushButton#statCard:hover, QPushButton#statCard[active="true"] {{ background: {palette['header']}; border-color: {palette['accent']}; }}
        QPushButton#statCard QLabel {{ background: transparent; }}
        QPushButton#statCard QLabel#statValue {{ color: {palette['accent']}; font-size: 26px; font-weight: 700; }}
        QLineEdit, QComboBox {{ min-height: 36px; padding: 0 10px; background: {palette['field']}; color: {palette['ink']}; border: 1px solid {palette['field_border']}; border-radius: 3px; }}
        QLineEdit:focus, QComboBox:focus {{ border-color: {palette['accent']}; }}
        QPushButton {{ min-height: 36px; padding: 0 16px; background: {palette['panel']}; color: {palette['ink']}; border: 1px solid {palette['button_border']}; border-radius: 3px; font-weight: 600; }}
        QPushButton:hover {{ border-color: {palette['ink']}; }}
        QPushButton#primaryButton {{ background: {palette['accent']}; color: white; border: 0; }}
        QPushButton#primaryButton:hover {{ background: {palette['accent_hover']}; }}
        QTableWidget {{ background: {palette['panel']}; color: {palette['ink']}; alternate-background-color: {palette['alternate']}; border: 1px solid {palette['line']}; gridline-color: {palette['grid']}; selection-background-color: {palette['selection']}; selection-color: {palette['selection_ink']}; }}
        QHeaderView::section {{ min-height: 34px; background: {palette['header']}; color: {palette['muted']}; border: 0; border-right: 1px solid {palette['line']}; padding: 0 8px; font-weight: 700; }}
        QTextBrowser {{ background: {palette['panel']}; color: {palette['ink']}; border: 0; }}
    """


def camera_dialog_stylesheet(theme: ThemeName) -> str:
    palette = _palette(theme)
    return f"""
        QDialog {{ background: {palette['paper']}; color: {palette['ink']}; font-family: 'Segoe UI'; font-size: 13px; }}
        QLabel#dialogTitle {{ font-size: 20px; font-weight: 700; }}
        QLabel#dialogSubtitle, QLabel#statusLabel, QLabel#cameraMeta {{ color: {palette['muted']}; }}
        QScrollArea {{ border: 0; background: transparent; }}
        QScrollArea QWidget {{ background: transparent; color: {palette['ink']}; }}
        QFrame#cameraCard {{ background: {palette['panel']}; border: 1px solid {palette['line']}; border-radius: 3px; }}
        QLabel#cameraTitle {{ font-size: 16px; font-weight: 700; color: {palette['accent']}; }}
        QLabel#cameraImage {{ color: {palette['muted']}; background: {palette['image_bg']}; padding: 8px; border-radius: 3px; }}
        QPushButton {{ min-height: 34px; padding: 0 14px; background: {palette['panel']}; color: {palette['ink']}; border: 1px solid {palette['button_border']}; border-radius: 3px; font-weight: 600; }}
        QPushButton:hover {{ border-color: {palette['ink']}; }}
    """


def _palette(theme: ThemeName) -> dict[str, str]:
    if theme == "dark":
        return {
            "paper": "#101820",
            "panel": "#1d2935",
            "ink": "#edf2f7",
            "muted": "#aab6c4",
            "line": "#344252",
            "field": "#121c25",
            "field_border": "#465769",
            "button_border": "#526477",
            "accent": "#f87171",
            "accent_hover": "#ef4444",
            "alternate": "#17212b",
            "grid": "#2b3948",
            "header": "#253342",
            "selection": "#7f1d1d",
            "selection_ink": "#ffffff",
            "image_bg": "#111a22",
        }
    return {
        "paper": "#f4f6f5",
        "panel": "#ffffff",
        "ink": "#17212b",
        "muted": "#475569",
        "line": "#d7dde1",
        "field": "#ffffff",
        "field_border": "#b8c1c8",
        "button_border": "#aeb7be",
        "accent": "#b91c1c",
        "accent_hover": "#991b1b",
        "alternate": "#f8fafb",
        "grid": "#e2e7ea",
        "header": "#e9edef",
        "selection": "#fee2e2",
        "selection_ink": "#17212b",
        "image_bg": "#eef1f2",
    }