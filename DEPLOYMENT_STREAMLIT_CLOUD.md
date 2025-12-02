# 🚀 Hướng dẫn Deploy lên Streamlit Cloud

## Bước 1: Chuẩn bị Repository

### 1.1 Tạo file `.streamlit/secrets.toml` (cho production)
```toml
# Không commit file này lên GitHub!
# Sẽ nhập trực tiếp trên Streamlit Cloud dashboard
```

### 1.2 Cập nhật `.gitignore`
```
# Đã có sẵn trong project
.streamlit/secrets.toml
.env
data/
```

### 1.3 Kiểm tra `requirements.txt`
```
streamlit
pandas
python-dotenv
google-generativeai>=0.7.0
pypdf
python-docx
```

## Bước 2: Push lên GitHub

```bash
# Khởi tạo Git (nếu chưa có)
git init

# Add tất cả files
git add .

# Commit
git commit -m "Initial commit - Script Doctor Pro"

# Tạo repo trên GitHub và push
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Bước 3: Deploy trên Streamlit Cloud

1. Truy cập: https://share.streamlit.io/
2. Đăng nhập bằng GitHub
3. Click "New app"
4. Chọn repository: `YOUR_USERNAME/YOUR_REPO_NAME`
5. Branch: `main`
6. Main file path: `app.py`
7. Click "Deploy"

## Bước 4: Cấu hình Secrets

Trong Streamlit Cloud dashboard:
1. Vào "Settings" → "Secrets"
2. Thêm:
```toml
GEMINI_API_KEY = "your_actual_api_key_here"
```

## ✅ Hoàn tất!

App sẽ có URL dạng: `https://your-app-name.streamlit.app`

---

## 🔒 Lưu ý Bảo mật

- **KHÔNG** commit API keys vào GitHub
- Sử dụng Streamlit Secrets cho production
- File `.env` chỉ dùng cho local development
- Kiểm tra `.gitignore` trước khi push

---

## 🐛 Troubleshooting

### Lỗi: "ModuleNotFoundError"
→ Kiểm tra `requirements.txt` có đầy đủ dependencies

### Lỗi: "File not found" cho data/
→ App sẽ tự tạo thư mục `data/` khi chạy lần đầu

### App chạy chậm
→ Streamlit Cloud free tier có giới hạn resources
→ Cân nhắc upgrade hoặc optimize code
