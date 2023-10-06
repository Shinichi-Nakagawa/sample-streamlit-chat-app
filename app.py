import streamlit as st
import time

st.title("[sample]阪神タイガースChat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
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
        if prompt.startswith("阪神"):
            assistant_response = "優勝したがな"
        elif prompt.startswith("どうやって"):
            assistant_response = "データ見たらわかるがな"
        elif prompt.startswith("ほんまか"):
            assistant_response = "しゃーない, データ見てみようか"
        else:
            assistant_response = "阪神関係ないがな"

        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
