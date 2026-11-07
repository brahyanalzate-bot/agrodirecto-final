ALTER TABLE profiles ADD COLUMN IF NOT EXISTS push_token TEXT;
CREATE INDEX idx_profiles_push_token ON profiles(push_token);
