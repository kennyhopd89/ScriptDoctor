# 📁 Kế hoạch Quản lý Dự án - Script Doctor Pro

## 🎯 Mục tiêu

Cho phép users làm việc với **nhiều kịch bản song song**, mỗi kịch bản là một dự án riêng biệt với:
- Scenes riêng
- Analysis riêng
- Action plan riêng
- Cost tracking riêng

---

## 📊 Hiện trạng

### Vấn đề:
1. ❌ Chỉ có 1 session duy nhất
2. ❌ Không thể switch giữa các kịch bản
3. ❌ Data lưu local JSON - mất khi restart
4. ❌ Không có project management UI

### Code hiện tại:
```python
# app.py - Sidebar (dòng 590-600)
selected_project = st.selectbox(
    "Chọn dự án",
    options=project_list if project_list else ["(Chưa có dự án)"],
    label_visibility="collapsed"
)

if st.button("+ Tạo dự án mới", use_container_width=True, type="primary"):
    st.info("Tính năng tạo dự án đang phát triển...")  # ← CHƯA IMPLEMENT
```

---

## ✅ Giải pháp

### 1. Database Backend (Supabase)
- ✅ File `database.py` đã tạo
- ✅ Schema SQL đã tạo (`supabase_schema.sql`)
- ✅ Hướng dẫn setup (`SUPABASE_SETUP.md`)

### 2. Project Management UI
Cần update `app.py` để:
- Hiển thị danh sách projects
- Tạo project mới
- Switch giữa projects
- Delete projects
- Rename projects

---

## 🚀 Implementation Plan

### Phase 1: Setup Database (30 phút)
**Status:** ✅ READY

**Files:**
- `database.py` - Database operations
- `supabase_schema.sql` - Database schema
- `SUPABASE_SETUP.md` - Setup guide

**Action:**
1. Làm theo `SUPABASE_SETUP.md`
2. Test connection
3. Verify tables created

---

### Phase 2: Update App UI (2 giờ)
**Status:** ⏳ TODO

**Changes needed in `app.py`:**

#### 2.1 Sidebar - Project Management Section
```python
# Replace current code (line 590-600) with:

with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="sidebar-title">Quản lý Dự án</h2>', unsafe_allow_html=True)
    
    # Check if Supabase is enabled
    if database.is_supabase_enabled():
        # Load projects
        projects = database.get_projects()
        project_options = {p['name']: p['id'] for p in projects}
        
        if project_options:
            # Project selector
            selected_name = st.selectbox(
                "Chọn dự án",
                options=list(project_options.keys()),
                key="project_selector"
            )
            
            # Load project when changed
            if selected_name:
                project_id = project_options[selected_name]
                if st.session_state.get('current_project_id') != project_id:
                    database.load_project_to_session(project_id)
                    st.rerun()
        else:
            st.info("Chưa có dự án. Tạo dự án mới để bắt đầu!")
        
        # Create new project button
        if st.button("+ Tạo dự án mới", use_container_width=True, type="primary"):
            st.session_state['show_create_project_dialog'] = True
        
        # Create project dialog
        if st.session_state.get('show_create_project_dialog'):
            with st.form("create_project_form"):
                project_name = st.text_input("Tên dự án", placeholder="VD: Heo Năm Móng - Draft 1")
                project_desc = st.text_area("Mô tả (optional)", placeholder="Mô tả ngắn về dự án...")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Tạo", use_container_width=True, type="primary"):
                        if project_name:
                            project = database.create_project(project_name, project_desc)
                            if project:
                                st.success(f"Đã tạo dự án: {project_name}")
                                st.session_state['show_create_project_dialog'] = False
                                database.load_project_to_session(project['id'])
                                st.rerun()
                        else:
                            st.error("Vui lòng nhập tên dự án!")
                
                with col2:
                    if st.form_submit_button("Hủy", use_container_width=True):
                        st.session_state['show_create_project_dialog'] = False
                        st.rerun()
        
        # Project actions
        if st.session_state.get('current_project_id'):
            with st.expander("⚙️ Tùy chọn dự án"):
                if st.button("💾 Lưu dự án", use_container_width=True):
                    if database.save_current_project():
                        st.success("Đã lưu!")
                    else:
                        st.error("Lỗi lưu dự án!")
                
                if st.button("🗑️ Xóa dự án", use_container_width=True, type="secondary"):
                    st.session_state['show_delete_confirm'] = True
                
                if st.session_state.get('show_delete_confirm'):
                    st.warning("⚠️ Xóa dự án sẽ mất toàn bộ dữ liệu!")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Xác nhận xóa", type="primary"):
                            project_id = st.session_state['current_project_id']
                            if database.delete_project(project_id):
                                st.success("Đã xóa dự án!")
                                # Clear session
                                for key in ['current_project_id', 'scene_list', 'analysis_results']:
                                    st.session_state.pop(key, None)
                                st.rerun()
                    with col2:
                        if st.button("Hủy"):
                            st.session_state['show_delete_confirm'] = False
                            st.rerun()
    else:
        # Fallback to local storage
        st.warning("⚠️ Supabase chưa được cấu hình. Đang dùng lưu trữ local.")
        st.info("Xem `SUPABASE_SETUP.md` để setup database.")
    
    st.markdown('</div>', unsafe_allow_html=True)
```

