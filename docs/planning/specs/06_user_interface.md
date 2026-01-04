# 06 - Felhasználói Felület (User Interface) - Streamlit MVVM

## 🎯 Cél és Szándék

Ez a dokumentum definiálja a **Neural AI Next** felhasználói felületének architektúráját és implementációs stratégiáját Streamlit keretrendszerrel, MVVM (Model-View-ViewModel) mintával. A rendszer egy modern, valós idejű webes felületet biztosít a kereskedési stratégiák monitorozására, konfiguráció kezelésére és analitikák megjelenítésére.

**Filozófia:** *"Real-time insights, intuitive control, zero learning curve"*

**Architektúra:** Streamlit MVVM (Model-View-ViewModel) minta

---

## 🏗️ Architektúra Áttekintés

### Streamlit MVVM Stack

```
┌─────────────────────────────────────────────────────────┐
│         STREAMLIT MVVM ARCHITECTURE                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────┐      │
│  │   VIEW LAYER (Streamlit Pages)               │      │
│  │   - 01_🚀_Launchpad.py                       │      │
│  │   - 02_🛠️_Dev_Center.py                     │      │
│  │   - 03_📥_Data_Hub.py                        │      │
│  │   - 04_🧠_AI_Lab.py                          │      │
│  │   - 05_🪲_Strategy_Lab.py                    │      │
│  │   - 06_⚡_Live_Ops.py                        │      │
│  └──────────────┬───────────────────────────────┘      │
│                 │                                       │
│                 │ Session State + Callbacks             │
│                 ▼                                       │
│  ┌──────────────────────────────────────────────┐      │
│  │   VIEWMODEL LAYER (Services)                 │      │
│  │   - ui/services/                             │      │
│  │     • dashboard_service.py                   │      │
│  │     • config_service.py                      │      │
│  │     • data_service.py                        │      │
│  │     • analytics_service.py                   │      │
│  │     • strategy_service.py                    │      │
│  │     • live_trading_service.py                │      │
│  └──────────────┬───────────────────────────────┘      │
│                 │                                       │
│                 │ Dependency Injection                  │
│                 ▼                                       │
│  ┌──────────────────────────────────────────────┐      │
│  │   BRIDGE LAYER (Core Integration)            │      │
│  │   - ui/bridges/                              │      │
│  │     • core_bridge.py                         │      │
│  │     • data_bridge.py                         │      │
│  │     • config_bridge.py                       │      │
│  └──────────────┬───────────────────────────────┘      │
│                 │                                       │
│                 │ Interface-based Access                │
│                 ▼                                       │
│  ┌──────────────────────────────────────────────┐      │
│  │   CORE BACKEND (neural_ai/)                  │      │
│  │   - Logger, Config, Storage, Events          │      │
│  │   - Collectors, Processors                   │      │
│  │   - Database (SQLAlchemy)                    │      │
│  └──────────────────────────────────────────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### MVVM Minta Részletezése

#### 1. **View Layer (Streamlit Pages)**
- **Feladat:** A felhasználói felület megjelenítése, interakciók kezelése
- **Technológia:** Streamlit >=1.30.0
- **Strukturálás:** Minden oldal egy külön Python fájl a `ui/pages/` mappában
- **Jellemzők:**
  - Csupán megjelenítési logika
  - Nincs üzleti logika
  - Minden művelet delegálása a Service rétegnek
  - Session state használata állapot kezelésére

#### 2. **ViewModel Layer (Services)**
- **Feladat:** Üzleti logika, adatok előkészítése a View számára
- **Elhelyezés:** `ui/services/`
- **Jellemzők:**
  - Független a Streamlit keretrendszertől
  - Interface-eken keresztül éri el a Core backendet
  - Adatok átalakítása, validálása
  - Komplex műveletek koordinálása

#### 3. **Bridge Layer (Core Integration)**
- **Feladat:** Kapcsolat biztosítása a Core backenddel
- **Elhelyezés:** `ui/bridges/`
- **Jellemzők:**
  - Dependency Injection használata
  - Factory-k használata példányosításhoz
  - Interface-eken keresztül kommunikál
  - Hibakezelés és visszajelzés

---

## 📦 Technológiai Stack

### Streamlit Frontend Függőségek

```toml
# pyproject.toml - UI szekció
[project.dependencies]
# Core Streamlit
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

# Utilities
python-dotenv = ">=1.0.0"
pyyaml = ">=6.0"
```

### Architektúra Szabványok

```python
# ui/__init__.py
"""
Neural AI Next - Streamlit UI Package

MVVM Architecture:
- View: pages/ (Streamlit oldalak)
- ViewModel: services/ (Üzleti logika)
- Bridge: bridges/ (Core integráció)
"""

__version__ = "1.0.0"
```

---

## 🖥️ Fő Komponensek (Streamlit Pages)

### 1. 🚀 Launchpad (01_🚀_Launchpad.py)

#### Funkciók
- Rendszer indítása és inicializálás
- Környezet validálás (CUDA, adatbázis, config)
- Gyors hozzáférés a főbb modulokhoz
- Rendszer állapot figyelés

#### Implementáció Vázlat

```python
# ui/pages/01_🚀_Launchpad.py
import streamlit as st
from ui.services.dashboard_service import DashboardService
from ui.bridges.core_bridge import CoreBridge
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import ILogger
    from neural_ai.core.config.interfaces.config_interface import IConfigManager

# Page Config
st.set_page_config(
    page_title="Neural AI - Launchpad",
    page_icon="🚀",
    layout="wide"
)

@st.cache_resource
def init_services() -> tuple[DashboardService, CoreBridge]:
    """Service-ek inicializálása Dependency Injectionnel."""
    # Factory-k használata a Core komponensek létrehozásához
    logger_factory = CoreBridge.get_logger_factory()
    config_factory = CoreBridge.get_config_factory()
    
    logger: ILogger = logger_factory.get_logger("ui.launchpad")
    config: IConfigManager = config_factory.get_manager()
    
    dashboard_service = DashboardService(logger=logger, config=config)
    core_bridge = CoreBridge(logger=logger, config=config)
    
    return dashboard_service, core_bridge

