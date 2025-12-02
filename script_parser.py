import pypdf
import io
import re

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file uploaded via Streamlit.
    """
    try:
        pdf_reader = pypdf.PdfReader(uploaded_file)
        text = ""
        
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def clean_text(raw_text):
    """
    Pre-processing: Clean PDF artifacts.
    """
    lines = raw_text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            continue
            
        # Skip standalone page numbers
        if stripped.isdigit():
            continue
        if stripped.lower().startswith("page ") and len(stripped.split()) == 2:
            continue
            
        cleaned_lines.append(stripped)
    
    return '\n'.join(cleaned_lines)

def parse_scenes(full_text):
    """
    Multi-layer scene detection with real ID extraction.
    Uses 3-layer detection strategy to catch all scene headers.
    """
    cleaned_text = clean_text(full_text)
    lines = cleaned_text.split('\n')
    
    scenes = []
    current_scene_lines = []
    current_header = None
    current_scene_id = None
    auto_counter = 0
    
    for line_idx, line in enumerate(lines):
        stripped = line.strip()
        
        if not stripped:
            continue
        
        is_header = False
        extracted_id = None
        clean_header = stripped
        
        # LAYER 1: Detect duplicate number pattern (PDF error: "...NIGHT11 11")
        layer1_pattern = r'^(.*?)\s+([0-9]+[A-Z]?)\s+\2\s*$'
        layer1_match = re.match(layer1_pattern, stripped)
        
        if layer1_match:
            is_header = True
            extracted_id = layer1_match.group(2)
            clean_header = layer1_match.group(1).strip()
            # print(f"[LAYER 1] Detected: [{stripped}] -> ID: {extracted_id} | Header: {clean_header}")
        
        # LAYER 2: Standard keywords
        if not is_header:
            layer2_pattern = r'^\s*(?:CẢNH|SCENE|PHÂN ĐOẠN|INT\.|EXT\.|NỘI\.|NGOẠI\.|I\/E\.|BỐI CẢNH).*$'
            if re.match(layer2_pattern, stripped, re.IGNORECASE):
                is_header = True
                
                # Try to extract ID from end of line
                id_pattern = r'(\d+[A-Z]*)\s*$'
                id_match = re.search(id_pattern, stripped)
                
                if id_match:
                    extracted_id = id_match.group(1)
                    clean_header = stripped[:id_match.start()].strip()
                    # Clean stuck numbers in words (e.g., "NIGHT23" -> "NIGHT")
                    clean_header = re.sub(r'([A-ZĂÂĐÊÔƠƯÁÀẢÃẠÉÈẺẼẸÍÌỈĨỊÓÒỎÕỌÚÙỦŨỤÝỲỶỸỴ]+)(\d+)', r'\1', clean_header)
                    clean_header = ' '.join(clean_header.split())
                else:
                    extracted_id = None
                    clean_header = stripped
                
                # print(f"[LAYER 2] Detected: [{stripped}] -> ID: {extracted_id} | Header: {clean_header}")
        
        # LAYER 3: All caps with number (catch-all)
        if not is_header:
            # Check if line is mostly uppercase and contains at least one digit
            if stripped.isupper() and any(char.isdigit() for char in stripped):
                is_header = True
                
                # Try to extract ID
                id_pattern = r'(\d+[A-Z]*)\s*$'
                id_match = re.search(id_pattern, stripped)
                
                if id_match:
                    extracted_id = id_match.group(1)
                    clean_header = stripped[:id_match.start()].strip()
                else:
                    extracted_id = None
                    clean_header = stripped
                
                # print(f"[LAYER 3] Detected: [{stripped}] -> ID: {extracted_id} | Header: {clean_header}")
        
        # If this is a header, save previous scene and start new one
        if is_header:
            # Save previous scene
            if current_header is not None:
                scenes.append({
                    "id": current_scene_id,
                    "header": current_header,
                    "content": '\n'.join(current_scene_lines).strip(),
                    "original_index": len(scenes)
                })
            
            # Start new scene
            auto_counter += 1
            
            # Assign ID: Use extracted ID if found, otherwise use AUTO_X
            if extracted_id:
                current_scene_id = extracted_id
            else:
                current_scene_id = f"AUTO_{auto_counter}"
            
            current_header = clean_header
            current_scene_lines = []
        else:
            # Accumulate content
            if current_header is not None:
                current_scene_lines.append(stripped)
    
    # Save last scene
    if current_header is not None:
        scenes.append({
            "id": current_scene_id,
            "header": current_header,
            "content": '\n'.join(current_scene_lines).strip(),
            "original_index": len(scenes)
        })
    
    # print(f"[SUMMARY] Total scenes detected: {len(scenes)}")
    
    # Fallback
    if not scenes:
        return [{
            "id": "AUTO_1",
            "header": "UNKNOWN SCENE",
            "content": cleaned_text,
            "original_index": 0
        }]
    
    return scenes
