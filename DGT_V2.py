import sys
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Set, Optional
from datetime import datetime
import webbrowser
from math import radians, sin, cos, sqrt, atan2

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QPushButton, QSpinBox, 
                              QTableWidget, QTableWidgetItem, QTextEdit, 
                              QGroupBox, QComboBox, QLineEdit, QCheckBox,
                              QHeaderView, QTabWidget, QFrame, QSplitter,
                              QScrollArea, QDialog)
from PyQt6.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette, QPixmap


TRADUCCIONES = {
    'accident': 'Accidente',
    'vehicleObstruction': 'Obstrucción de vehículo',
    'vehicleStuck': 'Vehículo averiado',
    'roadworks': 'Obras',
    'roadMaintenance': 'Mantenimiento',
    'weatherRelatedRoadConditions': 'Condiciones meteorológicas',
    'poorRoadConditions': 'Mal estado de la carretera',
    'poorEnvironment': 'Condiciones ambientales adversas',
    'poorEnvironmentConditions': 'Condiciones ambientales adversas',
    'fog': 'Niebla',
    'snow': 'Nieve',
    'snowfall': 'Nevada',
    'rain': 'Lluvia',
    'ice': 'Hielo',
    'flooding': 'Inundación',
    'heavySnowfall': 'Nevada intensa',
    'blizzard': 'Ventisca',
    'sleet': 'Aguanieve',
    'frost': 'Helada',
    'blackIce': 'Hielo negro',
    'heavyRain': 'Lluvia intensa',
    'strongWinds': 'Vientos fuertes',
    'storm': 'Tormenta',
    'hail': 'Granizo',
    'obstruction': 'Obstrucción',
    'GenericSituationRecord': 'Registro de situación genérico',
    'environmentalObstruction': 'Obstrucción ambiental',
    'infrastructureDamageObstruction': 'Infraestructura dañada',
    'rockfalls': 'Desprendimientos',
    'damagedRoadSurface': 'Superficie dañada',
    'fallen': 'Caída',
    'fallenTrees': 'Árboles caídos',
    'landslips': 'Deslizamiento de tierra',
    'mudslide': 'Deslizamiento de barro',
    'other': 'Otro',
    

    'animalPresenceObstruction': 'Presencia de animales',
    'peopleOnRoadway': 'Personas en la calzada',
    'childrenOnRoadway': 'Niños en la calzada',
    'cyclistsOnRoadway': 'Ciclistas en la calzada',
    'vehicleOnFire': 'Vehículo en llamas',
    'vehicleBreakdown': 'Avería de vehículo',
    'abnormalTraffic': 'Tráfico anómalo',
    'slowTraffic': 'Tráfico lento',
    'heavyTraffic': 'Tráfico denso',
    'stationaryTraffic': 'Tráfico detenido',
    'trafficCongestion': 'Congestión de tráfico',
    'longQueue': 'Cola larga',
    'queuesLikelyToOccur': 'Probable formación de colas',
    

    'RoadOrCarriagewayOrLaneManagement': 'Gestión de tráfico',
    'NonWeatherRelatedRoadConditions': 'Condiciones de carretera',
    'PoorEnvironmentConditions': 'Condiciones ambientales',
    'Accident': 'Accidente',
    'EquipmentOrSystemFault': 'Fallo de equipo',
    'roadOrCarriagewayOrLaneManagement': 'Gestión de tráfico',
    

    'highest': 'Crítica',
    'high': 'Alta',
    'medium': 'Media',
    'low': 'Baja',
    

    'northBound': 'Dirección Norte',
    'southBound': 'Dirección Sur',
    'eastBound': 'Dirección Este',
    'westBound': 'Dirección Oeste',
    'northEastBound': 'Dirección Noreste',
    'northWestBound': 'Dirección Noroeste',
    'southEastBound': 'Dirección Sureste',
    'southWestBound': 'Dirección Suroeste',
    'unknown': 'Desconocida',
    'positive': 'Positivo',
    'negative': 'Negativo',
    'both': 'Ambos sentidos',
    

    'roadClosed': 'Carretera cerrada',
    'carriagewayClosures': 'Cierre de calzada',
    'laneClosures': 'Cierre de carril',
    'intermittentShortTermClosures': 'Cierres intermitentes',
    

    'allLanesCompleteCarriageway': 'Todos los carriles',
    '_extended': 'Extendido',
    'leftHandLane': 'Carril izquierdo',
    'rightHandLane': 'Carril derecho',
    'centralReservation': 'Mediana',
    

    'narrowLanes': 'Carriles estrechos',
    'singleAlternateLineTraffic': 'Tráfico alternativo de un carril',
    'lanesDeviated': 'Carriles desviados',
    'newRoadworksLayout': 'Nueva disposición por obras',
    'doNotUseSpecifiedLanesOrCarriagewaysAllowed': 'No usar carriles especificados',
    'useOfSpecifiedLanesOrCarriagewaysAllowed': 'Uso de carriles permitido',
    'weightRestrictionInOperation': 'Restricción de peso activa',
    'speedRestrictionInOperation': 'Restricción de velocidad activa',
    

    'rightLane': 'Carril derecho',
    'leftLane': 'Carril izquierdo',
    'tidalFlowLane': 'Carril reversible',
    

    'certain': 'Confirmado',
    'active': 'Activo',
    'real': 'Real',
    'mandatory': 'Obligatorio',
    'advisory': 'Recomendación',
    'anyVehicle': 'Cualquier vehículo',
    

    'badWeather': 'Mal tiempo',
    'roadSurfaceInPoorCondition': 'Superficie en mal estado',
    

    'objectOnTheRoad': 'Objeto en la vía'
}


def traducir(texto: str) -> str:
    """Traducir términos técnicos al español"""
    if not texto:
        return 'N/A'
    return TRADUCCIONES.get(texto, texto)


def limpiar_texto(texto: str) -> str:
    """Limpiar caracteres mal codificados"""
    if not texto:
        return texto
    

    reemplazos = {
        'Ã¨': 'è',
        'Ã©': 'é',
        'Ã¡': 'á',
        'Ã­': 'í',
        'Ã³': 'ó',
        'Ãº': 'ú',
        'Ã±': 'ñ',
        'Á': 'Á',
        'É': 'É',
        'Í': 'Í',
        'Ó': 'Ó',
        'Ú': 'Ú',
        'Ñ': 'Ñ',
        'Ã¼': 'ü',
        'Ã¤': 'ä',
        'Ã¶': 'ö',
        'Ã§': 'ç',
        'À': 'À',
        'Â': 'Â',
        'Ã': 'Ã',
        'Ä': 'Ä',
        'Å': 'Å',
        'Æ': 'Æ',
        'Ç': 'Ç',
        'È': 'È',
        'Ê': 'Ê',
        'Ë': 'Ë',
        'Ì': 'Ì',
        'Î': 'Î',
        'Ï': 'Ï',
        'Ò': 'Ò',
        'Ô': 'Ô',
        'Õ': 'Õ',
        'Ö': 'Ö',
        'Ù': 'Ù',
        'Û': 'Û',
        'Ü': 'Ü',
        'Ý': 'Ý',
        'Ã ': 'à',
        'Ã¢': 'â',
        'Ã£': 'ã',
        'Ã¥': 'å',
        'Ã¦': 'æ',
        'Ãª': 'ê',
        'Ã«': 'ë',
        'Ã¬': 'ì',
        'Ã®': 'î',
        'Ã¯': 'ï',
        'Ã°': 'ð',
        'Ã²': 'ò',
        'Ã´': 'ô',
        'Ãµ': 'õ',
        'Ã¸': 'ø',
        'Ã¹': 'ù',
        'Ã»': 'û',
        'Ã½': 'ý',
        'Ã¿': 'ÿ',
    }
    
    for malo, bueno in reemplazos.items():
        texto = texto.replace(malo, bueno)
    
    return texto

