# 🚀 Hướng dẫn Setup Supabase - 30 phút

## 📋 Tổng quan

Supabase sẽ thay thế lưu trữ JSON local, cho phép:
- ✅ Quản lý nhiều dự án song song
- ✅ Lưu trữ persistent (không mất data khi restart)
- ✅ Backup tự động
- ✅ Scalable cho nhiều users

---

## 🎯 Bước 1: Tạo Supabase Account (5 phút)

### 1.1 Đăng ký
1. Truy cập: https://supabase.com/
2. Click: **"Start your project"**
3. Sign up với GitHub (khuyến nghị) hoặc email

### 1.2 Tạo Project mới
1. Click: **"New project"**
2. Điền thông tin:
   ```
   Name: script-doctor-pro
   Database Password: [Tạo password mạnh]
   Region: Southeast Asia (Singapore) - gần VN nhất
   Pricing Plan: Free
   ```
3. Click: **"Create new project"**
4. Đợi 2-3 phút để Supabase setup database

---

## 🗄️ Bước 2: Tạo Database Schema (10 phút)

### 2.1 Mở SQL Editor
1. Trong Supabase dashboard
2. Click: **"SQL Editor"** (sidebar bên trái)
3. Click: **"New query"**

### 2.2 Run Schema Script
1. Mở file `supabase_schema.sql` trong project
2. Copy toàn bộ nội dung
3. Paste vào SQL Editor
4. Click: **"Run"** (hoặc Ctrl+Enter)

**Kết quả:** Sẽ thấy message "Success. No rows returned"

### 2.3 Verify Tables
1. Click: **"Table Editor"** (sidebar)
2. Phải thấy 4 tables:
   - `projects`
   - `scenes`
   - `analysis_results`
   - `action_plans`

---

## 🔑 Bước 3: Lấy API Keys (2 phút)

### 3.1 Vào Settings
1. Click: **"Settings"** (icon ⚙️ ở sidebar)
2. Click: **"API"**

### 3.2 Copy Keys
Bạn cần 2 keys:

**1. Project URL:**
```
https://xxxxxxxxxxxxx.supabase.co
```

**2. Anon/Public Key:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6...
```

**⚠️ LƯU Ý:** 
- KHÔNG dùng `service_role` key (key này có full access, không an toàn)
- Chỉ dùng `anon` key (key này có RLS protection)

---

## 💻 Bước 4: Cấu hình Local (5 phút)

### 4.1 Update `.env` file
```bash
# Thêm vào file .env
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 4.2 Update `.streamlit/secrets.toml`
```toml
# Thêm vào file .streamlit/secrets.toml
GEMINI_API_KEY = "your_gemini_key"
SUPABASE_URL = "https://xxxxxxxxxxxxx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 4.3 Install Dependencies
```bash
pip install supabase
```

Hoặc nếu dùng requirements.txt:
```bash
pip install -r requirements.txt
```

---

## 🧪 Bước 5: Test Connection (5 phút)

### 5.1 Test Script
Tạo file `test_supabase.py`:

```python
import streamlit as st
from database import get_supabase_client, create_project, get_projects

# Test connection
client = get_supabase_client()
if client:
    print("✅ Connected to Supabase!")
    
    # Test create project
    project = create_project("Test Project", "This is a test")
    if project:
        print(f"✅ Created project: {project['name']}")
        
        # Test get projects
        projects = get_projects()
        print(f"✅ Found {len(projects)} projects")
    else:
        print("❌ Failed to create project")
else:
    print("❌ Failed to connect to Supabase")
```

### 5.2 Run Test
```bash
streamlit run test_supabase.py
```

**Kết quả mong đợi:**
```
✅ Connected to Supabase!
✅ Created project: Test Project
✅ Found 1 projects
```

---

## 🚀 Bước 6: Deploy lên Streamlit Cloud (3 phút)

### 6.1 Push Code
```bash
git add .
git commit -m "Add: Supabase integration for project management"
git push
```

### 6.2 Update Streamlit Secrets
1. Vào Streamlit Cloud dashboard
2. Click vào app
3. Settings → Secrets
4. Thêm:
```toml
GEMINI_API_KEY = "your_gemini_key"
SUPABASE_URL = "https://xxxxxxxxxxxxx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```
5. Save