def render_system_status(dashboard_service: DashboardService):
    """Rendszer állapotának megjelenítése."""
    st.header("🎯 System Status")
    
    # Health check a Service-en keresztül
    health_status = dashboard_service.get_system_health()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="CUDA Status",
            value=health_status.cuda_status,
            delta="Available" if health_status.cuda_available else "Disabled"
        )
    
    with col2:
        st.metric(
            label="Database",
            value=health_status.database_status,
            delta=f"Tables: {health_status.database_tables}"
        )
    
    with col3:
        st.metric(
            label="Config Loaded",
            value=health_status.config_status,
            delta=f"Entries: {health_status.config_entries}"
        )
    
    with col4:
        st.metric(
            label="Active Collectors",
            value=health_status.active_collectors,
            delta=f"Total: {health_status.total_collectors}"
        )

def render_quick_actions(core_bridge: CoreBridge):
    """Gyors műveletek panel."""
    st.header("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Start All Collectors", type="primary"):
            with st.spinner("Starting collectors..."):
                result = core_bridge.start_all_collectors()
                if result.success:
                    st.success("✅ All collectors started")
                else:
                    st.error(f"❌ Error: {result.error}")
    
    with col2:
        if st.button("📊 View Live Dashboard"):
            st.switch_page("pages/06_⚡_Live_Ops.py")
    
    with col3:
        if st.button("🛠️ Open Dev Center"):
            st.switch_page("pages/02_🛠️_Dev_Center.py")

def render_data_overview(dashboard_service: DashboardService):
    """Adatok áttekintése."""
    st.header("📊 Data Overview")
    
    data_info = dashboard_service.get_data_summary()
    
    # Chart a meglévő adatokról
    fig = dashboard_service.create_data_volume_chart(data_info)
    st.plotly_chart(fig, use_container_width=True)
    
    # Táblázat a szimbólumokról
    st.dataframe(
        data_info.symbols_df,
        use_container_width=True,
        hide_index=True
    )

def main():
    """Fő oldal logika."""
    st.title("🚀 Neural AI Next - Launchpad")
    
    # Service-ek inicializálása
    dashboard_service, core_bridge = init_services()
    
    # Oldal tartalom
    render_system_status(dashboard_service)
    render_quick_actions(core_bridge)
    render_data_overview(dashboard_service)
    
    # Sidebar info
    with st.sidebar:
        st.header("System Info")
        st.write(f"Version: {core_bridge.get_system_version()}")
        st.write(f"Python: {core_bridge.get_python_version()}")
        st.write(f"PyTorch: {core_bridge.get_torch_version()}")

if __name__ == "__main__":
    main()
```

### 2. 🛠️ Dev Center (02_🛠️_Dev_Center.py)

#### Funkciók
- Kód szerkesztő beágyazása
- Konfigurációk módosítása (Hot Reload)
- Logok valós idejű megjelenítése
- Tesztelési eszközök

#### Implementáció Vázlat

```python
# ui/pages/02_🛠️_Dev_Center.py
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import TYPE_CHECKING
from ui.services.config_service import ConfigService
from ui.services.log_service import LogService

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import ILogger

# Page Config
st.set_page_config(
    page_title="Neural AI - Dev Center",
    page_icon="🛠️",
    layout="wide"
)

def render_log_viewer(log_service: LogService):
    """Log megjelenítő komponens."""
    st.header("📋 Live Log Viewer")
    
    # Szűrők
    col1, col2, col3 = st.columns(3)
    
    with col1:
        log_level = st.selectbox(
            "Log Level",
            options=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            index=1
        )
    
    with col2:
        component_filter = st.multiselect(
            "Components",
            options=log_service.get_available_components(),
            default=[]
        )
    
    with col3:
        time_range = st.selectbox(
            "Time Range",
            options=["Last 1h", "Last 6h", "Last 24h", "All"],
            index=0
        )
    
    # Log táblázat
    logs_df = log_service.get_filtered_logs(
        level=log_level,
        components=component_filter,
        time_range=time_range
    )
    
    st.dataframe(
        logs_df,
        use_container_width=True,
        height=400
    )
    
    # Log statisztikák
    st.subheader("📊 Log Statistics")
    stats = log_service.get_log_statistics()
    
    fig = go.Figure(data=[
        go.Bar(
            x=stats['level'],
            y=stats['count'],
            marker_color=['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6']
        )
    ])
    
    fig.update_layout(
        title="Log Distribution by Level",
        xaxis_title="Log Level",
        yaxis_title="Count"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_config_editor(config_service: ConfigService):
    """Konfiguráció szerkesztő."""
    st.header("⚙️ Configuration Editor")
    
    # Config szekciók
    config_sections = config_service.get_config_sections()
    
    selected_section = st.selectbox(
        "Select Section",
        options=list(config_sections.keys())
    )
    
    if selected_section:
        # Config értékek betöltése
        config_data = config_service.get_section_config(selected_section)
        
        # Szerkesztő felület
        with st.form(f"edit_{selected_section}"):
            st.subheader(f"Editing: {selected_section}")
            
            edited_config = {}
            for key, value in config_data.items():
                if isinstance(value, bool):
                    edited_config[key] = st.checkbox(key, value=value)
                elif isinstance(value, int):
                    edited_config[key] = st.number_input(key, value=value)
                elif isinstance(value, float):
                    edited_config[key] = st.number_input(key, value=value, format="%.4f")
                else:
                    edited_config[key] = st.text_input(key, value=str(value))
            
            submitted = st.form_submit_button("💾 Save & Reload", type="primary")
            
            if submitted:
                result = config_service.update_section_config(
                    selected_section,
                    edited_config
                )
                
                if result.success:
                    st.success("✅ Configuration updated successfully!")
                    st.balloons()
                else:
                    st.error(f"❌ Error: {result.error}")

def main():
    """Fő oldal logika."""
    st.title("🛠️ Dev Center")
    
    # Service-ek inicializálása
    config_service = ConfigService()
    log_service = LogService()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "📋 Log Viewer",
        "⚙️ Config Editor",
        "🧪 Test Tools"
    ])
    
    with tab1:
        render_log_viewer(log_service)
    
    with tab2:
        render_config_editor(config_service)
    
    with tab3:
        st.header("🧪 Testing Tools")
        st.write("Test tools will be implemented here...")