class DataFetchThread(QThread):
    """Hilo para obtener datos sin bloquear la interfaz"""
    data_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.url = "https://nap.dgt.es/datex2/v3/dgt/SituationPublication/datex2_v36.xml"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/xml,text/xml,*/*"
        }
        self.running = True
    
    def run(self):
        """Obtener y parsear datos"""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()

            response.encoding = 'utf-8'
            incidents = self.parse_all(response.text)
            self.data_ready.emit(incidents)
        except Exception as e:
            self.error_occurred.emit(str(e))
    
    def parse_situation(self, situation_elem) -> Optional[Dict]:
        """Parsear una situación del XML"""
        def get_text(parent, tag_name):
            for elem in parent.iter():
                if elem.tag.endswith(tag_name):
                    return elem.text
            return ''
        
        def get_elem(parent, tag_name):
            for elem in parent.iter():
                if elem.tag.endswith(tag_name):
                    return elem
            return None
        
        situation_id = situation_elem.get('id')
        record = get_elem(situation_elem, 'situationRecord')
        
        if record is None:
            return None
        
        data = {
            'id': situation_id,
            'record_id': record.get('id', ''),
            'version': record.get('version', ''),
            'creation_time': get_text(record, 'situationRecordCreationTime'),
            'source': get_text(record, 'sourceIdentification'),
            'start_time': get_text(record, 'overallStartTime'),
            'end_time': get_text(record, 'overallEndTime'),
            'severity': get_text(record, 'severity') or get_text(situation_elem, 'overallSeverity')
        }
        
        xsi_type = record.get('{http://www.w3.org/2001/XMLSchema-instance}type', '')
        data['type'] = xsi_type.split(':')[-1] if xsi_type else 'Unknown'
        

        cause = limpiar_texto(get_text(record, 'causeType'))
        detailed_cause_elem = get_elem(record, 'detailedCauseType')
        if detailed_cause_elem is not None:
            for child in detailed_cause_elem:
                if child.text:
                    cause += f" - {limpiar_texto(child.text)}"
                    break
        data['cause'] = cause if cause else 'Unknown'
        

        data['road'] = limpiar_texto(get_text(record, 'roadName') or 'Desconocida')
        data['destination'] = limpiar_texto(get_text(record, 'roadDestination') or '')
        data['municipality'] = limpiar_texto(get_text(record, 'municipality') or '')
        data['province'] = limpiar_texto(get_text(record, 'province') or '')
        data['community'] = limpiar_texto(get_text(record, 'autonomousCommunity') or '')
        data['km'] = get_text(record, 'kilometerPoint') or ''
        data['direction'] = get_text(record, 'tpegDirection')
        data['direction_road'] = get_text(record, 'tpegDirectionRoad')
        

        lat = get_text(record, 'latitude')
        lon = get_text(record, 'longitude')
        if lat and lon:
            try:
                data['latitude'] = float(lat)
                data['longitude'] = float(lon)
            except ValueError:
                pass
        

        data['lane_usage'] = get_text(record, 'laneUsage')
        data['management_type'] = get_text(record, 'roadOrCarriagewayOrLaneManagementType')
        data['maintenance_type'] = get_text(record, 'roadMaintenanceType')
        

        data['information_status'] = get_text(situation_elem, 'informationStatus')
        data['probability'] = get_text(record, 'probabilityOfOccurrence')
        data['compliance'] = get_text(record, 'complianceOption')
        data['vehicle_type'] = get_text(record, 'vehicleType')
        

        data['temp_speed_limit'] = get_text(record, 'temporarySpeedLimit')
        

        data['environment_type'] = get_text(record, 'poorEnvironmentType')
        data['road_condition_type'] = get_text(record, 'nonWeatherRelatedRoadConditionType')
        

        data['location_description'] = limpiar_texto(get_text(record, 'locationDescription'))
        data['geographic_descriptor'] = limpiar_texto(get_text(record, 'geographicDescriptor'))
        
        return data
    
    def parse_all(self, xml_content: str) -> List[Dict]:
        """Parsear todas las situaciones"""
        if not xml_content:
            return []
        
        try:
            root = ET.fromstring(xml_content)
            situations = []
            
            for elem in root.iter():
                if elem.tag.endswith('situation'):
                    parsed = self.parse_situation(elem)
                    if parsed:
                        situations.append(parsed)
            
            return situations
        except Exception as e:
            return []


class CameraFetchThread(QThread):
    """Hilo para obtener datos de cámaras"""
    cameras_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.url = "https://nap.dgt.es/datex2/v3/dgt/DevicePublication/camaras_datex2_v36.xml"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/xml,text/xml,*/*"
        }
    
    def run(self):
        """Obtener y parsear datos de cámaras"""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=15)
            response.raise_for_status()
            response.encoding = 'utf-8'
            cameras = self.parse_cameras(response.text)
            self.cameras_ready.emit(cameras)
        except Exception as e:
            self.error_occurred.emit(str(e))
    
    def parse_cameras(self, xml_content: str) -> List[Dict]:
        """Parsear todas las cámaras del XML"""
        if not xml_content:
            return []
        
        try:
            root = ET.fromstring(xml_content)
            cameras = []
            

            for elem in root.iter():
                if 'device' in elem.tag and elem.get('{http://www.w3.org/2001/XMLSchema-instance}type', '').endswith('ExtendedDevice'):
                    camera_data = self.parse_camera_device(elem)
                    if camera_data:
                        cameras.append(camera_data)
            
            return cameras
        except Exception as e:
            print(f"Error parsing cameras: {e}")
            return []
    
    def parse_camera_device(self, device_elem) -> Optional[Dict]:
        """Parsear un dispositivo cámara individual"""
        def get_text(parent, tag_name):
            for elem in parent.iter():
                if tag_name in elem.tag:
                    return elem.text
            return ''
        
        def find_coordinates(parent):
            """Buscar coordenadas en el elemento"""
            for elem in parent.iter():
                if 'latitude' in elem.tag and elem.text:
                    try:
                        lat = float(elem.text)

                        for sibling in parent.iter():
                            if 'longitude' in sibling.tag and sibling.text:
                                lon = float(sibling.text)
                                return lat, lon
                    except (ValueError, TypeError):
                        pass
            return None, None
        

        device_type = get_text(device_elem, 'typeOfDevice')
        if device_type != 'camera':
            return None
        
        camera_data = {
            'id': device_elem.get('id', ''),
            'road': get_text(device_elem, 'roadName'),
            'province': get_text(device_elem, 'province'),
            'km': get_text(device_elem, 'kilometerPoint'),
            'image_url': get_text(device_elem, 'deviceUrl')
        }
        

        lat, lon = find_coordinates(device_elem)
        if lat and lon:
            camera_data['latitude'] = lat
            camera_data['longitude'] = lon
        

        return camera_data if camera_data['image_url'] else None


