"""
Database module for Supabase integration
Handles all database operations for project management
"""

import streamlit as st
from supabase import create_client, Client
from typing import List, Dict, Optional
import json
from datetime import datetime

def get_supabase_client() -> Optional[Client]:
    """
    Get Supabase client from Streamlit secrets.
    Returns None if Supabase is not configured (fallback to local storage).
    """
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
        
        if not url or not key:
            return None
            
        return create_client(url, key)
    except Exception as e:
        print(f"Supabase not configured: {e}")
        return None

def is_supabase_enabled() -> bool:
    """Check if Supabase is configured and available"""
    return get_supabase_client() is not None

# ============================================================================
# PROJECT OPERATIONS
# ============================================================================

def create_project(name: str, description: str = "") -> Optional[Dict]:
    """Create a new project"""
    supabase = get_supabase_client()
    if not supabase:
        return None
    
    try:
        user_id = st.session_state.get("user_id", "default_user")
        data = {
            "user_id": user_id,
            "name": name,
            "description": description,
            "metadata": {}
        }
        
        result = supabase.table("projects").insert(data).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        st.error(f"Error creating project: {e}")
        return None

def get_projects() -> List[Dict]:
    """Get all projects for current user"""
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        user_id = st.session_state.get("user_id", "default_user")
        result = supabase.table("projects")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("updated_at", desc=True)\
            .execute()
        
        return result.data if result.data else []
    except Exception as e:
        st.error(f"Error fetching projects: {e}")
        return []

def get_project(project_id: str) -> Optional[Dict]:
    """Get a specific project by ID"""
    supabase = get_supabase_client()
    if not supabase:
        return None
    
    try:
        result = supabase.table("projects")\
            .select("*")\
            .eq("id", project_id)\
            .single()\
            .execute()
        
        return result.data if result.data else None
    except Exception as e:
        st.error(f"Error fetching project: {e}")
        return None

def update_project(project_id: str, name: str = None, description: str = None, metadata: Dict = None) -> bool:
    """Update project details"""
    supabase = get_supabase_client()
    if not supabase:
        return False
    
    try:
        data = {"updated_at": datetime.now().isoformat()}
        
        if name:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if metadata:
            data["metadata"] = metadata
        
        supabase.table("projects").update(data).eq("id", project_id).execute()
        return True
    except Exception as e:
        st.error(f"Error updating project: {e}")
        return False

def delete_project(project_id: str) -> bool:
    """Delete a project and all related data"""
    supabase = get_supabase_client()
    if not supabase:
        return False
    
    try:
        supabase.table("projects").delete().eq("id", project_id).execute()
        return True
    except Exception as e:
        st.error(f"Error deleting project: {e}")
        return False

# ============================================================================
# SCENE OPERATIONS
# ============================================================================

def save_scenes(project_id: str, scenes: List[Dict]) -> bool:
    """Save scenes for a project (replaces all existing scenes)"""
    supabase = get_supabase_client()
    if not supabase:
        return False
    
    try:
        # Delete old scenes
        supabase.table("scenes").delete().eq("project_id", project_id).execute()
        
        # Insert new scenes
        if scenes:
            data = [{
                "project_id": project_id,
                "scene_id": scene["id"],
                "header": scene["header"],
                "content": scene["content"],
                "original_index": scene.get("original_index", 0)
            } for scene in scenes]
            
            supabase.table("scenes").insert(data).execute()
        
        # Update project timestamp
        update_project(project_id)
        
        return True
    except Exception as e:
        st.error(f"Error saving scenes: {e}")
        return False

def get_scenes(project_id: str) -> List[Dict]:
    """Get all scenes for a project"""
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        result = supabase.table("scenes")\
            .select("*")\
            .eq("project_id", project_id)\
            .order("original_index")\
            .execute()
        
        return result.data if result.data else []
    except Exception as e:
        st.error(f"Error fetching scenes: {e}")
        return []

# ============================================================================
# ANALYSIS OPERATIONS
# ============================================================================

def save_analysis(project_id: str, creative_report: Dict, marketing_report: str, summary: List[Dict]) -> bool:
    """Save analysis results for a project"""
    supabase = get_supabase_client()
    if not supabase:
        return False
    
    try:
        # Delete old analysis
        supabase.table("analysis_results").delete().eq("project_id", project_id).execute()
        
        # Insert new analysis
        data = {
            "project_id": project_id,
            "creative_report": creative_report,
            "marketing_report": marketing_report,
            "summary": summary
        }
        
        supabase.table("analysis_results").insert(data).execute()
        
        # Update project timestamp
        update_project(project_id)
        
        return True
    except Exception as e:
        st.error(f"Error saving analysis: {e}")
        return False