if __name__ == "__main__":
    main()
```

### 3. 📥 Data Hub (03_📥_Data_Hub.py)

#### Funkciók
- Adatgyűjtők kezelése (JForex, MT5, IBKR)
- Történelmi adatok letöltése
- Adatok validálása és vizualizációja
- Parquet tároló kezelés

#### Implementáció Vázlat

```python
# ui/pages/03_📥_Data_Hub.py
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
from typing import TYPE_CHECKING
from ui.services.data_service import DataService
from ui.bridges.data_bridge import DataBridge

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import ILogger

# Page Config
st.set_page_config(
    page_title="Neural AI - Data Hub",
    page_icon="📥",
    layout="wide"
)

def render_collector_control(data_service: DataService):
    """Adatgyűjtők vezérlőpanelje."""
    st.header("🎛️ Collector Control")
    
    # Collector állapotok
    collectors = data_service.get_collector_status()
    
    for collector in collectors:
        with st.expander(f"{collector.name} - {collector.status}", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Type:** {collector.type}")
                st.write(f"**Symbols:** {', '.join(collector.active_symbols)}")
                st.write(f"**Last Update:** {collector.last_update}")
                st.write(f"**Data Points:** {collector.data_points:,}")
            
            with col2:
                if collector.status == "Running":
                    if st.button("⏹️ Stop", key=f"stop_{collector.id}"):
                        result = data_service.stop_collector(collector.id)
                        if result.success:
                            st.success("Collector stopped")
                        else:
                            st.error(result.error)
                else:
                    if st.button("▶️ Start", key=f"start_{collector.id}"):
                        result = data_service.start_collector(collector.id)
                        if result.success:
                            st.success("Collector started")
                        else:
                            st.error(result.error)

def render_historical_download(data_service: DataService):
    """Történelmi adatok letöltése."""
    st.header("📥 Historical Data Download")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        symbols = st.multiselect(
            "Symbols",
            options=["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"],
            default=["EURUSD"]
        )
    
    with col2:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=30)
        )
    
    with col3:
        end_date = st.date_input("End Date", value=datetime.now())
    
    # Letöltés indítása
    if st.button("🚀 Download Historical Data", type="primary"):
        with st.spinner("Downloading data..."):
            progress_bar = st.progress(0)
            
            def progress_callback(progress: float):
                progress_bar.progress(progress)
            
            result = data_service.download_historical_data(
                symbols=symbols,
                start_date=start_date,
                end_date=end_date,
                progress_callback=progress_callback
            )
            
            progress_bar.empty()
            
            if result.success:
                st.success("✅ Download completed!")
                st.write(f"**Downloaded:** {result.total_records:,} records")
                st.write(f"**Size:** {result.total_size_mb:.2f} MB")
            else:
                st.error(f"❌ Download failed: {result.error}")

def render_data_validation(data_service: DataService):
    """Adatok validálása."""
    st.header("🔍 Data Validation")
    
    selected_symbol = st.selectbox(
        "Select Symbol",
        options=data_service.get_available_symbols()
    )
    
    if selected_symbol:
        # Validáció futtatása
        if st.button("🔍 Run Validation", type="secondary"):
            with st.spinner("Validating data..."):
                validation_result = data_service.validate_symbol_data(selected_symbol)
            
            # Eredmények megjelenítése
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total Records",
                    f"{validation_result.total_records:,}",
                    delta=f"{validation_result.duplicates} duplicates"
                )
            
            with col2:
                st.metric(
                    "Date Range",
                    validation_result.date_range,
                    delta=f"{validation_result.missing_days} gaps"
                )
            
            with col3:
                st.metric(
                    "Data Quality",
                    f"{validation_result.quality_score:.1f}%",
                    delta=f"{validation_result.outliers} outliers"
                )
            
            with col4:
                status_color = "🟢" if validation_result.is_valid else "🔴"
                st.metric("Status", status_color)
            
            # Hibák listázása
            if validation_result.errors:
                st.subheader("⚠️ Validation Errors")
                for error in validation_result.errors:
                    st.error(f"**{error.type}:** {error.message}")

def main():
    """Fő oldal logika."""
    st.title("📥 Data Hub")
    
    # Service-ek inicializálása
    data_service = DataService()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "🎛️ Collectors",
        "📥 Historical Download",
        "🔍 Validation"
    ])
    
    with tab1:
        render_collector_control(data_service)
    
    with tab2:
        render_historical_download(data_service)
    
    with tab3:
        render_data_validation(data_service)

if __name__ == "__main__":
    main()
```

### 4. 🧠 AI Lab (04_🧠_AI_Lab.py)

#### Funkciók
- Modellek betanítása és kezelése
- TensorBoard integráció
- Teljesítmény metrikák
- Hyperparameter tuning

#### Implementáció Vázlat

```python
# ui/pages/04_🧠_AI_Lab.py
import streamlit as st
import plotly.graph_objects as go
from typing import TYPE_CHECKING
from ui.services.analytics_service import AnalyticsService

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import ILogger

# Page Config
st.set_page_config(
    page_title="Neural AI - AI Lab",
    page_icon="🧠",
    layout="wide"
)

