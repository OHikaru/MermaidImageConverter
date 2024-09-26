import streamlit as st
import base64
from PIL import Image
import io
import requests

def mermaid_to_image(mermaid_code):
    graphbiz_url = "https://mermaid.ink/img/"

    # Mermaidコードのエンコード
    encoded_code = base64.urlsafe_b64encode(mermaid_code.encode('utf-8')).decode('utf-8')

    # URLの構築
    url = f"{graphbiz_url}{encoded_code}"

    # URLにGETリクエストを送信
    response = requests.get(url)

    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    else:
        st.error(f"エラー: 画像を生成できませんでした。ステータスコード: {response.status_code}")
        return None

def main():
    st.title("Mermaid図形生成アプリ")

    # Mermaidコード入力用のテキストエリア
    mermaid_code = st.text_area("ここにMermaidコードを入力してください:", height=200)

    if st.button("図形を生成"):
        if mermaid_code:
            with st.spinner("図形を生成中..."):
                image = mermaid_to_image(mermaid_code)
                if image:
                    st.image(image, caption="生成された図形", use_column_width=True)

                    # 画像をバイトに変換
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()

                    # ダウンロードボタンの提供
                    st.download_button(
                        label="PNGをダウンロード",
                        data=img_byte_arr,
                        file_name="mermaid_diagram.png",
                        mime="image/png"
                    )
        else:
            st.warning("Mermaidコードを入力してください。")

if __name__ == "__main__":
    main()
