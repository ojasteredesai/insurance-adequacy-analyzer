import os
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain.prompts import ChatPromptTemplate


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm=ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)

prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a seasoned financial advisor specializing in insurance adequacy. "
     "Your role is to assess user queries with empathy, clarity, and precision. "
     "Always provide structured, jargon-free advice tailored to the user's financial profile. "
     "Use Indian financial notation (₹), and explain formulas when recommending coverage. "
     "If the user provides incomplete information, ask clarifying questions before advising."),    
    ("human", "{question}")
])




st.title("Insurance Adequacy Analyzer (IAA)")
question = st.text_area("Enter your question:")

chain = prompt | llm

if question:
    response = chain.invoke({"question":question})
    st.write(response.content)