def render_model_training(analytics_service: AnalyticsService):
    """Modell tanítási felület."""
    st.header("🏋️ Model Training")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Tanítási konfiguráció
        st.subheader("Configuration")
        
        model_type = st.selectbox(
            "Model Type",
            options=["LSTM", "GRU", "Transformer", "CNN-LSTM"]
        )
        
        epochs = st.slider("Epochs", 10, 500, 100)
        batch_size = st.selectbox("Batch Size", [16, 32, 64, 128], index=1)
        
        learning_rate = st.number_input(
            "Learning Rate",
            min_value=0.0001,
            max_value=0.01,
            value=0.001,
            format="%.4f"
        )
        
        # Adatkészlet kiválasztása
        dataset = st.selectbox(
            "Dataset",
            options=analytics_service.get_available_datasets()
        )
        
        # Tanítás indítása
        if st.button("🚀 Start Training", type="primary"):
            training_config = {
                "model_type": model_type,
                "epochs": epochs,
                "batch_size": batch_size,
                "learning_rate": learning_rate,
                "dataset": dataset
            }
            
            with st.spinner("Training in progress..."):
                result = analytics_service.start_training(training_config)
                
                if result.success:
                    st.success("✅ Training started!")
                    st.session_state.training_id = result.training_id
                else:
                    st.error(f"❌ Error: {result.error}")
    
    with col2:
        # TensorBoard integráció
        st.subheader("📊 TensorBoard")
        st.write("Training metrics visualization")
        
        # TensorBoard iframe
        tensorboard_url = "http://localhost:6006"
        st.components.v1.iframe(
            src=tensorboard_url,
            height=600,
            scrolling=True
        )

def render_model_performance(analytics_service: AnalyticsService):
    """Modell teljesítmény elemzés."""
    st.header("📈 Model Performance")
    
    # Elérhető modellek
    models = analytics_service.get_trained_models()
    
    if not models:
        st.info("No trained models available. Train a model first!")
        return
    
    selected_model = st.selectbox(
        "Select Model",
        options=[m.name for m in models]
    )
    
    if selected_model:
        # Teljesítmény metrikák
        metrics = analytics_service.get_model_metrics(selected_model)
        
        # Metrikák megjelenítése
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Accuracy", f"{metrics.accuracy:.2%}")
        
        with col2:
            st.metric("Precision", f"{metrics.precision:.2%}")
        
        with col3:
            st.metric("Recall", f"{metrics.recall:.2%}")
        
        with col4:
            st.metric("F1 Score", f"{metrics.f1_score:.2%}")
        
        # Confusion Matrix
        st.subheader("Confusion Matrix")
        cm_fig = analytics_service.plot_confusion_matrix(selected_model)
        st.plotly_chart(cm_fig, use_container_width=True)
        
        # Loss Curve
        st.subheader("Training History")
        loss_fig = analytics_service.plot_training_history(selected_model)
        st.plotly_chart(loss_fig, use_container_width=True)

def main():
    """Fő oldal logika."""
    st.title("🧠 AI Lab")
    
    # Service-ek inicializálása
    analytics_service = AnalyticsService()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "🏋️ Training",
        "📈 Performance",
        "🔬 Analysis"
    ])
    
    with tab1:
        render_model_training(analytics_service)
    
    with tab2:
        render_model_performance(analytics_service)
    
    with tab3:
        st.header("🔬 Model Analysis")
        st.write("Detailed model analysis tools will be implemented here...")

if __name__ == "__main__":
    main()
```

### 5. 🪲 Strategy Lab (05_🪲_Strategy_Lab.py)

#### Funkciók
- Stratégia backtesting
- Jelzés generálás tesztelése
- Teljesítmény analízis
- Stratégia optimalizálás

#### Implementáció Vázlat

```python
# ui/pages/05_🪲_Strategy_Lab.py
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import TYPE_CHECKING
from ui.services.strategy_service import StrategyService

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import ILogger

# Page Config
st.set_page_config(
    page_title="Neural AI - Strategy Lab",
    page_icon="🪲",
    layout="wide"
)

def render_backtest_config(strategy_service: StrategyService):
    """Backtest konfiguráció."""
    st.header("🧪 Backtest Configuration")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Alap konfiguráció
        st.subheader("Test Parameters")
        
        strategy_name = st.text_input("Strategy Name", "MyStrategy")
        
        symbols = st.multiselect(
            "Symbols",
            options=["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"],
            default=["EURUSD"]
        )
        
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=90)
        )
        
        end_date = st.date_input("End Date", value=datetime.now())
        
        initial_balance = st.number_input(
            "Initial Balance (USD)",
            min_value=1000,
            max_value=1000000,
            value=10000
        )
    
    with col2:
        # Stratégia paraméterek
        st.subheader("Strategy Parameters")
        
        risk_per_trade = st.slider(
            "Risk per Trade (%)",
            min_value=0.1,
            max_value=5.0,
            value=1.0,
            step=0.1
        )
        
        stop_loss_pips = st.number_input(
            "Stop Loss (pips)",
            min_value=5,
            max_value=100,
            value=20
        )
        
        take_profit_pips = st.number_input(
            "Take Profit (pips)",
            min_value=5,
            max_value=200,
            value=40
        )
        
        # Backtest indítása
        if st.button("🚀 Run Backtest", type="primary"):
            config = {
                "strategy_name": strategy_name,
                "symbols": symbols,
                "start_date": start_date,
                "end_date": end_date,
                "initial_balance": initial_balance,
                "risk_per_trade": risk_per_trade,
                "stop_loss_pips": stop_loss_pips,
                "take_profit_pips": take_profit_pips
            }
            
            with st.spinner("Running backtest..."):
                result = strategy_service.run_backtest(config)
                
                if result.success:
                    st.session_state.backtest_result = result
                    st.success("✅ Backtest completed!")
                else:
                    st.error(f"❌ Error: {result.error}")

def render_backtest_results(strategy_service: StrategyService):
    """Backtest eredmények."""
    st.header("📊 Backtest Results")
    
    if "backtest_result" not in st.session_state:
        st.info("Run a backtest to see results here!")
        return
    
    result = st.session_state.backtest_result
    
    # Fő metrikák
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Final Balance",
            f"${result.final_balance:,.2f}",
            delta=f"{result.total_return:.2%}"
        )
    
    with col2:
        st.metric(
            "Total Trades",
            result.total_trades,
            delta=f"Win Rate: {result.win_rate:.1%}"
        )
    
    with col3:
        st.metric(
            "Max Drawdown",
            f"{result.max_drawdown:.2%}",
            delta=f"${result.max_drawdown_usd:,.2f}"
        )
    
    with col4:
        st.metric(
            "Sharpe Ratio",
            f"{result.sharpe_ratio:.2f}",
            delta=f"Profit Factor: {result.profit_factor:.2f}"
        )
    
    # Equity Curve
    st.subheader("📈 Equity Curve")
    equity_fig = strategy_service.plot_equity_curve(result)
    st.plotly_chart(equity_fig, use_container_width=True)
    
    # Trades táblázat
    st.subheader("📋 Trade History")
    st.dataframe(
        result.trades_df,
        use_container_width=True,
        height=400
    )

