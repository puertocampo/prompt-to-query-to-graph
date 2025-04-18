import psycopg2
import psycopg2.extras
import json

# PostgreSQL接続情報
DB_HOST = "127.0.0.1"
DB_PORT = 5434
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "mypass"

QUERY_DATABASES = """
    SELECT * from courses;
"""

# テーブルとカラム情報を取得するSQLクエリ
QUERY_TABLES = """
    SELECT 
        c.relname AS table_name, 
        COALESCE(d.description, '') AS table_comment
    FROM pg_catalog.pg_class c
    LEFT JOIN pg_catalog.pg_description d ON d.objoid = c.oid
    WHERE c.relkind = 'r'
    AND c.relnamespace = (SELECT oid FROM pg_catalog.pg_namespace WHERE nspname = 'public')
    AND d.objsubid = 0;
"""

QUERY_COLUMNS = """
    SELECT 
        c.table_name, 
        c.column_name, 
        c.data_type,
        COALESCE(d.description, '') AS column_comment
    FROM information_schema.columns c
    LEFT JOIN pg_catalog.pg_description d 
        ON d.objoid = (
            SELECT oid FROM pg_catalog.pg_class 
            WHERE relname = c.table_name 
            AND relnamespace = (
                SELECT oid FROM pg_catalog.pg_namespace 
                WHERE nspname = c.table_schema
            )
        )
        AND d.objsubid = c.ordinal_position
    WHERE c.table_schema = 'public';
"""

def fetch_catalog_data():
    """PostgreSQLのスキーマ情報を取得し、カタログデータを生成"""
    try:
        # PostgreSQLへ直接接続
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            cursor_factory=psycopg2.extras.DictCursor
        )
        cur = conn.cursor()

        # テーブル情報を取得
        cur.execute(QUERY_TABLES)
        tables = {table: {"table": table, "description": comment, "columns": []} for table, comment in cur.fetchall()}

        # カラム情報を取得
        cur.execute(QUERY_COLUMNS)
        for table_name, column_name, data_type, column_comment in cur.fetchall():
            if table_name in tables:
                tables[table_name]["columns"].append({
                    "column_name": column_name,
                    "data_type": data_type,
                    "description": column_comment
                })

        # JSON形式に整形
        catalog_data = list(tables.values())
        json_output = json.dumps(catalog_data, indent=4, ensure_ascii=False)
        
        # JSONファイルに出力
        with open('db_schema.json', 'w', encoding='utf-8') as f:
            f.write(json_output)

        # 接続を閉じる
        cur.close()
        conn.close()

        return json_output

    except Exception as e:
        print(f"Error: {e}")

# カタログデータを取得
fetch_catalog_data()
