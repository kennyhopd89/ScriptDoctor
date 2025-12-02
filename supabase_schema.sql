-- Supabase Database Schema for Script Doctor Pro
-- Run this in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- PROJECTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_projects_user_id ON projects(user_id);
CREATE INDEX IF NOT EXISTS idx_projects_updated_at ON projects(updated_at DESC);

-- ============================================================================
-- SCENES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS scenes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    scene_id TEXT NOT NULL,
    header TEXT NOT NULL,
    content TEXT NOT NULL,
    original_index INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_scenes_project_id ON scenes(project_id);
CREATE INDEX IF NOT EXISTS idx_scenes_original_index ON scenes(original_index);

-- ============================================================================
-- ANALYSIS RESULTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS analysis_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    creative_report JSONB,
    marketing_report TEXT,
    summary JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_analysis_project_id ON analysis_results(project_id);
CREATE INDEX IF NOT EXISTS idx_analysis_created_at ON analysis_results(created_at DESC);

-- ============================================================================
-- ACTION PLANS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS action_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_strategy TEXT,
    plan JSONB,
    task_completion JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_action_plans_project_id ON action_plans(project_id);
CREATE INDEX IF NOT EXISTS idx_action_plans_updated_at ON action_plans(updated_at DESC);

-- ============================================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================================

-- Enable RLS on all tables
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE scenes ENABLE ROW LEVEL SECURITY;
ALTER TABLE analysis_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE action_plans ENABLE ROW LEVEL SECURITY;

-- Projects policies
CREATE POLICY "Users can view own projects"
    ON projects FOR SELECT
    USING (user_id = current_setting('request.jwt.claims', true)::json->>'sub'
           OR user_id = 'default_user'); -- Allow default user for testing

CREATE POLICY "Users can insert own projects"
    ON projects FOR INSERT
    WITH CHECK (user_id = current_setting('request.jwt.claims', true)::json->>'sub'
                OR user_id = 'default_user');

CREATE POLICY "Users can update own projects"
    ON projects FOR UPDATE
    USING (user_id = current_setting('request.jwt.claims', true)::json->>'sub'
           OR user_id = 'default_user');

CREATE POLICY "Users can delete own projects"
    ON projects FOR DELETE
    USING (user_id = current_setting('request.jwt.claims', true)::json->>'sub'
           OR user_id = 'default_user');

-- Scenes policies (inherit from projects)
CREATE POLICY "Users can view scenes of own projects"
    ON scenes FOR SELECT
    USING (project_id IN (
        SELECT id FROM projects 
        WHERE user_id = current_setting('request.jwt.claims', true)::json->>'sub'
           OR user_id = 'default_user'
    ));

CREATE POLICY "Users can insert scenes to own projects"
    ON scenes FOR INSERT
    WITH CHECK (project_id IN (
        SELECT id FROM projects 
        WHERE user_id = current_setting('request.jwt.claims', true)::json->>'sub'
           OR user_id = 'default_user'
    ));

CREATE POLICY "Users can update scenes of own projects"
    ON scenes FOR UPDATE
    USING (project_id IN (
        SELECT id FROM projects 
        WHERE user_id = current_setting('request.jwt.claims', true)::json->>'sub'
           OR user_id = 'default_user'
    ));

CREATE POLICY "Users can delete scenes of own projects"
    ON scenes FOR DELETE
    USING (project_id IN (
        SELECT id FROM projects 
        WHERE user_id = current_setting('request.jwt.claims', true)::json->>'sub'
           OR user_id = 'default_user'
    ));

-- Analysis results policies (same pattern)
CREATE POLICY "Users can view analysis of own projects"
    ON analysis_results FOR SELECT
    USING (project_id IN (
        SELECT id FROM projects 
        WHERE user_id = current_setting('request.jwt.claims', true)::json->>'sub'
           OR user_id = 'default_user'
    ));

CREATE POLICY "Users can insert analysis to own projects"
    ON analysis_results FOR INSERT
    WITH CHECK (project_id IN (
        SELECT id FROM projects 
        WHERE user_id = current_setting('request.jwt.claims', true)::json->>'sub'
           OR user_id = 'default_user'
    ));

CREATE POLICY "Users can delete analysis of own projects"
    ON analysis_results FOR DELETE
    USING (project_id IN (
        SELECT id FROM projects 
        WHERE user_id = current_setting('request.jwt.claims', true)::json->>'sub'
           OR user_id = 'default_user'
    ));

-- Action plans policies (same pattern)
CREATE POLICY "Users can view action plans of own projects"
    ON action_plans FOR SELECT
    USING (project_id IN (
        SELECT id FROM projects 
        WHERE user_id = current_setting('request.jwt.claims', true)::json->>'sub'
           OR user_id = 'default_user'
    ));

CREATE POLICY "Users can insert action plans to own projects"
    ON action_plans FOR INSERT
    WITH CHECK (project_id IN (
        SELECT id FROM projects 
        WHERE user_id = current_setting('request.jwt.claims', true)::json->>'sub'
           OR user_id = 'default_user'
    ));

CREATE POLICY "Users can update action plans of own projects"
    ON action_plans FOR UPDATE
    USING (project_id IN (
        SELECT id FROM projects 
        WHERE user_id = current_setting('request.jwt.claims', true)::json->>'sub'
           OR user_id = 'default_user'
    ));

CREATE POLICY "Users can delete action plans of own projects"
    ON action_plans FOR DELETE
    USING (project_id IN (
        SELECT id FROM projects 
        WHERE user_id = current_setting('request.jwt.claims', true)::json->>'sub'
           OR user_id = 'default_user'
    ));

-- ============================================================================
-- FUNCTIONS & TRIGGERS
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_scenes_updated_at BEFORE UPDATE ON scenes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_action_plans_updated_at BEFORE UPDATE ON action_plans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- SAMPLE DATA (Optional - for testing)
-- ============================================================================

-- Insert a sample project
-- INSERT INTO projects (user_id, name, description) 
-- VALUES ('default_user', 'Sample Project', 'This is a test project');

-- ============================================================================
-- CLEANUP (if needed)
-- ============================================================================

-- To drop all tables and start fresh:
-- DROP TABLE IF EXISTS action_plans CASCADE;
-- DROP TABLE IF EXISTS analysis_results CASCADE;
-- DROP TABLE IF EXISTS scenes CASCADE;
-- DROP TABLE IF EXISTS projects CASCADE;
-- DROP FUNCTION IF EXISTS update_updated_at_column CASCADE;