def main():
    """Fő oldal logika."""
    st.title("🪲 Strategy Lab")
    
    # Service-ek inicializálása
    strategy_service = StrategyService()
    
    # Tabs
    tab1, tab2 = st.tabs([
        "🧪 Backtest",
        "📊 Results"
    ])
    
    with tab1:
        render_backtest_config(strategy_service)
    
    with tab2:
        render_backtest_results(strategy_service)

if __name__ == "__main__":
    main()
```

### 6. ⚡ Live Ops (06_⚡_Live_Ops.py)

#### Funkciók
- Valós idejű kereskedés monitorozás
- Aktív pozíciók kezelése
- PnL nyomon követés
- Riasztások és értesítések

#### Implementáció Vázlat

```python
# ui/pages/06_⚡_Live_Ops.py
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from typing import TYPE_CHECKING
from ui.services.live_trading_service import LiveTradingService

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import ILogger

# Page Config
st.set_page_config(
    page_title="Neural AI - Live Ops",
    page_icon="⚡",
    layout="wide"
)

def render_live_dashboard(live_service: LiveTradingService):
    """Valós idejű vezérlőpult."""
    st.header("📊 Live Trading Dashboard")
    
    # Valós idejű adatok frissítése
    live_data = live_service.get_live_data()
    
    # Fő metrikák
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Live PnL",
            f"${live_data.current_pnl:+,.2f}",
            delta=f"{live_data.pnl_percentage:+.2%}"
        )
    
    with col2:
        st.metric(
            "Active Positions",
            live_data.active_positions,
            delta=f"Max: {live_data.max_positions}"
        )
    
    with col3:
        st.metric(
            "Today's Trades",
            live_data.todays_trades,
            delta=f"Win Rate: {live_data.today_win_rate:.1%}"
        )
    
    with col4:
        status_color = "🟢" if live_data.system_health == "OK" else "🔴"
        st.metric("System Health", f"{status_color} {live_data.system_health}")
    
    # Valós idejű PnL chart
    st.subheader("📈 Real-time PnL")
    pnl_fig = live_service.get_live_pnl_chart()
    st.plotly_chart(pnl_fig, use_container_width=True, config={'displayModeBar': False})

def render_active_positions(live_service: LiveTradingService):
    """Aktív pozíciók kezelése."""
    st.header("💰 Active Positions")
    
    positions = live_service.get_active_positions()
    
    if not positions:
        st.info("No active positions")
        return
    
    for position in positions:
        with st.expander(
            f"{position.symbol} - {position.direction} - ${position.current_pnl:+,.2f}",
            expanded=True
        ):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.write(f"**Entry Price:** {position.entry_price:.5f}")
                st.write(f"**Current Price:** {position.current_price:.5f}")
            
            with col2:
                st.write(f"**Size:** {position.size}")
                st.write(f"**Leverage:** {position.leverage}:1")
            
            with col3:
                st.write(f"**Stop Loss:** {position.stop_loss:.5f}")
                st.write(f"**Take Profit:** {position.take_profit:.5f}")
            
            with col4:
                pnl_color = "profit" if position.current_pnl >= 0 else "loss"
                st.write(f"**PnL:** :{pnl_color}[${position.current_pnl:+,.2f}]")
                
                if st.button("📊 Close Position", key=f"close_{position.id}"):
                    result = live_service.close_position(position.id)
                    if result.success:
                        st.success("Position closed")
                    else:
                        st.error(result.error)

def render_market_overview(live_service: LiveTradingService):
    """Piaci áttekintés."""
    st.header("🌍 Market Overview")
    
    market_data = live_service.get_market_overview()
    
    # Piaci adatok táblázatban
    st.dataframe(
        market_data,
        use_container_width=True,
        column_config={
            "symbol": "Symbol",
            "bid": st.column_config.NumberColumn("Bid", format="%.5f"),
            "ask": st.column_config.NumberColumn("Ask", format="%.5f"),
            "spread": st.column_config.NumberColumn("Spread", format="%.1f"),
            "change": st.column_config.NumberColumn("Change", format="%.2%"),
            "volume": st.column_config.NumberColumn("Volume", format="%d")
        }
    )

def main():
    """Fő oldal logika."""
    st.title("⚡ Live Operations")
    
    # Service-ek inicializálása
    live_service = LiveTradingService()
    
    # Auto-refresh
    if st.checkbox("🔄 Auto-refresh (5s)", value=True):
        st.rerun()
    
    # Oldal tartalom
    render_live_dashboard(live_service)
    render_active_positions(live_service)
    render_market_overview(live_service)

if __name__ == "__main__":
    main()
```

---

## 🔄 Valós Idejű Kommunikáció (Streamlit)

### Session State Management

```python
# ui/services/base_service.py
import streamlit as st
from typing import Any, Dict, Optional
from neural_ai.core.base.interfaces.component_interface import IComponent

class BaseService(IComponent):
    """Alap service osztály minden ViewModel rétegbeli komponenshez."""
    
    def __init__(self, logger, config):
        """Inicializálás Dependency Injectionnel."""
        self.logger = logger
        self.config = config
        self._init_session_state()
    
    def _init_session_state(self):
        """Session state inicializálása."""
        if 'services' not in st.session_state:
            st.session_state.services = {}
    
    def get_session_data(self, key: str, default: Any = None) -> Any:
        """Adatok lekérése a session state-ből."""
        full_key = f"{self.__class__.__name__}.{key}"
        return st.session_state.services.get(full_key, default)
    
    def set_session_data(self, key: str, value: Any):
        """Adatok mentése a session state-be."""
        full_key = f"{self.__class__.__name__}.{key}"
        st.session_state.services[full_key] = value
    
    def clear_session_data(self, key: str):
        """Adatok törlése a session state-ből."""
        full_key = f"{self.__class__.__name__}.{key}"
        if full_key in st.session_state.services:
            del st.session_state.services[full_key]