**App sẽ tự động restart với Supabase!**

---

## ✅ Bước 7: Verify Production (2 phút)

### 7.1 Test trên Production
1. Mở app: `https://your-app.streamlit.app`
2. Vào sidebar "Quản lý Dự án"
3. Click "Tạo dự án mới"
4. Nhập tên dự án
5. Upload PDF và parse scenes
6. Refresh page → Data vẫn còn!

### 7.2 Check Database
1. Vào Supabase dashboard
2. Table Editor → `projects`
3. Phải thấy project vừa tạo

---

## 🐛 Troubleshooting

### Lỗi: "Failed to connect to Supabase"
**Nguyên nhân:** Sai URL hoặc Key

**Giải pháp:**
1. Check lại URL và Key trong Supabase Settings → API
2. Đảm bảo dùng `anon` key, không phải `service_role`
3. Check không có khoảng trắng thừa

### Lỗi: "Row Level Security policy violation"
**Nguyên nhân:** RLS policies chưa được tạo

**Giải pháp:**
1. Vào SQL Editor
2. Run lại phần RLS trong `supabase_schema.sql`
3. Verify policies trong Table Editor → Policies

### Lỗi: "relation does not exist"
**Nguyên nhân:** Tables chưa được tạo

**Giải pháp:**
1. Vào SQL Editor
2. Run lại toàn bộ `supabase_schema.sql`
3. Check Table Editor để verify

### App chạy chậm
**Nguyên nhân:** Database ở region xa

**Giải pháp:**
1. Tạo project mới ở region gần hơn (Singapore)
2. Migrate data sang project mới
3. Update keys

---

## 📊 Monitoring

### Check Usage
1. Vào Supabase dashboard
2. Click: **"Settings"** → **"Usage"**
3. Monitor:
   - Database size
   - API requests
   - Bandwidth

### Free Tier Limits:
- Database: 500MB
- Storage: 1GB
- Bandwidth: 2GB/month
- API requests: Unlimited

**Ước tính:** Đủ cho 1000+ users, 5000+ projects

---

## 🔐 Security Best Practices

### 1. KHÔNG commit secrets
```bash
# Đảm bảo .env và secrets.toml trong .gitignore
echo ".env" >> .gitignore
echo ".streamlit/secrets.toml" >> .gitignore
```

### 2. Rotate keys định kỳ
- Mỗi 3-6 tháng
- Hoặc khi có nghi ngờ bị leak

### 3. Monitor logs
- Check Supabase logs thường xuyên
- Alert khi có activity bất thường

### 4. Backup data
- Supabase tự động backup daily
- Export manual backup mỗi tháng

---

## 📈 Next Steps

### Phase 1: Basic (Đã xong)
- ✅ Setup Supabase
- ✅ Create schema
- ✅ Test connection

### Phase 2: Integration (Tiếp theo)
- [ ] Update app.py để dùng database.py
- [ ] Implement project switcher
- [ ] Test multi-project workflow

### Phase 3: Advanced (Tương lai)
- [ ] Add user authentication
- [ ] Implement sharing/collaboration
- [ ] Add version history
- [ ] Export/Import projects

---

## 💡 Tips

1. **Bookmark Supabase dashboard** để truy cập nhanh
2. **Monitor usage** để tránh vượt free tier
3. **Backup keys** ở nơi an toàn
4. **Test local trước** khi deploy production
5. **Document changes** khi update schema

---

## 📞 Cần Giúp đỡ?

### Documentation:
- Supabase Docs: https://supabase.com/docs
- Python Client: https://supabase.com/docs/reference/python
- SQL Reference: https://www.postgresql.org/docs/

### Support:
- Supabase Discord: https://discord.supabase.com/
- GitHub Issues: https://github.com/supabase/supabase/issues

---

**Chúc bạn setup thành công! 🚀**

---

**Created:** December 2, 2025  
**Estimated Time:** 30 minutes  
**Difficulty:** ⭐⭐ (Medium)
