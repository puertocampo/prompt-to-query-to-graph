from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from IPython.display import Image, display
import generate_sql_query
import exec_sql_query
import generate_plot_code
import execute_plot_code
import argparse

# Stateを宣言
class State(TypedDict):
    user_prompt: str
    sql_query: str
    exec_results: any
    plot_code: str
    image_base64: str
    image_url: str  

# Nodeを宣言
def generate_sql_query_node(state: State, config: RunnableConfig):
    return {**state, "sql_query": generate_sql_query.generate_sql_query(state["user_prompt"])}

def check_sql_query_node(state: State, config: RunnableConfig):
    # 破壊的なSQLクエリでないかチェック
    print('sql_query', state["sql_query"])
    if state["sql_query"].startswith("SELECT"):
        print('破壊的なSQLクエリではありません')
        return "exec_sql_query"
    else:
        return "generate_sql_query"

def exec_sql_query_node(state: State, config: RunnableConfig):
    return {**state, "exec_results": exec_sql_query.execute_sql_query(state["sql_query"])}

def generate_plot_code_node(state: State, config: RunnableConfig):
    return {**state, "plot_code": generate_plot_code.generate_plot_code(state["exec_results"], state["user_prompt"])}

def execute_plot_code_node(state: State, config: RunnableConfig):
    return {**state, "image_base64": execute_plot_code.execute_plot_code(state["plot_code"])}

# Graphの作成
graph_builder = StateGraph(State)

# Nodeの追加
graph_builder.add_node("generate_sql_query", generate_sql_query_node)
graph_builder.add_node("exec_sql_query", exec_sql_query_node)
graph_builder.add_node("generate_plot_code", generate_plot_code_node)
graph_builder.add_node("execute_plot_code", execute_plot_code_node)

# Nodeをedgeに追加 
# graph_builder.add_conditional_edges("generate_sql_query", check_sql_query_node)
graph_builder.add_edge("generate_sql_query", "exec_sql_query")
graph_builder.add_edge("exec_sql_query", "generate_plot_code")
graph_builder.add_edge("generate_plot_code", "execute_plot_code")

# Graphの始点を宣言
graph_builder.set_entry_point("generate_sql_query")

# Graphの終点を宣言
graph_builder.set_finish_point("upload_image_to_s3")

# Graphをコンパイル
graph = graph_builder.compile()

# Graphの表示
display(Image(graph.get_graph().draw_mermaid_png()))

# コマンドライン引数の設定
parser = argparse.ArgumentParser(description='履修データベースのクエリと可視化を行うグラフ処理')
parser.add_argument('prompt', type=str, help='可視化したいデータの説明（例：教員が担当している学生数の分布）')

if __name__ == "__main__":
    # コマンドライン引数の解析
    args = parser.parse_args()

    # Graphの実行(引数にはStateの初期値を渡す)
    graph.invoke(
        {
            "user_prompt": args.prompt,
            "sql_query": "",
            "exec_results": [],
            "plot_code": "",
            "image_base64": "",
            "image_url": ""
        }
        # , debug=True
        )