```

### Service Layer Implementáció

```python
# ui/services/dashboard_service.py
from typing import Dict, Any, List
import plotly.express as px
from datetime import datetime, timedelta
from .base_service import BaseService

class DashboardService(BaseService):
    """Vezérlőpult service - ViewModel réteg."""
    
    def get_system_health(self) -> Dict[str, Any]:
        """Rendszer állapotának lekérése."""
        try:
            # Core bridge használata
            health_monitor = self._get_health_monitor()
            health_data = health_monitor.check_health()
            
            return {
                "cuda_status": "Available" if health_data.cuda_available else "Disabled",
                "cuda_available": health_data.cuda_available,
                "database_status": health_data.database.status,
                "database_tables": health_data.database.table_count,
                "config_status": health_data.config.status,
                "config_entries": health_data.config.entry_count,
                "active_collectors": health_data.collectors.active_count,
                "total_collectors": health_data.collectors.total_count
            }
        except Exception as e:
            self.logger.error(f"Error getting system health: {e}")
            return {
                "cuda_status": "Error",
                "cuda_available": False,
                "database_status": "Error",
                "database_tables": 0,
                "config_status": "Error",
                "config_entries": 0,
                "active_collectors": 0,
                "total_collectors": 0
            }
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Adatok összegzésének lekérése."""
        try:
            # Data bridge használata
            data_bridge = self._get_data_bridge()
            summary = data_bridge.get_data_summary()
            
            # DataFrame készítése a szimbólumokról
            import pandas as pd
            symbols_df = pd.DataFrame([
                {
                    "Symbol": s.name,
                    "Records": s.record_count,
                    "Start Date": s.start_date,
                    "End Date": s.end_date,
                    "Size (MB)": s.size_mb
                }
                for s in summary.symbols
            ])
            
            return {
                "total_records": summary.total_records,
                "total_size_mb": summary.total_size_mb,
                "symbols_count": summary.symbol_count,
                "symbols_df": symbols_df
            }
        except Exception as e:
            self.logger.error(f"Error getting data summary: {e}")
            import pandas as pd
            return {
                "total_records": 0,
                "total_size_mb": 0.0,
                "symbols_count": 0,
                "symbols_df": pd.DataFrame()
            }
    
    def create_data_volume_chart(self, data_info: Dict[str, Any]) -> Any:
        """Adatmennyiség chart létrehozása."""
        if data_info['symbols_df'].empty:
            return px.bar(title="No Data Available")
        
        fig = px.bar(
            data_info['symbols_df'],
            x='Symbol',
            y='Records',
            title='Data Volume by Symbol',
            labels={'Records': 'Number of Records', 'Symbol': 'Symbol'},
            color='Records',
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            height=400,
            showlegend=False
        )
        
        return fig
    
    def _get_health_monitor(self):
        """Health monitor lekérése a Core-ból."""
        from ui.bridges.core_bridge import CoreBridge
        return CoreBridge.get_health_monitor()
    
    def _get_data_bridge(self):
        """Data bridge lekérése."""
        from ui.bridges.data_bridge import DataBridge
        return DataBridge(logger=self.logger, config=self.config)
```

### Bridge Layer Implementáció

```python
# ui/bridges/core_bridge.py
from typing import TYPE_CHECKING
from neural_ai.core.base.factory import ComponentFactory

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import ILogger
    from neural_ai.core.config.interfaces.config_interface import IConfigManager
    from neural_ai.core.system.interfaces.health_interface import IHealthMonitor

class CoreBridge:
    """Bridge a Core backendhez - Dependency Injection támogatással."""
    
    def __init__(self, logger: ILogger, config: IConfigManager):
        """Inicializálás DI-vel."""
        self.logger = logger
        self.config = config
        self._component_factory = ComponentFactory()
    
    @staticmethod
    def get_logger_factory():
        """Logger factory lekérése."""
        from neural_ai.core.logger.factory import LoggerFactory
        return LoggerFactory()
    
    @staticmethod
    def get_config_factory():
        """Config factory lekérése."""
        from neural_ai.core.config.factory import ConfigFactory
        return ConfigFactory()
    
    def get_health_monitor(self) -> IHealthMonitor:
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
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_system_version(self) -> str:
        """Rendszer verzió lekérése."""
        return self.config.get("system.version", "1.0.0")
    
    def get_python_version(self) -> str:
        """Python verzió lekérése."""
        import sys
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    def get_torch_version(self) -> str:
        """PyTorch verzió lekérése."""
        try:
            import torch
            return torch.__version__
        except ImportError:
            return "Not installed"
```

---

## 🎨 Design System (Streamlit)

### Theme Konfiguráció

```python
# ui/theme.py
"""
Streamlit theme konfiguráció a Neural AI Next-hez.
"""

import streamlit as st

# Custom CSS
def inject_custom_css():
    """Egyedi CSS injektálása."""
    st.markdown(
        """
        <style>
        /* Fő stílusok */
        .main {
            background-color: #0f172a;
            color: #f8fafc;
        }
        
        /* Trading színek */
        .profit {
            color: #10b981;
        }
        
        .loss {
            color: #ef4444;
        }
        
        .neutral {
            color: #6b7280;
        }
        
        /* Gombok */
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
        }
        
        .stButton>button.kind-primary {
            background-color: #3b82f6;
            border-color: #3b82f6;
        }
        
        /* Card stílusok */
        .card {
            background-color: #1e293b;
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #334155;
        }
        
        /* Metrikák */
        .metric-card {
            background-color: #1e293b;
            border-radius: 8px;
            padding: 1rem;
            border: 1px solid #334155;
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
    "loss": "#ef4444",
    "neutral": "#6b7280"
}
```

### Komponens Library

```python
# ui/components/__init__.py
"""
Egyedi Streamlit komponensek a Neural AI Next-hez.
"""

from .cards import MetricCard, InfoCard, WarningCard
from .charts import PnLChart, EquityCurveChart, VolumeChart
from .tables import DataTable, LogTable, TradeTable