#### 2.2 Auto-save on Changes
```python
# Add this function at the top of app.py
def auto_save_project():
    """Auto-save current project to database"""
    if database.is_supabase_enabled() and st.session_state.get('current_project_id'):
        database.save_current_project()

# Call this after major changes:
# - After editing scene
# - After running analysis
# - After creating action plan
```

#### 2.3 Import PDF - Create Project
```python
# In Tab 1, when uploading PDF:
if uploaded_file is not None:
    with st.spinner(f"Đang xử lý file: {uploaded_file.name}"):
        try:
            import script_parser
            script_text = script_parser.extract_text_from_pdf(uploaded_file)
            scenes = script_parser.parse_scenes(script_text)
            
            # If Supabase enabled, create project
            if database.is_supabase_enabled():
                # Ask for project name
                project_name = st.text_input("Tên dự án", value=uploaded_file.name.replace('.pdf', ''))
                if st.button("Tạo dự án"):
                    project = database.create_project(project_name)
                    if project:
                        st.session_state['current_project_id'] = project['id']
                        st.session_state['scene_list'] = scenes
                        database.save_scenes(project['id'], scenes)
                        st.success(f"Đã tạo dự án: {project_name}")
                        st.rerun()
            else:
                # Fallback to session state only
                st.session_state['scene_list'] = scenes
                st.success(f"Đã bóc tách {len(scenes)} cảnh!")
                
        except Exception as e:
            st.error(f"Lỗi Import: {str(e)}")
```

---

### Phase 3: Testing (1 giờ)
**Status:** ⏳ TODO

**Test cases:**
1. ✅ Create new project
2. ✅ Upload PDF to project
3. ✅ Run analysis
4. ✅ Create action plan
5. ✅ Switch between projects
6. ✅ Delete project
7. ✅ Data persists after refresh
8. ✅ Multiple users (different user_id)

---

### Phase 4: Migration (optional)
**Status:** ⏳ TODO

**Migrate existing data:**
```python
# migration_script.py
import json
from database import create_project, save_scenes

# Load old data
with open('data/current_session.json', 'r') as f:
    old_data = json.load(f)

# Create project
project = create_project("Migrated Project", "Data from old session")

# Save scenes
if 'scene_list' in old_data:
    save_scenes(project['id'], old_data['scene_list'])

print(f"Migrated to project: {project['id']}")
```

---

## 📊 Database Structure

