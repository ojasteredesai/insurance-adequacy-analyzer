import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

prompt = PromptTemplate(
    input_variables=['name', 'age', 'location', 'occupation', 'annualIncome', 'dependents', 'existingInsurance'],
    template="""
You are a financial insurance advisor helping individuals assess the adequacy of their current insurance coverage.

User Profile:
- Name: {name}
- Age: {age}
- Location: {location}
- Occupation: {occupation}
- Annual Income: ₹{annualIncome}
- Number of Dependents: {dependents}
- Existing Insurance Details: {existingInsurance}

Your task:
1. Evaluate whether the user's current insurance coverage is sufficient across life, health, and asset categories.
2. Highlight any gaps or risks based on their income, dependents, and occupation.
3. Recommend ideal coverage amounts and types of insurance they should consider.
4. Provide actionable next steps in simple, jargon-free language.

Respond with a clear, structured advisory that empowers the user to make informed decisions.
Finally create a tabular summary of the recommendations and highlight recommendations with appropriate green and red text colors with appropriate check and cross image.
Explain with formula how you arrived at the recommended coverage amounts.
"""
)


llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)

st.title("Insurance Adequacy Analyzer (IAA) App")

name = st.text_input("Name")
age = st.number_input("Age", min_value=18, max_value=65, step=1)
location = st.text_input("Location")
occupation = st.text_input("Occupation")
annualIncome = st.text_input("Annual Income")
dependents = st.text_input("Dependents")
existingInsurance = st.text_area("Existing Insurance")

if name and age and location and occupation and annualIncome and dependents and existingInsurance:
    response = llm.invoke(prompt.format(name=name,
                                        age=age,
                                        location=location,
                                        occupation=occupation,
                                        annualIncome=annualIncome,
                                        dependents=dependents,
                                        existingInsurance=existingInsurance))
    st.write(response.content)