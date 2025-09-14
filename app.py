from dotenv import load_dotenv
import os
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os

# Webアプリの概要・操作説明
st.title("専門家AI相談アプリ")
st.markdown("""
このアプリは、あなたの質問に対してAIが専門家として回答します。下記の手順でご利用ください：

1. 専門家の種類を選択してください。
2. 質問内容を入力し、送信ボタンを押してください。
3. AIによる回答が画面に表示されます。
""")

# 専門家の種類（自由に設定）
expert_types = {
	"医療の専門家": "あなたは優秀な医師です。医学的な知識に基づき、分かりやすく丁寧に回答してください。",
	"法律の専門家": "あなたは経験豊富な弁護士です。法律的な観点から、分かりやすく丁寧に回答してください。",
	"ITの専門家": "あなたはIT分野のプロフェッショナルです。技術的な観点から、分かりやすく丁寧に回答してください。"
}

# OpenAI APIキーの取得（環境変数から）
openai_api_key = os.getenv("OPENAI_API_KEY")

# LLM応答関数
def get_llm_response(input_text: str, expert_type: str) -> str:
	system_message = expert_types.get(expert_type, "あなたは優秀な専門家です。分かりやすく回答してください。")
	chat = ChatOpenAI(api_key=openai_api_key, model="gpt-4o-mini")
	messages = [
		SystemMessage(content=system_message),
		HumanMessage(content=input_text)
	]
	response = chat.invoke(messages)
	return response.content

# 入力フォーム
with st.form("input_form"):
	expert_type = st.radio("専門家の種類を選択してください", list(expert_types.keys()))
	input_text = st.text_area("質問内容を入力してください")
	submitted = st.form_submit_button("送信")

if submitted and input_text:
	with st.spinner("AIが回答中です..."):
		answer = get_llm_response(input_text, expert_type)
	st.markdown("### AIの回答")
	st.write(answer)

