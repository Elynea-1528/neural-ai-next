# UI Architektúra - Streamlit MVVM

## 🎯 Áttekintés

Ez a dokumentum a **Neural AI Next** felhasználói felületének Streamlit alapú MVVM (Model-View-ViewModel) architektúráját dokumentálja.

**Architektúra:** Streamlit MVVM minta  
**Verzió:** 1.0.0  
**Utolsó frissítés:** 2026-01-04

---

## 🏗️ Architektúra Rétegek

### 1. View Layer (Streamlit Pages)

A felhasználói felület megjelenítési rétege, amely kizárólag a vizuális elemekkel és interakciók kezelésével foglalkozik.

#### Struktúra

```
ui/
├── pages/                    # Streamlit oldalak
│   ├── 01_🚀_Launchpad.py
│   ├── 02_🛠️_Dev_Center.py
│   ├── 03_📥_Data_Hub.py
│   ├── 04_🧠_AI_Lab.py
│   ├── 05_🪲_Strategy_Lab.py
│   └── 06_⚡_Live_Ops.py
├── main.py                   # Fő alkalmazás
└── theme.py                  # Design system
```

#### Jellemzők

- **Csupán megjelenítési logika:** Nincs üzleti logika
- **Interakciók delegálása:** Minden művelet a Service rétegnek delegálódik
- **Session state:** Állapot kezelésére használatos
- **Komponensek:** Reusable UI komponensek

#### Példa: Launchpad Oldal

```python
# ui/pages/01_🚀_Launchpad.py
import streamlit as st
from ui.services.dashboard_service import DashboardService
from ui.bridges.core_bridge import CoreBridge

@st.cache_resource
def init_services() -> tuple[DashboardService, CoreBridge]:
    """Service-ek inicializálása Dependency Injectionnel."""
    logger_factory = CoreBridge.get_logger_factory()
    config_factory = CoreBridge.get_config_factory()
    
    logger = logger_factory.get_logger("ui.launchpad")
    config = config_factory.get_manager()
    
    dashboard_service = DashboardService(logger=logger, config=config)
    core_bridge = CoreBridge(logger=logger, config=config)
    
    return dashboard_service, core_bridge

def main():
    """Fő oldal logika."""
    st.title("🚀 Neural AI Next - Launchpad")
    
    # Service-ek inicializálása
    dashboard_service, core_bridge = init_services()
    
    # Rendszer állapotának megjelenítése
    health_status = dashboard_service.get_system_health()
    
    # ... (UI logika)
```

---

### 2. ViewModel Layer (Services)

Az üzleti logika rétege, amely az adatokat előkészíti a View számára és koordinálja a komplex műveleteket.

#### Struktúra

```
ui/
└── services/                 # ViewModel réteg
    ├── base_service.py       # Alap service osztály
    ├── dashboard_service.py  # Vezérlőpult logika
    ├── config_service.py     # Konfiguráció kezelés
    ├── data_service.py       # Adatkezelés
    ├── analytics_service.py  # Analitika
    ├── strategy_service.py   # Stratégia kezelés
    └── live_trading_service.py  # Live kereskedés
```

#### Jellemzők

- **Független a Streamlit-től:** Könnyű tesztelhetőség
- **Interface-eken keresztül kommunikál:** Loose coupling
- **Adatok átalakítása:** Formázás, validálás
- **Komplex műveletek koordinálása:** Több Bridge hívása

#### Példa: DashboardService

```python
# ui/services/dashboard_service.py
from typing import Dict, Any
from .base_service import BaseService

class DashboardService(BaseService):
    """Vezérlőpult service - ViewModel réteg."""
    
    def get_system_health(self) -> Dict[str, Any]:
        """Rendszer állapotának lekérése."""
        try:
            health_monitor = self._get_health_monitor()
            health_data = health_monitor.check_health()
            
            return {
                "cuda_status": "Available" if health_data.cuda_available else "Disabled",
                "cuda_available": health_data.cuda_available,
                "database_status": health_data.database.status,
                "database_tables": health_data.database.table_count,
                # ...
            }
        except Exception as e:
            self.logger.error(f"Error getting system health: {e}")
            return self._get_default_health_status()
```

---

### 3. Bridge Layer (Core Integration)

A kapcsolatot biztosítja a Core backenddel, Dependency Injection támogatással.

