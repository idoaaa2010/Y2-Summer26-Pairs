/*
# Create Pit Wall schema (single-tenant, no auth)

1. Overview
This migration sets up the database for the F1 "Pit Wall" chat application.
The app has no sign-in screen, so all data is intentionally shared/public
and policies are scoped to `anon, authenticated` so the anon-key frontend
can read and write.

2. New Tables
- `tracks`
  - `id` (text, primary key) — slug-style identifier, e.g. "monaco"
  - `name` (text, not null) — display name, e.g. "Monaco"
  - `country` (text, not null)
  - `lap_count` (int, not null) — total laps in a grand prix
  - `key_corner` (text, not null) — name of the defining corner
  - `created_at` (timestamptz, default now)
- `chat_sessions`
  - `id` (uuid, primary key, default gen_random_uuid())
  - `track_id` (text, foreign key -> tracks.id, on delete cascade)
  - `mode` (text, not null) — "engineer" or "driver"
  - `title` (text, not null) — short label for the session
  - `created_at` (timestamptz, default now)
- `chat_messages`
  - `id` (uuid, primary key, default gen_random_uuid())
  - `session_id` (uuid, foreign key -> chat_sessions.id, on delete cascade)
  - `role` (text, not null) — "user" or "assistant"
  - `content` (text, not null)
  - `tokens_used` (int, nullable) — token cost metadata from the API
  - `latency_ms` (int, nullable) — response latency metadata
  - `created_at` (timestamptz, default now)

3. Indexes
- `chat_sessions_track_id_idx` on `chat_sessions(track_id)`
- `chat_messages_session_id_idx` on `chat_messages(session_id)`
- `chat_messages_created_at_idx` on `chat_messages(created_at)`

4. Security
- RLS enabled on all three tables.
- All tables use `TO anon, authenticated` with `USING (true)` / `WITH CHECK (true)`
  because the app is single-tenant with no sign-in and the data is intentionally
  shared/public. This is the documented exception to the ownership-check rule.

5. Important Notes
- The `tracks` table is seeded with five circuits (Monaco, Silverstone, Monza,
  Spa, Austria) so the frontend has data on first load.
- `chat_sessions` and `chat_messages` support cascade deletes: removing a
  session also removes its messages.
*/

-- ------------------------------------------------------------------ --
-- tracks
-- ------------------------------------------------------------------ --
CREATE TABLE IF NOT EXISTS tracks (
  id text PRIMARY KEY,
  name text NOT NULL,
  country text NOT NULL,
  lap_count int NOT NULL,
  key_corner text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE tracks ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "anon_select_tracks" ON tracks;
CREATE POLICY "anon_select_tracks" ON tracks FOR SELECT
  TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "anon_insert_tracks" ON tracks;
CREATE POLICY "anon_insert_tracks" ON tracks FOR INSERT
  TO anon, authenticated WITH CHECK (true);

DROP POLICY IF EXISTS "anon_update_tracks" ON tracks;
CREATE POLICY "anon_update_tracks" ON tracks FOR UPDATE
  TO anon, authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "anon_delete_tracks" ON tracks;
CREATE POLICY "anon_delete_tracks" ON tracks FOR DELETE
  TO anon, authenticated USING (true);

-- ------------------------------------------------------------------ --
-- chat_sessions
-- ------------------------------------------------------------------ --
CREATE TABLE IF NOT EXISTS chat_sessions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  track_id text NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
  mode text NOT NULL CHECK (mode IN ('engineer', 'driver')),
  title text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "anon_select_chat_sessions" ON chat_sessions;
CREATE POLICY "anon_select_chat_sessions" ON chat_sessions FOR SELECT
  TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "anon_insert_chat_sessions" ON chat_sessions;
CREATE POLICY "anon_insert_chat_sessions" ON chat_sessions FOR INSERT
  TO anon, authenticated WITH CHECK (true);

DROP POLICY IF EXISTS "anon_update_chat_sessions" ON chat_sessions;
CREATE POLICY "anon_update_chat_sessions" ON chat_sessions FOR UPDATE
  TO anon, authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "anon_delete_chat_sessions" ON chat_sessions;
CREATE POLICY "anon_delete_chat_sessions" ON chat_sessions FOR DELETE
  TO anon, authenticated USING (true);

CREATE INDEX IF NOT EXISTS chat_sessions_track_id_idx ON chat_sessions(track_id);

-- ------------------------------------------------------------------ --
-- chat_messages
-- ------------------------------------------------------------------ --
CREATE TABLE IF NOT EXISTS chat_messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id uuid NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
  role text NOT NULL CHECK (role IN ('user', 'assistant')),
  content text NOT NULL,
  tokens_used int,
  latency_ms int,
  created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "anon_select_chat_messages" ON chat_messages;
CREATE POLICY "anon_select_chat_messages" ON chat_messages FOR SELECT
  TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "anon_insert_chat_messages" ON chat_messages;
CREATE POLICY "anon_insert_chat_messages" ON chat_messages FOR INSERT
  TO anon, authenticated WITH CHECK (true);

DROP POLICY IF EXISTS "anon_update_chat_messages" ON chat_messages;
CREATE POLICY "anon_update_chat_messages" ON chat_messages FOR UPDATE
  TO anon, authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "anon_delete_chat_messages" ON chat_messages;
CREATE POLICY "anon_delete_chat_messages" ON chat_messages FOR DELETE
  TO anon, authenticated USING (true);

CREATE INDEX IF NOT EXISTS chat_messages_session_id_idx ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS chat_messages_created_at_idx ON chat_messages(created_at);

-- ------------------------------------------------------------------ --
-- Seed tracks
-- ------------------------------------------------------------------ --
INSERT INTO tracks (id, name, country, lap_count, key_corner) VALUES
  ('monaco', 'Monaco', 'Monaco', 78, 'Grand Hotel Hairpin'),
  ('silverstone', 'Silverstone', 'United Kingdom', 52, 'Copse'),
  ('monza', 'Monza', 'Italy', 53, 'Parabolica'),
  ('spa', 'Spa-Francorchamps', 'Belgium', 44, 'Eau Rouge'),
  ('austria', 'Red Bull Ring', 'Austria', 71, 'Turn 3')
ON CONFLICT (id) DO NOTHING;
