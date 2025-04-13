-- ユーザーを作成
CREATE USER myuser WITH PASSWORD 'mypass';

-- データベースの所有権をユーザーに付与
ALTER DATABASE mydb OWNER TO myuser;

-- スキーマの作成と権限の付与
CREATE SCHEMA IF NOT EXISTS public;
GRANT ALL ON SCHEMA public TO myuser;
GRANT ALL ON ALL TABLES IN SCHEMA public TO myuser;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO myuser;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO myuser; 