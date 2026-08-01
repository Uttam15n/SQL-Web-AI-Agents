from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_community.utilities import GoogleSerperAPIWrapper
import streamlit as st
from langgraph.checkpoint.memory import MemorySaver

st.subheader("Hello Your AI Assistant Here Chat Now")

llm=ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite",streaming=True)

search=GoogleSerperAPIWrapper()


history=[]

if "memory" not in st.session_state:
  st.session_state.memory=MemorySaver()

if "history" not in st.session_state:
    st.session_state.history = []

history = st.session_state.history

agent=create_agent(
  model=llm,
  tools=[search.run],
  system_prompt="Your are an AI Assistant and you can use the tool for seraching",
  checkpointer=st.session_state.memory
)



query=st.chat_input()

for message in history:
  role=message["role"]
  text=message["content"]
  st.chat_message(role).markdown(text)

if query:
  st.chat_message("user").markdown(query)
  history.append({"role":"user","content":query})
  def generate():
    for chunk in agent.stream({"messages":[{"role":"user","content":query}]},{"configurable":{"thread_id":"asd123"}}):
      print(chunk)
      yield str(chunk)
  
  st.write_stream(generate())
  
  