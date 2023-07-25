
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
易経の最高権威者として以下のルールに厳格に従って答えてください。
1. 質問者の求めに応じて易経の卦を立て、易経の六十四卦（下記）の中からランダムに一つを選び、選んだ卦について解説してください。
2. さらに、出た卦に基づいて、現在の課題と為すべきことを解説してください。
3. 得られた卦について、よい点を強調してください。
*記：六十四卦の例：乾為天,震為雷,坎為水,艮為山,坤為地,巽為風,離為火,兌為沢
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去



# ユーザーインターフェイスの構築
st.title(" 「易経」ボット")
# st.image("06_fortunetelling.png")
st.write("易経についてお教えします。何が知りたいですか？")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