class DGTTrafficGUI(QMainWindow):
    """Interfaz gráfica principal del monitor de tráfico DGT"""
    
    def __init__(self):
        super().__init__()
        self.incidents: List[Dict] = []
        self.filtered_incidents: List[Dict] = []
        self.cameras: List[Dict] = []
        self.open_dialogs: List[QDialog] = []
        self.previous_ids: Set[str] = set()
        self.update_count = 0
        
        self.init_ui()
        self.setup_timer()
        
    def init_ui(self):
        """Inicializar interfaz de usuario"""
        self.setWindowTitle("🚦 Monitor de Tráfico DGT - Tiempo Real")
        self.setGeometry(100, 100, 1400, 750)
        

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0d1117;
            }
            QWidget {
                background-color: #0d1117;
                color: #c9d1d9;
            }
        """)
        

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # ==================== PANEL IZQUIERDO ====================
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(8)
        left_layout.setContentsMargins(0, 0, 0, 0)
        

        header = self.create_header()
        left_layout.addWidget(header)
        

        control_panel = self.create_control_panel()
        left_layout.addWidget(control_panel)
        

        stats_panel = self.create_stats_panel()
        left_layout.addWidget(stats_panel)
        

        incidents_group = QGroupBox("📋 Incidentes en Tiempo Real")
        incidents_group.setStyleSheet("""
            QGroupBox {
                background-color: #161b22;
                border: 2px solid #30363d;
                border-radius: 8px;
                margin-top: 5px;
                font-weight: bold;
                padding: 8px;
                color: #58a6ff;
            }
            QGroupBox::title {
                color: #58a6ff;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        incidents_layout = QVBoxLayout(incidents_group)
        incidents_layout.setContentsMargins(5, 15, 5, 5)
        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "🚨", "Carretera", "Municipio", "Provincia", 
            "Causa", "Severidad", "Km", "Hora"
        ])
        

        self.table.setColumnWidth(0, 40)  
        table_header = self.table.horizontalHeader()
        if table_header is not None:
            table_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            table_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            table_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
            table_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(5, 80)  
        self.table.setColumnWidth(6, 60)  
        self.table.setColumnWidth(7, 120) 
        
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.itemSelectionChanged.connect(self.on_incident_selected)
        self.table.itemDoubleClicked.connect(self.on_table_double_click)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #0d1117;
                alternate-background-color: #161b22;
                gridline-color: #30363d;
                border: 1px solid #30363d;
                border-radius: 4px;
                color: #c9d1d9;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QTableWidget::item:selected {
                background-color: #1f6feb;
                color: white;
            }
            QHeaderView::section {
                background-color: #161b22;
                color: #58a6ff;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #30363d;
                font-weight: bold;
            }
            QScrollBar:vertical {
                border: none;
                background: #161b22;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #30363d;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #484f58;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                border: none;
                background: #161b22;
                height: 12px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #30363d;
                border-radius: 6px;
                min-width: 30px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #484f58;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)
        
        incidents_layout.addWidget(self.table)
        left_layout.addWidget(incidents_group)
        

        self.status_label = QLabel("⏸️ Listo para iniciar")
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #21262d;
                color: #8b949e;
                padding: 6px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
        """)
        left_layout.addWidget(self.status_label)
        
        # ==================== PANEL DERECHO ====================
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(8)
        right_layout.setContentsMargins(0, 0, 0, 0)
        

        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #30363d;
                background-color: #161b22;
                border-radius: 6px;
            }
            QTabBar::tab {
                background-color: #21262d;
                color: #8b949e;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #238636;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #30363d;
            }
        """)
        tabs.addTab(self.create_details_view(), "🔍 Detalles del Incidente")
        tabs.addTab(self.create_log_view(), "📋 Log de Operaciones")
        
        right_layout.addWidget(tabs)
        
        # ==================== SPLITTER PRINCIPAL ====================
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 5) 
        splitter.setStretchFactor(1, 5)  
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #30363d;
                width: 3px;
            }
            QSplitter::handle:hover {
                background-color: #58a6ff;
            }
        """)
        
        main_layout.addWidget(splitter)
        
    def create_header(self) -> QWidget:
        """Crear cabecera compacta y elegante"""
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2c3e50, stop:1 #3498db);
                border-radius: 6px;
            }
        """)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(15, 8, 15, 8)
        

        title_layout = QHBoxLayout()
        icon = QLabel("🚦")
        icon.setFont(QFont("Arial", 16))
        icon.setStyleSheet("background: transparent;")
        title_layout.addWidget(icon)
        
        title = QLabel("Monitor de Tráfico DGT")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        title_layout.addWidget(title)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        

        self.datetime_label = QLabel()
        self.datetime_label.setStyleSheet("color: white; font-size: 11px; font-weight: bold; background: transparent;")
        self.update_datetime()
        layout.addWidget(self.datetime_label)
        
        layout.addSpacing(15)
        

        version = QLabel("v7.1")
        version.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 10px; background: transparent;")
        layout.addWidget(version)
        
        return header
    
    def create_control_panel(self) -> QGroupBox:
        """Crear panel de control compacto"""
        panel = QGroupBox("⚙️ Control")
        panel.setStyleSheet("""
            QGroupBox {
                background-color: #161b22;
                border: 2px solid #30363d;
                border-radius: 8px;
                margin-top: 5px;
                font-weight: bold;
                padding: 8px;
                color: #58a6ff;
            }
            QGroupBox::title {
                color: #58a6ff;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        layout = QVBoxLayout()
        layout.setSpacing(5)
        

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(5)
        
        self.btn_start = QPushButton("▶️ Iniciar")
        self.btn_start.clicked.connect(self.start_monitoring)
        self.btn_start.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2ea043;
            }
            QPushButton:disabled {
                background-color: #21262d;
                color: #484f58;
            }
        """)
        btn_layout.addWidget(self.btn_start)
        
        self.btn_stop = QPushButton("⏹️ Detener")
        self.btn_stop.clicked.connect(self.stop_monitoring)
        self.btn_stop.setEnabled(False)
        self.btn_stop.setStyleSheet("""
            QPushButton {
                background-color: #da3633;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #f85149;
            }
            QPushButton:disabled {
                background-color: #21262d;
                color: #484f58;
            }
        """)
        btn_layout.addWidget(self.btn_stop)
        
        self.btn_refresh = QPushButton("🔄 Actualizar")
        self.btn_refresh.clicked.connect(self.fetch_data)
        self.btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #1f6feb;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #388bfd;
            }
        """)
        btn_layout.addWidget(self.btn_refresh)
        
        btn_layout.addWidget(QLabel("Intervalo:"))
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(10, 600)
        self.interval_spin.setValue(60)
        self.interval_spin.setSuffix(" seg")
        self.interval_spin.setStyleSheet("""
            QSpinBox {
                padding: 6px;
                border: 1px solid #30363d;
                border-radius: 6px;
                background-color: #0d1117;
                color: #c9d1d9;
                font-weight: bold;
                min-width: 80px;
            }
            QSpinBox:focus {
                border: 1px solid #58a6ff;
            }
        """)
        btn_layout.addWidget(self.interval_spin)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        

        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(5)
        
        filter_style = """
            QLineEdit, QComboBox {
                padding: 6px;
                border: 1px solid #30363d;
                border-radius: 6px;
                background-color: #0d1117;
                color: #c9d1d9;
                font-size: 11px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #58a6ff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #c9d1d9;
                margin-right: 5px;
            }
        """
        

        filter_layout.addWidget(QLabel("🗺️"))
        self.province_input = QLineEdit()
        self.province_input.setPlaceholderText("Provincia")
        self.province_input.setStyleSheet(filter_style)
        self.province_input.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.province_input)
        
        filter_layout.addWidget(QLabel("🏙️"))
        self.municipality_input = QLineEdit()
        self.municipality_input.setPlaceholderText("Municipio")
        self.municipality_input.setStyleSheet(filter_style)
        self.municipality_input.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.municipality_input)
        
        filter_layout.addWidget(QLabel("🛣️"))
        self.road_input = QLineEdit()
        self.road_input.setPlaceholderText("Carretera")
        self.road_input.setStyleSheet(filter_style)
        self.road_input.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.road_input)
        
        filter_layout.addWidget(QLabel("⚠️"))
        self.severity_combo = QComboBox()
        self.severity_combo.addItems(["Todas", "Crítica", "Alta", "Media", "Baja"])
        self.severity_combo.setStyleSheet(filter_style)
        self.severity_combo.currentTextChanged.connect(self.filter_by_severity_click)

        filter_layout.addWidget(self.severity_combo)

        self.btn_clear_filters = QPushButton("🗑️")
        self.btn_clear_filters.setToolTip("Limpiar todos los filtros")
        self.btn_clear_filters.clicked.connect(self.clear_all_filters)
        self.btn_clear_filters.setStyleSheet("""
            QPushButton {
                background-color: #6e7681;
                color: white;
                border: none;
                padding: 6px 10px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
                max-width: 40px;
            }
            QPushButton:hover {
                background-color: #8b949e;
            }
        """)
        filter_layout.addWidget(self.btn_clear_filters)        
        
        layout.addLayout(filter_layout)
        
        panel.setLayout(layout)
        return panel
        
    def clear_all_filters(self):
        """Limpiar todos los filtros activos"""
        self.province_input.clear()
        self.municipality_input.clear()
        self.road_input.clear()
        self.severity_combo.setCurrentText("Todas")
        self.add_log("🗑️ Todos los filtros han sido limpiados")
        self.apply_filters()        
        
    
    def create_stats_panel(self) -> QGroupBox:
        """Crear panel de estadísticas compacto y clickeable"""
        panel = QGroupBox("📊 Estadísticas (Click para filtrar)")
        panel.setStyleSheet("""
            QGroupBox {
                background-color: #161b22;
                border: 2px solid #30363d;
                border-radius: 8px;
                margin-top: 5px;
                font-weight: bold;
                padding: 8px;
                color: #58a6ff;
            }
            QGroupBox::title {
                color: #58a6ff;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.stats_labels = {}
        self.stats_buttons = {}
        stats = [
            ("Total", "total", "#1f6feb", "all"),
            ("💥 Accidentes", "accidents", "#da3633", "accident"),
            ("🚧 Obras", "roadworks", "#fb8500", "roadworks"),
            ("🔧 Averías", "stuck", "#d29922", "stuck"),
            ("🚫 Obstrucciones", "obstructions", "#8957e5", "obstruction"),
            ("🌫️ Clima", "weather", "#3fb950", "weather")
        ]
        
        for label_text, key, color, filter_type in stats:
            btn = QPushButton(f"{label_text}\n0")
            btn.setFont(QFont("Arial", 9, QFont.Weight.Bold))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 5px;
                    min-width: 80px;
                    max-height: 55px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: {color};
                    border: 2px solid white;
                }}
                QPushButton:pressed {{
                    background-color: {color};
                    border: 3px solid yellow;
                }}
            """)
            btn.clicked.connect(lambda checked, ft=filter_type: self.filter_by_type(ft))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            
            self.stats_labels[key] = btn
            self.stats_buttons[key] = btn
            layout.addWidget(btn)
        
        layout.addStretch()
        panel.setLayout(layout)
        return panel
    
    
    def create_details_view(self) -> QWidget:
        """Crear vista de detalles con scroll"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        header_layout = QHBoxLayout()
        
        info_label = QLabel("📋 Selecciona un incidente para ver detalles")
        info_label.setStyleSheet("""
            QLabel {
                background-color: #1f6feb;
                color: white;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
        """)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(info_label)
        

        self.btn_cameras = QPushButton("📸 Buscar Cámaras Cercanas")
        self.btn_cameras.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.btn_cameras.clicked.connect(self.buscar_camaras_cercanas)
        header_layout.addWidget(self.btn_cameras)
        
        layout.addLayout(header_layout)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setFont(QFont("Consolas", 9))
        self.details_text.setStyleSheet("""
            QTextEdit {
                background-color: #0d1117;
                color: #c9d1d9;
                border: 2px solid #30363d;
                border-radius: 6px;
                padding: 10px;
            }
            QScrollBar:vertical {
                border: none;
                background: #161b22;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #30363d;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #484f58;
            }
        """)
        layout.addWidget(self.details_text)
        
        return widget
        
    def create_log_view(self) -> QWidget:
        """Crear vista de log de operaciones"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        header_layout = QHBoxLayout()
        
        log_title = QLabel("📋 LOG DE OPERACIONES")
        log_title.setStyleSheet("""
            QLabel {
                background-color: #1f6feb;
                color: white;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
        """)
        header_layout.addWidget(log_title)
        
        self.btn_clear_log = QPushButton("🗑️ Limpiar Log")
        self.btn_clear_log.clicked.connect(self.clear_log)
        self.btn_clear_log.setStyleSheet("""
            QPushButton {
                background-color: #fb8500;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ffb703;
            }
        """)
        header_layout.addWidget(self.btn_clear_log)
        
        layout.addLayout(header_layout)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #0d1117;
                color: #8b949e;
                border: 2px solid #30363d;
                border-radius: 6px;
                padding: 10px;
            }
            QScrollBar:vertical {
                border: none;
                background: #161b22;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #30363d;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #484f58;
            }
        """)
        

        self.add_log("✅ Sistema de logs activado - Todo se mostrará aquí")
        
        layout.addWidget(self.log_text)
        return widget
    
    def add_log(self, message: str):
        """Agregar mensaje al log"""
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        self.log_text.append(f"{timestamp} {message}")
    
    def clear_log(self):
        """Limpiar el log"""
        self.log_text.clear()
        self.add_log("🗑️ Log limpiado")

    def open_url(self, url: str):
        """Abrir URL en el navegador"""
        import webbrowser
        webbrowser.open(url)

    def show_non_modal_dialog(self, dialog: QDialog):
        """Mostrar un diálogo sin bloquear el resto de ventanas."""
        dialog.setModal(False)
        dialog.setWindowModality(Qt.WindowModality.NonModal)
        dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.open_dialogs.append(dialog)
        dialog.finished.connect(lambda _result, dlg=dialog: self.open_dialogs.remove(dlg) if dlg in self.open_dialogs else None)
        dialog.show()
    
    def setup_timer(self):
        """Configurar temporizador para actualizaciones automáticas"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.fetch_data)
    
    def update_datetime(self):
        """Actualizar fecha y hora"""
        now = datetime.now()
        text = f"📅 {now.strftime('%d/%m/%Y')}   ⏰ {now.strftime('%H:%M:%S')}   🔄 Actualización #{self.update_count}"
        self.datetime_label.setText(text)
    
    def start_monitoring(self):
        """Iniciar monitoreo automático"""
        interval_ms = self.interval_spin.value() * 1000
        self.timer.start(interval_ms)
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.status_label.setText(f"✅ Monitoreo activo (actualización cada {self.interval_spin.value()}s)")
        self.add_log(f"▶️ Monitoreo iniciado - Intervalo: {self.interval_spin.value()}s")
        self.fetch_data()
    
    def stop_monitoring(self):
        """Detener monitoreo automático"""
        self.timer.stop()
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.status_label.setText("⏸️ Monitoreo detenido")
        self.add_log("⏹️ Monitoreo detenido")
    
    def fetch_data(self):
        """Obtener datos del servidor DGT"""
        self.status_label.setText("⏳ Obteniendo datos...")
        self.add_log("🔄 Solicitando datos del servidor DGT...")
        self.fetch_thread = DataFetchThread()
        self.fetch_thread.data_ready.connect(self.on_data_received)
        self.fetch_thread.error_occurred.connect(self.on_error)
        self.fetch_thread.start()
    
    def on_data_received(self, incidents: List[Dict]):
        """Procesar datos recibidos"""
        self.incidents = incidents
        self.update_count += 1
        self.update_datetime()
        

        current_ids = {inc['id'] for inc in incidents}
        new_ids = current_ids - self.previous_ids
        self.previous_ids = current_ids
        
        if new_ids:
            self.status_label.setText(f"🆕 {len(new_ids)} nuevos incidentes detectados")
            self.add_log(f"🆕 {len(new_ids)} nuevos incidentes detectados")
        else:
            self.status_label.setText(f"✅ Datos actualizados ({len(incidents)} incidentes)")
            self.add_log(f"✅ Datos actualizados - Total: {len(incidents)} incidentes")
        
        self.apply_filters()
        self.update_statistics()
    
    def on_error(self, error_msg: str):
        """Manejar errores"""
        self.status_label.setText(f"❌ Error: {error_msg}")
        self.add_log(f"❌ Error: {error_msg}")
    
    def apply_filters(self):
        """Aplicar filtros a los incidentes"""
        filtered = self.incidents.copy()
        

        province_filter = self.province_input.text().strip().lower()
        if province_filter:
            filtered = [inc for inc in filtered 
                       if province_filter in inc.get('province', '').lower()]
        

        municipality_filter = self.municipality_input.text().strip().lower()
        if municipality_filter:
            filtered = [inc for inc in filtered 
                       if municipality_filter in inc.get('municipality', '').lower()]
        

        road_filter = self.road_input.text().strip().upper()
        if road_filter:
            filtered = [inc for inc in filtered 
                       if road_filter in inc.get('road', '').upper()]
        

        severity_filter = self.severity_combo.currentText()
        if severity_filter != "Todas":
            severity_map = {
                "Crítica": "highest",
                "Alta": "high",
                "Media": "medium",
                "Baja": "low"
            }
            sev = severity_map.get(severity_filter, "")
            filtered = [inc for inc in filtered 
                       if inc.get('severity', '').lower() == sev]
        

        active_filters = []
        if province_filter:
            active_filters.append(f"Provincia: {self.province_input.text()}")
        if municipality_filter:
            active_filters.append(f"Municipio: {self.municipality_input.text()}")
        if road_filter:
            active_filters.append(f"Carretera: {road_filter}")
        if severity_filter != "Todas":
            active_filters.append(f"Severidad: {severity_filter}")
        
        if active_filters:
            filter_text = " | ".join(active_filters)
            self.add_log(f"🔍 Filtros aplicados: {filter_text} = {len(filtered)} resultados")
        
        self.filtered_incidents = filtered
        self.update_table()
        self.update_statistics()

    def filter_by_type(self, filter_type: str):
        """Filtrar incidentes por tipo desde las estadísticas, preservando otros filtros"""

        
        if filter_type == "all":

            self.apply_filters()
            self.add_log("🔍 Mostrando todos los tipos de incidentes")
        else:

            filtered = self.incidents.copy()
            

            province_filter = self.province_input.text().strip().lower()
            if province_filter:
                filtered = [inc for inc in filtered 
                           if province_filter in inc.get('province', '').lower()]
            

            municipality_filter = self.municipality_input.text().strip().lower()
            if municipality_filter:
                filtered = [inc for inc in filtered 
                           if municipality_filter in inc.get('municipality', '').lower()]
            

            road_filter = self.road_input.text().strip().upper()
            if road_filter:
                filtered = [inc for inc in filtered 
                           if road_filter in inc.get('road', '').upper()]
            

            severity_filter = self.severity_combo.currentText()
            if severity_filter != "Todas":
                severity_map = {
                    "Crítica": "highest",
                    "Alta": "high",
                    "Media": "medium",
                    "Baja": "low"
                }
                sev = severity_map.get(severity_filter, "")
                filtered = [inc for inc in filtered 
                           if inc.get('severity', '').lower() == sev]
            

            type_filtered = []
            for inc in filtered:
                cause_lower = inc.get('cause', '').lower()
                
                if filter_type == "accident" and 'accident' in cause_lower:
                    type_filtered.append(inc)
                elif filter_type == "roadworks" and ('roadworks' in cause_lower or 'maintenance' in cause_lower):
                    type_filtered.append(inc)
                elif filter_type == "stuck" and 'stuck' in cause_lower:
                    type_filtered.append(inc)
                elif filter_type == "obstruction" and 'obstruction' in cause_lower:
                    type_filtered.append(inc)
                elif filter_type == "weather" and any(w in cause_lower for w in ['weather', 'fog', 'snow', 'flooding', 'ice']):
                    type_filtered.append(inc)
            
            self.filtered_incidents = type_filtered
            
            type_names = {
                "accident": "Accidentes",
                "roadworks": "Obras",
                "stuck": "Averías",
                "obstruction": "Obstrucciones",
                "weather": "Meteorología"
            }
            

            active_filters = []
            if province_filter:
                active_filters.append(f"Provincia: {self.province_input.text()}")
            if municipality_filter:
                active_filters.append(f"Municipio: {self.municipality_input.text()}")
            if road_filter:
                active_filters.append(f"Carretera: {road_filter}")
            if severity_filter != "Todas":
                active_filters.append(f"Severidad: {severity_filter}")
            
            filter_text = " | ".join(active_filters) if active_filters else "sin filtros adicionales"
            self.add_log(f"🔍 Filtrando por: {type_names.get(filter_type, filter_type)} ({filter_text}) = {len(type_filtered)} resultados")
        
        self.update_table()
        self.update_statistics()
    
    def filter_by_severity_click(self, severity: str):
        """Filtrar por severidad desde el combo"""
        severity_map_reverse = {
            "Todas": "Todas",
            "Crítica": "highest",
            "Alta": "high",
            "Media": "medium",
            "Baja": "low"
        }
        
        if severity == "Todas":
            self.add_log("🔍 Mostrando todas las severidades")
        else:
            self.add_log(f"🔍 Filtrando por severidad: {severity}")
        
        self.apply_filters()
    
    def update_table(self):
        """Actualizar tabla de incidentes - MOSTRAR TODOS"""
        self.table.setRowCount(len(self.filtered_incidents))
        
        for row, inc in enumerate(self.filtered_incidents):

            emoji = self.get_cause_emoji(inc['cause'])
            emoji_item = QTableWidgetItem(emoji)
            emoji_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, emoji_item)
            

            self.table.setItem(row, 1, QTableWidgetItem(inc.get('road', 'N/A')))
            self.table.setItem(row, 2, QTableWidgetItem(inc.get('municipality', 'N/A')))
            self.table.setItem(row, 3, QTableWidgetItem(inc.get('province', 'N/A')))
            

            cause_parts = inc.get('cause', '').split(' - ')
            cause_translated = ' - '.join([traducir(p.strip()) for p in cause_parts])
            self.table.setItem(row, 4, QTableWidgetItem(cause_translated))
            

            severity = traducir(inc.get('severity', ''))
            severity_item = QTableWidgetItem(severity)
            severity_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            

            severity_colors = {
                'Crítica': QColor(218, 54, 51),
                'Alta': QColor(251, 133, 0),
                'Media': QColor(210, 153, 34),
                'Baja': QColor(63, 185, 80)
            }
            if severity in severity_colors:
                severity_item.setBackground(severity_colors[severity])
                severity_item.setForeground(QColor(255, 255, 255))
            
            self.table.setItem(row, 5, severity_item)
            self.table.setItem(row, 6, QTableWidgetItem(inc.get('km', 'N/A')))
            

            start_time = inc.get('start_time', '')[:16] if inc.get('start_time') else 'N/A'
            self.table.setItem(row, 7, QTableWidgetItem(start_time))
    
    def update_statistics(self):
        """Actualizar panel de estadísticas"""
        total = len(self.filtered_incidents)
        accidents = sum(1 for inc in self.filtered_incidents 
                       if 'accident' in inc.get('cause', '').lower())
        roadworks = sum(1 for inc in self.filtered_incidents 
                       if 'roadworks' in inc.get('cause', '').lower() or 
                          'roadmaintenance' in inc.get('cause', '').lower() or
                          'maintenance' in inc.get('cause', '').lower())
        stuck = sum(1 for inc in self.filtered_incidents 
                   if 'stuck' in inc.get('cause', '').lower())
        obstructions = sum(1 for inc in self.filtered_incidents 
                          if 'obstruction' in inc.get('cause', '').lower())
        weather = sum(1 for inc in self.filtered_incidents 
                     if any(w in inc.get('cause', '').lower() 
                           for w in ['weather', 'fog', 'snow', 'flooding', 'ice']))
        
        self.stats_labels['total'].setText(f"Total\n{total}")
        self.stats_labels['accidents'].setText(f"💥 Accidentes\n{accidents}")
        self.stats_labels['roadworks'].setText(f"🚧 Obras\n{roadworks}")
        self.stats_labels['stuck'].setText(f"🔧 Averías\n{stuck}")
        self.stats_labels['obstructions'].setText(f"🚫 Obstrucciones\n{obstructions}")
        self.stats_labels['weather'].setText(f"🌫️ Clima\n{weather}")
    
    def on_incident_selected(self):
        """Mostrar detalles del incidente seleccionado"""
        selected_rows = self.table.selectedIndexes()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        if row >= len(self.filtered_incidents):
            return
        
        inc = self.filtered_incidents[row]
        

        cause_parts = inc.get('cause', '').split(' - ')
        cause_translated = ' - '.join([traducir(p.strip()) for p in cause_parts])
        
        direction = traducir(inc.get('direction', ''))
        direction_road = traducir(inc.get('direction_road', ''))
        severity = traducir(inc.get('severity', ''))
        management = traducir(inc.get('management_type', ''))
        lane = traducir(inc.get('lane_usage', ''))
        tipo_traducido = traducir(inc.get('type', ''))
        
        details = f"""

           DETALLES DEL INCIDENTE    


