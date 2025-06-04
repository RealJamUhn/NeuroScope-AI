# NeuroScope-AI
SCSP Hackathon Submission

## Setup

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/NeuroScopeAI.git
cd NeuroScopeAI
```
### 2. Create a Virtual Environment (Optional)
```bash
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Add Your Anthropic Key
Create a .env file or set this in a .py file
```bash
import os
os.environ["ANTHROPIC_API_KEY"] = "your-key-here"
