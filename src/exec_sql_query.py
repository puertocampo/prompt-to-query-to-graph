import psycopg2
import psycopg2.extras

# PostgreSQL接続情報
DB_HOST = "127.0.0.1"
DB_PORT = 5434
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "mypass"

def execute_sql_query(query: str) -> list:
    """
    SQLクエリを実行し、結果を返す関数。結果の先頭行にカラム名が含まれる。

    Args:
        query (str): 実行するSQLクエリ

    Returns:
        list: クエリの実行結果（先頭行にカラム名を含む）
    """
    try:
        # PostgreSQLへ接続
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            cursor_factory=psycopg2.extras.DictCursor
        )
        cur = conn.cursor()

        # クエリを実行
        cur.execute(query)
        results = cur.fetchall()
        
        # カラム名を取得
        column_names = [desc[0] for desc in cur.description]

        # カラム名を結果の先頭に追加
        results = [column_names] + list(results)

        # 接続を閉じる
        cur.close()
        conn.close()

        print('\033[32mSQL query executed:\033[0m \n{} '.format(results))
        return results

    except Exception as e:
        print(f"Error: {e}")
        return []
