/* adminは、ユーザは作成できるが、自身ではテーブルの参照等はできない */
CREATE USER admin CREATEROLE NOINHERIT NOBYPASSRLS PASSWORD 'postgres';
ALTER USER admin SET search_path TO my_schema;

/*
 * ro ロールは、どのテーブルの参照も可能な権限を持つ
 */
CREATE ROLE ro NOINHERIT NOBYPASSRLS NOLOGIN;

-- スキーマを利用する権限を付与
GRANT USAGE ON SCHEMA my_schema TO ro;
-- スキーマ配下の全テーブルに対する参照権限を付与
GRANT SELECT ON ALL TABLES IN SCHEMA my_schema TO ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA my_schema GRANT SELECT ON TABLES TO ro;

/*
CREATE USER ro_kiririmode PASSWORD 'kiririmode' VALID UNTIL '2023-07-17 18:00:00 JST' IN ROLE ro;
-- デフォルトスキーマを変更。search_pathは継承できないため、ユーザごとに設定する必要がある。
ALTER USER ro_kiririmode SET search_path TO my_schema;
*/
