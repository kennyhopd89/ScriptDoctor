# ✅ Deployment Checklist - Script Doctor Pro

## 📋 Trước khi Push lên GitHub

### Bảo mật
- [ ] File `.env` có trong `.gitignore`
- [ ] File `.streamlit/secrets.toml` có trong `.gitignore`
- [ ] Không có API key hardcoded trong code
- [ ] Đã xóa mọi thông tin nhạy cảm (email, phone, passwords)
- [ ] Kiểm tra `git status` - không có file nhạy cảm

### Code Quality
- [ ] Tất cả file Python chạy được (không có syntax error)
- [ ] `requirements.txt` đầy đủ dependencies
- [ ] README.md có hướng dẫn rõ ràng
- [ ] Đã test app locally: `streamlit run app.py`

### File Structure
- [ ] Có file `app.py` (entry point)
- [ ] Có file `requirements.txt`
- [ ] Có thư mục `.streamlit/` với `config.toml.example`
- [ ] Có thư mục `data/` với `.gitkeep`
- [ ] Có file `README.md` hoặc `README_GITHUB.md`

---

## 🚀 Push lên GitHub

### Khởi tạo Git
```bash
git init
git add .
git status  # Kiểm tra lại
git commit -m "Initial commit: Script Doctor Pro"
```

### Tạo GitHub Repository
1. Truy cập: https://github.com/new
2. Tên repo: `script-doctor-pro`
3. Chọn **Public** (để dùng Streamlit Cloud free)
4. **KHÔNG** chọn "Initialize with README"
5. Click "Create repository"

### Push Code
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### Xác nhận
- [ ] Code đã xuất hiện trên GitHub
- [ ] Không có file `.env` trên GitHub
- [ ] Không có file `secrets.toml` trên GitHub
- [ ] Không có thư mục `__pycache__/` hoặc `.venv/`

---

## ☁️ Deploy lên Streamlit Cloud

### Chuẩn bị
- [ ] Đã có GitHub repository (public)
- [ ] Đã có Gemini API Key
- [ ] Đã đăng ký tài khoản Streamlit Cloud

### Deploy Steps
1. Truy cập: https://share.streamlit.io/
2. Click "New app"
3. Chọn repository: `YOUR_USERNAME/YOUR_REPO_NAME`
4. Branch: `main`
5. Main file path: `app.py`
6. Click "Advanced settings"
7. Python version: `3.10`
8. Click "Deploy"

### Cấu hình Secrets
1. Trong Streamlit Cloud dashboard
2. Vào "Settings" → "Secrets"
3. Thêm:
```toml
GEMINI_API_KEY = "your_actual_api_key_here"
```
4. Click "Save"

### Kiểm tra
- [ ] App đã deploy thành công
- [ ] URL hoạt động: `https://your-app-name.streamlit.app`
- [ ] API key hoạt động (test "Kiểm tra kết nối")
- [ ] Upload PDF và parse scenes hoạt động
- [ ] AI analysis hoạt động
- [ ] Export DOCX hoạt động

---

## 🔄 Cập nhật sau Deploy

### Khi sửa code
```bash
git add .
git commit -m "Mô tả thay đổi"
git push
```

**Streamlit Cloud sẽ tự động redeploy!**

### Khi thay đổi dependencies
1. Cập nhật `requirements.txt`
2. Push lên GitHub
3. Streamlit Cloud sẽ rebuild

### Khi thay đổi secrets
1. Vào Streamlit Cloud dashboard
2. Settings → Secrets
3. Cập nhật giá trị
4. Click "Save" (app sẽ restart)

---

## 🐛 Troubleshooting

### App không start
- [ ] Kiểm tra logs trong Streamlit Cloud dashboard
- [ ] Xác nhận `requirements.txt` đúng format
- [ ] Xác nhận Python version tương thích

### API Key không hoạt động
- [ ] Kiểm tra Secrets đã nhập đúng
- [ ] Không có khoảng trắng thừa trong key
- [ ] Key chưa bị revoke trên Google AI Studio

### Import PDF lỗi
- [ ] Kiểm tra `pypdf` đã có trong `requirements.txt`
- [ ] PDF không bị password-protected
- [ ] PDF có text (không phải scan)

### Export DOCX lỗi
- [ ] Kiểm tra `python-docx` đã có trong `requirements.txt`
- [ ] Đã có scenes trong session state

---

## 📊 Monitoring

### Sau khi Deploy
- [ ] Kiểm tra app mỗi ngày trong tuần đầu
- [ ] Monitor usage trong Streamlit Cloud dashboard
- [ ] Theo dõi API costs trong Google AI Studio
- [ ] Đọc user feedback (nếu có)

### Performance
- [ ] App load time < 5 giây
- [ ] AI response time < 30 giây
- [ ] Không có memory leaks
- [ ] Session state được lưu đúng

---

## 🎉 Hoàn tất!

Khi tất cả checklist đã ✅:

**App của bạn đã sẵn sàng production!**

Share URL với users: `https://your-app-name.streamlit.app`

---

## 📞 Support Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [Streamlit Community](https://discuss.streamlit.io/)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [GitHub Issues](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/issues)

---

**Last Updated:** December 2, 2025