🆔 ID: {inc.get('id', 'N/A')}
📝 Versión: {inc.get('version', 'N/A')}

📍 UBICACIÓN
   • Carretera: {inc.get('road', 'N/A')}
   • Municipio: {inc.get('municipality', 'N/A')}
   • Provincia: {inc.get('province', 'N/A')}
   • Comunidad: {inc.get('community', 'N/A')}
   • Kilómetro: {inc.get('km', 'N/A')}
   • Destino: {inc.get('destination', 'N/A')}

🚨 INCIDENTE
   • Causa: {cause_translated}
   • Severidad: {severity}
   • Tipo: {tipo_traducido}

🚗 TRÁFICO
   • Dirección: {direction}
   • Sentido: {direction_road}
   • Gestión: {management}
   • Carril: {lane}

⏰ TEMPORALIDAD
   • Inicio: {inc.get('start_time', 'N/A')}
   • Fin previsto: {inc.get('end_time', 'N/A')}
   • Hora de creación: {inc.get('creation_time', 'N/A')}

📊 INFORMACIÓN ADICIONAL"""
        
        if inc.get('temp_speed_limit'):
            details += f"\n   • Límite de velocidad temporal: {inc.get('temp_speed_limit')} km/h"
        
        if inc.get('environment_type'):
            details += f"\n   • Tipo de condición ambiental: {traducir(inc.get('environment_type', ''))}"
        
        if inc.get('road_condition_type'):
            details += f"\n   • Condición de la carretera: {traducir(inc.get('road_condition_type', ''))}"
        
        details += f"""

