/*
  # Intruder Detection System Database Schema

  1. New Tables
    - `camera_configs`
      - `id` (uuid, primary key)
      - `source_type` (text) - webcam, rtsp, upload
      - `rtsp_url` (text, nullable)
      - `video_file` (text, nullable)
      - `is_active` (boolean)
      - `created_at` (timestamp)
      - `updated_at` (timestamp)
    
    - `detection_rules`
      - `id` (uuid, primary key)
      - `name` (text) - rule name
      - `object_type` (text) - person, animal, vehicle
      - `threshold` (integer) - alert threshold count
      - `is_active` (boolean)
      - `created_at` (timestamp)
    
    - `alerts`
      - `id` (uuid, primary key)
      - `rule_id` (uuid, foreign key)
      - `rule_name` (text)
      - `object_type` (text)
      - `count` (integer)
      - `message` (text)
      - `created_at` (timestamp)
    
    - `detection_logs`
      - `id` (uuid, primary key)
      - `person_count` (integer)
      - `animal_count` (integer)
      - `vehicle_count` (integer)
      - `created_at` (timestamp)
    
    - `alert_settings`
      - `id` (uuid, primary key)
      - `email` (text)
      - `is_active` (boolean)
      - `created_at` (timestamp)

  2. Security
    - Enable RLS on all tables
    - Add policies for public access (no auth required for demo)
*/

-- Create camera_configs table
CREATE TABLE IF NOT EXISTS camera_configs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  source_type text NOT NULL,
  rtsp_url text,
  video_file text,
  is_active boolean DEFAULT false,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create detection_rules table
CREATE TABLE IF NOT EXISTS detection_rules (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  object_type text NOT NULL CHECK (object_type IN ('person', 'animal', 'vehicle')),
  threshold integer NOT NULL CHECK (threshold > 0),
  is_active boolean DEFAULT true,
  created_at timestamptz DEFAULT now()
);

-- Create alerts table
CREATE TABLE IF NOT EXISTS alerts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  rule_id uuid REFERENCES detection_rules(id) ON DELETE SET NULL,
  rule_name text NOT NULL,
  object_type text NOT NULL,
  count integer NOT NULL,
  message text NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Create detection_logs table
CREATE TABLE IF NOT EXISTS detection_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  person_count integer DEFAULT 0,
  animal_count integer DEFAULT 0,
  vehicle_count integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Create alert_settings table
CREATE TABLE IF NOT EXISTS alert_settings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email text NOT NULL UNIQUE,
  is_active boolean DEFAULT true,
  created_at timestamptz DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE camera_configs ENABLE ROW LEVEL SECURITY;
ALTER TABLE detection_rules ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE detection_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE alert_settings ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (no authentication required for demo)
CREATE POLICY "Allow public read camera_configs"
  ON camera_configs FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Allow public insert camera_configs"
  ON camera_configs FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE POLICY "Allow public update camera_configs"
  ON camera_configs FOR UPDATE
  TO anon, authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow public read detection_rules"
  ON detection_rules FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Allow public insert detection_rules"
  ON detection_rules FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE POLICY "Allow public update detection_rules"
  ON detection_rules FOR UPDATE
  TO anon, authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow public delete detection_rules"
  ON detection_rules FOR DELETE
  TO anon, authenticated
  USING (true);

CREATE POLICY "Allow public read alerts"
  ON alerts FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Allow public insert alerts"
  ON alerts FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE POLICY "Allow public read detection_logs"
  ON detection_logs FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Allow public insert detection_logs"
  ON detection_logs FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE POLICY "Allow public read alert_settings"
  ON alert_settings FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Allow public insert alert_settings"
  ON alert_settings FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE POLICY "Allow public delete alert_settings"
  ON alert_settings FOR DELETE
  TO anon, authenticated
  USING (true);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_detection_rules_active ON detection_rules(is_active);
CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON alerts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_detection_logs_created_at ON detection_logs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_alert_settings_active ON alert_settings(is_active);