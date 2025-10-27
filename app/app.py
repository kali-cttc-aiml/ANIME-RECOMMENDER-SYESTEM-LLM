import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv
import re
import base64

st.set_page_config(page_title="Anime Recommender", layout="wide", page_icon="🎥")

# Function to add super cool animated background
def add_super_cool_background():
    st.markdown(
        """
        <style>
        body {
            font-size: 18px;
        }
        h1, h2, h3, h4, h5, h6 {
            font-size: 2em;
            text-align: center;
        }
        .stApp {
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c, #4facfe, #00f2fe);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .stApp > header {
            background-color: rgba(255, 255, 255, 0.9);
        }
        .stSidebar {
            background-color: rgba(255, 255, 255, 0.95);
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: rgba(255, 255, 255, 0.9);
        }
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 255, 255, 0.9);
        }
        .stButton > button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 15px 30px;
            font-size: 20px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
            background: linear-gradient(45deg, #764ba2, #667eea);
        }
        .stTextInput > div > div > input {
            border-radius: 15px;
            border: 2px solid #667eea;
            padding: 15px;
            font-size: 18px;
            transition: all 0.3s ease;
            text-align: center;
        }
        .stTextInput > div > div > input:focus {
            border-color: #764ba2;
            box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
        }
        .stExpander {
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            background-color: rgba(255, 255, 255, 0.8);
            text-align: center;
        }
        .stColumns {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .stMarkdown, .stText, .stInfo, .stSuccess {
            text-align: center;
        """,
        unsafe_allow_html=True
    )

add_super_cool_background()

load_dotenv()

@st.cache_resource
def init_pipeline():
    return AnimeRecommendationPipeline()

pipeline = init_pipeline()

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state.history = []

# Initialize session state for current view
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'recommend'

# Sidebar
with st.sidebar:
    st.header("🎥 Anime Recommender")
    st.markdown("Discover your next favorite anime based on your preferences!")
    st.markdown("---")
    st.subheader("About")
    st.markdown("This app uses AI to recommend anime based on your descriptions. Powered by LangChain and Groq.")
    st.markdown("---")
    if st.button("Clear History"):
        st.session_state.history = []
        st.success("History cleared!")

# Main content
st.title("🎥 Anime Recommender System")

# Buttons to switch views
col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 Get Recommendations"):
        st.session_state.current_view = 'recommend'
with col2:
    if st.button("📚 View History"):
        st.session_state.current_view = 'history'

# Display content based on current view
if st.session_state.current_view == 'recommend':
    st.subheader("Find Your Next Anime")
    query = st.text_input("Enter your anime preferences (e.g., light-hearted anime with school settings)", placeholder="Describe what you're looking for...")

    if query:
        with st.spinner("🔍 Fetching recommendations for you..."):
            progress_bar = st.progress(0)
            progress_bar.progress(50)
            response = pipeline.recommend(query)
            progress_bar.progress(100)
            progress_bar.empty()

        # Add to history
        st.session_state.history.append({"query": query, "response": response})

        st.success("Recommendations ready! 🎉")

        # Parse and display recommendations
        st.markdown("### 🎯 Your Recommendations")

        # Split response into recommendations (assuming the response is structured)
        recommendations = re.split(r'\d+\.', response.strip())
        recommendations = [rec.strip() for rec in recommendations if rec.strip()]

        if recommendations:
            cols = st.columns(3)
            for i, rec in enumerate(recommendations[:3]):  # Limit to 3
                with cols[i % 3]:
                    with st.expander(f"📺 Recommendation {i+1}"):
                        st.write(rec)
        else:
            st.write(response)

elif st.session_state.current_view == 'history':
    st.subheader("Your Recommendation History")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Query {len(st.session_state.history)-i}: {item['query'][:50]}..."):
                st.markdown(f"**Query:** {item['query']}")
                st.markdown("**Recommendations:**")
                st.write(item['response'])
    else:
        st.info("No history yet. Start by making some recommendations! 🎬")


