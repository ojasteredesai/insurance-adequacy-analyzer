import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
import os

# 🔐 Load API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🧠 Define prompt template
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

🧾 Format your response EXACTLY as follows:

---
## Insurance Adequacy Report

### Coverage Evaluation
- Life Insurance: [Adequate/Inadequate]
- Health Insurance: [Adequate/Inadequate]
- Asset Insurance: [Adequate/Inadequate]

### Identified Gaps
- [List of gaps]

### Recommended Coverage
| Type           | Recommended Amount | Rationale / Formula |
|----------------|--------------------|----------------------|
| Life Insurance | ₹X                 | [Formula]            |
| Health         | ₹Y                 | [Formula]            |
| Asset          | ₹Z                 | [Formula]            |

### Next Steps ✅
1. [Step 1]
2. [Step 2]
3. [Step 3]

Use ✅ for good coverage and ❌ for gaps. Use green text for adequate and red for inadequate.
---
"""
)

# 🤖 Define model and parser
llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
parser = StrOutputParser()

# 🔗 Build LCEL chain: prompt → model → parser
chain = prompt | llm | parser

# 🖥️ Streamlit UI
st.title("Insurance Adequacy Analyzer (IAA) App")

name = st.text_input("Name")
age = st.number_input("Age", min_value=18, max_value=65, step=1)
location = st.text_input("Location")
occupation = st.text_input("Occupation")
annualIncome = st.text_input("Annual Income")
dependents = st.text_input("Dependents")
existingInsurance = st.text_area("Existing Insurance")

# 🚀 Run chain if all inputs are filled
if name and age and location and occupation and annualIncome and dependents and existingInsurance:
    inputs = {
        "name": name,
        "age": age,
        "location": location,
        "occupation": occupation,
        "annualIncome": annualIncome,
        "dependents": dependents,
        "existingInsurance": existingInsurance
    }
    response = chain.invoke(inputs)
    st.write(response)