__all__ = [
    'MetricCard',
    'InfoCard',
    'WarningCard',
    'PnLChart',
    'EquityCurveChart',
    'VolumeChart',
    'DataTable',
    'LogTable',
    'TradeTable'
]
```

```python
# ui/components/cards.py
import streamlit as st
from typing import Optional

def MetricCard(title: str, value: str, delta: Optional[str] = None, delta_color: str = "normal"):
    """Metrika kártya komponens."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(title)
        st.metric("", value, delta=delta, delta_color=delta_color)
    
    with col2:
        st.write("")  # Placeholder for icon

def InfoCard(title: str, content: str, icon: str = "ℹ️"):
    """Információs kártya."""
    with st.container():
        st.markdown(f"**{icon} {title}**")
        st.write(content)
        st.markdown("---")

def WarningCard(title: str, content: str, icon: str = "⚠️"):
    """Figyelmeztető kártya."""
    with st.container():
        st.markdown(f"**:warning[{icon} {title}]**")
        st.warning(content)
```

---

## 🔐 Biztonság (Streamlit)

### Authentication & Session Management

```python
# ui/auth.py
"""
Authentikáció és session management a Streamlit UI-hoz.
"""

import streamlit as st
import hashlib
import secrets
from typing import Optional, Dict
from datetime import datetime, timedelta

class AuthManager:
    """Authentikáció kezelő."""
    
    def __init__(self):
        """Inicializálás."""
        self.session_timeout = timedelta(hours=8)
    
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
        """Bejelentkezési oldal megjelenítése."""
        st.title("🔐 Neural AI Next - Login")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            submitted = st.form_submit_button("Login", type="primary")
            
            if submitted:
                if self._validate_credentials(username, password):
                    st.session_state.authenticated = True
                    st.session_state.auth_time = datetime.now()
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid credentials")
    
    def logout(self):
        """Kijelentkezés."""
        for key in ['authenticated', 'auth_time', 'username']:
            if key in st.session_state:
                del st.session_state[key]
    
    def _validate_credentials(self, username: str, password: str) -> bool:
        """Hitelesítő adatok validálása."""
        # Jelszó hash-elés
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Egyszerű validáció (éles környezetben adatbázisból kell ellenőrizni)
        valid_users = {
            "admin": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"  # "password"
        }
        
        return username in valid_users and valid_users[username] == password_hash

# Globális auth manager
auth_manager = AuthManager()
```

### Biztonságos Oldal Dekorátor

```python
# ui/decorators.py
"""
Dekorátorok a biztonságos oldalakhoz.
"""

import streamlit as st
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
```

### Biztonságos Oldal Használata

```python
# ui/pages/01_🚀_Launchpad.py (módosított)
import streamlit as st
from ui.decorators import require_auth
from ui.auth import auth_manager

# ... (előző kód)

@require_auth
def main():
    """Fő oldal logika - authentikációval védve."""
    # Logout gomb a sidebar-ban
    with st.sidebar:
        if st.button("🚪 Logout"):
            auth_manager.logout()
            st.rerun()
    
    # ... (további kód)

# ...
```

---

## 📊 Chart Komponensek (Plotly)

### Plotly Integráció

```python
# ui/components/charts.py
"""
Plotly chart komponensek a Neural AI Next-hez.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any
import pandas as pd

class PnLChart:
    """Profit/Loss chart komponens."""
    
    def __init__(self, data: List[Dict[str, Any]]):
        """Inicializálás."""
        self.data = pd.DataFrame(data)
    
    def create_chart(self) -> go.Figure:
        """Chart létrehozása."""
        if self.data.empty:
            return self._create_empty_chart()
        
        fig = go.Figure()
        
        # PnL vonal
        fig.add_trace(go.Scatter(
            x=self.data['timestamp'],
            y=self.data['pnl_cumulative'],
            mode='lines',
            name='Cumulative PnL',
            line=dict(color='#10b981', width=2)
        ))
        
        # Zero line
        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color="white",
            opacity=0.5
        )
        
        fig.update_layout(
            title="Cumulative Profit & Loss",
            xaxis_title="Time",
            yaxis_title="PnL (USD)",
            template="plotly_dark",
            hovermode='x unified',
            height=400
        )
        
        return fig
    
    def _create_empty_chart(self) -> go.Figure:
        """Üres chart létrehozása."""
        fig = go.Figure()
        fig.update_layout(
            title="No Data Available",
            template="plotly_dark",
            height=400
        )
        return fig

class EquityCurveChart:
    """Equity curve chart."""
    
    def __init__(self, data: List[Dict[str, Any]]):
        """Inicializálás."""
        self.data = pd.DataFrame(data)
    
    def create_chart(self) -> go.Figure:
        """Chart létrehozása."""
        if self.data.empty:
            return self._create_empty_chart()
        
        fig = go.Figure()
        
        # Equity curve
        fig.add_trace(go.Scatter(
            x=self.data['date'],
            y=self.data['equity'],
            mode='lines',
            name='Equity',
            line=dict(color='#3b82f6', width=2),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.2)'
        ))
        
        # Drawdown areas
        fig.add_trace(go.Scatter(
            x=self.data['date'],
            y=self.data['drawdown'],
            mode='lines',
            name='Drawdown',
            line=dict(color='#ef4444', width=1),
            fill='tozeroy',
            fillcolor='rgba(239, 68, 68, 0.2)'
        ))
        
        fig.update_layout(
            title="Equity Curve & Drawdown",
            xaxis_title="Date",
            yaxis_title="Value (USD)",
            template="plotly_dark",
            height=400
        )
        
        return fig
    
    def _create_empty_chart(self) -> go.Figure:
        """Üres chart létrehozása."""
        return PnLChart([])._create_empty_chart()
```

---

## 🔧 Fejlesztői Eszközök

### Hot Reload Konfiguráció

```python
# .streamlit/config.toml
[server]
port = 8501
address = "0.0.0.0"
headless = true

[client]
showErrorDetails = true

[runner]
magicEnabled = false

[server.fileWatcherType]
# Watchdog használata fejlettebb file watching-hez
type = "watchdog"
```

### Development Script

```bash
#!/bin/bash
# scripts/run_ui_dev.sh

