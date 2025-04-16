from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from IPython.display import Image, display
import generate_sql_query
import exec_sql_query
import generate_plot_code
import execute_plot_code
import upload_image_to_s3

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
    print('will generate_sql_query')
    sql_query = generate_sql_query.generate_sql_query(state["user_prompt"])
    print('generate_sql_query sql_query', sql_query, type(sql_query))
    return {**state, "sql_query": generate_sql_query.generate_sql_query(state["user_prompt"])}

def exec_sql_query_node(state: State, config: RunnableConfig):
    return {**state, "exec_results": exec_sql_query.execute_sql_query(state["sql_query"])}

def generate_plot_code_node(state: State, config: RunnableConfig):
    return {**state, "plot_code": generate_plot_code.generate_plot_code(state["exec_results"], state["user_prompt"])}

def execute_plot_code_node(state: State, config: RunnableConfig):
    return {**state, "image_base64": execute_plot_code.execute_plot_code(state["plot_code"])}

def upload_image_to_s3_node(state: State, config: RunnableConfig):
    return {**state, "image_url": upload_image_to_s3.upload_image_to_s3(state["image_base64"])}

# Graphの作成
graph_builder = StateGraph(State)

# Nodeの追加
graph_builder.add_node("generate_sql_query", generate_sql_query_node)
graph_builder.add_node("exec_sql_query", exec_sql_query_node)
graph_builder.add_node("generate_plot_code", generate_plot_code_node)
graph_builder.add_node("execute_plot_code", execute_plot_code_node)
graph_builder.add_node("upload_image_to_s3", upload_image_to_s3_node)

# Nodeをedgeに追加 
graph_builder.add_edge("generate_sql_query", "exec_sql_query")
graph_builder.add_edge("exec_sql_query", "generate_plot_code")
graph_builder.add_edge("generate_plot_code", "execute_plot_code")
graph_builder.add_edge("execute_plot_code", "upload_image_to_s3")

# Graphの始点を宣言
graph_builder.set_entry_point("generate_sql_query")

# Graphの終点を宣言
graph_builder.set_finish_point("upload_image_to_s3")

# Graphをコンパイル
graph = graph_builder.compile()

# Graphの表示
display(Image(graph.get_graph().draw_mermaid_png()))

# Graphの実行(引数にはStateの初期値を渡す)
graph.invoke(
    {
        "user_prompt": "教員が担当している学生数の分布を表示してください。",
        "sql_query": "",
        "exec_results": [],
        "plot_code": "",
        "image_base64": "",
        "image_url": ""
    }, debug=True)