# 🧩 Agile User Story Parser (LangChain Structured Output)

Turn raw requirement text into a **clean, structured Agile user story** with:
- `title`
- `description`
- `acceptance_criteria_1 … acceptance_criteria_5`
- `severity` (e.g., Low, Medium, High, Critical)
- `type` (feature, bug fix, improvement, technical task)

Powered by **LangChain** `StructuredOutputParser` + **OpenAI** GPT-4o-mini for schema-aligned JSON.

---

## ✨ What this does

- Accepts free-form requirement text.
- Uses **response schemas** (`ResponseSchema`) to coerce the LLM into a **strict JSON** shape.
- Expands multiple acceptance criteria into **separate fields** (AC1–AC5) and avoids comma-stuffed ACs.
- Fills missing fields intelligently (e.g., constructs a brief `title` if not provided).


## 🧱 Project layout
├─ src/
│ └─ agile_user_story_parser.py # main script (your code)
├─ examples/
│ └─ sample_input.txt # optional input example
├─ .env.example
├─ requirements.txt
├─ .gitignore
└─ README.md



## 🔐 Setup

1) **Clone & enter**
```bash
git clone https://github.com/<your-username>/langchain-agile-user-story-parser.git
cd langchain-agile-user-story-parser



2. Create venv (recommended)

bash
Copy code
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate


3. Install deps

bash
Copy code
pip install -r requirements.txt


4. Set your key

Copy .env.example → .env and paste your key:


OPENAI_API_KEY=your_openai_api_key_here
If .env is missing, the script will securely prompt you once at runtime.


▶️ Run
python src/agile_user_story_parser.py


The script includes a sample user_story_requirement:

I want an option to stay logged in, so that i dont have to enter my credentials every time.


It will print a JSON like:

{
  "title": "Stay Logged In option",
  "description": "As a user, I want a 'Remember me' or 'Stay logged in' option so I don't need to re-enter credentials every time.",
  "acceptance_criteria_1": "Given I select 'Stay logged in', when I log in successfully, then my session persists across browser restarts.",
  "acceptance_criteria_2": "Given inactivity policies, when the max idle time is exceeded, then the session is securely invalidated.",
  "acceptance_criteria_3": "Given I manually sign out, when I log out, then the session is cleared and I must re-authenticate.",
  "acceptance_criteria_4": "",
  "acceptance_criteria_5": "",
  "severity": "Medium",
  "type": "feature"
}


Notes:

Empty AC fields are left as "" when fewer than five are needed.

If a user provides comma-separated ACs, the parser splits into separate criteria where possible.

-------------------------------------------------------------

🧠 How it works

Defines a response schema with ResponseSchema for each desired field.

Builds a prompt with ChatPromptTemplate that instructs the model to:

Create/normalize title, description.

Expand acceptance criteria into independent bullets.

Keep extra properties out (StructuredOutputParser enforces shape).

Calls the LLM and parses its text output into a Python dict with:

output_dict = output_parser.parse(response.content)


Core libraries:

langchain_core.prompts.ChatPromptTemplate

langchain.output_parsers.ResponseSchema

langchain.output_parsers.StructuredOutputParser

langchain_openai.ChatOpenAI

---------------------------------------------------------------------------------

🧪 Try your own input

Replace in src/agile_user_story_parser.py:

user_story_requirement = \"\"\"\
As a shopper, I want to filter products by price range so I can quickly find items within my budget.
\"\"\"

Run again:

python src/agile_user_story_parser.py

---------------------------------------------------------------------------------

🛡️ Quality tips

Determinism: lower temperature (e.g., 0.2) for more consistent JSON.

Validation: you can add jsonschema or pydantic to hard-validate after parsing.

Scaling ACs: if you need dynamic AC lists, switch to an array field (e.g., acceptance_criteria: string[]) instead of fixed 1..5.

---------------------------------------------------------------------------------

🔮 Roadmap ideas

Export results to Jira/Azure Boards via API.

CLI flags to pass input text/file.

Web UI (FastAPI/Streamlit) with copy-to-Jira button.

Add priority, story_points, epic, and labels to schema.

---------------------------------------------------------------------------------

📄 License

MIT