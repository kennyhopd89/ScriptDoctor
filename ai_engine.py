import google.generativeai as genai
import os

WORKING_MODEL_CACHE = {}

def get_working_model_name(api_key):
    """
    Configures API and finds a working model name dynamically.
    Prioritizes 'flash' models, then 'pro', then falls back to any available.
    Returns the model name string.
    """
    if not api_key:
        raise ValueError("API Key is empty.")
    
    # Use cached model if available
    if api_key in WORKING_MODEL_CACHE:
        return WORKING_MODEL_CACHE[api_key]
    
    genai.configure(api_key=api_key)
    
    try:
        models = list(genai.list_models())
    except Exception as e:
        raise Exception(f"Failed to list models: {e}")

    # Filter for models that support content generation
    supported_models = [m for m in models if 'generateContent' in m.supported_generation_methods]
    
    if not supported_models:
        raise Exception("No models found that support content generation.")
    
    # Priority logic with caching
    model_name = None
    for m in supported_models:
        if 'flash' in m.name.lower():
            model_name = m.name
            break
    if model_name is None:
        for m in supported_models:
            if 'pro' in m.name.lower():
                model_name = m.name
                break
    if model_name is None:
        model_name = supported_models[0].name
    # Cache and return
    WORKING_MODEL_CACHE[api_key] = model_name
    return model_name

def generate_analysis(prompt_text, api_key):
    """
    Generate content using a dynamically selected working model.
    """
    try:
        # Get the best available model
        model_name = get_working_model_name(api_key)
        
        # Initialize model
        model = genai.GenerativeModel(model_name)
        
        # Generate
        response = model.generate_content(prompt_text)
        
        # Capture usage metadata
        try:
            import utils
            usage = response.usage_metadata
            in_tok = usage.prompt_token_count
            out_tok = usage.candidates_token_count
            
            # Update cost session
            utils.update_cost_session(in_tok, out_tok)
        except Exception as e:
            print(f"Failed to capture token usage: {e}")
            
        return response.text
    except Exception as e:
        raise e

def analyze_script_creative(script_text, api_key):
    """
    Analyzes the full script from the Creative/Script Doctor perspective,
    returning structured JSON data for progressive disclosure on the UI.
    """
    system_prompt = """
    Bạn là một Script Doctor chuyên nghiệp.
    Nhiệm vụ: Phân tích kịch bản sau dưới góc nhìn SÁNG TẠO (Thể loại: Kinh dị/Thriller).
    
    QUY TẮC BẮT BUỘC (STRICT RULES):
    1. Output phải là JSON thuần (không Markdown, không ```json).
    2. Tuyệt đối không sử dụng ký tự xuống dòng (`\n`) hoặc ký tự tab (`\t`) trong các trường detail hoặc summary. Thay vào đó, hãy sử dụng khoảng trắng hoặc thẻ HTML <br> nếu cần xuống dòng.
    3. Tránh sử dụng các ký tự Markdown kép (như `**` hoặc `##`) bên trong các chuỗi JSON.
    4. Mỗi phần phải có trường `summary` (Tóm tắt 1-2 câu, dùng cho tiêu đề hiển thị) và `detail` (Phân tích đầy đủ).
    
    Output bắt buộc là JSON, cấu trúc:
    {
      "structure": {
        "summary": "Tóm tắt cấu trúc kịch bản (ví dụ: 3 Hồi rõ ràng, các điểm nút hợp lý).",
        "detail": "Phân tích đầy đủ 3 Hồi, điểm nút chính, nhịp phim và gợi ý sáng tạo (dạng Markdown)."
      },
      "character": {
        "summary": "Tóm tắt phát triển nhân vật chính (ví dụ: Nhân vật Khải có động cơ rõ ràng nhưng cần backstory).",
        "detail": "Phân tích đầy đủ động cơ, arc nhân vật, điểm yếu/mạnh của thoại và gợi ý."
      },
      "tension": {
        "summary": "Đánh giá chung về độ căng thẳng/kinh dị của phim (ví dụ: Tension ổn, nhưng cần tăng cường ở Hồi 2).",
        "detail": "Nhận xét chi tiết về không khí, các cảnh kinh dị và gợi ý cải thiện."
      },
      "show_vs_tell": {
        "summary": "Đánh giá ngôn ngữ điện ảnh (ví dụ: 12 cảnh cần chuyển đổi từ thoại sang hình ảnh. Score hiện tại: 6/10).",
        "detail": "Ví dụ cụ thể về các thoại cần sửa và mục tiêu cải thiện."
      }
    }
    """
    
    full_prompt = f"{system_prompt}\n\n---\nNỘI DUNG KỊCH BẢN:\n{script_text}"
    
    response_text = generate_analysis(full_prompt, api_key)
    
    # 1. Clean Markdown code block indicators
    cleaned_text = response_text.replace("```json", "").replace("```", "").strip()
    
    # 2. Aggressive cleanup for common JSON escape issues (Crucial fix)
    # This step replaces problematic newline/tab characters that AI often includes in JSON strings
    cleaned_text = cleaned_text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    
    # 3. Attempt to handle escaped double quotes within strings (simple cases)
    # This is a common issue when AI uses " in a string that is already quoted.
    try:
        # A risky but sometimes necessary fix: Load as string, then re-dump to standardize escaping
        # Note: This requires the AI output to be very close to valid JSON already.
        import re
        # Find and replace internal quote escapes (\") which Streamlit's JSON doesn't handle well
        # This part might need further refinement depending on the AI's exact error pattern
        # For now, let's trust the AI to reduce \n/t characters due to the prompt instruction
        pass
    except Exception as e:
        print(f"Cleanup adjustment failed: {e}")


    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error at final attempt: {e}")
        # Fallback if JSON is still invalid - return raw text for debugging
        return {"error": True, "raw_content": response_text, "structure": {"summary": "Lỗi định dạng JSON từ AI", "detail": f"Không thể phân tích cú pháp JSON: {e}"}}