📡 FUENTE DE DATOS
   • Origen: {inc.get('source', 'DGT')}
"""
        
        if inc.get('latitude') and inc.get('longitude'):
            maps_url = f"https://maps.google.com/?q={inc['latitude']},{inc['longitude']}"
            details += f"""
🗺️ COORDENADAS GPS
   • Latitud: {inc['latitude']:.6f}
   • Longitud: {inc['longitude']:.6f}
   • 🔗 Ver en Google Maps: {maps_url}

📸 CÁMARAS DE TRÁFICO CERCANAS
   Para ver cámaras en tiempo real de esta zona:
   1. Haz clic en el botón "📸 Buscar Cámaras Cercanas" arriba
   2. Se buscarán cámaras en: {inc.get('province', 'N/A')} - {inc.get('road', 'N/A')}
   
   💡 TIP: Las cámaras se ordenarán por distancia al incidente
"""
        else:
            details += """

⚠️ No hay coordenadas GPS disponibles para este incidente

📸 CÁMARAS DE TRÁFICO:
   Para ver cámaras en tiempo real, use el botón "📸 Buscar Cámaras Cercanas"
"""
        
        details += """
       INFORMACIÓN DE CONTACTO DGT                          

📞 TELÉFONOS DE INFORMACIÓN:
   • Información de Tráfico: 011 (gratuito desde España)
   • Emergencias: 112
   • Guardia Civil Tráfico: 062

