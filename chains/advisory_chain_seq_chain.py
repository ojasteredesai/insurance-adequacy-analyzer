import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
import os
import json
import re

# 🔐 Load API key from environment variable for secure access
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize LLMs and output parser
llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
llm1 = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
parser = StrOutputParser()

# Step 1: Prompt for evaluating insurance coverage adequacy
coverage_evaluator_prompt = PromptTemplate(
    input_variables=[
        'name', 'age', 'location', 'occupation', 'annualIncome', 'dependents',
        'existingLifeInsurance', 'existingHealthInsurance', 'existingAssetInsurance'
    ],
    template="""
You are an expert insurance advisor. Analyze the following user profile and evaluate the adequacy of their insurance coverage in three categories: life, health, and asset.

User Profile:
- Name: {name}
- Age: {age}
- Location: {location}
- Occupation: {occupation}
- Annual Income: ₹{annualIncome}
- Dependents: {dependents}
- Existing Life Insurance Amount: ₹{existingLifeInsurance}
- Existing Health Insurance Amount: ₹{existingHealthInsurance}
- Existing Asset Insurance Amount: ₹{existingAssetInsurance}

Coverage Evaluation:
- Name: {name}
- Life Insurance: [Sufficient/Insufficient]
- Health Insurance: [Sufficient/Insufficient]
- Asset Insurance: [Sufficient/Insufficient]

Return a JSON object with these keys:
- life_status: "Sufficient" or "Insufficient"
- life_existing_amount: existing life insurance amount in ₹ (Indian format)
- health_status: "Sufficient" or "Insufficient"
- health_existing_amount: existing health insurance amount in ₹ (Indian format)
- asset_status: "Sufficient" or "Insufficient"
- asset_existing_amount: existing asset insurance amount in ₹ (Indian format)

Respond ONLY with valid JSON. Do not include any explanation or extra text.
"""
)

# Step 2: Prompt for modeling coverage and identifying gaps
coverage_model_prompt = PromptTemplate(
    input_variables=['name','coverage_data_raw'],
    template="""
You are an advanced insurance corpus modeling expert. Analyze the following coverage evaluation and provide a structured analysis.

Coverage Evaluation: {coverage_data_raw}
Name: {name}

For each category (Life, Health, Asset), do the following:
- Clearly state the existing coverage amount (if available). If not provided, estimate a reasonable amount based on the user's profile and typical industry averages.
- Calculate and recommend the required coverage amount using standard industry formulas:
    - Life Insurance: Required Amount = 10 × Annual Income × (1 + 0.05 × Number of Dependents)
    - Health Insurance: Required Amount = 50% of Annual Income per family member
    - Asset Insurance: Required Amount = Estimated value of major assets (home, car, etc.)
- For each category, show:
    - Existing coverage amount (in ₹, Indian format, and in words)
    - Required coverage amount (in ₹, Indian format, and in words)
    - The gap between existing and required (in ₹, Indian format, and in words)
- List actionable recommendations to address these gaps with detailed reasons with calculations.

**Important:** Never return "unavailable" for any amount. Always provide a best estimate or placeholder value if data is missing.
**Format all currency amounts in Indian Rupees (₹) using Indian number formatting (e.g., ₹12,34,567.89) and also show the amount in words (e.g., Twelve Lakh Thirty Four Thousand Five Hundred Sixty Seven Rupees and Eighty Nine Paise).**

Return a JSON object with these keys:
- Hello {name}, Here is your insurance coverage analysis.
- coverage_summary: A concise summary of the adequacy of life, health, and asset insurance, including both existing, required, and gap amounts for each category, with all amounts in figures and words. It must have status (Sufficient/Insufficient) for each category.
- life_insurance: Detailed analysis for life insurance, including existing, required, and gap amounts (figures and words). Explain with formula how you arrived at the recommended coverage amounts.
- health_insurance: Detailed analysis for health insurance, including existing, required, and gap amounts (figures and words). Explain with formula how you arrived at the recommended coverage amounts.
- asset_insurance: Detailed analysis for asset insurance, including existing, required, and gap amounts (figures and words). Explain with formula how you arrived at the recommended coverage amounts.
- gaps_identified: List any gaps or inadequacies in coverage, with both existing and required amounts (figures and words). Explain the gaps with valid reasons and calculations.
- improvement_recommendations: Actionable suggestions to improve the user's insurance adequacy.

Respond ONLY with valid JSON. Do not include any explanation or extra text.
"""
)

# Chain for evaluating coverage adequacy
coverage_evaluator_chain = coverage_evaluator_prompt | llm | parser
# Chain for modeling coverage and identifying gaps
coverage_model_chain = coverage_model_prompt | llm1 | parser

# Streamlit UI setup
st.title("Insurance Adequacy Analyzer (IAA)")

# Collect user inputs for insurance profile
name = st.text_input("Name")
age = st.number_input("Age", min_value=18, max_value=65, step=1)
location = st.text_input("Location")
occupation = st.text_input("Occupation")
annualIncome = st.text_input("Annual Income")
dependents = st.text_input("Dependents")
existingLifeInsurance = st.text_area("Existing Life Insurance")
existingHealthInsurance = st.text_area("Existing Health Insurance")
existingAssetInsurance = st.text_area("Existing Asset Insurance")

# Run analysis only if all required fields are filled
if name and age and location and occupation and annualIncome and dependents and existingLifeInsurance and existingHealthInsurance and existingAssetInsurance:

    # Step 1: Invoke coverage evaluator chain with user inputs
    coverage_evaluator_response = coverage_evaluator_chain.invoke({
        "name": name,
        "age": age,
        "location": location,
        "occupation": occupation,
        "annualIncome": annualIncome,   
        "dependents": dependents,
        "existingLifeInsurance": existingLifeInsurance,
        "existingHealthInsurance": existingHealthInsurance,
        "existingAssetInsurance": existingAssetInsurance
    })

    # Step 2: Clean response and parse JSON from coverage evaluator
    # Remove code block markers if present
    if coverage_evaluator_response.strip().startswith("```"):
        coverage_evaluator_response_clean = re.sub(
            r"^```json\s*|^```\s*|```$", "", coverage_evaluator_response.strip(), flags=re.MULTILINE
        ).strip()
    else:
        coverage_evaluator_response_clean = coverage_evaluator_response.strip()

    # Convert JSON string to Python dictionary
    coverage_data_raw = json.loads(coverage_evaluator_response_clean)

    # Step 3: Invoke coverage model chain with evaluator output
    coverage_model_response = coverage_model_chain.invoke({
        "coverage_data_raw": json.dumps(coverage_data_raw),
        "name": name
    })
    
    # Step 4: Clean response and parse JSON from coverage model
    # Remove code block markers if present
    if coverage_model_response.strip().startswith("```"):
        coverage_model_response_clean = re.sub(
            r"^```json\s*|^```\s*|```$", "", coverage_model_response.strip(), flags=re.MULTILINE
        ).strip()
    else:
        coverage_model_response_clean = coverage_model_response.strip()

    # Convert JSON string to Python dictionary
    coverage_model_data_raw = json.loads(coverage_model_response_clean)
    st.write("Raw coverage model  output:", coverage_model_data_raw)  # Debug output
