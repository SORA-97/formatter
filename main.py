import streamlit as st

st.set_page_config(page_title="エンジニア整形ツール", layout="wide")
st.title("🛠 エンジニア整形ツール")

# --- サイドバー設定 ---
with st.sidebar:
    st.header("設定")
    mode = st.radio(
        "変換モードを選択:",
        ["1次元リスト", "2次元リスト", "辞書 (Dict)"]
    )
    
    st.write("---")
    if mode == "1次元リスト":
        wrap_count = st.number_input("何個ごとに改行する？ (0は改行なし)", min_value=0, value=0)
    
    if mode == "2次元リスト":
        chunk_size = st.number_input("何個ずつグループにする？", min_value=1, value=2)
    
    if mode == "辞書 (Dict)":
        st.info("奇数番目がキー、偶数番目が値になります")

# --- メイン処理 ---
raw_input = st.text_area("入力を貼り付けてください (カンマやスペース混在OK):", 
                         placeholder="A, 4, B, 5 や 1 2 3 4...", height=200)

def smart_format(item):
    """数値ならそのまま、文字列なら引用符をつける"""
    if item.isdigit():
        return item
    return f"'{item}'"

if raw_input:
    # カンマをスペースに置換してから分割（これでカンマを無視できる）
    clean_input = raw_input.replace(',', ' ')
    items = clean_input.split()
    
    if mode == "1次元リスト":
        formatted = [smart_format(x) for x in items]
        if wrap_count > 0:
            # 指定数ごとに改行を加えた文字列を作る
            lines = []
            for i in range(0, len(formatted), wrap_count):
                lines.append(", ".join(formatted[i:i + wrap_count]))
            res = "[\n    " + ",\n    ".join(lines) + "\n]"
        else:
            res = "[" + ", ".join(formatted) + "]"
        st.code(res, language="python")

    elif mode == "2次元リスト":
        chunks = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
        formatted_chunks = []
        for c in chunks:
            row = "[" + ", ".join(smart_format(x) for x in c) + "]"
            formatted_chunks.append(row)
        res = "[\n    " + ",\n    ".join(formatted_chunks) + "\n]"
        st.code(res, language="python")

    elif mode == "辞書 (Dict)":
        if len(items) % 2 != 0:
            st.warning("要素が奇数です。最後の要素は無視されます。")
        it = iter(items)
        d = {smart_format(k): smart_format(v) for k, v in zip(it, it)}
        dict_str = "{\n    " + ",\n    ".join([f"{k}: {v}" for k, v in d.items()]) + "\n}"
        st.code(dict_str, language="python")

    st.success(f"変換成功！ 合計要素数: {len(items)}")