#!/bin/bash

# Neural AI Next - UI Development Script

# Environment activation
source /home/elynea/miniconda3/bin/activate neural-ai-next

# Port setting
PORT=${1:-8501}

echo "🚀 Starting Neural AI Next UI on port $PORT..."

# Run Streamlit with hot reload
/home/elynea/miniconda3/envs/neural-ai-next/bin/streamlit run \
    ui/main.py \
    --server.port $PORT \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.fileWatcherType watchdog \
    --logger.level debug
```

### Tesztelési Stratégia

```python
# tests/test_ui_services.py
"""
UI service-ek tesztelése.
"""

import pytest
from unittest.mock import Mock, patch
from ui.services.dashboard_service import DashboardService

class TestDashboardService:
    """DashboardService tesztelése."""
    
    @pytest.fixture
    def mock_logger(self):
        """Mock logger."""
        return Mock()
    
    @pytest.fixture
    def mock_config(self):
        """Mock config."""
        return Mock()
    
    @pytest.fixture
    def dashboard_service(self, mock_logger, mock_config):
        """DashboardService példány."""
        return DashboardService(logger=mock_logger, config=mock_config)
    
    def test_get_system_health_success(self, dashboard_service, mock_logger):
        """Rendszer állapotának sikeres lekérése."""
        # Mock health monitor
        mock_health_monitor = Mock()
        mock_health_data = Mock()
        mock_health_data.cuda_available = True
        mock_health_data.database.status = "OK"
        mock_health_data.database.table_count = 10
        mock_health_data.config.status = "Loaded"
        mock_health_data.config.entry_count = 50
        mock_health_data.collectors.active_count = 3
        mock_health_data.collectors.total_count = 5
        mock_health_monitor.check_health.return_value = mock_health_data
        
        with patch.object(dashboard_service, '_get_health_monitor', return_value=mock_health_monitor):
            result = dashboard_service.get_system_health()
            
            assert result['cuda_status'] == 'Available'
            assert result['cuda_available'] is True
            assert result['database_status'] == 'OK'
            assert result['database_tables'] == 10
            assert result['config_status'] == 'Loaded'
            assert result['config_entries'] == 50
            assert result['active_collectors'] == 3
            assert result['total_collectors'] == 5
    
    def test_get_system_health_error(self, dashboard_service, mock_logger):
        """Rendszer állapotának lekérése hibával."""
        with patch.object(dashboard_service, '_get_health_monitor', side_effect=Exception("Test error")):
            result = dashboard_service.get_system_health()
            
            assert result['cuda_status'] == 'Error'
            assert result['database_status'] == 'Error'
            mock_logger.error.assert_called_once()
    
    def test_create_data_volume_chart(self, dashboard_service):
        """Adatmennyiség chart létrehozása."""
        import pandas as pd
        
        data_info = {
            'symbols_df': pd.DataFrame({
                'Symbol': ['EURUSD', 'GBPUSD'],
                'Records': [1000, 2000]
            })
        }
        
        chart = dashboard_service.create_data_volume_chart(data_info)
        
        assert chart is not None
        assert chart.layout.height == 400
    
    def test_create_data_volume_chart_empty(self, dashboard_service):
        """Adatmennyiség chart létrehozása üres adatokkal."""
        import pandas as pd
        
        data_info = {
            'symbols_df': pd.DataFrame()
        }
        
        chart = dashboard_service.create_data_volume_chart(data_info)
        
        assert chart is not None
```

---

## 📱 Reszponzív Design

### Layout Komponensek

```python
# ui/layouts.py
"""
Reszponzív layout komponensek.
"""

import streamlit as st
from typing import List, Any

def create_responsive_grid(items: List[Any], columns: int = 3):
    """Reszponzív grid létrehozása."""
    cols = st.columns(columns)
    
    for index, item in enumerate(items):
        with cols[index % columns]:
            if callable(item):
                item()
            else:
                st.write(item)

def create_dashboard_layout():
    """Dashboard layout létrehozása."""
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        # Navigation items
    
    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Main dashboard content
        pass
    
    with col2:
        # Side panel
        pass
```

---

## 📋 Következő Lépések

1. **UI Projekt Struktúra Létrehozása:**
   ```bash
   mkdir -p ui/{pages,services,bridges,components,layouts}
   touch ui/__init__.py ui/main.py
   ```

2. **Service Layer Fejlesztése:**
   - DashboardService implementálása
   - ConfigService implementálása
   - DataService implementálása
   - AnalyticsService implementálása
   - StrategyService implementálása
   - LiveTradingService implementálása

3. **Bridge Layer Fejlesztése:**
   - CoreBridge implementálása
   - DataBridge implementálása
   - ConfigBridge implementálása

4. **Streamlit Oldalak Fejlesztése:**
   - 01_🚀_Launchpad.py
   - 02_🛠️_Dev_Center.py
   - 03_📥_Data_Hub.py
   - 04_🧠_AI_Lab.py
   - 05_🪲_Strategy_Lab.py
   - 06_⚡_Live_Ops.py

5. **Komponens Library Fejlesztése:**
   - Chart komponensek (Plotly)
   - Card komponensek
   - Table komponensek
   - Form komponensek

6. **Authentikáció Implementálása:**
   - AuthManager fejlesztése
   - Session management
   - Biztonságos oldalak

7. **Tesztelés:**
   - Unit tesztek a service-ekhez
   - Integration tesztek
   - E2E tesztek

8. **Dokumentáció:**
   - Mirror dokumentáció frissítése
   - API dokumentáció
   - Felhasználói útmutató

---

## 🔗 Kapcsolódó Dokumentumok

- [Rendszerarchitektúra](01_system_architecture.md)
- [Dinamikus Konfiguráció](02_dynamic_configuration.md)
- [Megfigyelhetőség](03_observability_logging.md)
- [Adattárház](04_data_warehouse.md)
- [Collector Stratégiák](05_collectors_strategy.md)
- [Fejlesztési Útmutató](docs/development/unified_development_guide.md)
- [UI Architektúra Szabványok](docs/components/ui/architecture.md)