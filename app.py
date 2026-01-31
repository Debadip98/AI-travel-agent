# pylint: disable = invalid-name
import os
import uuid
import streamlit as st
from langchain_core.messages import HumanMessage
from agents.agent import Agent

# Page Config
st.set_page_config(page_title="AI Travel Agent", page_icon="✈️", layout="wide")

# --- CUSTOM CSS: ANTIGRAVITY THEME ---
st.markdown("""
<style>
    /* Dark Mode Body */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Hero Title */
    .hero-title {
        font-size: 4em;
        font-weight: 800;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 1em;
        margin-bottom: 0.2em;
        text-shadow: 0px 0px 20px rgba(0, 210, 255, 0.5);
    }
    
    .hero-subtitle {
        font-size: 1.5em;
        text-align: center;
        color: #b0b0b0;
        margin-bottom: 2em;
    }

    /* Cards (Glassmorphism) */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Primary Button */
    .stButton > button {
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.6);
    }
    
    /* Text Inputs */
    .stTextArea textarea {
        background-color: #1a1e26;
        color: white;
        border: 1px solid #333;
        border-radius: 10px;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #00d2ff !important;
    }
</style>
""", unsafe_allow_html=True)


def initialize_agent():
    if 'agent' not in st.session_state:
        st.session_state.agent = Agent()

def landing_page():
    st.markdown('<div class="hero-title">AI Travel Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Plan your next adventure with <b>Antigravity</b> precision.</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h3>Start Your Journey</h3>
            <p>Describe your dream trip (budget, location, preferences).</p>
        </div>
        """, unsafe_allow_html=True)

def process_query(user_input):
    if user_input:
        try:
            thread_id = str(uuid.uuid4())
            st.session_state.thread_id = thread_id
            
            with st.spinner("🤖 AI is researching flight & hotel options..."):
                messages = [HumanMessage(content=user_input)]
                config = {'configurable': {'thread_id': thread_id}}
                result = st.session_state.agent.graph.invoke({'messages': messages}, config=config)
                
            st.session_state.travel_info = result['messages'][-1].content
            st.rerun()

        except Exception as e:
            st.error(f'Error: {e}')
    else:
        st.error('Please enter a travel query.')

def generate_html_itinerary():
    if 'travel_info' in st.session_state and 'thread_id' in st.session_state:
        with st.spinner("🎨 Generating beautiful itinerary..."):
            # Invoke the graph specifically to trigger the email logic (which now returns HTML)
            # We need to replicate the 'email_sender' call or just invoke with None if the graph state is saved.
            # The previous code called `agent.graph.invoke(None, config=config)`. 
            # Since `email_sender` is interrupt_before, we continue the graph.
            config = {'configurable': {'thread_id': st.session_state.thread_id}}
            result = st.session_state.agent.graph.invoke(None, config=config)
            
            # The result keys will contain the output of the last node run
            last_message = result['messages'][-1]
            if hasattr(last_message, 'name') and last_message.name == "html_itinerary":
                st.session_state.html_content = last_message.content
                st.success("Itinerary generated!")
            else:
                 # Fallback if the graph didn't return what we expected
                 st.warning("Could not generate HTML. Showing text version.")
                 st.session_state.html_content = f"<html><body><pre>{st.session_state.travel_info}</pre></body></html>"


def main():
    # Check for API keys
    if not os.getenv("OPENAI_API_KEY"):
         st.error("⚠️ OPENAI_API_KEY is missing!")
         st.info("To fix this, go to your Streamlit App settings -> Secrets and add your OpenAI API key.")
         st.code('OPENAI_API_KEY = "sk-..."', language="toml")
         st.stop()
         
    if not os.getenv("SERPAPI_API_KEY"):
         st.warning("⚠️ SERPAPI_API_KEY is missing. Search functionality may not work.")
         st.info("Add it to Streamlit Secrets if you want live travel data.")

    initialize_agent()
    
    # Sidebar
    with st.sidebar:
        st.image('images/ai-travel.png', caption='Antigravity Travel')
        st.markdown("### 🛠 Preferences")
        st.info("Operating in 'Cheapest Traveler' Mode.")
        st.markdown("---")
        st.caption("Powered by LangGraph & Google DeepMind Antigravity")

    # Main Content
    if 'travel_info' not in st.session_state:
        landing_page()
        
    # Input Area (Always visible at bottom or top - let's keep it usually central)
    user_input = st.text_area("Where do you want to go?", height=100, placeholder="Plan a trip to Norway for Northern Lights...")
    
    if st.button("Plan Trip 🚀"):
        process_query(user_input)

    # Results Display
    if 'travel_info' in st.session_state:
        st.markdown("---")
        st.markdown("### 🗺️ Research Results")
        
        with st.expander("View Raw Research Data", expanded=True):
            st.markdown(st.session_state.travel_info)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
             st.info("Satisfied with the research? Generate a visual itinerary.")
        with col2:
             if st.button("✨ Generate Visual Itinerary"):
                 generate_html_itinerary()
                 
    # HTML Itinerary Display
    if 'html_content' in st.session_state:
        st.markdown("### 🎫 Your Itinerary")
        st.components.v1.html(st.session_state.html_content, height=800, scrolling=True)
        
        # Download Button
        st.download_button(
            label="Download Itinerary HTML",
            data=st.session_state.html_content,
            file_name="itinerary.html",
            mime="text/html"
        )

if __name__ == '__main__':
    main()