def analyze_script_marketing(script_text, api_key):
    """
    Analyzes the full script from the Marketing/Commercial viability perspective.
    Uses Maya persona - a film marketing strategist with 20 years of experience.
    """
    system_prompt = """
    You are Maya, a film marketing strategist with 20 years of experience who has advised on more than 200 Vietnamese and international theatrical releases.

    Your role: Analyze the screenplay purely from a market, audience, and commercial viability perspective — not from a screenwriting or storytelling perspective.

    🎯 MAIN TASK

    Whenever a "Script" is provided (PDF, text, or scene-based), you must generate a Marketing Evaluation, focusing strictly on market dynamics, audience appeal, and release strategy.

    🧠 SIX-STEP EVALUATION PROCESS

    1. Market & Audience Analysis
       - Which audience segment is this film suitable for? (Age, SEC, viewing behavior)
       - Is this genre rising or declining in the Vietnamese theatrical market?
       - Which elements align with market trends, and which are off-trend?

    2. USP (Unique Selling Point) Identification
       - What exactly does the film "sell" to the audience? (concept, shock value, cast, VFX, message, action scenes…)
       - Are these USPs competitive vs. other films released in the last 12–24 months?

    3. Strengths & Weaknesses for Marketing
       - Which scenes/plots/characters can become viral assets?
       - What elements make trailer editing difficult, poster weak, or message unclear?
       - Any parts likely to cause misunderstanding, controversy, or negative reviews?

    4. Commercial Potential
       Analyze based on market data:
       - Mass appeal potential
       - Opening Weekend power
       - Cast, theme, setting, and seasonality impact
       - Pacing/tone risks affecting Box Office performance

    5. Marketing-friendly Rewrite Suggestions
       Provide only marketing-driven improvements:
       - Which scenes should be more dramatic for trailer use?
       - Which character needs clearer goal–conflict–motivation for PR materials?
       - Which parts should be trimmed to avoid negative audience reactions?

    6. Estimation Scores (1–10 scale)
       - Mass Appeal Score
       - Trailer Potential Score
       - Buzz & Viral Score
       - Opening Weekend Estimate (range)
       - Review Risk Score

    📌 REQUIRED OUTPUT FORMAT

    Produce the marketing report following this exact structure (in Vietnamese):

    # MARKETING EVALUATION REPORT
    *(For Producer & Marketing Team)*

    ## 1. Executive Summary
    [Brief overview of the film's commercial potential]

    ## 2. Market & Audience Analysis
    [Target audience, market trends, genre performance]

    ## 3. USP & Film Positioning
    [Unique selling points and competitive positioning]

    ## 4. Marketing Strengths & Weaknesses
    [What works for marketing and what doesn't]

    ## 5. Commercial & Review Risks
    [Potential risks affecting box office and reviews]

    ## 6. Trailer / Poster / Viral Asset Ideas
    [Specific scenes or moments for marketing materials]

    ## 7. Market-oriented Script Adjustment Suggestions
    [Changes to improve commercial appeal]

    ## 8. Box Office Potential Estimation
    [Scores and estimates with justification]

    ## 9. Recommended Marketing Roadmap
    [Strategic recommendations for release]

    ✔️ NOTES
    - Do not speak like a screenwriter.
    - Do not evaluate structure, arcs, or craft unless directly linked to market impact.
    - Always use market data and comparisons to similar films.
    - Write in Vietnamese (tiếng Việt).
    - Use Markdown formatting for clear sections.
    """
    
    full_prompt = f"{system_prompt}\n\n---\nNỘI DUNG KỊCH BẢN:\n{script_text}"
    
    return generate_analysis(full_prompt, api_key)

