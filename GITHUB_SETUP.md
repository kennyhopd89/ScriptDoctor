# 📦 Hướng dẫn Push lên GitHub

## Bước 1: Kiểm tra trước khi Push

### 1.1 Xác nhận .gitignore đã đúng
```bash
# Kiểm tra file nào sẽ được commit
git status
```

**Đảm bảo KHÔNG có:**
- `.env` (chứa API keys)
- `.streamlit/secrets.toml`
- `data/*.json` (session data)
- `__pycache__/`
- `.venv/`

### 1.2 Xóa API key khỏi code (nếu có)
Kiểm tra không có hardcoded API keys trong:
- `app.py`
- `ai_engine.py`
- Bất kỳ file Python nào

---

## Bước 2: Khởi tạo Git Repository

```bash
# Nếu chưa có Git repo
git init

# Thêm tất cả files (trừ những file trong .gitignore)
git add .

# Kiểm tra lại lần cuối
git status

# Commit
git commit -m "Initial commit: Script Doctor Pro - AI Screenplay Assistant"
```

---

## Bước 3: Tạo Repository trên GitHub

### 3.1 Trên GitHub.com:
1. Đăng nhập GitHub
2. Click nút "+" → "New repository"
3. Đặt tên: `script-doctor-pro` (hoặc tên bạn muốn)
4. Chọn **Public** (để dùng Streamlit Cloud free)
5. **KHÔNG** chọn "Initialize with README" (vì đã có local)
6. Click "Create repository"

### 3.2 Link Local với GitHub:
```bash
# Thay YOUR_USERNAME và YOUR_REPO_NAME
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Đổi branch sang main (nếu đang là master)
git branch -M main

# Push lên GitHub
git push -u origin main
```

---

## Bước 4: Xác nhận trên GitHub

Truy cập: `https://github.com/YOUR_USERNAME/YOUR_REPO_NAME`

**Kiểm tra:**
- ✅ Có file `app.py`, `requirements.txt`, `README.md`
- ✅ Có thư mục `.streamlit/` (nhưng không có `secrets.toml`)
- ✅ Có thư mục `data/` (nhưng rỗng, chỉ có `.gitkeep`)
- ❌ KHÔNG có `.env`
- ❌ KHÔNG có `__pycache__/`
- ❌ KHÔNG có `.venv/`

---

## Bước 5: Cập nhật sau này

```bash
# Sau khi sửa code
git add .
git commit -m "Mô tả thay đổi"
git push
```

---

## 🔒 Checklist Bảo mật

Trước khi push, đảm bảo:

- [ ] File `.env` đã có trong `.gitignore`
- [ ] File `.streamlit/secrets.toml` đã có trong `.gitignore`
- [ ] Không có API key nào trong code
- [ ] File `data/*.json` không được commit
- [ ] Đã xóa mọi thông tin nhạy cảm khỏi code

---

## ⚠️ Nếu Đã Push Nhầm API Key

**NGAY LẬP TỨC:**

1. **Revoke API key cũ** trên Google AI Studio
2. **Tạo API key mới**
3. **Xóa key khỏi Git history:**
```bash
# Cài BFG Repo-Cleaner
# https://rtyley.github.io/bfg-repo-cleaner/

# Xóa file chứa secrets
bfg --delete-files .env

# Force push
git push --force
```

4. **Cập nhật key mới** trong Streamlit Cloud Secrets

---

## 📞 Hỗ trợ

Nếu gặp lỗi:
- `git status` - Xem trạng thái hiện tại
- `git log` - Xem lịch sử commit
- `git remote -v` - Xem remote URL

**Lỗi thường gặp:**

### "Permission denied (publickey)"
→ Cần setup SSH key hoặc dùng HTTPS với Personal Access Token

### "Repository not found"
→ Kiểm tra lại URL remote: `git remote -v`

### "Large files detected"
→ Kiểm tra `.gitignore`, có thể đang commit nhầm `.venv/` hoặc file lớn