🌐 WEB Y REDES SOCIALES:
   • Web DGT: https://www.dgt.es
   • Twitter: @DGTes
   • Infocar: https://infocar.dgt.es

📧 EMAIL:
   • info@dgt.es
   • buzon-dgt@dgt.es
"""
        
        self.details_text.setText(details)
        
    def open_camera_url(self, lat=None, lon=None, provincia=None, carretera=None):
        """Abrir página de cámaras de la DGT con filtros de provincia y carretera"""
        import webbrowser
        

        provincia_codes = {
            'Albacete': '2', 'Alicante/Alacant': '3', 'Almería': '4', 'Araba/Álava': '1',
            'Asturias': '33', 'Ávila': '5', 'Badajoz': '6', 'Balears, Illes': '7',
            'Barcelona': '8', 'Bizkaia': '48', 'Burgos': '9', 'Cáceres': '10',
            'Cádiz': '11', 'Cantabria': '39', 'Castellón/Castelló': '12', 'Ceuta': '51',
            'Ciudad Real': '13', 'Córdoba': '14', 'Coruña, A': '15', 'Cuenca': '16',
            'Gipuzkoa': '20', 'Girona': '17', 'Granada': '18', 'Guadalajara': '19',
            'Huelva': '21', 'Huesca': '22', 'Jaén': '23', 'León': '24',
            'Lleida': '25', 'Lugo': '27', 'Madrid': '28', 'Málaga': '29',
            'Melilla': '52', 'Murcia': '30', 'Navarra': '31', 'Ourense': '32',
            'Palencia': '34', 'Palmas, Las': '35', 'Pontevedra': '36', 'Rioja, La': '26',
            'Salamanca': '37', 'Santa Cruz de Tenerife': '38', 'Segovia': '40',
            'Sevilla': '41', 'Soria': '42', 'Tarragona': '43', 'Teruel': '44',
            'Toledo': '45', 'Valencia/València': '46', 'Valladolid': '47',
            'Zamora': '49', 'Zaragoza': '50'
        }
        

        base_url = "https://www.dgt.es/conoce-el-estado-del-trafico/camaras-de-trafico/"
        

        params = []
        params.append('pag=1')
        
        if provincia:
            prov_code = provincia_codes.get(provincia)
            if prov_code:
                params.append(f'prov={prov_code}')
                self.add_log(f"🔍 Código de provincia: {provincia} = {prov_code}")
            else:
                self.add_log(f"⚠️ No se encontró código para provincia: '{provincia}'")
        
        if carretera:


            params.append(f'carr={carretera}')
            self.add_log(f"🔍 Carretera: {carretera}")
        

        camera_url = f"{base_url}?{'&'.join(params)}"
        
        self.add_log(f"🌐 URL generada: {camera_url}")
        webbrowser.open(camera_url)
        

        if provincia and carretera:
            self.add_log(f"🎥 Abriendo cámaras DGT: {provincia} - {carretera}")
        elif provincia:
            self.add_log(f"🎥 Abriendo cámaras DGT: {provincia}")
        else:
            self.add_log(f"🎥 Abriendo página de cámaras de tráfico de la DGT")
    
    def open_camera_from_selection(self):
        """Abrir cámaras desde el incidente seleccionado"""
        selected_rows = self.table.selectedIndexes()
        if not selected_rows:
            self.add_log("⚠️ Por favor, selecciona un incidente primero")
            self.open_camera_url()  
            return
        
        row = selected_rows[0].row()
        if row >= len(self.filtered_incidents):
            return
        
        inc = self.filtered_incidents[row]
        provincia = inc.get('province', '')
        carretera = inc.get('road', '')
        
        self.add_log(f"🔍 DEBUG - Provincia: '{provincia}', Carretera: '{carretera}'")
        
        if provincia or carretera:
            self.open_camera_url(provincia=provincia, carretera=carretera)
        else:
            self.open_camera_url()
    
    def on_table_double_click(self, item):
        """Manejar doble click en la tabla para abrir cámaras"""
        row = item.row()
        if row >= len(self.filtered_incidents):
            return
        
        inc = self.filtered_incidents[row]
        provincia = inc.get('province', '')
        carretera = inc.get('road', '')
        
        self.add_log(f"🔍 DEBUG - Provincia obtenida: '{provincia}'")
        self.add_log(f"🔍 DEBUG - Carretera obtenida: '{carretera}'")
        
        if provincia or carretera:
            self.open_camera_url(provincia=provincia, carretera=carretera)
        else:
            self.open_camera_url()
            self.add_log(f"⚠️ No hay datos de provincia o carretera disponibles")      
        
    
    def get_cause_emoji(self, cause: str) -> str:
        """Obtener emoji según la causa"""
        cause_lower = cause.lower()
        if 'accident' in cause_lower:
            return '💥'
        if 'vehiclestuck' in cause_lower.replace(' ', '') or 'stuck' in cause_lower:
            return '🔧'
        if 'roadworks' in cause_lower.replace(' ', '') or 'maintenance' in cause_lower:
            return '🚧'
        if 'obstruction' in cause_lower or 'object' in cause_lower:
            return '🚫'
        if 'weather' in cause_lower or 'fog' in cause_lower:
            return '🌫️'
        if 'snow' in cause_lower or 'ice' in cause_lower:
            return '❄️'
        if 'flooding' in cause_lower or 'flood' in cause_lower:
            return '🌊'
        if 'rockfall' in cause_lower:
            return '🪨'
        if 'damaged' in cause_lower or 'poor' in cause_lower:
            return '⚠️'
        return '⚠️'

    # ==================== MÉTODOS NUEVOS PARA CÁMARAS ====================
    
    def buscar_camaras_cercanas(self):
        """Buscar cámaras cercanas al incidente seleccionado"""
        selected_rows = self.table.selectedIndexes()
        if not selected_rows:
            self.add_log("⚠️ Por favor, selecciona un incidente primero")
            return
        
        row = selected_rows[0].row()
        if row >= len(self.filtered_incidents):
            return
        
        inc = self.filtered_incidents[row]
        provincia = inc.get('province', '')
        carretera = inc.get('road', '')
        
        self.add_log(f"🔍 Buscando cámaras para: {provincia} - {carretera}")
        

        if not self.cameras:
            self.obtener_camaras(provincia, carretera)
        else:
            self.mostrar_camaras_cercanas(provincia, carretera)
    
    def obtener_camaras(self, provincia, carretera):
        """Obtener datos de cámaras"""
        self.add_log("🔄 Cargando datos de cámaras DGT...")
        self.camera_thread = CameraFetchThread()
        self.camera_thread.cameras_ready.connect(lambda cams: self.on_camaras_obtenidas(cams, provincia, carretera))
        self.camera_thread.error_occurred.connect(self.on_error_camaras)
        self.camera_thread.start()
    
    def on_camaras_obtenidas(self, cameras, provincia, carretera):
        """Procesar cámaras obtenidas"""
        self.cameras = cameras
        self.add_log(f"✅ Se encontraron {len(cameras)} cámaras")
        self.mostrar_camaras_cercanas(provincia, carretera)
    
    def on_error_camaras(self, error_msg: str):
        """Manejar errores de cámaras"""
        self.add_log(f"❌ Error al obtener cámaras: {error_msg}")
    
    def mostrar_camaras_cercanas(self, provincia, carretera):
        """Mostrar cámaras cercanas al incidente ordenadas por distancia"""
        selected_rows = self.table.selectedIndexes()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        if row >= len(self.filtered_incidents):
            return
        
        inc = self.filtered_incidents[row]
        inc_lat = inc.get('latitude')
        inc_lon = inc.get('longitude')
        
        camaras_encontradas = []
        
        for camara in self.cameras:
            cam_province = camara.get('province', '')
            cam_road = camara.get('road', '')
            cam_lat = camara.get('latitude')
            cam_lon = camara.get('longitude')
            

            province_match = provincia and cam_province and provincia.lower() in cam_province.lower()
            road_match = carretera and cam_road and carretera.upper() in cam_road.upper()
            

            distancia = None
            if inc_lat and inc_lon and cam_lat and cam_lon:
                distancia = self.calcular_distancia(inc_lat, inc_lon, cam_lat, cam_lon)
            
            if province_match or road_match:
                camara['distancia'] = distancia
                camaras_encontradas.append(camara)
        

        camaras_encontradas.sort(key=lambda x: x['distancia'] if x['distancia'] is not None else float('inf'))
        
        if camaras_encontradas:
            self.mostrar_dialogo_camaras(camaras_encontradas, provincia, carretera, inc_lat, inc_lon)
        else:
            self.add_log(f"ℹ️ No se encontraron cámaras para: {provincia} - {carretera}")
    
    def calcular_distancia(self, lat1, lon1, lat2, lon2):
        """Calcular distancia en km entre dos coordenadas usando fórmula haversine"""

        R = 6371.0
        

        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)
        

        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        

        a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        return R * c
    
    def mostrar_dialogo_camaras(self, camaras, provincia, carretera, inc_lat, inc_lon):
        """Mostrar diálogo con las cámaras encontradas ordenadas por distancia"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"📸 Cámaras Cercanas: {provincia} - {carretera}")
        dialog.setGeometry(200, 200, 800, 600)
        
        layout = QVBoxLayout(dialog)
        

        if inc_lat and inc_lon:
            header_text = f"📸 {len(camaras)} cámaras cercanas al incidente"
        else:
            header_text = f"📸 {len(camaras)} cámaras en la zona"
        
        header = QLabel(header_text)
        header.setStyleSheet("""
            QLabel {
                background-color: #1f6feb;
                color: white;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        

        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        for i, camara in enumerate(camaras, 1):
            cam_frame = QFrame()
            cam_frame.setStyleSheet("""
                QFrame {
                    background-color: #161b22;
                    border: 1px solid #30363d;
                    border-radius: 6px;
                    margin: 5px;
                    padding: 5px;
                }
            """)
            cam_layout = QHBoxLayout(cam_frame)
            

            info_text = f"{i}. 🛣️ {camara.get('road', 'N/A')}"
            info_text += f" - 🏛️ {camara.get('province', 'N/A')}"
            info_text += f" - 📍 Km {camara.get('km', 'N/A')}"
            

            if camara.get('distancia') is not None:
                distancia_km = camara['distancia']
                if distancia_km < 1:
                    distancia_text = f"{distancia_km*1000:.0f}m"
                else:
                    distancia_text = f"{distancia_km:.1f}km"
                info_text += f" - 📏 {distancia_text}"
            
            info_label = QLabel(info_text)
            info_label.setStyleSheet("QLabel { padding: 8px; }")
            cam_layout.addWidget(info_label)
            
            cam_layout.addStretch()
            

            btn_ver = QPushButton("👀 Ver Imagen")
            btn_ver.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2ecc71;
                }
            """)
            btn_ver.clicked.connect(lambda checked, url=camara.get('image_url', ''): self.ver_imagen_camara(url))
            cam_layout.addWidget(btn_ver)
            

            if camara.get('latitude') and camara.get('longitude'):
                btn_mapa = QPushButton("🗺️ Mapa")
                btn_mapa.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        border: none;
                        padding: 8px 15px;
                        border-radius: 4px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                """)
                btn_mapa.clicked.connect(lambda checked, lat=camara['latitude'], lon=camara['longitude']: 
                                       self.ver_en_mapa(lat, lon))
                cam_layout.addWidget(btn_mapa)
            
            scroll_layout.addWidget(cam_frame)
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        

        btn_cerrar = QPushButton("❌ Cerrar")
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: #da3633;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f85149;
            }
        """)
        btn_cerrar.clicked.connect(dialog.close)
        layout.addWidget(btn_cerrar)
        
        self.show_non_modal_dialog(dialog)
    
    def ver_imagen_camara(self, url):
        """Mostrar imagen de la cámara en un diálogo separado"""
        if not url:
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("📸 Imagen de Cámara")
        dialog.setGeometry(300, 300, 800, 600)
        
        layout = QVBoxLayout(dialog)
        

        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("""
            QLabel {
                background-color: #000000;
                border: 3px solid #30363d;
                border-radius: 8px;
                min-height: 400px;
            }
        """)
        image_label.setText("🔄 Cargando imagen...")
        layout.addWidget(image_label)
        

        btn_layout = QHBoxLayout()
        
        btn_actualizar = QPushButton("🔄 Actualizar")
        btn_actualizar.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        btn_actualizar.clicked.connect(lambda: self.cargar_imagen(url, image_label))
        btn_layout.addWidget(btn_actualizar)
        
        btn_web = QPushButton("🌐 Abrir en Navegador")
        btn_web.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        btn_web.clicked.connect(lambda: webbrowser.open(url))
        btn_layout.addWidget(btn_web)
        
        btn_cerrar = QPushButton("❌ Cerrar")
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: #da3633;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f85149;
            }
        """)
        btn_cerrar.clicked.connect(dialog.close)
        btn_layout.addWidget(btn_cerrar)
        
        layout.addLayout(btn_layout)
        

        self.cargar_imagen(url, image_label)
        
        self.show_non_modal_dialog(dialog)
    
    def cargar_imagen(self, url, image_label):
        """Cargar imagen de la cámara"""
        image_label.setText("🔄 Cargando imagen...")
        QTimer.singleShot(100, lambda: self.descargar_imagen(url, image_label))
    
    def descargar_imagen(self, url, image_label):
        """Descargar imagen en segundo plano"""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                image_data = response.content
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                
                if not pixmap.isNull():

                    scaled_pixmap = pixmap.scaled(700, 500, Qt.AspectRatioMode.KeepAspectRatio, 
                                                Qt.TransformationMode.SmoothTransformation)
                    image_label.setPixmap(scaled_pixmap)
                else:
                    image_label.setText("❌ Error al cargar la imagen")
            else:
                image_label.setText("❌ No se pudo cargar la imagen")
        except Exception as e:
            image_label.setText(f"❌ Error: {str(e)}")
    
    def ver_en_mapa(self, lat, lon):
        """Abrir ubicación en Google Maps"""
        maps_url = f"https://maps.google.com/?q={lat},{lon}"
        webbrowser.open(maps_url)
        self.add_log(f"🗺️ Abriendo ubicación en mapa: {lat}, {lon}")


def main():
    """Función principal"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(236, 240, 241))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(44, 62, 80))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(189, 195, 199))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(52, 152, 219))
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Text, QColor(44, 62, 80))
    palette.setColor(QPalette.ColorRole.Button, QColor(52, 152, 219))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.BrightText, QColor(231, 76, 60))
    palette.setColor(QPalette.ColorRole.Link, QColor(41, 128, 185))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(52, 152, 219))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    app.setPalette(palette)
    
    window = DGTTrafficGUI()
    window.show()
    

    QTimer.singleShot(2000, lambda: window.obtener_camaras("", ""))
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
