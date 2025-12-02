import ai_engine

def analyze_character(full_script, character_name, api_key):
    """
    Analyzes a specific character's arc and presence in the script.
    """
    prompt = f"""
    Bạn là một Script Doctor. Hãy phân tích nhân vật "{character_name}" trong kịch bản sau.
    
    Yêu cầu Output (Markdown):
    1. **Tóm tắt Hành trình (Arc)**: Mô tả sự phát triển/thay đổi của nhân vật từ đầu đến cuối.
    2. **Vai trò**: Chính diện, phản diện, hay hỗ trợ? Mục tiêu của họ là gì?
    3. **Danh sách Scene xuất hiện**: Liệt kê các Scene ID mà nhân vật này có thoại hoặc hành động quan trọng (Dựa trên context).
    
    ---
    NỘI DUNG KỊCH BẢN:
    {full_script}
    """
    return ai_engine.generate_analysis(prompt, api_key)

def fix_character_issue(character_name, issue_description, related_scenes_content, api_key):
    """
    Suggests fixes for a specific character logic issue.
    """
    prompt = f"""
    Bạn là Script Doctor. Đang xử lý vấn đề logic của nhân vật "{character_name}".
    
    VẤN ĐỀ CẦN FIX: "{issue_description}"
    
    Dưới đây là nội dung các cảnh liên quan:
    {related_scenes_content}
    
    YÊU CẦU:
    Hãy đề xuất giải pháp sửa đổi cụ thể cho từng cảnh để giải quyết vấn đề trên mà không làm hỏng cấu trúc phim.
    Định dạng Output:
    - **Scene [ID]**: [Nội dung cần sửa/thêm/bớt]
    - **Lý do**: Tại sao sửa như vậy giải quyết được vấn đề.
    """
    return ai_engine.generate_analysis(prompt, api_key)