#### Struktúra

```
ui/
└── bridges/                  # Bridge réteg
    ├── core_bridge.py        # Core backend integráció
    ├── data_bridge.py        # Adatkezelés integráció
    └── config_bridge.py      # Konfiguráció integráció
```

#### Jellemzők

- **Dependency Injection:** Factory-k használata
- **Interface-based access:** Csak interfészeken keresztül
- **Hibakezelés:** Centralizált hibakezelés
- **Visszajelzés:** Hibák és státuszok továbbítása

#### Példa: CoreBridge

```python
# ui/bridges/core_bridge.py
from neural_ai.core.base.factory import ComponentFactory
from neural_ai.core.logger.interfaces.logger_interface import ILogger
from neural_ai.core.config.interfaces.config_interface import IConfigManager

class CoreBridge:
    """Bridge a Core backendhez."""
    
    def __init__(self, logger: ILogger, config: IConfigManager):
        """Inicializálás DI-vel."""
        self.logger = logger
        self.config = config
        self._component_factory = ComponentFactory()
    
    def get_health_monitor(self):
        """Health monitor lekérése."""
        return self._component_factory.create_health_monitor(
            logger=self.logger,
            config=self.config
        )
    
    def start_all_collectors(self) -> Dict[str, Any]:
        """Összes adatgyűjtő indítása."""
        try:
            from neural_ai.core.ingestion.market_data_persister import MarketDataPersister
            
            persister = MarketDataPersister(
                logger=self.logger,
                config=self.config
            )
            
            result = persister.start_all_collectors()
            
            return {
                "success": True,
                "started_count": result.started_count,
                "total_count": result.total_count
            }
        except Exception as e:
            self.logger.error(f"Error starting collectors: {e}")
            return {"success": False, "error": str(e)}
```

---

## 🔄 Kommunikációs Folyamat

### MVVM Adatfolyam

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│    VIEW     │◄────────┤   VIEWMODEL  │◄────────┤    BRIDGE   │
│ (Streamlit) │         │   (Service)  │         │   (Bridge)  │
└─────────────┘         └──────────────┘         └─────────────┘
       │                       │                       │
       │ User Interaction      │ Business Logic       │ Core Access
       │                       │                       │
       ▼                       ▼                       ▼
  ┌─────────┐            ┌──────────┐            ┌─────────┐
  │ Session │            │   Data   │            │  Core   │
  │  State  │            │  Transform│           │ Backend │
  └─────────┘            └──────────┘            └─────────┘
```

### 1. User Interaction Flow

```python
# 1. Felhasználó interakció a View-ban
if st.button("Start Collectors"):
    # 2. Hívás a ViewModel rétegre
    result = dashboard_service.start_all_collectors()
    
    # 3. Eredmény megjelenítése
    if result.success:
        st.success("Collectors started")
    else:
        st.error(result.error)
```

### 2. Service-Bridge Kommunikáció

```python
# Service réteg
class DashboardService(BaseService):
    def get_system_health(self):
        # Bridge hívása
        health_monitor = self._get_health_monitor()
        health_data = health_monitor.check_health()
        
        # Adatok átalakítása
        return self._transform_health_data(health_data)
```

### 3. Bridge-Core Kommunikáció

```python
# Bridge réteg
class CoreBridge:
    def start_all_collectors(self):
        # Core komponens létrehozása Factory-vel
        persister = MarketDataPersister(
            logger=self.logger,
            config=self.config
        )
        
        # Művelet végrehajtása
        result = persister.start_all_collectors()
        
        # Visszajelzés formázása
        return {
            "success": True,
            "started_count": result.started_count
        }
```

---

## 📦 Technológiai Stack

### Fő Függőségek

```toml
# Streamlit Framework
streamlit = ">=1.30.0"
streamlit-aggrid = ">=0.3.0"
streamlit-antd-components = ">=0.2.0"

# Charting
plotly = ">=5.18.0"
plotly-express = ">=0.4.0"

# Data Handling
pandas = ">=2.0.0"
numpy = ">=1.24.0"
pyarrow = ">=14.0.0"
fastparquet = ">=2023.0.0"

# Monitoring
watchdog = ">=3.0.0"
tensorboard = ">=2.14.0"