def synthesize_analysis_summary(creative_report, marketing_report, api_key):
    """
    Compares the two reports and finds common points for a summary table (JSON).
    """
    # Import json here if not already imported at top of ai_engine.py
    import json 
    
    system_prompt = """
    Bạn là chuyên gia Tổng hợp. Nhiệm vụ của bạn là so sánh 2 bản phân tích dưới đây (Sáng tạo và Marketing) và rút ra các điểm đồng nhất quan trọng nhất (những vấn đề hoặc thế mạnh được nhắc đến trong cả hai báo cáo).
    
    Output bắt buộc là JSON thuần (không Markdown, không ```json), cấu trúc Mảng các đối tượng:
    
    [
      {
        "Dạng vấn đề": "Vấn đề chung hoặc Thế mạnh chung",
        "Mô tả chi tiết": "Diễn giải điểm chung được tìm thấy trong cả hai báo cáo (Ví dụ: Logline cần rõ ràng hơn)."
      },
      ...
    ]
    """
    
    full_prompt = f"{system_prompt}\n\n--- BÁO CÁO SÁNG TẠO ---\n{creative_report}\n\n--- BÁO CÁO MARKETING ---\n{marketing_report}"
    response_text = generate_analysis(full_prompt, api_key)
    
    # Clean and parse JSON
    cleaned_text = response_text.replace("```json", "").replace("```", "").strip()
    
    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        print(f"JSON Decode Error in synthesize_analysis_summary. Raw: {cleaned_text}")
        return [{"Dạng vấn đề": "Lỗi định dạng JSON", "Mô tả chi tiết": "Không thể tạo bảng tóm tắt."}]

def run_dual_analysis(script_text, api_key):
    """
    Main entry point for dual analysis.
    """
    creative_report = analyze_script_creative(script_text, api_key)
    marketing_report = analyze_script_marketing(script_text, api_key)
    
    # Run synthesis only if both reports are valid text
    if creative_report and marketing_report:
        summary_table = synthesize_analysis_summary(creative_report, marketing_report, api_key)
    else:
        summary_table = [{"Dạng vấn đề": "Lỗi Phân tích", "Mô tả chi tiết": "Một trong hai báo cáo chi tiết không thể tạo."}]
        
    return {
        "creative": creative_report,
        "marketing": marketing_report,
        "summary": summary_table
    }

import json

