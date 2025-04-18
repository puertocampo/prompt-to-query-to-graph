from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from pydantic import BaseModel

class PlotCode(BaseModel):
    code: str

def generate_plot_code(data: list, user_prompt: str) -> str:
    """
    RDBから取得したデータを可視化するmatplotlibのコードを生成する関数

    Args:
        data (list): RDBから取得したデータ
        plot_description (str): 図解する内容についての説明

    Returns:
        str: 生成されたmatplotlibのコード
    """
    # 環境変数の読み込み
    load_dotenv()

    # Prompt Templateの作成
    prompt = PromptTemplate(
        input_variables=["data", "description"],
        template="""以下のデータを可視化するmatplotlibのPythonコードを生成してください。
        
データ:
{data}

可視化の要件:
{user_prompt}

以下の要件を満たすコードを生成してください：
- dataの先頭データはカラム名であることを考慮すること
- dataをハードコーディングによって書き下し、引数の不要なコードとすること
- dataの他にマスタテーブルのデータを用いる必要がある場合は、data内の値からマスタテーブルのデータを推論すること
- 関数内で利用する変数が正しく定義済みかどうかを確認すること
- Pythonによって記述されていること
- matplotlibを使用すること
- グラフは見やすく、色分けを用いて理解しやすいものにすること
- 必要に応じて適切な色やスタイルを設定すること
- X軸・Y軸のラベルとグラフタイトルは英語で記述すること
- 最終的にグラフをplt.show()で表示すること
"""
    )

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2).with_structured_output(PlotCode)
    chain = prompt | model

    result = chain.invoke({'data': str(data), 'user_prompt': user_prompt})
    print('\033[32mGenerated plot code:\033[0m \n{}'.format(result.code))
    return result.code

