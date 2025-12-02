# ⚡ Quick Deploy Guide - 20 phút

## 🎯 Mục tiêu
Deploy Script Doctor Pro lên Streamlit Cloud trong 20 phút.

---

## 📋 Chuẩn bị (2 phút)

### Cần có:
- [ ] Tài khoản GitHub (tạo tại: https://github.com/signup)
- [ ] Gemini API Key (lấy tại: https://ai.google.dev/)
- [ ] Git đã cài đặt trên máy

### Kiểm tra:
```bash
git --version  # Phải có output
```

---

## 🚀 Bước 1: Push lên GitHub (8 phút)

### 1.1 Khởi tạo Git
```bash
cd /path/to/ScriptDoctor_App
git init
git add .
git commit -m "Initial commit: Script Doctor Pro"
```

### 1.2 Tạo GitHub Repository
1. Mở: https://github.com/new
2. Repository name: `script-doctor-pro`
3. Chọn: **Public**
4. **KHÔNG** chọn "Initialize with README"
5. Click: **Create repository**

### 1.3 Push code
```bash
# Thay YOUR_USERNAME bằng username GitHub của bạn
git remote add origin https://github.com/YOUR_USERNAME/script-doctor-pro.git
git branch -M main
git push -u origin main
```

**Nhập username và password (hoặc Personal Access Token) khi được hỏi.**

### 1.4 Xác nhận
Mở: `https://github.com/YOUR_USERNAME/script-doctor-pro`

Phải thấy:
- ✅ File `app.py`
- ✅ File `requirements.txt`
- ✅ Thư mục `.streamlit/`
- ❌ KHÔNG có file `.env`

---

## ☁️ Bước 2: Deploy lên Streamlit Cloud (10 phút)

### 2.1 Đăng ký/Đăng nhập
1. Mở: https://share.streamlit.io/
2. Click: **Sign in with GitHub**
3. Authorize Streamlit

### 2.2 Tạo App mới
1. Click: **New app**
2. Điền thông tin:
   - **Repository:** `YOUR_USERNAME/script-doctor-pro`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Click: **Advanced settings**
4. **Python version:** `3.10`
5. Click: **Deploy**

### 2.3 Đợi Deploy (3-5 phút)
Streamlit sẽ:
- Clone repository
- Install dependencies
- Start app

**Đợi cho đến khi thấy app chạy.**

### 2.4 Cấu hình API Key
1. Trong Streamlit Cloud dashboard
2. Click vào app name
3. Click: **Settings** (góc phải)
4. Click: **Secrets**
5. Paste vào:
```toml
GEMINI_API_KEY = "your_actual_gemini_api_key_here"
```
6. Click: **Save**

**App sẽ tự động restart.**

---

## ✅ Bước 3: Test App (5 phút)

### 3.1 Mở App
URL sẽ có dạng: `https://your-app-name.streamlit.app`

### 3.2 Test các tính năng:
1. **Sidebar:**
   - [ ] Click "Kiểm tra kết nối" → Phải thấy "Kết nối thành công"

2. **Tab 1 - Review:**
   - [ ] Upload file PDF screenplay
   - [ ] Xem scenes được parse
   - [ ] Click "Phân tích Lại Kịch bản"
   - [ ] Xem báo cáo Creative + Marketing

3. **Tab 2 - Brainstorm:**
   - [ ] Chọn scene từ sidebar
   - [ ] Nhập director's note
   - [ ] Click "Brainstorm Ideas"
   - [ ] Xem các phương án AI đề xuất

4. **Tab 3 - Action Plan:**
   - [ ] Nhập chiến lược
   - [ ] Click "Lập Action Plan"
   - [ ] Test "AI Fix" cho một scene

5. **Export:**
   - [ ] Click "Tạo file Word (.docx)"
   - [ ] Download và mở file

### 3.3 Nếu có lỗi:
- Check logs trong Streamlit Cloud dashboard
- Xem phần Troubleshooting bên dưới

---

## 🎉 Hoàn tất!

**App của bạn đã live!**

Share URL với team: `https://your-app-name.streamlit.app`

---

## 🐛 Troubleshooting

### Lỗi: "Permission denied" khi push GitHub
**Giải pháp:**
```bash
# Dùng Personal Access Token thay vì password
# Tạo token tại: https://github.com/settings/tokens
# Chọn: repo (full control)
# Copy token và dùng làm password khi push
```

### Lỗi: "ModuleNotFoundError" trên Streamlit Cloud
**Giải pháp:**
- Kiểm tra `requirements.txt` có đầy đủ
- Xem logs để biết module nào thiếu
- Thêm vào `requirements.txt` và push lại

### Lỗi: "API Key not found"
**Giải pháp:**
1. Vào Settings → Secrets
2. Xác nhận có dòng: `GEMINI_API_KEY = "..."`
3. Không có khoảng trắng thừa
4. Save và đợi app restart

### Lỗi: "App is sleeping"
**Giải pháp:**
- Free tier có sleep sau không dùng
- Click vào URL để wake up
- Đợi 10-15 giây

### App chạy chậm
**Giải pháp:**
- Free tier có giới hạn resources
- Optimize code (giảm API calls)
- Hoặc upgrade lên paid tier

---

## 🔄 Cập nhật App sau này

### Khi sửa code:
```bash
git add .
git commit -m "Mô tả thay đổi"
git push
```

**Streamlit Cloud sẽ tự động redeploy!**

### Khi thay đổi API key:
1. Vào Streamlit Cloud dashboard
2. Settings → Secrets
3. Cập nhật key
4. Save (app sẽ restart)

---

## 📚 Tài liệu đầy đủ

Nếu cần chi tiết hơn:
- `DEPLOYMENT_SUMMARY.md` - Tổng quan đầy đủ
- `DEPLOYMENT_STREAMLIT_CLOUD.md` - Hướng dẫn chi tiết
- `GITHUB_SETUP.md` - Git & GitHub chi tiết
- `DEPLOYMENT_CHECKLIST.md` - Checklist đầy đủ

---

## 💡 Tips

1. **Bookmark URL app** để truy cập nhanh
2. **Monitor usage** trong Streamlit Cloud dashboard
3. **Check API costs** trong Google AI Studio
4. **Backup code** thường xuyên (Git push)
5. **Test trên mobile** để đảm bảo responsive

---

## 📞 Cần giúp?

- Streamlit Docs: https://docs.streamlit.io/
- Streamlit Community: https://discuss.streamlit.io/
- GitHub Issues: https://github.com/YOUR_USERNAME/script-doctor-pro/issues

---

**Chúc bạn deploy thành công! 🚀**