# ML/DL
torch = ">=2.5.1"
torchinfo = ">=1.8.0"
lightning = ">=2.5.5"
```

### Fejlesztői Eszközök

```bash
# Streamlit futtatása
/home/elynea/miniconda3/envs/neural-ai-next/bin/streamlit run ui/main.py

# Tesztelés
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/test_ui_services.py

# Linting
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check ui/
```

---

## 🎨 Design System

### Theme Konfiguráció

```python
# ui/theme.py
import streamlit as st

def inject_custom_css():
    """Egyedi CSS injektálása."""
    st.markdown(
        """
        <style>
        .main {
            background-color: #0f172a;
            color: #f8fafc;
        }
        
        .profit { color: #10b981; }
        .loss { color: #ef4444; }
        .neutral { color: #6b7280; }
        
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Color palette
COLORS = {
    "primary": "#3b82f6",
    "secondary": "#8b5cf6",
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "profit": "#10b981",
    "loss": "#ef4444"
}
```

### Komponens Library

```python
# ui/components/__init__.py
from .cards import MetricCard, InfoCard, WarningCard
from .charts import PnLChart, EquityCurveChart, VolumeChart
from .tables import DataTable, LogTable, TradeTable

__all__ = [
    'MetricCard', 'InfoCard', 'WarningCard',
    'PnLChart', 'EquityCurveChart', 'VolumeChart',
    'DataTable', 'LogTable', 'TradeTable'
]
```

---

## 🔐 Biztonság

### Authentication System

```python
# ui/auth.py
import streamlit as st
import hashlib
from datetime import datetime, timedelta

class AuthManager:
    """Authentikáció kezelő."""
    
    def check_authentication(self) -> bool:
        """Authentikáció ellenőrzése."""
        if 'authenticated' not in st.session_state:
            return False
        
        if not st.session_state.authenticated:
            return False
        
        # Session timeout ellenőrzés
        if 'auth_time' in st.session_state:
            auth_time = st.session_state.auth_time
            if datetime.now() - auth_time > self.session_timeout:
                self.logout()
                return False
        
        return True
    
    def login_page(self):
        """Bejelentkezési oldal."""
        st.title("🔐 Neural AI Next - Login")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login", type="primary"):
                if self._validate_credentials(username, password):
                    st.session_state.authenticated = True
                    st.session_state.auth_time = datetime.now()
                    st.rerun()
```

### Biztonságos Oldal Dekorátor

```python
# ui/decorators.py
from functools import wraps
from .auth import auth_manager

def require_auth(func):
    """Dekorátor authentikáció megköveteléséhez."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not auth_manager.check_authentication():
            auth_manager.login_page()
            return
        return func(*args, **kwargs)
    return wrapper

# Használat
@require_auth
def main():
    """Biztonságos oldal."""
    # ...
```

---

## 📊 Chart Komponensek

### Plotly Integráció

```python
# ui/components/charts.py
import plotly.graph_objects as go
import pandas as pd

class PnLChart:
    """Profit/Loss chart komponens."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
    
    def create_chart(self) -> go.Figure:
        """Chart létrehozása."""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=self.data['timestamp'],
            y=self.data['pnl_cumulative'],
            mode='lines',
            name='Cumulative PnL',
            line=dict(color='#10b981', width=2)
        ))
        
        fig.update_layout(
            title="Cumulative Profit & Loss",
            template="plotly_dark",
            height=400
        )
        
        return fig
```

---

## 🧪 Tesztelés

### Service Tesztelés

```python
# tests/test_ui_services.py
import pytest
from unittest.mock import Mock, patch
from ui.services.dashboard_service import DashboardService

class TestDashboardService:
    """DashboardService tesztelése."""
    
    @pytest.fixture
    def mock_logger(self):
        return Mock()
    
    @pytest.fixture
    def mock_config(self):
        return Mock()
    
    @pytest.fixture
    def dashboard_service(self, mock_logger, mock_config):
        return DashboardService(logger=mock_logger, config=mock_config)
    
    def test_get_system_health_success(self, dashboard_service):
        """Rendszer állapotának sikeres lekérése."""
        mock_health_monitor = Mock()
        mock_health_data = Mock()
        mock_health_data.cuda_available = True
        mock_health_monitor.check_health.return_value = mock_health_data
        
        with patch.object(dashboard_service, '_get_health_monitor', return_value=mock_health_monitor):
            result = dashboard_service.get_system_health()
            
            assert result['cuda_status'] == 'Available'
            assert result['cuda_available'] is True
```

### Teszt Futtatás

```bash
# Unit tesztek
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/test_ui_services.py -v

# Coverage report
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/test_ui_services.py --cov=ui/services --cov-report=html
```

---

## 📱 Reszponzív Design

### Layout Komponensek

```python
# ui/layouts.py
import streamlit as st

def create_responsive_grid(items: list, columns: int = 3):
    """Reszponzív grid létrehozása."""
    cols = st.columns(columns)
    
    for index, item in enumerate(items):
        with cols[index % columns]:
            if callable(item):
                item()
            else:
                st.write(item)

def create_dashboard_layout():
    """Dashboard layout."""
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
    
    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Main content
        pass
    
    with col2:
        # Side panel
        pass
```

---

## 🚀 Fejlesztési Workflow

### 1. Új Oldal Létrehozása

```bash
# 1. Fájl létrehozása
touch ui/pages/07_📊_New_Page.py

# 2. Alap struktúra
cat > ui/pages/07_📊_New_Page.py << EOF
import streamlit as st
from ui.services.new_service import NewService

# Page config
st.set_page_config(
    page_title="Neural AI - New Page",
    page_icon="📊",
    layout="wide"
)

def main():
    st.title("📊 New Page")
    
    # Service inicializálás
    service = NewService()
    
    # UI logika
    # ...

if __name__ == "__main__":
    main()
EOF
```

### 2. Új Service Létrehozása

```bash
# Service fájl
touch ui/services/new_service.py

# Alap service struktúra
cat > ui/services/new_service.py << EOF
from .base_service import BaseService

class NewService(BaseService):
    """Új service komponens."""
    
    def __init__(self, logger, config):
        super().__init__(logger, config)
    
    def get_data(self):
        """Adatok lekérése."""
        # Implementáció
        pass
EOF
```

### 3. Új Bridge Létrehozása

```bash
# Bridge fájl
touch ui/bridges/new_bridge.py

# Alap bridge struktúra
cat > ui/bridges/new_bridge.py << EOF
from neural_ai.core.base.factory import ComponentFactory

class NewBridge:
    """Új bridge komponens."""
    
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self._component_factory = ComponentFactory()
    
    def get_core_component(self):
        """Core komponens lekérése."""
        return self._component_factory.create_component(
            logger=self.logger,
            config=self.config
        )
EOF
```

---

## 📋 Best Practices

### 1. Dependency Injection Használata

```python
# ✅ Jó
class DashboardService(BaseService):
    def __init__(self, logger, config):
        super().__init__(logger, config)

# ❌ Rossz
class DashboardService:
    def __init__(self):
        from neural_ai.core.logger.factory import LoggerFactory
        self.logger = LoggerFactory().get_logger("dashboard")
```

### 2. Session State Használata

```python
# ✅ Jó
def get_data():
    if 'cached_data' not in st.session_state:
        st.session_state.cached_data = expensive_operation()
    return st.session_state.cached_data

# ❌ Rossz
cached_data = None  # Globális változó
```

### 3. Hibakezelés

```python
# ✅ Jó
try:
    result = service.get_data()
    if result.success:
        st.success("Success")
    else:
        st.error(f"Error: {result.error}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    st.error("Unexpected error occurred")

# ❌ Rossz
result = service.get_data()  # Nincs hibakezelés
```

### 4. Type Hints

```python
# ✅ Jó
from typing import Dict, Any, Optional

def get_data(self) -> Dict[str, Any]:
    """Adatok lekérése."""
    pass

# ❌ Rossz
def get_data(self):
    pass
```

---

## 🔗 Kapcsolódó Dokumentumok

- [UI Specifikáció](../../planning/specs/06_user_interface.md)
- [Core Architektúra](../core/base/index.md)
- [Logger Dokumentáció](../core/logger/index.md)
- [Config Dokumentáció](../core/config/index.md)
- [Fejlesztési Útmutató](../../development/unified_development_guide.md)

---

## 📞 Support

Ha kérdésed van az UI architektúrával kapcsolatban, kérjük vedd fel a kapcsolatot a fejlesztői csapattal vagy hozz létre egy issue-t a projekt repository-ban.