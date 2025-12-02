# 📊 Phương án Lưu trữ Dữ liệu Dài hạn

## 🔍 Phân tích Hiện trạng

### Vấn đề hiện tại:
1. **Lưu trữ local JSON** - Không persistent trên Streamlit Cloud
2. **Chỉ 1 session** - Không quản lý được nhiều dự án
3. **Mất data khi restart** - Streamlit Cloud restart app thường xuyên
4. **Không có backup** - Rủi ro mất dữ liệu cao

### Dữ liệu cần lưu:
```python
# Per Project:
- project_id
- project_name
- created_date
- last_modified
- scene_list (array)
- analysis_results (JSON)
- action_plan (JSON)
- cost_stats (JSON)

# Global:
- user_settings
- api_key (encrypted)
```

---

## 🎯 Phương án Khuyến nghị

### **Option 1: Supabase (PostgreSQL) - KHUYẾN NGHỊ** ⭐⭐⭐⭐⭐

**Ưu điểm:**
- ✅ Miễn phí (500MB database, 50,000 monthly active users)
- ✅ PostgreSQL - Reliable, scalable
- ✅ Real-time subscriptions
- ✅ Built-in authentication
- ✅ Row Level Security
- ✅ Python SDK dễ dùng
- ✅ Backup tự động

**Nhược điểm:**
- ⚠️ Cần setup database schema
- ⚠️ Cần học SQL cơ bản

**Chi phí:**
- Free tier: $0/tháng
- Pro: $25/tháng (nếu cần scale)

**Setup time:** 30 phút

---

### **Option 2: Firebase Firestore** ⭐⭐⭐⭐

**Ưu điểm:**
- ✅ Miễn phí (1GB storage, 50K reads/day)
- ✅ NoSQL - Flexible schema
- ✅ Real-time sync
- ✅ Google authentication
- ✅ Python SDK

**Nhược điểm:**
- ⚠️ Phức tạp hơn Supabase
- ⚠️ Pricing model khó tính

**Chi phí:**
- Free tier: $0/tháng
- Pay as you go

**Setup time:** 45 phút

---

### **Option 3: MongoDB Atlas** ⭐⭐⭐⭐

**Ưu điểm:**
- ✅ Miễn phí (512MB storage)
- ✅ NoSQL - JSON native
- ✅ Powerful queries
- ✅ Python SDK (pymongo)

**Nhược điểm:**
- ⚠️ Free tier có giới hạn connections
- ⚠️ Cần học MongoDB query

**Chi phí:**
- Free tier: $0/tháng
- Shared: $9/tháng

**Setup time:** 30 phút

---

### **Option 4: AWS S3 + DynamoDB** ⭐⭐⭐

**Ưu điểm:**
- ✅ Scalable vô hạn
- ✅ S3 cho file lớn (PDF, DOCX)
- ✅ DynamoDB cho metadata
- ✅ AWS Free Tier

**Nhược điểm:**
- ⚠️ Phức tạp setup
- ⚠️ Cần AWS account
- ⚠️ Pricing phức tạp

**Chi phí:**
- Free tier: $0/tháng (12 tháng đầu)
- Sau đó: ~$1-5/tháng

**Setup time:** 60 phút

---

### **Option 5: Streamlit Cloud + GitHub** ⭐⭐

**Ưu điểm:**
- ✅ Không cần database
- ✅ Version control tự động
- ✅ Miễn phí hoàn toàn

**Nhược điểm:**
- ❌ Không real-time
- ❌ Phải commit mỗi lần save
- ❌ Không scalable
- ❌ Không phù hợp cho production

**Chi phí:** $0

**Setup time:** 10 phút

---

## 📊 So sánh Chi tiết

| Feature | Supabase | Firebase | MongoDB | AWS | GitHub |
|---------|----------|----------|---------|-----|--------|
| **Miễn phí** | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| **Dễ setup** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Scalable** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| **Real-time** | ✅ | ✅ | ⚠️ | ⚠️ | ❌ |
| **Backup** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Python SDK** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🎯 Khuyến nghị Cuối cùng

### Cho dự án này: **SUPABASE**

**Lý do:**
1. Miễn phí, đủ dùng cho 1000+ users
2. Setup nhanh (30 phút)
3. PostgreSQL - Reliable, proven
4. Python SDK dễ dùng
5. Built-in authentication
6. Backup tự động
7. Dashboard quản lý trực quan

---

