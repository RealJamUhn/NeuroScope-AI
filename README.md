# 🧠 NeuroScope AI: MultiModal Autism Diagnostic Assistant
This is a repository for all the code used in my SCSP Hackathon submission.

**NeuroScope AI** is an intelligent diagnostic assistant that evaluates Autism Spectrum Disorder (ASD) using a multi-modal, clinically grounded approach. Powered by **Claude 4 Opus**, the system integrates four specialized agents to analyze a patient's:

- 🩺 **Medical and developmental history**
- 👁️ **Visual behavior from video**
- 🔊 **Speech and audio characteristics**
- 🕓 **Age-specific context**

These agents collaborate under a unified **DiagnosisAgent**, which synthesizes their outputs and compares them against structured DSM-5 criteria. This comparison is facilitated by a custom-built **Model Context Protocol (MCP) server**, which exposes the DSM-5 as a structured, queryable diagnostic knowledge base.

---

## 🔍 Key Features

- 🤖 **Claude 4 Opus–powered agents** for behavioral, audio, visual, and history analysis
- 📼 **Video frame analysis** to detect physical behavioral indicators
- 🎙️ **Audio transcription with delay tracking** between questions and responses
- 📊 **Structured DSM-5 reference via MCP** tools and criteria matching
- 🧠 **Evidence-based diagnosis** with confidence score and comorbidity assessment
- ⚡ **Fast, scalable, and explainable** alternative to traditional ASD evaluations

---

## 🎯 Project Goal

NeuroScope AI aims to reduce diagnostic ambiguity, enhance early detection, and provide clinicians with a fast, accessible, and affordable tool for autism screening. By automating key aspects of the diagnostic process while retaining clinical rigor, the system is designed to improve healthcare equity and empower data-driven decision-making in developmental mental health.

---

### 🔧 Prerequisites

- Python 3.11
- An [Anthropic Claude API key](https://docs.anthropic.com/claude/docs/api-reference)
- A modern browser (for Streamlit UI)
- Recommended: Virtual environment

## 🚀 Setup

### 1. Clone the Repo
In your computer terminal type the following:
```bash
git clone https://github.com/yourusername/NeuroScopeAI.git
cd NeuroScopeAI
```
### 2. Create a Virtual Environment (Optional)
In your IDE terminal type the following:
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
```
### 5. Run The Streamlit App
In your IDE terminal:
```bash
streamlit run main.py
```
