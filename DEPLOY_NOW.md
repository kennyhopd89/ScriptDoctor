# ⚡ DEPLOY NGAY - 5 PHÚT

**Code đã lên GitHub! Bây giờ deploy lên Streamlit Cloud.**

---

## 🎯 Bước 1: Vào Streamlit Cloud

**Link:** https://share.streamlit.io/

1. Click: **"Sign in with GitHub"**
2. Authorize Streamlit

---

## 🚀 Bước 2: Tạo App (2 phút)

1. Click: **"New app"**

2. Điền thông tin:
   ```
   Repository: kennyhopd89/ScriptDoctor
   Branch: main
   Main file path: app.py
   ```

3. Click: **"Deploy!"**

4. Đợi 3-5 phút (Streamlit đang install dependencies)

---

## 🔑 Bước 3: Thêm API Key (1 phút)

**QUAN TRỌNG:** App sẽ không chạy nếu thiếu bước này!

1. Trong Streamlit dashboard
2. Click vào app name
3. Click: **"Settings"** (⚙️)
4. Click: **"Secrets"**
5. Paste:

```toml
GEMINI_API_KEY = "your_actual_api_key_here"
```

**Thay bằng API key thật của bạn!**

6. Click: **"Save"**

App sẽ restart với API key.

---

## ✅ Bước 4: Test (2 phút)

### URL App:
`https://scriptdoctor-xxxxx.streamlit.app`

### Quick Test:
1. Vào Sidebar
2. Click "Kiểm tra kết nối"
3. Phải thấy: "Kết nối thành công! 🚀"

**Nếu OK → App đã LIVE!** 🎉

---

## 🐛 Nếu Có Lỗi:

### "API Key not found"
→ Quay lại Bước 3, thêm API key vào Secrets

### "ModuleNotFoundError"
→ Xem logs, có thể thiếu package (hiếm khi xảy ra)

### App chậm
→ Bình thường, free tier có giới hạn resources

---

## 📱 Share App

**URL của bạn:**
```
https://scriptdoctor-xxxxx.streamlit.app
```

Copy và share với team!

---

## 📚 Chi tiết hơn?

Đọc: `NEXT_STEPS.md`

---

**Chúc bạn deploy thành công! 🚀**