## 🚀 Implementation Plan

### Phase 1: Setup Supabase (30 phút)
1. Tạo account: https://supabase.com/
2. Tạo project mới
3. Tạo tables:
   - `projects`
   - `scenes`
   - `analysis_results`
   - `action_plans`
4. Get API keys

### Phase 2: Update Code (2 giờ)
1. Install `supabase-py`
2. Tạo `database.py` module
3. Update `utils.py` để dùng Supabase
4. Update `app.py` project management
5. Test local

### Phase 3: Deploy (30 phút)
1. Add Supabase keys vào Streamlit Secrets
2. Push code lên GitHub
3. Test production

**Tổng thời gian:** ~3 giờ

---

## 💾 Database Schema (Supabase)

### Table: `projects`
```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);
```

### Table: `scenes`
```sql
CREATE TABLE scenes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    scene_id TEXT NOT NULL,
    header TEXT NOT NULL,
    content TEXT NOT NULL,
    original_index INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Table: `analysis_results`
```sql
CREATE TABLE analysis_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    creative_report JSONB,
    marketing_report TEXT,
    summary JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Table: `action_plans`
```sql
CREATE TABLE action_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    user_strategy TEXT,
    plan JSONB,
    task_completion JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## 📝 Code Example

### `database.py` (New file)
```python
from supabase import create_client, Client
import streamlit as st

def get_supabase_client() -> Client:
    """Get Supabase client from secrets"""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def create_project(name, description=""):
    """Create new project"""
    supabase = get_supabase_client()
    data = {
        "user_id": st.session_state.get("user_id", "default"),
        "name": name,
        "description": description
    }
    result = supabase.table("projects").insert(data).execute()
    return result.data[0]

def get_projects():
    """Get all projects for current user"""
    supabase = get_supabase_client()
    user_id = st.session_state.get("user_id", "default")
    result = supabase.table("projects")\
        .select("*")\
        .eq("user_id", user_id)\
        .order("updated_at", desc=True)\
        .execute()
    return result.data

def save_scenes(project_id, scenes):
    """Save scenes for a project"""
    supabase = get_supabase_client()
    
    # Delete old scenes
    supabase.table("scenes")\
        .delete()\
        .eq("project_id", project_id)\
        .execute()
    
    # Insert new scenes
    data = [{
        "project_id": project_id,
        "scene_id": scene["id"],
        "header": scene["header"],
        "content": scene["content"],
        "original_index": scene["original_index"]
    } for scene in scenes]
    
    result = supabase.table("scenes").insert(data).execute()
    return result.data
```

---

## 🔐 Security

### Streamlit Secrets (`.streamlit/secrets.toml`)
```toml
GEMINI_API_KEY = "your_gemini_key"
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your_anon_key"
```

### Row Level Security (RLS)
```sql
-- Enable RLS
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own projects
CREATE POLICY "Users can view own projects"
ON projects FOR SELECT
USING (user_id = current_setting('app.user_id'));

-- Policy: Users can insert own projects
CREATE POLICY "Users can insert own projects"
ON projects FOR INSERT
WITH CHECK (user_id = current_setting('app.user_id'));
```

---

## 📈 Migration Plan

### Step 1: Parallel Run (1 tuần)
- Giữ JSON storage
- Thêm Supabase storage
- Sync cả hai

### Step 2: Testing (1 tuần)
- Test tất cả features
- Monitor errors
- Fix bugs

### Step 3: Full Migration (1 ngày)
- Remove JSON storage
- Chỉ dùng Supabase
- Update documentation

---

## 💰 Cost Estimate

### Free Tier (Đủ cho 1000 users):
- Database: 500MB
- Storage: 1GB
- Bandwidth: 2GB
- API requests: Unlimited

### Khi nào cần upgrade?
- > 500MB data (~5000 projects)
- > 50,000 monthly active users
- > 2GB bandwidth/tháng

**Ước tính:** Có thể dùng free tier 1-2 năm

---

## 🎯 Next Steps

1. **Đọc file này** - Hiểu phương án
2. **Quyết định** - Chọn Supabase hay option khác?
3. **Setup** - Làm theo hướng dẫn
4. **Test** - Thử nghiệm local
5. **Deploy** - Push lên production

**Tôi có thể giúp implement ngay nếu bạn muốn!**

---

**Created:** December 2, 2025  
**Status:** Proposal  
**Recommended:** Supabase PostgreSQL