### Tables:
```
projects
├── id (UUID)
├── user_id (TEXT)
├── name (TEXT)
├── description (TEXT)
├── created_at (TIMESTAMP)
├── updated_at (TIMESTAMP)
└── metadata (JSONB)

scenes
├── id (UUID)
├── project_id (UUID) → projects.id
├── scene_id (TEXT)
├── header (TEXT)
├── content (TEXT)
├── original_index (INTEGER)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

analysis_results
├── id (UUID)
├── project_id (UUID) → projects.id
├── creative_report (JSONB)
├── marketing_report (TEXT)
├── summary (JSONB)
└── created_at (TIMESTAMP)

action_plans
├── id (UUID)
├── project_id (UUID) → projects.id
├── user_strategy (TEXT)
├── plan (JSONB)
├── task_completion (JSONB)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
```

---

## 🔄 User Workflow

### Workflow 1: Tạo dự án mới
1. Click "Tạo dự án mới"
2. Nhập tên dự án
3. Upload PDF
4. Scenes được parse và lưu vào database
5. Bắt đầu làm việc

### Workflow 2: Làm việc với dự án
1. Chọn dự án từ dropdown
2. Data được load từ database
3. Edit scenes, run analysis, create action plan
4. Auto-save sau mỗi thay đổi

### Workflow 3: Switch giữa dự án
1. Chọn dự án khác từ dropdown
2. Current project được auto-save
3. New project được load
4. Continue working

### Workflow 4: Xóa dự án
1. Mở "Tùy chọn dự án"
2. Click "Xóa dự án"
3. Confirm
4. Project và tất cả data bị xóa

---

## 💾 Data Persistence

### Local Storage (Hiện tại):
```
data/
├── current_session.json  ← Mất khi restart
└── projects.json         ← Chưa dùng
```

### Supabase (Mới):
```
Supabase Database
├── projects table        ← Persistent
├── scenes table          ← Persistent
├── analysis_results      ← Persistent
└── action_plans          ← Persistent
```

**Ưu điểm:**
- ✅ Không mất data khi restart
- ✅ Sync across devices
- ✅ Backup tự động
- ✅ Scalable

---

## 🎯 Success Criteria

### Must Have:
- [x] Database schema created
- [x] Database module implemented
- [ ] Project CRUD UI implemented
- [ ] Project switcher working
- [ ] Data persists after refresh
- [ ] Auto-save working

### Nice to Have:
- [ ] Project search/filter
- [ ] Project tags/categories
- [ ] Export/Import projects
- [ ] Share projects with others
- [ ] Version history
- [ ] Duplicate project

---

## 📈 Future Enhancements

### Phase 5: User Authentication
- Google OAuth
- Email/Password
- User profiles

### Phase 6: Collaboration
- Share projects with team
- Real-time editing
- Comments & feedback

### Phase 7: Advanced Features
- Version control
- Compare versions
- Merge changes
- Conflict resolution

---

## 💡 Tips

1. **Test local first** trước khi deploy
2. **Backup data** trước khi migrate
3. **Monitor usage** để tránh vượt free tier
4. **Document changes** khi update schema
5. **Use transactions** cho operations phức tạp

---

## 📞 Next Steps

### Immediate (Bây giờ):
1. ✅ Đọc `DATA_STORAGE_PLAN.md`
2. ✅ Đọc `SUPABASE_SETUP.md`
3. ⏳ Setup Supabase (30 phút)
4. ⏳ Test database connection

### Short-term (Tuần này):
1. ⏳ Update app.py với project management UI
2. ⏳ Test multi-project workflow
3. ⏳ Deploy lên production

### Long-term (Tháng này):
1. ⏳ Add user authentication
2. ⏳ Implement sharing
3. ⏳ Add version history

---

**Bạn muốn tôi implement Phase 2 (Update App UI) ngay không?**

---

**Created:** December 2, 2025  
**Status:** Planning Complete  
**Next:** Implementation
