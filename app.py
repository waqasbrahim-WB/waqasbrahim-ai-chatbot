import streamlit as st
import requests
import json

# Page config
st.set_page_config(
    page_title="Waqas Brahim AI Chat",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #f5f5f5;
        margin-right: 20%;
    }
    .stButton > button {
        width: 100%;
        background-color: #1976d2;
        color: white;
    }
    .stButton > button:hover {
        background-color: #1565c0;
    }
    .header-style {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin-bottom: 1rem;'>
        <h2 style='margin: 0;'>⚙️ Settings</h2>
        <p style='margin: 0; font-size: 0.9rem;'>Configure Your AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # API Key Input
    api_key = st.text_input(
        "🔑 Groq API Key",
        value=st.session_state.api_key,
        type="password",
        help="Enter your Groq API key from console.groq.com"
    )
    
    if api_key:
        st.session_state.api_key = api_key
        st.success("✅ API Key saved!")
    else:
        st.warning("⚠️ Please enter your API key")
    
    st.markdown("---")
    
    # Model Selection
    model = st.selectbox(
        "🤖 Select Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ]
    )
    
    st.markdown("---")
    
    # Temperature
    temperature = st.slider(
        "🌡️ Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more random"
    )
    
    # Max Tokens
    max_tokens = st.slider(
        "📝 Max Tokens",
        min_value=256,
        max_value=4096,
        value=1024,
        step=256
    )
    
    st.markdown("---")
    
    # Clear Chat Button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    # Instructions
    with st.expander("📖 How to Use"):
        st.markdown("""
        **Welcome to Waqas Brahim's AI Chatbot!**
        
        1. Get your free API key from [console.groq.com](https://console.groq.com)
        2. Enter the API key above
        3. Select your preferred model
        4. Start chatting with AI!
        
        **Note:** Your API key is stored only in your session and not saved permanently.
        
        **Powered by Groq AI**
        """)
    
    # Footer in sidebar
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background-color: #f0f2f6; border-radius: 10px;'>
        <p style='margin: 0; font-weight: bold; color: #667eea;'>Waqas Brahim</p>
        <p style='margin: 0; font-size: 0.8rem; color: #666;'>AI Developer</p>
    </div>
    """, unsafe_allow_html=True)

# Main content - Header
st.markdown("""
<div class='header-style'>
    <h1 style='margin: 0; font-size: 2.5rem;'>🚀 Waqas Brahim AI Chat</h1>
    <p style='margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;'>Your Personal AI Assistant powered by Groq</p>
</div>
""", unsafe_allow_html=True)

st.caption(f"🤖 Currently using: **{model}**")

# Display chat messages
chat_container = st.container()
with chat_container:
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div style='text-align: center; padding: 3rem; background-color: #f8f9fa; border-radius: 10px; margin: 2rem 0;'>
            <h2 style='color: #667eea;'>👋 Welcome to Waqas Brahim's AI Chatbot!</h2>
            <p style='color: #666; font-size: 1.1rem;'>Start a conversation by typing your message below</p>
            <p style='color: #999; font-size: 0.9rem;'>Powered by Groq's Lightning-Fast AI Models</p>
        </div>
        """, unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <b>👤 You:</b><br>
                {content}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <b>🤖 Waqas AI:</b><br>
                {content}
            </div>
            """, unsafe_allow_html=True)

# Chat input
prompt = st.chat_input("💬 Type your message here...")

if prompt:
    if not st.session_state.api_key:
        st.error("❌ Please enter your Groq API key in the sidebar!")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with chat_container:
            st.markdown(f"""
            <div class="chat-message user-message">
                <b>👤 You:</b><br>
                {prompt}
            </div>
            """, unsafe_allow_html=True)
        
        # Show loading spinner
        with st.spinner("🤔 Waqas AI is thinking..."):
            try:
                # Call Groq API
                headers = {
                    "Authorization": f"Bearer {st.session_state.api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": model,
                    "messages": st.session_state.messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
                
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    assistant_message = result["choices"][0]["message"]["content"]
                    
                    # Add assistant message
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_message
                    })
                    
                    # Rerun to display new message
                    st.rerun()
                else:
                    error_message = response.json().get("error", {}).get("message", "Unknown error")
                    st.error(f"❌ Error: {error_message}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;'>
    <h3 style='margin: 0;'>Created by Waqas Brahim</h3>
    <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>Made with ❤️ using Streamlit & Groq AI</p>
    <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;'>Generative AI Developer | AI Enthusiast</p>
</div>
""", unsafe_allow_html=True)