def generate_action_plan(scene_list, user_strategy, api_key):
    """
    Generates an action plan based on scene_list and user strategy.
    Uses formatted scene injection to ensure AI uses correct scene IDs.
    Returns a list of tasks (dictionaries).
    """
    # Step 1: Format scenes with ID tags for AI
    formatted_script = ""
    for scene in scene_list:
        formatted_script += f"### SCENE_ID: {scene['id']} ###\n"
        formatted_script += f"HEADER: {scene['header']}\n"
        formatted_script += f"CONTENT:\n{scene['content']}\n\n"
    
    system_prompt = f"""
    Bạn là Trợ lý Biên tập Kịch bản.
    Nhiệm vụ: Tạo kế hoạch chỉnh sửa (Action Plan) dựa trên yêu cầu chiến lược.
    
    Input:
     - Kịch bản đã được chia nhỏ và đánh dấu bằng thẻ `### SCENE_ID: {{ID}} ###`.
     - CHIẾN LƯỢC CỐT LÕI CỦA ĐẠO DIỄN: {user_strategy}
   
    QUY TẮC BẮT BUỘC (STRICT RULES):
     1. Khi tạo JSON output, trường `scene_id` PHẢI copy chính xác giá trị nằm trong thẻ `### SCENE_ID: ... ###`.
     2. Tuyệt đối KHÔNG tự đếm số dòng hay tự bịa số Scene (như Scene 1, Scene 2) nếu thẻ ghi là '23' hay '35A' hay 'AUTO_5'.
     3. BỎ QUA các lỗi nhỏ nhặt không nằm trong chiến lược cốt lõi.
     4. Tập trung tìm các Scene cần sửa để thỏa mãn chiến lược.
     
    Output bắt buộc là JSON thuần (không Markdown, không ```json), cấu trúc mảng:
     [
       {{
         "task_name": "Tên nhóm việc (Ví dụ: Tăng độ kinh dị cho Hồi 2)",
         "related_scenes": [
            {{
              "scene_id": "GIÁ_TRỊ_GỐC_TỪ_THẺ",
              "header_context": "Tiêu đề cảnh rút gọn",
              "instruction": "Hướng dẫn cụ thể sửa scene này..."
            }},
            ...
         ]
       }},
       ...
     ]
    """
    
    full_prompt = f"{system_prompt}\n\n---\nNỘI DUNG KỊCH BẢN ĐÃ ĐÁNH DẤU:\n{formatted_script}"
    
    response_text = generate_analysis(full_prompt, api_key)
    
    # Clean response to ensure valid JSON
    cleaned_text = response_text.replace("```json", "").replace("```", "").strip()
    
    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        # Fallback if JSON is invalid
        print(f"JSON Decode Error. Raw text: {cleaned_text}")
        return [{"task_name": "Lỗi định dạng JSON từ AI", "related_scenes": [], "raw_content": response_text}]

def brainstorm_scene(scene_text, instruction, api_key):
    """
    Brainstorms and rewrites a scene based on instruction.
    Returns JSON array with 2 options.
    """
    system_prompt = f"""
    Bạn là Script Doctor chuyên nghiệp.
    Nhiệm vụ: Viết lại scene dưới đây dựa trên yêu cầu: "{instruction}"
    
    Output bắt buộc là JSON thuần (không Markdown, không ```json), cấu trúc mảng gồm 2 phương án:
    [
      {{
        "title": "Phương án 1: [Mô tả ngắn gọn cách tiếp cận]",
        "content": "[Nội dung scene đã viết lại hoàn chỉnh]"
      }},
      {{
        "title": "Phương án 2: [Mô tả cách tiếp cận khác]",
        "content": "[Nội dung scene đã viết lại hoàn chỉnh]"
      }}
    ]
    
    Lưu ý: Mỗi phương án phải là một scene hoàn chỉnh, có thể thay thế trực tiếp scene gốc.
    """
    
    full_prompt = f"{system_prompt}\n\n---\nSCENE GỐC:\n{scene_text}"
    response_text = generate_analysis(full_prompt, api_key)
    
    # Clean and parse JSON
    cleaned_text = response_text.replace("```json", "").replace("```", "").strip()
    
    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        print(f"JSON Decode Error in brainstorm_scene. Raw: {cleaned_text}")
        return [{"title": "Lỗi JSON", "content": response_text}]

