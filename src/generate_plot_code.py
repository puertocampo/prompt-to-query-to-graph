from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from pydantic import BaseModel

class PlotCode(BaseModel):
    code: str

def generate_plot_code(data: list, plot_description: str) -> str:
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
{description}

以下の要件を満たすコードを生成してください：
- dataをハードコーディングによって書き下し、引数の不要なコードとすること
- Pythonによって記述されていること
- matplotlibを使用すること
- 日本語のラベルやタイトルが正しく表示されるように設定すること
- グラフは見やすく、色分けを用いて理解しやすいものにすること
- 必要に応じて適切な色やスタイルを設定すること
- X軸・Y軸のラベルとグラフタイトルは英語で記述すること
- 最終的にグラフをplt.show()で表示すること
"""
    )

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2).with_structured_output(PlotCode)
    chain = prompt | model

    result = chain.invoke({'data': str(data), 'description': plot_description})
    print('generated plot code: {}'.format(result.code))
    return result.code

