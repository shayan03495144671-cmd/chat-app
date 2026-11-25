import os
import streamlit as st
from anthropic import Anthropic, APIError, AuthenticationError, RateLimitError

MODEL = "claude-sonnet-5-5"
MAX_HISTORY = 20  # sirf akhri 20 messages bhejte hain taake tokens kam lagein

st.set_page_config(page_title="Chat App", page_icon="💬")
st.title("💬 Chat App")


def get_api_key():
    key = os.getenv("ANTHROPIC_API_KEY")
    if key:
        return key
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        return None


api_key = get_api_key()
if not api_key:
    st.error("API key nahi mili. ANTHROPIC_API_KEY set karein.")
    st.stop()

client = Anthropic(api_key=api_key)

# ---- session state ----
if "messages" not in st.session_state:
    st.session_state.messages = []
if "tokens_in" not in st.session_state:
    st.session_state.tokens_in = 0
if "tokens_out" not in st.session_state:
    st.session_state.tokens_out = 0

# ---- sidebar: settings ----
with st.sidebar:
    st.header("Settings")
    instructions = st.text_area(
        "Custom instructions",
        value="You are a helpful assistant. Keep answers short and clear.",
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.slider("Max response tokens", 100, 2000, 500, 100)

    st.divider()
    st.write(f"Input tokens: {st.session_state.tokens_in}")
    st.write(f"Output tokens: {st.session_state.tokens_out}")

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.session_state.tokens_in = 0
        st.session_state.tokens_out = 0
        st.rerun()

# ---- purani chat dikhao ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---- nayi input ----
user_input = st.chat_input("Kuch poochein...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Soch raha hoon..."):
                response = client.messages.create(
                    model=MODEL,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=instructions,
                    messages=st.session_state.messages[-MAX_HISTORY:],
                )
            reply = response.content[0].text
            st.write(reply)

            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.tokens_in += response.usage.input_tokens
            st.session_state.tokens_out += response.usage.output_tokens
            st.rerun()

        except AuthenticationError:
            st.error("API key galat hai.")
        except RateLimitError:
            st.error("Bohat zyada requests. Thori der baad try karein.")
        except APIError as e:
            st.error(f"API error: {e}")
        except Exception as e:
            st.error(f"Kuch masla hua: {e}")