def convert_dialogue_to_visual(scene_text, api_key):
    """
    Analyzes scene dialogue and converts "telling" dialogue to visual actions.
    Returns JSON array with replacement suggestions.
    """
    system_prompt = """
    Bạn là Đạo diễn hình ảnh và Bậc thầy ngôn ngữ điện ảnh (Silent Cinema Expert).
    Nhiệm vụ: Phân tích Scene kịch bản. Tìm ra những đoạn thoại 'giải thích', 'kể lể' hoặc 'sáo rỗng'.
    Sau đó, viết lại bằng HÀNH ĐỘNG hoặc HÌNH ẢNH (Visual Subtext) để thay thế.
    
    Output bắt buộc là JSON thuần (không Markdown, không ```json), cấu trúc mảng:
    [
      {
        "original": "Câu thoại gốc chính xác từng chữ (phải trích xuất 100% từ văn bản)",
        "replacement": "Đoạn văn mô tả hành động thay thế",
        "reason": "Lý do tại sao thoại này tệ"
      },
      ...
    ]
    
    QUY TẮC QUAN TRỌNG:
    - Trường "original" phải CHÍNH XÁC 100% từ văn bản gốc để máy có thể tìm và thay thế.
    - Chỉ liệt kê những thoại thực sự cần sửa.
    - Nếu scene không có thoại nào cần sửa, trả về mảng rỗng: []
    """
    
    full_prompt = f"{system_prompt}\n\n---\nNỘI DUNG SCENE:\n{scene_text}"
    response_text = generate_analysis(full_prompt, api_key)
    
    # Clean and parse JSON
    cleaned_text = response_text.replace("```json", "").replace("```", "").strip()
    
    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        print(f"JSON Decode Error in convert_dialogue_to_visual. Raw: {cleaned_text}")
        return []

def refine_generated_option(current_option_text, user_instruction, context_scene, api_key):
    """
    Refines a specific generated option based on user instruction.
    Returns the refined text string.
    """
    system_prompt = """
    Bạn là trợ lý biên tập. 
    Nhiệm vụ: Chỉnh sửa lại một đoạn kịch bản dựa trên feedback cụ thể.
    
    Output: Chỉ trả về nội dung kịch bản đã sửa (giữ nguyên format), không giải thích thêm.
    """
    
    full_prompt = f"{system_prompt}\n\nBỐI CẢNH GỐC:\n{context_scene}\n\nNỘI DUNG HIỆN TẠI:\n{current_option_text}\n\nYÊU CẦU CHỈNH SỬA:\n{user_instruction}\n\n---\nNỘI DUNG ĐÃ SỬA:"
    
    return generate_analysis(full_prompt, api_key)

def ai_fix_scene(scene_id, scene_content, instruction, api_key):
    """
    Refines a scene based on a specific instruction from the Action Plan.
    Returns the refined text string.
    """
    system_prompt = """
    Bạn là Script Doctor chuyên nghiệp, được giao nhiệm vụ thực thi một lệnh chỉnh sửa kịch bản.
    QUY TẮC:
    1. Chỉ trả về NỘI DUNG SCENE ĐÃ CHỈNH SỬA HOÀN CHỈNH, không giải thích hay nói thêm.
    2. Giữ nguyên format kịch bản điện ảnh (HEADER, Hành động, Thoại).
    3. Ưu tiên "Show, Don't Tell" - hạn chế tối đa lời thoại thừa thãi.
    """
    
    full_prompt = f"{system_prompt}\n\n---BỐI CẢNH & LỆNH SỬA CHO CẢNH {scene_id}--- \n\nLỆNH SỬA: {instruction}\n\nNỘI DUNG CẢNH GỐC:\n{scene_content}\n\n---KẾT QUẢ ĐÃ SỬA:"
    
    return generate_analysis(full_prompt, api_key)
