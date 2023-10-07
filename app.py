import streamlit as st
import time
import pandas as pd
import plotly.graph_objs as go

from graph import bar

df_team_batting: pd.DataFrame = pd.read_csv('./data/20230930_172103_team_stats_batting.csv')
df_team_pitching: pd.DataFrame = pd.read_csv('./data/20230930_172103_team_stats_pitcing.csv')

st.set_page_config(layout="wide")
st.title("[sample]阪神タイガースChat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if type(message["content"]) == go.Figure:
            st.plotly_chart(message["content"], use_container_width=True)
        else:
            st.markdown(message["content"])

prompt: str = ""
# Accept user input
if prompt := st.chat_input("阪神タイガースについて何でも聞いてみて"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = ""
        fig = None
        if prompt.startswith("阪神"):
            assistant_response = "優勝したがな"
        elif prompt.startswith("どうやって"):
            assistant_response = "データ見たらわかるがな"
        elif prompt.startswith("データ見せて"):
            assistant_response = "沢山散歩して勝ったんだよ"
            fig = bar(
                df=df_team_batting.sort_values(['pa_bb'], ascending=False),
                x=['pa_k', 'pa_bb'],
                y='team',
                x_dtick=2,
                x_range=[0, 18],
                title='【チーム打撃成績】三振および四球獲得までの平均打席数 ※2023/9/30集計',
                x_title='pa_k（三振するまでの平均打席数）, ab_bb（四球獲得までの平均打席数）',
                y_title='チーム名（pa_bbの昇順）'
            )
        else:
            assistant_response = "阪神関係ないがな"

        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        if fig:
            message_placeholder.plotly_chart(fig, use_container_width=True)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    if fig:
        st.session_state.messages.append({"role": "assistant", "content": fig})
