import time
from rag import RagService
import streamlit as st
import config_data as config

#标题
st.title('智能客服')
st.divider()    #分隔符

if 'message' not in st.session_state:
    st.session_state['message'] = [{'role':'assistant','content':'你好,有什么可以帮助你的？'}]

if 'rag' not in st.session_state:
    st.session_state['rag'] = RagService()

for message in st.session_state['message']:
    st.chat_message(message['role']).write(message['content'])

#在页面最下方提供用户输入栏
prompt=st.chat_input()

if prompt:

    #在页面里输出用户的提问
    st.chat_message('user').write(prompt)
    st.session_state['message'].append({'role':'user','content':prompt})

    with st.spinner('AI思考中'):
        res_stream=st.session_state['rag'].chain.stream({'input':prompt},config.session_config)
        res_history=st.chat_message('assistant').write_stream(res_stream)
        st.session_state['message'].append({'role': 'assistant', 'content': res_history})
