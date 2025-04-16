from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from pydantic import BaseModel
import json

# SQLクエリの型定義
class SQLQuery(BaseModel):
    query: str

def generate_sql_query(user_prompt: str) -> str:
    """
    プロンプトに合わせたSQLクエリを生成する関数
    
    Returns:
        str: 生成されたSQLクエリ
    """
    # 環境変数の読み込み
    load_dotenv()

    # db_schema.jsonの読み込み
    with open('db_schema.json', 'r', encoding='utf-8') as f:
        db_schema = json.load(f)

    # Prompt Templateの作成
    prompt = PromptTemplate(
        input_variables=["schema", "user_prompt"],
        template="""以下のスキーマ構造を持つpostgreSQLにより構築されたrelationalデータベースに対して、「{user_prompt}」を実現するSQLクエリを生成してください。

スキーマ情報:
{schema}"""
    )

    # テンプレートに値を挿入
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2).with_structured_output(SQLQuery)
    chain = prompt | model

    result = chain.invoke({'schema': json.dumps(db_schema, indent=2, ensure_ascii=False), 'user_prompt': user_prompt})
    print('generated SQL query: {}'.format(result.query))
    return result.query