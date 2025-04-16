import matplotlib.pyplot as plt
import io
import base64

def execute_plot_code(plot_code: str) -> str:
    """
    matplotlibのコードを実行し、生成されたグラフをbase64エンコードされた画像データとして返す関数

    Args:
        plot_code (str): 実行するmatplotlibのコード

    Returns:
        str: 生成されたグラフの画像データ(base64エンコード済み)
    """
    try:
        # プロットをクリア
        plt.clf()
        
        # コードを実行
        exec(plot_code)
        
        # 画像をバイト列として保存
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=300)
        buf.seek(0)
        image_data = buf.getvalue()
        
        # バッファとプロットをクリア
        buf.close()
        plt.close()
        
        # base64エンコード
        base64_image = base64.b64encode(image_data).decode('utf-8')
        print('plot image base64: {}'.format(base64_image[:30]))
        return base64_image
        
    except Exception as e:
        print(f"Error executing plot code: {e}")
        return None
