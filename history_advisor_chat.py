import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableConfig

# 🔐 Load API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🤖 Model
llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)

# 🧠 Prompt with history placeholder
prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a seasoned financial advisor specializing in insurance adequacy. "
     "Your role is to assess user queries with empathy, clarity, and precision. "
     "Always provide structured, jargon-free advice tailored to the user's financial profile. "
     "Use Indian financial notation (₹), and explain formulas when recommending coverage. "
     "If the user provides incomplete information, ask clarifying questions before advising."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

# 🔗 Chain
chain = prompt | llm

# 💬 Chat history stored in Streamlit session state
chat_history = StreamlitChatMessageHistory(key="chat_messages")

# 🧩 Wrap chain with message history
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: chat_history,
    input_messages_key="question",
    history_messages_key="chat_history"
)

# 🖥️ Streamlit UI
st.title("Insurance Adequacy Analyzer (IAA)")

# Display past messages
for msg in chat_history.messages:
    st.chat_message(msg.type).write(msg.content)

# Input box for new message
if prompt := st.chat_input("Ask your insurance question..."):
    st.chat_message("human").write(prompt)

    # Invoke chain with memory
    response = chain_with_history.invoke(
        {"question": prompt},
        config=RunnableConfig(configurable={"session_id": "user-session"})
    )

    st.chat_message("ai").write(response.content)