def get_analysis(project_id: str) -> Optional[Dict]:
    """Get analysis results for a project"""
    supabase = get_supabase_client()
    if not supabase:
        return None
    
    try:
        result = supabase.table("analysis_results")\
            .select("*")\
            .eq("project_id", project_id)\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()
        
        return result.data[0] if result.data else None
    except Exception as e:
        st.error(f"Error fetching analysis: {e}")
        return None

# ============================================================================
# ACTION PLAN OPERATIONS
# ============================================================================

def save_action_plan(project_id: str, user_strategy: str, plan: List[Dict], task_completion: Dict = None) -> bool:
    """Save action plan for a project"""
    supabase = get_supabase_client()
    if not supabase:
        return False
    
    try:
        # Delete old action plan
        supabase.table("action_plans").delete().eq("project_id", project_id).execute()
        
        # Insert new action plan
        data = {
            "project_id": project_id,
            "user_strategy": user_strategy,
            "plan": plan,
            "task_completion": task_completion or {}
        }
        
        supabase.table("action_plans").insert(data).execute()
        
        # Update project timestamp
        update_project(project_id)
        
        return True
    except Exception as e:
        st.error(f"Error saving action plan: {e}")
        return False

def get_action_plan(project_id: str) -> Optional[Dict]:
    """Get action plan for a project"""
    supabase = get_supabase_client()
    if not supabase:
        return None
    
    try:
        result = supabase.table("action_plans")\
            .select("*")\
            .eq("project_id", project_id)\
            .order("updated_at", desc=True)\
            .limit(1)\
            .execute()
        
        return result.data[0] if result.data else None
    except Exception as e:
        st.error(f"Error fetching action plan: {e}")
        return None

def update_task_completion(project_id: str, task_completion: Dict) -> bool:
    """Update task completion status"""
    supabase = get_supabase_client()
    if not supabase:
        return False
    
    try:
        data = {
            "task_completion": task_completion,
            "updated_at": datetime.now().isoformat()
        }
        
        supabase.table("action_plans")\
            .update(data)\
            .eq("project_id", project_id)\
            .execute()
        
        return True
    except Exception as e:
        st.error(f"Error updating task completion: {e}")
        return False

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def load_project_to_session(project_id: str) -> bool:
    """Load a project and all its data into session state"""
    try:
        # Load project
        project = get_project(project_id)
        if not project:
            return False
        
        st.session_state['current_project_id'] = project_id
        st.session_state['current_project_name'] = project['name']
        
        # Load scenes
        scenes = get_scenes(project_id)
        if scenes:
            st.session_state['scene_list'] = scenes
        
        # Load analysis
        analysis = get_analysis(project_id)
        if analysis:
            st.session_state['analysis_results'] = {
                'creative': analysis['creative_report'],
                'marketing': analysis['marketing_report'],
                'summary': analysis['summary']
            }
            st.session_state['analysis_report'] = analysis['creative_report']
        
        # Load action plan
        action_plan = get_action_plan(project_id)
        if action_plan:
            st.session_state['action_plan'] = action_plan['plan']
            st.session_state['user_strategy'] = action_plan['user_strategy']
            st.session_state['task_completion'] = action_plan['task_completion']
        
        return True
    except Exception as e:
        st.error(f"Error loading project: {e}")
        return False

def save_current_project() -> bool:
    """Save current session state to database"""
    project_id = st.session_state.get('current_project_id')
    if not project_id:
        return False
    
    try:
        # Save scenes
        if 'scene_list' in st.session_state:
            save_scenes(project_id, st.session_state['scene_list'])
        
        # Save analysis
        if 'analysis_results' in st.session_state:
            results = st.session_state['analysis_results']
            save_analysis(
                project_id,
                results.get('creative', {}),
                results.get('marketing', ''),
                results.get('summary', [])
            )
        
        # Save action plan
        if 'action_plan' in st.session_state:
            save_action_plan(
                project_id,
                st.session_state.get('user_strategy', ''),
                st.session_state['action_plan'],
                st.session_state.get('task_completion', {})
            )
        
        return True
    except Exception as e:
        st.error(f"Error saving project: {e}")
        return False
