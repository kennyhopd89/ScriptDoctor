# 🚀 Supabase Setup - Bước tiếp theo

## ✅ Đã hoàn thành

1. ✅ Code đã được push lên GitHub
2. ✅ Database module đã implement
3. ✅ Project management UI đã update
4. ✅ Auto-save đã tích hợp
5. ✅ Supabase credentials đã cấu hình

---

## 📋 Bước tiếp theo (5 phút)

### Bước 1: Run SQL Schema trên Supabase

1. **Mở Supabase Dashboard:**
   - Truy cập: https://supabase.com/dashboard/project/jmpmmgljqnmqkvypzsgi

2. **Vào SQL Editor:**
   - Click "SQL Editor" ở sidebar bên trái
   - Click "New query"

3. **Copy & Run Schema:**
   - Mở file `supabase_schema.sql` trong project
   - Copy toàn bộ nội dung (Ctrl+A, Ctrl+C)
   - Paste vào SQL Editor
   - Click "Run" (hoặc Ctrl+Enter)

4. **Verify:**
   - Phải thấy message: "Success. No rows returned"
   - Click "Table Editor" → Phải thấy 4 tables:
     - `projects`
     - `scenes`
     - `analysis_results`
     - `action_plans`

---

### Bước 2: Test Local (2 phút)

```bash
# Test Supabase connection
streamlit run test_supabase.py
```

**Kết quả mong đợi:**
- ✅ Supabase is configured!
- ✅ Connected to Supabase!
- ✅ All tables exist!
- ✅ Can create test project

**Nếu có lỗi:**
- Check `.streamlit/secrets.toml` có đúng keys không
- Check đã run SQL schema chưa
- Check internet connection

---

### Bước 3: Test Main App (3 phút)

```bash
# Run main app
streamlit run app.py
```

**Test workflow:**

1. **Tạo dự án mới:**
   - Vào Sidebar → "Quản lý Dự án"
   - Click "+ Tạo dự án mới"
   - Nhập tên: "Test Project 1"
   - Click "Tạo"
   - ✅ Phải thấy: "Đã tạo: Test Project 1"

2. **Upload PDF:**
   - Tab 1: "Review & Phân tích"
   - Upload file PDF screenplay
   - ✅ Scenes được parse
   - ✅ Data được lưu vào database

3. **Refresh page:**
   - Refresh browser (F5)
   - ✅ Data vẫn còn! (không mất như trước)

4. **Tạo dự án thứ 2:**
   - Click "+ Tạo dự án mới"
   - Nhập tên: "Test Project 2"
   - Upload PDF khác
   - ✅ Có 2 projects trong dropdown

5. **Switch giữa projects:**
   - Chọn "Test Project 1" từ dropdown
   - ✅ Scenes của Project 1 hiện ra
   - Chọn "Test Project 2"
   - ✅ Scenes của Project 2 hiện ra

6. **Lưu thủ công:**
   - Edit một scene
   - Click "⚙️ Tùy chọn dự án" → "💾 Lưu dự án"
   - ✅ Thấy "Đã lưu!"

7. **Xóa project:**
   - Click "⚙️ Tùy chọn dự án" → "🗑️ Xóa dự án"
   - Confirm
   - ✅ Project bị xóa khỏi dropdown

---

### Bước 4: Verify trên Supabase Dashboard (1 phút)

1. Vào Supabase Dashboard
2. Click "Table Editor"
3. Click table "projects"
4. ✅ Phải thấy projects vừa tạo
5. Click table "scenes"
6. ✅ Phải thấy scenes của projects

---

### Bước 5: Deploy lên Streamlit Cloud (5 phút)

**Code đã được push, giờ chỉ cần update secrets:**

1. **Vào Streamlit Cloud:**
   - https://share.streamlit.io/
   - Click vào app "ScriptDoctor"

2. **Update Secrets:**
   - Settings → Secrets
   - Thêm (hoặc update):
   ```toml
   GEMINI_API_KEY = "your_gemini_key"
   SUPABASE_URL = "https://jmpmmgljqnmqkvypzsgi.supabase.co"
   SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImptcG1tZ2xqcW5tcWt2eXB6c2dpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ2NTk3NjEsImV4cCI6MjA4MDIzNTc2MX0.wBnXflqSaLOe_eD-s43EABDi_vHNmhFjtnmM3b1G3JE"
   ```
   - Click "Save"

3. **Wait for Restart:**
   - App sẽ tự động restart (1-2 phút)

4. **Test Production:**
   - Mở app URL
   - Test tạo project, upload PDF
   - Refresh page → Data vẫn còn!

---

## 🎉 Hoàn tất!

**Bạn đã có:**
- ✅ Multi-project management
- ✅ Persistent data storage
- ✅ Auto-save
- ✅ Scalable database
- ✅ Backup tự động

---

## 📊 Monitoring

### Check Supabase Usage:
1. Vào Supabase Dashboard
2. Settings → Usage
3. Monitor:
   - Database size
   - API requests
   - Bandwidth

### Free Tier Limits:
- Database: 500MB (đủ cho ~5000 projects)
- API requests: Unlimited
- Bandwidth: 2GB/month

**Ước tính:** Đủ dùng 1-2 năm với traffic thấp

---

## 🐛 Troubleshooting

### Lỗi: "Supabase chưa được cấu hình"
**Giải pháp:**
- Check `.streamlit/secrets.toml` có đúng keys
- Restart app

### Lỗi: "relation does not exist"
**Giải pháp:**
- Chưa run SQL schema
- Vào SQL Editor và run `supabase_schema.sql`

### Lỗi: "Row Level Security policy violation"
**Giải pháp:**
- RLS policies chưa được tạo
- Run lại phần RLS trong SQL schema

### Data không persist
**Giải pháp:**
- Check auto_save() được gọi sau các thao tác
- Check database.save_current_project() hoạt động
- Check logs trong Supabase

---

## 💡 Tips

1. **Backup thường xuyên:**
   - Supabase tự động backup daily
   - Export manual backup mỗi tháng

2. **Monitor usage:**
   - Check usage mỗi tuần
   - Alert khi gần limit

3. **Security:**
   - KHÔNG commit secrets vào Git
   - Rotate keys mỗi 6 tháng

4. **Performance:**
   - Index được tạo tự động
   - Monitor slow queries trong Supabase

---

## 🎯 Next Features (Optional)

### Phase 1: User Authentication
- Google OAuth
- Email/Password
- User profiles

### Phase 2: Collaboration
- Share projects
- Real-time editing
- Comments

### Phase 3: Advanced
- Version history
- Export/Import
- Analytics

---

## 📞 Cần Giúp?

### Documentation:
- `DATA_STORAGE_PLAN.md` - Phân tích phương án
- `SUPABASE_SETUP.md` - Setup chi tiết
- `PROJECT_MANAGEMENT_PLAN.md` - Implementation plan

### External:
- Supabase Docs: https://supabase.com/docs
- Supabase Discord: https://discord.supabase.com/

---

**Chúc bạn thành công! 🚀**

---

**Created:** December 2, 2025  
**Status:** Ready to deploy  
**Next:** Run SQL schema → Test → Deploy
