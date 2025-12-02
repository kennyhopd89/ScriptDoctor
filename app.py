import streamlit as st
import utils
import os
import time
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

# Helper function for auto-save
def auto_save():
    """Auto-save to both local storage and database (if enabled)"""
    # Save to local storage
    utils.save_session_state(st.session_state)
    
    # Save to database if enabled
    try:
        import database
        if database.is_supabase_enabled() and st.session_state.get('current_project_id'):
            database.save_current_project()
    except Exception as e:
        print(f"Database auto-save error: {e}")

# Custom CSS for professional screenplay look with Glassmorphism
def load_custom_css():
    """Load advanced CSS theme matching t.html reference design."""
    st.markdown("""
    <style>
    /* Import modern fonts - Using system fonts + Courier Prime */
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap');
    
    /* 1. DEFINE DESIGN SYSTEM VARIABLES */
    :root {
        /* Brand Colors (Primary: Cyan) */
        --color-primary: #00B8D4;
        --color-primary-dark: #008BA3;
        --color-primary-light: #62EFFF;
        
        /* Semantic Colors */
        --color-success: #00C853; /* Green */
        --color-warning: #FF9800; /* Orange */
        --color-error: #F44336; /* Red */
        --color-info: #2196F3; /* Blue */
        
        /* Neutrals */
        --color-gray-900: #0A0E1A; /* Background */
        --color-gray-800: #1A1F2E; /* Cards, sidebar */
        --color-gray-700: #2D3748; /* Borders, Disabled Bg */
        --color-gray-600: #4A5568; /* Disabled Text */
        --color-gray-500: #718096; /* Muted text */
        --color-gray-400: #A0AEC0; /* Secondary Text */
        --color-text-primary: #FFFFFF;
        
        /* Spacing & Radius */
        --space-xs: 4px;
        --space-sm: 8px;
        --space-md: 16px;
        --space-lg: 24px;
        --space-xl: 32px;
        --radius-sm: 4px;
        --radius-md: 6px;
        --radius-lg: 8px;
    }
    
    /* 2. BASE LAYOUT & BACKGROUND */
    .stApp {
        background: var(--color-gray-900);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: var(--color-text-primary);
        line-height: 1.6;
    }
    
    /* Sidebar styling - Match t.html */
    [data-testid="stSidebar"] {
        background: var(--color-gray-800) !important;
        border-right: 1px solid var(--color-gray-700) !important;
        padding: 24px 16px !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 0 !important;
    }
    
    /* Card styling - Match t.html */
    .glass-card, .card {
        background: var(--color-gray-800);
        border: 1px solid var(--color-gray-700);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
        margin-bottom: var(--space-lg);
        transition: all 0.2s;
    }
    
    .glass-card:hover, .card:hover {
        border-color: var(--color-gray-600);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: var(--space-md);
    }
    
    .card-title {
        font-size: 18px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: var(--space-sm);
    }
    
    .card-content {
        color: var(--color-gray-400);
        font-size: 14px;
        line-height: 1.6;
    }
    
    .card-collapsed .card-content {
        display: none;
    }
    
    .card-expanded .card-content {
        display: block;
    }
    
    /* Script container for screenplay text */
    .script-container {
        font-family: 'Courier Prime', 'Courier New', monospace;
        font-size: 14px;
        line-height: 1.7; /* Relaxed line-height for readability */
        padding: var(--space-lg);
        background: var(--color-gray-900);
        border: 1px solid var(--color-gray-700);
        color: var(--color-gray-100);
        white-space: pre-wrap;
        border-radius: var(--radius-lg);
        margin: var(--space-md) 0;
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* Text areas - Editor styling */
    .stTextArea textarea {
        font-family: 'Courier Prime', 'Courier New', monospace !important;
        font-size: 16px !important;
        line-height: 1.7 !important; /* Screenplay standard */
        background: var(--color-gray-900) !important;
        border: 1px solid var(--color-gray-700) !important;
        border-radius: var(--radius-lg) !important;
        color: var(--color-text-primary) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--color-primary) !important;
        box-shadow: 0 0 0 1px var(--color-primary-dark) !important;
    }
    
    /* 3. BUTTON STYLING - Match t.html */
    .stButton button {
        border-radius: var(--radius-md) !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
        font-size: 14px !important;
    }
    
    /* Primary Button */
    .stButton button[kind="primary"] {
        background: var(--color-primary) !important;
        color: white !important;
        border: none !important;
    }
    .stButton button[kind="primary"]:hover {
        background: var(--color-primary-dark) !important;
    }
    
    /* Secondary Button */
    .stButton button[kind="secondary"], 
    .stButton button:not([kind="primary"]) {
        background: transparent !important;
        color: var(--color-gray-400) !important;
        border: 1px solid var(--color-gray-600) !important;
    }
    .stButton button[kind="secondary"]:hover,
    .stButton button:not([kind="primary"]):hover {
        background: var(--color-gray-700) !important;
        color: var(--color-text-primary) !important;
    }
    
    /* Small buttons */
    .btn-small {
        padding: 6px 12px !important;
        font-size: 13px !important;
    }
    
    /* 4. TABS STYLING - Match t.html */
    .stTabs [data-baseweb="tab-list"] {
        gap: var(--space-xs);
        border-bottom: 1px solid var(--color-gray-700);
        background: var(--color-gray-800);
        padding: 0 var(--space-xl);
    }
    
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        color: var(--color-gray-500);
        padding: 12px 24px;
        border-bottom: 3px solid transparent;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--color-gray-400);
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: var(--color-primary) !important;
        border-bottom: 3px solid var(--color-primary) !important;
    }
    
    /* 5. HEADERS - Match t.html */
    h1, h2, h3 {
        font-weight: 700 !important;
        color: var(--color-text-primary) !important;
    }
    
    h1 {
        font-size: 24px !important;
        color: var(--color-primary) !important;
    }
    
    h2 {
        font-size: 20px !important;
    }
    
    h3 {
        font-size: 18px !important;
    }
    
    /* 6. ALERTS (Semantic Colors) */
    .stSuccess {
        background: rgba(0, 200, 83, 0.1) !important;
        border: 1px solid var(--color-success) !important;
        border-radius: var(--radius-lg) !important;
        color: var(--color-success) !important;
    }
    .stError {
        background: rgba(244, 67, 54, 0.1) !important;
        border: 1px solid var(--color-error) !important;
        border-radius: var(--radius-lg) !important;
        color: var(--color-error) !important;
    }
    .stInfo {
        background: rgba(33, 150, 243, 0.1) !important;
        border: 1px solid var(--color-info) !important;
        border-radius: var(--radius-lg) !important;
        color: var(--color-info) !important;
    }
    
    /* 7. EXPANDERS - Match t.html collapsible cards */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 16px;
        background: var(--color-gray-800) !important;
        border: 1px solid var(--color-gray-700) !important;
        border-radius: var(--radius-md) !important;
        color: var(--color-text-primary) !important;
        padding: 12px 16px !important;
    }
    .streamlit-expanderHeader:hover {
        background: var(--color-gray-700) !important;
        border-color: var(--color-gray-600) !important;
    }
    
    .streamlit-expanderContent {
        border: none !important;
        background: transparent !important;
    }
    
    /* 8. SCROLLBAR */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--color-gray-800);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--color-gray-600);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--color-primary-dark);
    }
    
    /* 9. PROGRESS BAR - Match t.html */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light)) !important;
    }
    
    .progress-section {
        background: var(--color-gray-800);
        border: 1px solid var(--color-gray-700);
        border-radius: var(--radius-lg);
        padding: 20px 24px;
        margin-bottom: var(--space-xl);
    }
    
    .progress-bar-container {
        height: 8px;
        background: var(--color-gray-700);
        border-radius: var(--radius-sm);
        overflow: hidden;
        margin: 12px 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light));
        transition: width 0.3s;
    }
    
    .progress-stats {
        display: flex;
        gap: var(--space-lg);
        margin-top: 12px;
        font-size: 14px;
    }
    
    .stat {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
    }
    
    .status-complete { color: var(--color-success); }
    .status-progress { color: var(--color-warning); }
    .status-pending { color: var(--color-gray-500); }
    
    /* 10. TASK LIST STYLING - Match t.html */
    .task-group {
        margin-bottom: var(--space-lg);
    }
    
    .task-group-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 16px;
        background: var(--color-gray-800);
        border-radius: var(--radius-md);
        cursor: pointer;
        margin-bottom: 12px;
        border: 1px solid var(--color-gray-700);
    }
    
    .task-group-title {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        font-size: 16px;
        font-weight: 600;
    }
    
    .task-item {
        background: var(--color-gray-800);
        border: 1px solid var(--color-gray-700);
        border-radius: var(--radius-md);
        padding: 16px;
        margin-bottom: var(--space-sm);
    }
    
    .task-header {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 12px;
    }
    
    .task-checkbox {
        width: 20px;
        height: 20px;
        margin-top: 2px;
        cursor: pointer;
    }
    
    .task-content {
        flex: 1;
    }
    
    .task-title {
        font-size: 15px;
        margin-bottom: 6px;
        color: var(--color-text-primary);
    }
    
    .task-scene {
        font-size: 13px;
        color: var(--color-gray-500);
        margin-bottom: 12px;
    }
    
    .task-actions {
        display: flex;
        gap: var(--space-sm);
        flex-wrap: wrap;
    }
    
    /* 11. SCENE NAVIGATOR - Match t.html */
    .scene-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .scene-item {
        padding: 12px;
        margin-bottom: var(--space-xs);
        border-radius: var(--radius-md);
        cursor: pointer;
        border-left: 3px solid transparent;
        transition: all 0.2s;
    }
    
    .scene-item:hover {
        background: var(--color-gray-900);
    }
    
    .scene-item.active {
        background: var(--color-gray-900);
        border-left-color: var(--color-primary);
    }
    
    .scene-number {
        font-size: 12px;
        color: var(--color-gray-500);
        margin-bottom: 4px;
    }
    
    .scene-location {
        font-size: 13px;
        color: var(--color-gray-400);
    }
    
    .scene-status {
        font-size: 11px;
        margin-top: 4px;
        display: flex;
        align-items: center;
        gap: var(--space-xs);
    }
    
    /* 12. SPLIT LAYOUT for Brainstorm - Match t.html */
    .split-container {
        display: flex;
        height: calc(100vh - 220px);
        gap: var(--space-md);
    }
    
    .editor-pane {
        flex: 0 0 68%;
        display: flex;
        flex-direction: column;
        background: var(--color-gray-800);
        border: 1px solid var(--color-gray-700);
        border-radius: var(--radius-lg);
        padding: 20px;
    }
    
    .ai-pane {
        flex: 1;
        display: flex;
        flex-direction: column;
        background: var(--color-gray-800);
        border: 1px solid var(--color-gray-700);
        border-radius: var(--radius-lg);
        padding: 20px;
        overflow-y: auto;
    }
    
    .editor-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: var(--space-md);
    }
    
    .editor-title {
        font-size: 16px;
        font-weight: 600;
    }
    
    .ai-suggestion {
        background: var(--color-gray-900);
        border: 1px solid var(--color-gray-700);
        border-radius: var(--radius-md);
        padding: 16px;
        margin-bottom: 12px;
    }
    
    .suggestion-header {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        margin-bottom: 12px;
        font-weight: 600;
        color: var(--color-primary);
    }
    
    .suggestion-content {
        color: var(--color-gray-400);
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 12px;
    }
    
    .suggestion-actions {
        display: flex;
        gap: var(--space-sm);
    }
    
    /* 13. SIDEBAR SECTIONS */
    .sidebar-section {
        margin-bottom: var(--space-xl);
    }
    
    .sidebar-title {
        font-size: 12px;
        font-weight: 700;
        color: var(--color-primary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: var(--space-md);
    }
    
    /* 14. Fix table layout in wide mode */
    [data-testid="stDataFrame"] {
        max-width: 100%;
        overflow-x: auto;
    }
    
    /* 15. UTILITY CLASSES */
    .hidden { display: none; }
    .mt-16 { margin-top: var(--space-md); }
    
    </style>
    """, unsafe_allow_html=True)

