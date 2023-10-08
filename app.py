import streamlit as st
import time
import pandas as pd
import plotly.graph_objs as go

from graph import bar

# Dataset
df_team_batting: pd.DataFrame = pd.read_csv('./data/20230930_172103_team_stats_batting.csv')
df_team_pitching: pd.DataFrame = pd.read_csv('./data/20230930_172103_team_stats_pitcing.csv')
# データ集計した日（固定値）
STATS_DATE: str = '2023/9/30'

st.set_page_config(layout="wide")
st.title("阪神タイガースの優勝を知るChat AI（もどき）")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if type(message["content"]) == go.Figure:
            # Display chart
            st.plotly_chart(message["content"], use_container_width=True)
        else:
            # Display chat
            st.markdown(message["content"])

prompt: str = ""
# Accept user input
if prompt := st.chat_input("阪神タイガースは今年優勝しましたか?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = ""
        fig = None
        if prompt.startswith("阪神タイガースは今年"):
            assistant_response = "優勝しましたなー"
        elif prompt.startswith("本当ですか"):
            assistant_response = "本当やで"
        elif prompt.startswith("どうして優勝したの"):
            assistant_response = "たくさんお散歩して、相手のお散歩の邪魔をしたからや"
        elif prompt.startswith("証拠見せてよ"):
            assistant_response = "これは打者のデータなんだけど、どのチームより沢山散歩しているのがわかるかな"
            fig = bar(
                df=df_team_batting.sort_values(['pa_bb'], ascending=False),
                x=['pa_k', 'pa_bb'],
                y='team',
                x_dtick=2,
                x_range=[0, 18],
                title=f'【チーム打撃成績】三振および四球獲得までの平均打席数 ※{STATS_DATE}集計',
                x_title='pa_k（三振するまでの平均打席数）, ab_bb（四球獲得までの平均打席数）',
                y_title='チーム名（pa_bbの昇順）'
            )
        elif prompt.startswith("すごいなー、ピッチャーは"):
            assistant_response = "投手は逆に相手の打者に四球、すなわちお散歩を許していないんだ"
            fig = bar(
                df=df_team_pitching.sort_values(['bb_p'], ascending=False),
                x=['so_p', 'bb_p'],
                y='team',
                x_dtick=1,
                x_range=[0, 9],
                title=f"【チーム投手成績】奪三振率と与四球率の比較 ※{STATS_DATE}集計",
                x_title='so_p（奪三振率）, bb_p（与四球率）',
                y_title='チーム名（与四球率の昇順）'
            )
        elif prompt.startswith("CSと日本シリーズも期待していいかな？"):
            assistant_response = "知らんがな"
        elif prompt.startswith("もうええわ"):
            assistant_response = "どうも、ありがとうございましたー"
        else:
            assistant_response = "なんでや！阪神！！関係ないやろ！！！"

        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        if fig:
            # Display chart
            message_placeholder = st.empty()
            message_placeholder.plotly_chart(fig, use_container_width=True)

    # Add session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    if fig:
        st.session_state.messages.append({"role": "assistant", "content": fig})
