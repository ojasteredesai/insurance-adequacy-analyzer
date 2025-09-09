# Insurance Adequacy Analyzer (IAA)

## Overview

Insurance Adequacy Analyzer (IAA) is an interactive Streamlit application powered by advanced LLMs (OpenAI GPT-4o or Mistral). It helps users assess the adequacy of their life, health, and asset insurance coverage based on their personal profile and industry benchmarks. The app provides actionable recommendations and models required coverage amounts using standard formulas.

---

## Features

- **User Profile Input:** Collects details such as name, age, location, occupation, annual income, dependents, and existing insurance amounts.
- **Coverage Evaluation:** Uses an LLM to evaluate the sufficiency of life, health, and asset insurance, returning a structured JSON summary.
- **Coverage Modeling:** Models required coverage amounts using industry-standard formulas and highlights gaps.
- **Recommendations:** Provides actionable suggestions to improve insurance adequacy.
- **Indian Currency Formatting:** All amounts are displayed in Indian Rupees (₹) with proper Indian number formatting and amounts in words.
- **Secure API Key Handling:** Loads API keys from environment variables.

---

## Tech Stack

- Python
- Streamlit
- LangChain
- OpenAI GPT-4o (or Mistral LLM)

---

## How It Works

1. **User Input:** Enter your insurance profile details in the Streamlit UI.
2. **Coverage Evaluation:** The app uses an LLM to analyze your profile and returns a JSON summary of insurance adequacy.
3. **Coverage Modeling:** The output is passed to a second LLM chain that models required coverage amounts, identifies gaps, and provides recommendations.
4. **Results Display:** All results are shown in the app, including raw JSON outputs for transparency and debugging.

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/insurance-adequacy-analyzer.git
   cd insurance-adequacy-analyzer
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set your OpenAI API key:**
   - On Windows:
     ```sh
     set OPENAI_API_KEY=your_openai_api_key
     ```
   - On Linux/Mac:
     ```sh
     export OPENAI_API_KEY=your_openai_api_key
     ```

---

## Usage

1. **Run the Streamlit app:**
   ```sh
   streamlit run chains/advisory_chain_seq_chain.py
   ```

2. **Fill in your insurance profile details in the UI.**
3. **View your coverage evaluation, modeled recommendations, and gaps.**

---

## Project Structure

```
insurance-adequacy-analyzer/
│
├── chains/
│   ├── advisory_chain_seq_chain.py   # Main Streamlit app and chains
│   └── example.py                   # Example chain usage
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation
```

---

## Customization

- **LLM Model:** You can switch between OpenAI GPT-4o and Mistral by changing the model name in the code.
- **Prompts:** Prompts for both chains are fully customizable for your business logic or region.
- **Currency Formatting:** All amounts are formatted in Indian style; you can adjust formatting logic if needed.

---

## License

This project is licensed under the MIT License.

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## Contact

For questions or support, please open an issue on.

Ojas Teredesai
