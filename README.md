# Chat App

Simple AI chat app (Python + Streamlit + Anthropic API).

Features: chat history, custom instructions, temperature / max token controls, token counter, error handling.

## Run locally
```
pip install -r requirements.txt
set ANTHROPIC_API_KEY=your_key      # Windows
streamlit run app.py
```

## Deploy
Streamlit Community Cloud par GitHub repo connect karein, aur Settings > Secrets mein yeh add karein:
```
ANTHROPIC_API_KEY = "your_key"
```
