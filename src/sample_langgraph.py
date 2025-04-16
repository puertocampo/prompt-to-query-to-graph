from typing import Any, Dict
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# from langchain.llms import OpenAI
from langchain_community.llms import OpenAI
from langchain.output_parsers import RegexParser
# from langgraph import Node, Graph, Edge, Condition
from langgraph.graph import StateGraph

# 1. LangChainの要素を定義
# PromptTemplate: プロンプトのテンプレート
prompt_template = PromptTemplate(
    input_variables=["topic"],
    template="""
    次の話題についてまとめを作成してください:
    {topic}

    - 箇条書きを含めてください
    - 出力形式は以下の指定に従ってください:
      タイトル: ...
      箇条書き:
      1. ...
      2. ...
    """
)

# 2. OutputParserの例
# 単純な例として、タイトルや箇条書きを抜き出すために正規表現パーサを使う
regex_pattern = r"タイトル:\s*(.*)\n箇条書き:\s*(1\.\s.*)"
output_parser = RegexParser(
    regex=regex_pattern,
    output_keys=["title", "bullets"]
)

# 3. LLMの定義
llm = OpenAI(
    temperature=0.7,
    max_tokens=512
)

# 4. LLMChainを作成
summarize_chain = LLMChain(
    llm=llm,
    prompt=prompt_template,
    output_key="summary",
    output_parser=output_parser,
)

# 5. langgraphのノードを定義
# NodeにはLLMChainそのものやPython関数などを割り当て可能
summarize_node = Node(
    id="summarize_node",
    chain=summarize_chain
)

# 6. 条件分岐を実装する例
#   - summarize_nodeの出力を見て判断
#   - 例えば、タイトルに特定のキーワードが含まれるかどうかで分岐する
def branch_condition(context: Dict[str, Any]) -> str:
    # summarize_nodeの出力を取得
    title = context["summarize_node"]["summary"]["title"]
    if "AI" in title:
        return "ai_detail_node"   # 「AI」に特化した処理へ
    else:
        return "general_detail_node"  # それ以外の処理へ

# Conditionで分岐ルールを定義
branch_decision = Condition(
    condition=branch_condition,
    # True/Falseや文字列などで、次のNode IDを返す
)

# 7. ループ的な処理の例
#   - この例では単純化し、「再度要約を繰り返したい」ケースを想定。
#   - contextの中にフラグやカウンタを持たせて一定数ループさせるイメージ。
def loop_condition(context: Dict[str, Any]) -> bool:
    # contextに iteration_count がなければ0で初期化
    if "iteration_count" not in context:
        context["iteration_count"] = 0
    
    context["iteration_count"] += 1

    # 例えば3回まで実行したらループを抜ける
    if context["iteration_count"] < 3:
        return True  # まだ続ける
    else:
        return False # ループ終了

def repeat_summarize(context: Dict[str, Any]) -> Dict[str, Any]:
    # 最後の summarize_node の出力を再度まとめる…など
    # （サンプルとして単純に前回のタイトルを再度使うだけ）
    last_title = context["summarize_node"]["summary"]["title"]
    topic = f"{last_title}についてさらに深掘り"
    return {"topic": topic}

# 8. ループノードの定義 (再度summarize_nodeを呼び出す用)
loop_edge = Edge(
    from_="summarize_node",
    to="summarize_node",  # 自分に戻る
    condition=loop_condition,
    prepare=repeat_summarize  # 次に渡すinputを作成
)

# 9. 分岐先のノード定義(ダミーとして空のNodeを使う)
ai_detail_node = Node(
    id="ai_detail_node",
    func=lambda context: {"result": "AIについてさらに詳しく解析しました！"}
)

general_detail_node = Node(
    id="general_detail_node",
    func=lambda context: {"result": "汎用的な話題の深堀りをしました！"}
)

# 10. グラフ構築
graph = StateGraph(
    nodes=[
        summarize_node,
        ai_detail_node,
        general_detail_node
    ],
    edges=[
        # summarize_nodeの出力を見て条件分岐するEdge
        Edge(
            from_="summarize_node",
            to=branch_decision,  # Conditionオブジェクトを通して行き先を決める
        ),
        loop_edge,
        # Condition結果 "ai_detail_node" へ
        Edge(from_="summarize_node", to="ai_detail_node", name="ai_detail_node"),
        # Condition結果 "general_detail_node" へ
        Edge(from_="summarize_node", to="general_detail_node", name="general_detail_node"),
    ]
)

# 11. 実行: topicを指定して開始
initial_input = {"topic": "AIと社会の未来"}
final_result = graph.run(initial_input)

print("\n=== Graph実行結果 ===")
print(final_result)
