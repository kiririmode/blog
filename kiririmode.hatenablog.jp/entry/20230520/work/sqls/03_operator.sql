CREATE USER operator NOINHERIT NOBYPASSRLS PASSWORD 'postgres';
ALTER USER operator SET search_path TO my_schema;

-- スキーマを利用する権限を付与
GRANT USAGE ON SCHEMA my_schema TO operator;
-- スキーマ配下の全テーブルに対する権限を付与
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA my_schema TO operator;
ALTER DEFAULT PRIVILEGES IN SCHEMA my_schema GRANT ALL PRIVILEGES ON TABLES TO operator;

-- スキーマ配下の全シーケンスに対する権限を付与
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA my_schema TO operator;
ALTER DEFAULT PRIVILEGES IN SCHEMA my_schema GRANT ALL PRIVILEGES ON SEQUENCES TO operator;

-- parents テーブルは氏名 (name) 以外は参照等可能
REVOKE ALL PRIVILEGES ON TABLE parents FROM operator;
GRANT ALL PRIVILEGES (id) ON TABLE parents TO operator;

-- children テーブルも氏名 (name) 以外は参照等可能
REVOKE ALL PRIVILEGES ON TABLE children FROM operator;
GRANT ALL PRIVILEGES (id, father_id, mother_id) ON TABLE children TO operator;