def compile_script_from_scenes():
    """Compiles the full screenplay text from the list of scenes in session state."""
    if 'scene_list' not in st.session_state or not st.session_state['scene_list']:
        return None
    
    full_script = ""
    for scene in st.session_state['scene_list']:
        # Concatenate header and content for full script review
        full_script += f"{scene['header']}\n\n{scene['content']}\n\n"
        
    return full_script.strip()

# 1. Config & Init
st.set_page_config(
    page_title="Script Doctor Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS
load_custom_css()

# Initialize app data structures
utils.init_app()

# Auto-load session state on startup
saved_data = utils.load_session_state()
if saved_data:
    for key, value in saved_data.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Default API key from environment if not loaded
if not st.session_state.get('gemini_api_key'):
    st.session_state['gemini_api_key'] = os.getenv('GEMINI_API_KEY', '')

# Initialize edit timestamp for UI reactivity
if 'edit_timestamp' not in st.session_state:
    st.session_state['edit_timestamp'] = 0

if 'option_updates' not in st.session_state:
    st.session_state['option_updates'] = {}

# 2. Sidebar
with st.sidebar:
    # Project Management Section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="sidebar-title">Quản lý Dự án</h2>', unsafe_allow_html=True)
    
    # Try to import database module
    try:
        import database
        supabase_enabled = database.is_supabase_enabled()
    except Exception as e:
        supabase_enabled = False
        print(f"Database module error: {e}")
    
    if supabase_enabled:
        # Load projects from Supabase
        projects = database.get_projects()
        
        if projects:
            # Create project options
            project_options = {p['name']: p['id'] for p in projects}
            project_names = list(project_options.keys())
            
            # Get current project index
            current_project_id = st.session_state.get('current_project_id')
            current_index = 0
            if current_project_id:
                for i, (name, pid) in enumerate(project_options.items()):
                    if pid == current_project_id:
                        current_index = i
                        break
            
            # Project selector
            selected_name = st.selectbox(
                "Chọn dự án",
                options=project_names,
                index=current_index,
                key="project_selector",
                label_visibility="collapsed"
            )
            
            # Load project when changed
            if selected_name:
                project_id = project_options[selected_name]
                if st.session_state.get('current_project_id') != project_id:
                    with st.spinner("Đang tải dự án..."):
                        if database.load_project_to_session(project_id):
                            st.success(f"Đã tải: {selected_name}")
                            st.rerun()
                        else:
                            st.error("Lỗi tải dự án!")
        else:
            st.info("Chưa có dự án. Tạo dự án mới để bắt đầu!")
        
        # Create new project button
        if st.button("+ Tạo dự án mới", use_container_width=True, type="primary"):
            st.session_state['show_create_project_dialog'] = True
        
        # Create project dialog
        if st.session_state.get('show_create_project_dialog'):
            with st.form("create_project_form"):
                st.markdown("#### Tạo dự án mới")
                project_name = st.text_input("Tên dự án *", placeholder="VD: Heo Năm Móng - Draft 1")
                project_desc = st.text_area("Mô tả (optional)", placeholder="Mô tả ngắn về dự án...")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("✓ Tạo", use_container_width=True, type="primary"):
                        if project_name:
                            project = database.create_project(project_name, project_desc)
                            if project:
                                st.success(f"Đã tạo: {project_name}")
                                st.session_state['show_create_project_dialog'] = False
                                database.load_project_to_session(project['id'])
                                st.rerun()
                            else:
                                st.error("Lỗi tạo dự án!")
                        else:
                            st.error("Vui lòng nhập tên dự án!")
                
                with col2:
                    if st.form_submit_button("✗ Hủy", use_container_width=True):
                        st.session_state['show_create_project_dialog'] = False
                        st.rerun()
        
        # Project actions
        if st.session_state.get('current_project_id'):
            with st.expander("⚙️ Tùy chọn dự án"):
                if st.button("💾 Lưu dự án", use_container_width=True):
                    with st.spinner("Đang lưu..."):
                        if database.save_current_project():
                            st.success("Đã lưu!")
                            st.toast("Dự án đã được lưu!", icon="✅")
                        else:
                            st.error("Lỗi lưu dự án!")
                
                st.markdown("---")
                
                if st.button("🗑️ Xóa dự án", use_container_width=True, type="secondary"):
                    st.session_state['show_delete_confirm'] = True
                
                if st.session_state.get('show_delete_confirm'):
                    st.warning("⚠️ Xóa dự án sẽ mất toàn bộ dữ liệu!")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Xác nhận xóa", type="primary", use_container_width=True):
                            project_id = st.session_state['current_project_id']
                            project_name = st.session_state.get('current_project_name', 'dự án')
                            if database.delete_project(project_id):
                                st.success(f"Đã xóa: {project_name}")
                                # Clear session
                                for key in ['current_project_id', 'current_project_name', 'scene_list', 
                                           'analysis_results', 'action_plan', 'user_strategy', 'task_completion']:
                                    st.session_state.pop(key, None)
                                st.session_state['show_delete_confirm'] = False
                                st.rerun()
                    with col2:
                        if st.button("Hủy", use_container_width=True):
                            st.session_state['show_delete_confirm'] = False
                            st.rerun()
    else:
        # Fallback to local storage
        st.warning("⚠️ Supabase chưa được cấu hình")
        st.info("Đang dùng lưu trữ local (mất data khi restart)")
        
        # Show setup instructions
        with st.expander("📖 Hướng dẫn setup Supabase"):
            st.markdown("""
            1. Đọc file `SUPABASE_SETUP.md`
            2. Tạo Supabase account
            3. Run SQL schema
            4. Thêm keys vào `.streamlit/secrets.toml`:
            ```toml
            SUPABASE_URL = "your_url"
            SUPABASE_KEY = "your_anon_key"
            ```
            5. Restart app
            """)
        
        # Local storage fallback (old code)
        projects_data = utils.load_json(utils.PROJECTS_FILE)
        project_list = [p["name"] for p in projects_data.get("projects", [])]
        
        if project_list:
            selected_project = st.selectbox(
                "Chọn dự án (Local)",
                options=project_list,
                label_visibility="collapsed"
            )
        else:
            st.caption("(Chưa có dự án local)")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()
    
    # AI Configuration Section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="sidebar-title">Cấu hình AI</h2>', unsafe_allow_html=True)
    
    api_key = st.text_input(
        "🔑 Gemini API Key", 
        value=st.session_state.get('gemini_api_key', ''),
        type="password", 
        help="Nhập API Key từ Google AI Studio",
        label_visibility="collapsed",
        placeholder="Nhập Gemini API Key..."
    )
    
    if api_key:
        st.session_state["gemini_api_key"] = api_key
        # Auto-save API key
        utils.save_session_state(st.session_state)
    
    if st.button("Kiểm tra kết nối", use_container_width=True, type="secondary"):
        if "gemini_api_key" in st.session_state and st.session_state["gemini_api_key"]:
            try:
                import ai_engine
                # Reload module to ensure latest code is used if modified while running
                import importlib
                importlib.reload(ai_engine)
                
                api_key = st.session_state["gemini_api_key"]
                
                # Get working model name
                model_name = ai_engine.get_working_model_name(api_key)
                
                # Test generation
                response = ai_engine.generate_analysis("Chào Gemini", api_key)
                
                st.success(f"Kết nối thành công! 🚀\nModel đang dùng: **{model_name}**")
                st.toast(f"Gemini ({model_name}): {response}")
                
            except Exception as e:
                st.error(f"Kết nối thất bại: {str(e)}")
        else:
            st.warning("Vui lòng nhập API Key trước.")
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    # Scene Navigator Section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="sidebar-title">🎬 Scene Navigator</h2>', unsafe_allow_html=True)
    
    selected_scene = None
    
    if 'scene_list' in st.session_state and st.session_state['scene_list']:
        scenes = st.session_state['scene_list']
        
        # Determine the content of the original script for comparison
        original_content_map = st.session_state.get('original_content_map', {})
        if not original_content_map:
            # Recreate original content map from the first time the script was loaded
            for scene in scenes:
                original_content_map[scene['id']] = scene['content']
            st.session_state['original_content_map'] = original_content_map

        # Create formatted labels with icons
        scene_labels = []
        default_index = 0
        target_id = st.session_state.get('target_scene_id')
        
        for i, s in enumerate(scenes):
            scene_id = s['id']
            # Determine status: 
            # 1. Check if the scene content is different from the original import
            is_edited = s['content'] != original_content_map.get(scene_id)
            # 2. Check if the scene has been marked as complete in the Action Plan (using a placeholder logic for now)
            is_completed = st.session_state.get('task_completion', {}).get(f"subtask_{scene_id}", False)
            
            icon = "✅" if is_completed else ("✏️" if is_edited else "📄")
            
            label = f"{icon} {scene_id}: {s['header']}"
            scene_labels.append(label)

            if str(scene_id) == str(target_id):
                default_index = i
        
        # Sidebar selection
        selected_label = st.radio(
            "Danh sách cảnh", 
            scene_labels, 
            index=default_index, 
            label_visibility="collapsed"
        )
        
        # Get selected scene
        selected_index = scene_labels.index(selected_label)
        selected_scene = scenes[selected_index]
        
        # Update target_scene_id to sync
        st.session_state['target_scene_id'] = selected_scene['id']
        
        st.caption(f"Total: {len(scenes)} scenes")
    else:
        st.info("Chưa có kịch bản. Vui lòng Import ở Tab 1.")
    
    st.markdown('</div>', unsafe_allow_html=True)
        
    st.divider()
    
    # Cost Tracker Section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    with st.expander("💸 Chi phí (Gemini 2.5 Flash)", expanded=True):
        stats = st.session_state.get('cost_stats', {'total_input': 0, 'total_output': 0, 'total_usd': 0.0})
        
        col1, col2 = st.columns(2)
        col1.metric("Input", f"{stats['total_input']:,}")
        col2.metric("Output", f"{stats['total_output']:,}")
        
        st.metric("Tổng chi phí (Ước tính)", f"${stats['total_usd']:.5f}", help="Dựa trên đơn giá Flash: $0.075/$0.30 per 1M tokens")
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    # Export Section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="sidebar-title">📤 Xuất Kịch bản</h2>', unsafe_allow_html=True)
    if st.button("Tạo file Word (.docx)", use_container_width=True, type="secondary"):
        if 'scene_list' not in st.session_state or not st.session_state['scene_list']:
            st.error("Chưa có dữ liệu kịch bản!")
        else:
            with st.spinner("Đang tạo file Word..."):
                try:
                    import export_engine
                    output_docx = "script_export.docx"
                    export_engine.create_screenplay_docx(st.session_state['scene_list'], output_docx)
                    
                    with open(output_docx, "rb") as f:
                        st.download_button(
                            label="⬇️ Tải xuống (.docx)",
                            data=f,
                            file_name="script_doctor_export.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    st.success("Đã tạo file thành công!")
                except Exception as e:
                    st.error(f"Lỗi xuất file: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# 3. Main Area
st.title("📚 Script Doctor & Brainstorm")

tab1, tab2, tab3 = st.tabs(["Review & Phân tích", "Brainstorm Sáng tạo", "Lập Kế hoạch (Action Plan)"])

# Tab 1: Import & Phân tích
with tab1:
    st.subheader("📊 Tổng quan Phân tích")
    
    # 1. IMPORT SECTION (Only visible if no script is loaded)
    if 'scene_list' not in st.session_state or not st.session_state['scene_list']:
        st.info("Chưa có kịch bản. Vui lòng tải lên file PDF để bắt đầu dự án.")
        uploaded_file = st.file_uploader("Upload file PDF", type=["pdf"])
        
        if uploaded_file is not None:
            # Replicate existing import logic
            with st.spinner(f"Đang xử lý file: {uploaded_file.name}"):
                try:
                    import script_parser
                    # Extract text
                    script_text = script_parser.extract_text_from_pdf(uploaded_file)
                    
                    # Auto-parse scenes
                    scenes = script_parser.parse_scenes(script_text)
                    st.session_state['scene_list'] = scenes
                    st.success(f"Đã bóc tách thành công {len(scenes)} cảnh!")
                    
                    # Store full text for initial analysis
                    st.session_state['full_script_text_on_import'] = script_text
                    
                    # Auto-save after parsing
                    auto_save()
                    st.rerun() # Rerun to switch to the review mode
                    
                except Exception as e:
                    st.error(f"Lỗi Import: {str(e)}")
        
    # 2. REVIEW & RE-ANALYZE SECTION (Visible if script is loaded)
    if 'scene_list' in st.session_state and st.session_state['scene_list']:
        
        # Full Script Preview Section
        st.divider()
        st.markdown("### 📝 Kịch bản Hiện tại (Sau khi sửa)")
        
        # Compile the current state of the script
        current_script_text = compile_script_from_scenes()
        
        with st.expander("Xem nội dung Kịch bản Hoàn chỉnh (Text)", expanded=False):
            # Use custom CSS class for screenplay formatting
            st.markdown(f'<div class="script-container">{current_script_text}</div>', unsafe_allow_html=True)
            
        st.divider()
        
        # Analysis Section
        st.markdown("### 🧠 Phân tích Tổng thể (Act-by-Act Review)")
        
        # New session state keys for dual analysis
        if 'analysis_results' not in st.session_state:
            st.session_state['analysis_results'] = {}
        
        if st.button("🔍 Phân tích Lại Kịch bản (Dual View)", type="primary"):
            if "gemini_api_key" not in st.session_state or not st.session_state["gemini_api_key"]:
                st.error("Vui lòng nhập API Key trong Sidebar trước!")
            else:
                with st.spinner("AI đang đọc lại và phân tích kịch bản dưới 2 góc độ... (Có thể mất 20-30s)"):
                    try:
                        import ai_engine
                        api_key = st.session_state["gemini_api_key"]
                        
                        # Use the re-compiled script text for analysis
                        current_script_text = compile_script_from_scenes() # Assumes this helper is defined
                        results = ai_engine.run_dual_analysis(current_script_text, api_key)
                        
                        # Save results to session state
                        st.session_state['analysis_results'] = results
                        
                        # Save analysis report (for Action Plan to continue using the main report - Creative View)
                        st.session_state['analysis_report'] = results['creative']
                        
                        auto_save()
                        
                        st.success("Đã hoàn tất phân tích lại dưới góc nhìn kép!")
                        
                    except Exception as e:
                        st.error(f"Lỗi phân tích: {str(e)}")
                        
        # Display the dual analysis report
        if st.session_state['analysis_results']:
            results = st.session_state['analysis_results']
            
            st.markdown("---")
            st.markdown("### 📊 Bảng Tóm tắt Các Điểm Đồng nhất")
            
            # Use st.dataframe for the summary table (JSON input)
            try:
                summary_df = pd.DataFrame(results['summary'])
                st.dataframe(
                    summary_df, 
                    use_container_width=True,
                    height=200,
                    hide_index=True
                )
            except Exception:
                st.error("Không thể hiển thị bảng tóm tắt.")
            
            st.markdown("---")
            st.markdown("### 📋 Báo cáo Chi tiết")
            
            # --- XỬ LÝ VÀ HIỂN THỊ BÁO CÁO SÁNG TẠO (JSON mới) ---
            creative_data = results['creative']
            
            if isinstance(creative_data, dict) and not creative_data.get('error'):
                st.markdown("#### 🎬 Góc nhìn Sáng tạo (Creative Doctor)")
                
                # Cấu trúc Kịch bản
                structure = creative_data.get('structure', {})
                with st.expander(f"⚙️ Cấu trúc Kịch bản: {structure.get('summary', 'Đang phân tích...')}", expanded=False):
                    st.markdown(structure.get('detail', 'Không có chi tiết.'))

                # Phát triển Nhân vật
                character = creative_data.get('character', {})
                with st.expander(f"👤 Phát triển Nhân vật: {character.get('summary', 'Đang phân tích...')}", expanded=False):
                    st.markdown(character.get('detail', 'Không có chi tiết.'))

                # Đánh giá Tension
                tension = creative_data.get('tension', {})
                with st.expander(f"🔥 Đánh giá Tension: {tension.get('summary', 'Đang phân tích...')}", expanded=False):
                    st.markdown(tension.get('detail', 'Không có chi tiết.'))
                    
                # Show vs Tell
                svt = creative_data.get('show_vs_tell', {})
                with st.expander(f"🗣️ Show vs Tell: {svt.get('summary', 'Đang phân tích...')}", expanded=False):
                    st.markdown(svt.get('detail', 'Không có chi tiết.'))
                
            elif isinstance(creative_data, dict) and creative_data.get('error'):
                st.error("Lỗi định dạng JSON từ AI cho báo cáo Sáng tạo. Xem nội dung thô bên dưới:")
                st.code(creative_data.get('raw_content', 'Không có nội dung thô.'))
            else:
                st.error("Lỗi: Báo cáo Sáng tạo không đúng định dạng JSON.")
                st.code(str(creative_data))

            # --- XỬ LÝ VÀ HIỂN THỊ BÁO CÁO MARKETING (Markdown cũ) ---
            st.markdown("---")
            st.markdown("#### 💰 Góc nhìn Marketing & Khán giả")
            
            # Báo cáo Marketing vẫn là Markdown, hiển thị trong expander đơn giản
            with st.expander("Báo cáo Chi tiết Marketing", expanded=False):
                st.markdown(results['marketing'])

        else:
            st.info("Nhấn 'Phân tích Lại Kịch bản (Dual View)' để nhận báo cáo review Act-by-Act và tổng thể từ 2 góc nhìn.")

# Tab 2: Brainstorm Sáng tạo
with tab2:
    if not selected_scene:
        st.info("👈 Vui lòng chọn một cảnh từ Sidebar để bắt đầu làm việc.")
    else:
        # Scene Header
        st.markdown(f"## 🎬 {selected_scene['header']}")
        
        # 2-Column Split Layout matching t.html (68% editor / 32% AI pane)
        col_script, col_brainstorm = st.columns([68, 32])
        
        with col_script:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            
            st.markdown("### 📝 Script Editor")
            
            # --- Mô phỏng Line Numbers và Syntax Highlighting ---
            
            # Split the scene content into lines
            scene_lines = selected_scene['content'].split('\n')
            num_lines = len(scene_lines)
            
            # Calculate the required height for the editor (min 500px, max based on content)
            editor_height = max(500, num_lines * 22) # 22px per line, min 500px
            
            # Use columns to position Line Numbers next to the editor
            col_lines, col_editor = st.columns([0.5, 9.5])
            
            # Line Numbers Column
            with col_lines:
                # Generate line numbers content
                line_numbers_content = "\n".join([str(i+1) for i in range(num_lines)])
                
                # Custom CSS for line numbers display
                st.markdown("""
                <style>
                .line-numbers-container {
                    background-color: var(--color-gray-900);
                    color: var(--color-gray-600);
                    font-family: 'Courier Prime', monospace;
                    font-size: 16px;
                    line-height: 1.7; 
                    text-align: right;
                    padding-right: 5px;
                    overflow: hidden;
                    height: 100%;
                    user-select: none; /* Prevent selection */
                }
                </style>
                """, unsafe_allow_html=True)
                
                st.markdown(
                    f'<div class="line-numbers-container" style="height: {editor_height}px;">{line_numbers_content}</div>', 
                    unsafe_allow_html=True
                )
            
            # Editor Column
            with col_editor:
                # Editable Text Area
                scene_content = st.text_area(
                    "Nội dung Scene",
                    value=selected_scene['content'],
                    height=editor_height, # Set height dynamically
                    key=f"editor_{selected_scene['id']}_{st.session_state['edit_timestamp']}",
                    label_visibility="collapsed"
                )
            
            # Director's Note Input (Moved to col_editor for better context, but hidden here as it's on the right)
            # The director_note variable is needed for the save logic later
            director_note = st.session_state.get(f"note_{selected_scene['id']}", "")
            
            # Save button
            if st.button("💾 Lưu", use_container_width=True, type="primary"):
                if 'undo_stack' not in st.session_state:
                    st.session_state['undo_stack'] = {}
                
                current_saved_content = selected_scene['content']
                
                if current_saved_content != scene_content:
                    if selected_scene['id'] not in st.session_state['undo_stack']:
                        st.session_state['undo_stack'][selected_scene['id']] = []
                    st.session_state['undo_stack'][selected_scene['id']].append(current_saved_content)
                
                # Update scene content
                for scene in st.session_state['scene_list']:
                    if scene['id'] == selected_scene['id']:
                        scene['content'] = scene_content
                        # Update original content map if this is the first edit (basic version tracking)
                        if scene['id'] not in st.session_state.get('original_content_map', {}):
                            st.session_state['original_content_map'][scene['id']] = current_saved_content
                        break
                
                auto_save()
                st.toast("Đã lưu nội dung cảnh! ✅")
            
            # Undo button
            has_undo = 'undo_stack' in st.session_state and \
                       selected_scene['id'] in st.session_state['undo_stack'] and \
                       len(st.session_state['undo_stack'][selected_scene['id']]) > 0
            
            if has_undo:
                if st.button("↩️ Undo", use_container_width=True, type="secondary"):
                    last_content = st.session_state['undo_stack'][selected_scene['id']].pop()
                    
                    for scene in st.session_state['scene_list']:
                        if scene['id'] == selected_scene['id']:
                            scene['content'] = last_content
                            break
                    
                    st.session_state['edit_timestamp'] = time.time()
                    utils.save_session_state(st.session_state)
                    st.toast("Đã hoàn tác! ↩️")
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

        with col_brainstorm:
            # Director's Note Section
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### ✍️ Ghi chú Đạo diễn")
            
            # Director's Note Input
            director_note = st.text_area(
                "Yêu cầu cho AI:", 
                placeholder="VD: Cảnh này cần tạo tension, thể hiện sự lưỡng lự của Khải...",
                key=f"note_{selected_scene['id']}",
                label_visibility="collapsed",
                height=80
            )
            
            st.write("") # Spacer
            btn_brainstorm = st.button("🎨 Brainstorm Ideas", type="primary", use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # AI Suggestions Section
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 💡 AI Suggestions")
            
            # Logic xử lý Brainstorm
            if btn_brainstorm:
                if "gemini_api_key" not in st.session_state or not st.session_state["gemini_api_key"]:
                    st.error("Chưa có API Key!")
                else:
                    with st.spinner("AI đang viết lại scene..."):
                        try:
                            import ai_engine
                            api_key = st.session_state["gemini_api_key"]
                            
                            instruction = director_note if director_note else "Cải thiện chất lượng thoại và hành động"
                            full_scene = f"{selected_scene['header']}\n\n{scene_content}"
                            
                            options = ai_engine.brainstorm_scene(full_scene, instruction, api_key)
                            
                            st.session_state['brainstorm_options'] = options
                            
                        except Exception as e:
                            st.error(f"Lỗi: {str(e)}")
            
            # Display brainstorm results with apply buttons
            if 'brainstorm_options' in st.session_state and st.session_state['brainstorm_options']:
                st.markdown("#### ✨ Phương án Viết lại:")
                
                options = st.session_state['brainstorm_options']
                
                # Initialize state for active preview
                if 'active_brainstorm_preview' not in st.session_state:
                    st.session_state['active_brainstorm_preview'] = None

                for i, opt in enumerate(options):
                    option_title = opt.get('title', f'Phương án {i+1}')
                    
                    # Use unique key for the option content
                    last_update = st.session_state['option_updates'].get(i, 0)
                    edited_content_key = f"opt_content_{i}_{last_update}"
                    
                    current_opt_content = options[i].get('content', '')
                    
                    is_active_preview = st.session_state['active_brainstorm_preview'] == i
                    
                    # Use expander to contain refinement and apply logic
                    with st.expander(f"✨ {option_title}", expanded=is_active_preview):
                        
                        # --- 1. Content Editor/Preview ---
                        
                        # The text area must be defined first to capture user edits
                        edited_content = st.text_area(
                            "Nội dung đề xuất (Có thể sửa tay)",
                            value=current_opt_content,
                            height=250, 
                            key=edited_content_key # Must use the unique key
                        )
                        
                        # Update the session state immediately if user changes the text area value (important for refinement)
                        if edited_content != current_opt_content:
                            options[i]['content'] = edited_content
                            st.session_state['brainstorm_options'] = options
                            utils.save_session_state(st.session_state)
                            st.session_state['option_updates'][i] = time.time()
                            # No rerun needed here, save change for next action

                        
                        col_preview, col_apply = st.columns([1, 1])
                        
                        with col_preview:
                            if st.button("👁 Preview", key=f"preview_diff_{i}", use_container_width=True, type="secondary"):
                                st.session_state['active_brainstorm_preview'] = i
                                st.rerun() # Force rerun to show the diff view below

                        with col_apply:
                            if st.button(f"✓ Apply", key=f"apply_opt_{i}", use_container_width=True, type="primary"):
                                for scene in st.session_state['scene_list']:
                                    if scene['id'] == selected_scene['id']:
                                        scene['content'] = edited_content # Use the potentially edited content
                                        break
                                
                                st.session_state['edit_timestamp'] = time.time()
                                utils.save_session_state(st.session_state)
                                st.session_state['active_brainstorm_preview'] = None
                                
                                st.success(f"Đã áp dụng phương án {i+1}!")
                                st.rerun()
                        
                        # --- 2. Refinement Section ---
                        with st.expander("💬 Tinh chỉnh phương án này với AI", expanded=False):
                            col_ref_input, col_ref_btn = st.columns([3, 1])
                            with col_ref_input:
                                refine_instruction = st.text_input(
                                    "Bạn muốn sửa gì?", 
                                    key=f"refine_input_{i}", 
                                    placeholder="VD: Ngắn hơn, thêm thoại, kịch tính hơn...",
                                    label_visibility="collapsed"
                                )
                            with col_ref_btn:
                                st.write("") # Spacer
                                if st.button("🔄 Refine", key=f"refine_btn_{i}", use_container_width=True, type="secondary"):
                                    if not refine_instruction:
                                        st.warning("Nhập yêu cầu trước!")
                                    else:
                                        with st.spinner("AI đang chỉnh sửa..."):
                                            try:
                                                import ai_engine
                                                refined_text = ai_engine.refine_generated_option(
                                                    edited_content, 
                                                    refine_instruction, 
                                                    f"{selected_scene['header']}\n\n{selected_scene['content']}",
                                                    st.session_state["gemini_api_key"]
                                                )
                                                
                                                st.session_state['brainstorm_options'][i]['content'] = refined_text
                                                st.session_state['option_updates'][i] = time.time()
                                                
                                                utils.save_session_state(st.session_state)
                                                
                                                st.success("Đã cập nhật!")
                                                st.rerun()
                                            except Exception as e:
                                                st.error(f"Lỗi: {str(e)}")

                # --- 3. Diff View Display (Shared Logic) ---
                if st.session_state.get('active_brainstorm_preview') is not None:
                    active_index = st.session_state['active_brainstorm_preview']
                    original_content = selected_scene['content']
                    preview_content = st.session_state['brainstorm_options'][active_index]['content']

                    st.divider()
                    st.info(f"🔍 DIFF VIEW: So sánh Phương án {active_index + 1} với Bản gốc")
                    
                    col_before, col_after = st.columns(2)
                    
                    with col_before:
                        st.markdown("##### Gốc (Original)")
                        st.text_area(
                            "Nội dung Gốc",
                            value=original_content,
                            height=300,
                            disabled=True,
                            key="diff_original_preview"
                        )
                        
                    with col_after:
                        st.markdown("##### Đề xuất (Proposed)")
                        st.text_area(
                            "Nội dung Đề xuất",
                            value=preview_content,
                            height=300,
                            disabled=True, # Disable editing here, editing is done in the expander above
                            key="diff_proposed_preview"
                        )
                    
                    if st.button("❌ Close Diff View", key="close_diff_preview", type="secondary"):
                        st.session_state['active_brainstorm_preview'] = None
                        st.rerun()
            
            st.divider()
            
            # Show, Don't Tell Section
            st.markdown("#### 🗣️ Phân tích Thoại")
            if st.button("😶 Show, Don't Tell", use_container_width=True, type="secondary"):
                if "gemini_api_key" not in st.session_state or not st.session_state["gemini_api_key"]:
                    st.error("Chưa có API Key!")
                else:
                    with st.spinner("AI đang phân tích thoại..."):
                        try:
                            import ai_engine
                            api_key = st.session_state["gemini_api_key"]
                            
                            full_scene = f"{selected_scene['header']}\n\n{scene_content}"
                            
                            replacements = ai_engine.convert_dialogue_to_visual(full_scene, api_key)
                            
                            st.session_state['dialogue_replacements'] = replacements
                            
                        except Exception as e:
                            st.error(f"Lỗi: {str(e)}")
            
            # Display dialogue replacement options with checkboxes
            if 'dialogue_replacements' in st.session_state and st.session_state['dialogue_replacements']:
                replacements = st.session_state['dialogue_replacements']
                
                if len(replacements) == 0:
                    st.info("Scene này đã tốt. Không có thoại nào cần chuyển thành hình ảnh.")
                else:
                    st.markdown("##### 📊 Gợi ý Thay thế:")
                    
                    if 'selected_replacements' not in st.session_state:
                        st.session_state['selected_replacements'] = []
                    
                    for i, item in enumerate(replacements):
                        original = item.get('original', '')
                        replacement = item.get('replacement', '')
                        reason = item.get('reason', '')
                        
                        is_checked = st.checkbox(
                            f"**{original}** ➔ {replacement}",
                            key=f"replace_{i}",
                            value=i in st.session_state.get('selected_replacements', []),
                            help=f"Lý do: {reason}"
                        )
                        
                        if is_checked and i not in st.session_state['selected_replacements']:
                            st.session_state['selected_replacements'].append(i)
                        elif not is_checked and i in st.session_state['selected_replacements']:
                            st.session_state['selected_replacements'].remove(i)
                    
                    if st.button("✨ Áp dụng thay thế", use_container_width=True, type="primary"):
                        if st.session_state['selected_replacements']:
                            current_content = scene_content
                            replaced_count = 0
                            
                            for idx in st.session_state['selected_replacements']:
                                item = replacements[idx]
                                original = item.get('original', '')
                                replacement = item.get('replacement', '')
                                
                                if original in current_content:
                                    # Use a counter to ensure we only replace the first occurrence of the exact phrase
                                    current_content = current_content.replace(original, replacement, 1)
                                    replaced_count += 1
                            
                            for scene in st.session_state['scene_list']:
                                if scene['id'] == selected_scene['id']:
                                    scene['content'] = current_content
                                    break
                            
                            st.session_state['edit_timestamp'] = time.time()
                            utils.save_session_state(st.session_state)
                            
                            st.session_state['selected_replacements'] = []
                            st.session_state.pop('dialogue_replacements', None)
                            
                            st.success(f"Đã thay thế {replaced_count} đoạn thoại!")
                            st.rerun()
                            
            st.markdown('</div>', unsafe_allow_html=True)

# Tab 3: Lập Kế hoạch (Action Plan)
with tab3:
    st.subheader("🚀 Lập Kế hoạch Chỉnh sửa Thông minh")
    
    if 'scene_list' not in st.session_state or not st.session_state['scene_list']:
        st.info("Vui lòng Upload kịch bản ở Tab 1 trước.")
    else:
        # 1. Strategy Form (Không thay đổi)
        with st.form("strategy_form"):
            st.markdown("### 🎯 Định hướng Chiến lược")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                strategy_ai = st.text_area("Chọn lọc lời khuyên từ AI (Paste từ Tab 1)", height=150, placeholder="- Tăng nhịp phim Hồi 2\n- Làm rõ động cơ nhân vật chính...")
            with col_s2:
                strategy_user = st.text_area("Yêu cầu riêng của Đạo diễn", height=150, placeholder="Ví dụ: Làm cho đoạn kết dark hơn, thêm yếu tố kinh dị tâm lý...")
            
            btn_plan = st.form_submit_button("Lập Action Plan 📝", type="primary")
            
        if btn_plan:
            if "gemini_api_key" not in st.session_state or not st.session_state["gemini_api_key"]:
                st.error("Chưa có API Key!")
            else:
                user_strategy = f"LỜI KHUYÊN AI:\n{strategy_ai}\n\nCHỈ ĐẠO ĐẠO DIỄN:\n{strategy_user}"
                with st.spinner("AI đang xây dựng kế hoạch hành động chi tiết..."):
                    try:
                        import ai_engine
                        api_key = st.session_state["gemini_api_key"]
                        
                        plan = ai_engine.generate_action_plan(st.session_state['scene_list'], user_strategy, api_key)
                        st.session_state['action_plan'] = plan
                        st.session_state['user_strategy'] = user_strategy
                        st.session_state['task_completion'] = {} # New tracking for completion
                        
                        auto_save()
                        
                        st.success("Đã lập kế hoạch thành công!")
                    except Exception as e:
                        st.error(f"Lỗi: {str(e)}")

        # 2. Display Action Plan
        if 'action_plan' in st.session_state:
            st.divider()
            
            plan = st.session_state['action_plan']
            
            # --- PROGRESS TRACKING LOGIC ---
            all_subtasks = []
            for task in plan:
                for scene_task in task.get('related_scenes', []):
                    all_subtasks.append(f"subtask_{scene_task.get('scene_id', '')}")
            
            total_tasks = len(all_subtasks)
            completed_tasks = sum(1 for key in all_subtasks if st.session_state.get('task_completion', {}).get(key, False))
            progress_percent = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

            # Progress Overview (Recommendation 3)
            st.markdown('<div class="progress-section">', unsafe_allow_html=True)
            st.markdown('<h3 style="margin-bottom: 8px;">📊 Progress Overview</h3>', unsafe_allow_html=True)
            
            # Progress bar with gradient
            st.markdown(f'''
            <div class="progress-bar-container">
                <div class="progress-bar" style="width: {progress_percent}%;"></div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Progress stats
            st.markdown(f'''
            <div class="progress-stats">
                <div class="stat status-complete">✅ {completed_tasks} Done</div>
                <div class="stat status-progress">⏳ {min(3, total_tasks - completed_tasks)} In Progress</div>
                <div class="stat status-pending">📋 {total_tasks - completed_tasks} Pending</div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

            # Initialize temp storage for AI fix result
            if 'active_ai_fix_scene' not in st.session_state:
                st.session_state['active_ai_fix_scene'] = None
            
            if 'temp_ai_fix_content' not in st.session_state:
                st.session_state['temp_ai_fix_content'] = {}
            
            
            for i, task in enumerate(plan):
                task_scenes = task.get('related_scenes', [])
                total_subtasks = len(task_scenes)
                completed_subtasks = 0
                
                # Calculate progress for this task group
                for scene_task in task_scenes:
                    scene_id = scene_task.get('scene_id', '')
                    subtask_key = f"subtask_{scene_id}"
                    if st.session_state.get('task_completion', {}).get(subtask_key, False):
                        completed_subtasks += 1

                # Determine priority emoji based on position
                priority_emoji = "🔥" if i == 0 else ("⚠️" if i == 1 else "📄")
                
                # Construct expander title with progress
                expander_title = f"{priority_emoji} {task.get('task_name', 'Task')} ({completed_subtasks}/{total_subtasks} hoàn thành)"
                
                # Task Group Header
                st.markdown('<div class="task-group">', unsafe_allow_html=True)
                
                with st.expander(expander_title, expanded=(completed_subtasks < total_subtasks)):
                    
                    for j, scene_task in enumerate(task_scenes):
                        scene_id = scene_task.get('scene_id', scene_task.get('id', 'N/A'))
                        header_ctx = scene_task.get('header_context', '')
                        instruction = scene_task.get('instruction', '')
                        subtask_key = f"subtask_{scene_id}"
                        
                        is_subtask_done = st.session_state.get('task_completion', {}).get(subtask_key, False)
                        
                        # Task Item with HTML structure
                        st.markdown('<div class="task-item">', unsafe_allow_html=True)
                        st.markdown('<div class="task-header">', unsafe_allow_html=True)
                        
                        # Use 4 columns: Checkbox, Description, Manual/View, AI Fix
                        col_check, col_desc, col_act1, col_act2 = st.columns([0.3, 6, 1.5, 1.2]) 

                        with col_check:
                            # Checkbox for manual completion
                            checked = st.checkbox(
                                "Done",
                                key=f"checkbox_{subtask_key}",
                                value=is_subtask_done,
                                help="Đánh dấu đã hoàn thành",
                                label_visibility="collapsed"
                            )
                            
                            if checked != is_subtask_done:
                                # Initialize task_completion if it doesn't exist
                                if 'task_completion' not in st.session_state:
                                    st.session_state['task_completion'] = {}
                                st.session_state['task_completion'][subtask_key] = checked
                                utils.save_session_state(st.session_state)
                                st.rerun()
                        
                        with col_desc:
                            # Task description with scene context
                            task_style = "text-decoration: line-through; color: #718096;" if is_subtask_done else ""
                            st.markdown(f'<div class="task-content">', unsafe_allow_html=True)
                            st.markdown(f'<div class="task-title" style="{task_style}">Scene {scene_id} - {instruction}</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="task-scene">📍 {header_ctx}</div>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)

                        with col_act1:
                            # Nút Sửa ngay (chuyển tab) -> Mở trong Brainstorm
                            if st.button("👁️ View", key=f"manual_edit_{scene_id}", use_container_width=True, type="secondary", disabled=is_subtask_done):
                                st.session_state['target_scene_id'] = str(scene_id)
                                st.session_state['target_instruction'] = instruction
                                st.toast(f"Đã nạp lệnh sửa cho Scene {scene_id}! Qua Tab 'Brainstorm' để thực thi.", icon="✅")
                        
                        with col_act2:
                            # Nút AI Tự động Sửa -> Chạy AI Fix
                            is_active_fix = st.session_state.get('active_ai_fix_scene') == str(scene_id)
                            
                            btn_label = "⚡ AI Fix" if not is_subtask_done else "✓ Done"
                            btn_type = "primary" if not is_subtask_done else "secondary"
                            
                            if st.button(btn_label, key=f"ai_fix_{scene_id}", use_container_width=True, type=btn_type, disabled=(is_active_fix or is_subtask_done)):
                                if "gemini_api_key" not in st.session_state or not st.session_state["gemini_api_key"]:
                                    st.error("Chưa có API Key!")
                                else:
                                    target_scene = next((s for s in st.session_state['scene_list'] if str(s['id']) == str(scene_id)), None)
                                    if target_scene:
                                        with st.spinner(f"AI đang viết lại Scene {scene_id}..."):
                                            try:
                                                import ai_engine
                                                api_key = st.session_state["gemini_api_key"]
                                                
                                                fixed_content = ai_engine.ai_fix_scene(
                                                    scene_id, 
                                                    target_scene['content'], 
                                                    instruction, 
                                                    api_key
                                                )
                                                
                                                st.session_state['temp_ai_fix_content'] = {
                                                    'scene_id': scene_id,
                                                    'new_content': fixed_content,
                                                    'original_content': target_scene['content']
                                                }
                                                st.session_state['active_ai_fix_scene'] = str(scene_id)
                                                
                                                st.toast(f"Đã nhận kết quả AI Fix cho Scene {scene_id}. Vui lòng kiểm tra bên dưới.", icon="✨")
                                                st.rerun()
                                            except Exception as e:
                                                st.error(f"Lỗi AI Fix: {str(e)}")
                                    else:
                                        st.error(f"Không tìm thấy Scene ID: {scene_id}")
                        
                        # Close task-header and task-item divs
                        st.markdown('</div>', unsafe_allow_html=True)  # Close task-header
                        st.markdown('</div>', unsafe_allow_html=True)  # Close task-item

                        # --- HIỂN THỊ KẾT QUẢ VÀ ÁP DỤNG (Review Panel) ---
                        if is_active_fix:
                            result = st.session_state['temp_ai_fix_content']
                            
                            st.markdown("---")
                            st.info(f"🔥 KẾT QUẢ AI TỰ ĐỘNG SỬA: Scene {result['scene_id']}")
                            
                            # Placeholder for Diff View (use two columns for before/after)
                            col_before, col_after = st.columns(2)
                            
                            with col_before:
                                st.markdown("##### Gốc (Original)")
                                st.text_area(
                                    "Nội dung Gốc",
                                    value=result['original_content'],
                                    height=300,
                                    disabled=True,
                                    key=f"original_fix_editor_{scene_id}"
                                )
                                
                            with col_after:
                                st.markdown("##### Đã sửa (AI Fixed)")
                                # Editable text area for final review
                                edited_fixed_content = st.text_area(
                                    "Nội dung đã sửa (Có thể chỉnh sửa lần cuối)",
                                    value=result['new_content'],
                                    height=300,
                                    key="final_ai_fix_editor"
                                )
                            
                            col_apply, col_cancel = st.columns(2)
                            
                            with col_apply:
                                if st.button("✅ Áp dụng & Lưu Thay đổi", type="primary", key=f"apply_fix_{scene_id}", use_container_width=True):
                                    # Find and update scene content
                                    for scene in st.session_state['scene_list']:
                                        if str(scene['id']) == str(result['scene_id']):
                                            scene['content'] = edited_fixed_content
                                            break
                                            
                                    st.session_state['edit_timestamp'] = time.time()
                                    st.session_state['task_completion'][subtask_key] = True # Mark as complete
                                    
                                    utils.save_session_state(st.session_state)
                                    st.session_state['active_ai_fix_scene'] = None
                                    st.session_state['temp_ai_fix_content'] = {}
                                    
                                    st.success(f"Đã áp dụng nội dung đã sửa cho Scene {result['scene_id']}!")
                                    st.rerun()
                            
                            with col_cancel:
                                if st.button("❌ Hủy bỏ (Không áp dụng)", key=f"cancel_fix_{scene_id}", use_container_width=True):
                                    st.session_state['active_ai_fix_scene'] = None
                                    st.session_state['temp_ai_fix_content'] = {}
                                    st.toast("Đã hủy bỏ thay đổi.")
                                    st.rerun()
                            
                            st.divider() # Separator after review section
                
                # Close task-group div
                st.markdown('</div>', unsafe_allow_html=True)
                
