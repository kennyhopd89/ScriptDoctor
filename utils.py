import os
import json

DATA_DIR = "data"
PROJECTS_FILE = os.path.join(DATA_DIR, "projects.json")
SESSION_FILE = os.path.join(DATA_DIR, "current_session.json")

def init_app():
    """Initialize the application by creating necessary directories and files."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    if not os.path.exists(PROJECTS_FILE):
        save_json(PROJECTS_FILE, {"projects": []})

def save_json(filepath, data):
    """Save a dictionary to a JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_json(filepath):
    """Load a dictionary from a JSON file."""
    if not os.path.exists(filepath):
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

import streamlit as st

# Pricing for Gemini 2.5 Flash (Estimated)
PRICE_INPUT_1M = 0.075   # $0.075 / 1M tokens
PRICE_OUTPUT_1M = 0.30   # $0.30 / 1M tokens

def update_cost_session(input_tokens, output_tokens):
    """Accumulate cost into session state"""
    # 1. Calculate current cost
    cost_in = (input_tokens / 1_000_000) * PRICE_INPUT_1M
    cost_out = (output_tokens / 1_000_000) * PRICE_OUTPUT_1M
    total_new_cost = cost_in + cost_out

    # 2. Initialize if not exists
    if 'cost_stats' not in st.session_state:
        st.session_state['cost_stats'] = {
            'total_input': 0,
            'total_output': 0,
            'total_usd': 0.0,
            'request_count': 0
        }

    # 3. Accumulate
    stats = st.session_state['cost_stats']
    stats['total_input'] += input_tokens
    stats['total_output'] += output_tokens
    stats['total_usd'] += total_new_cost
    stats['request_count'] += 1
    
    # 4. Auto-save
    save_session_state(st.session_state)

def save_session_state(state_dict):
    """Save current session state to file. Accepts a dictionary of state."""
    try:
        # Only save important keys
        keys_to_save = ['scene_list', 'analysis_results', 'analysis_report', 'action_plan', 'user_strategy', 'cost_stats']
        data = {k: state_dict.get(k) for k in keys_to_save if state_dict.get(k) is not None}
        
        save_json(SESSION_FILE, data)
    except Exception as e:
        print(f"Error saving session: {e}")

def load_session_state():
    """Load session state from file. Returns a dictionary."""
    try:
        if not os.path.exists(SESSION_FILE):
            return {}
        
        session_data = load_json(SESSION_FILE)
        
        # Clean up empty string API key
        if session_data.get("api_key") == "":
            session_data.pop("api_key", None)
        
        # Handle legacy format (api_key, scene_list tuple)
        if "gemini_api_key" not in session_data and "api_key" in session_data:
            session_data["gemini_api_key"] = session_data.pop("api_key")
            
        return session_data
    except Exception as e:
        print(f"Error loading session: {e}")
        return {}
