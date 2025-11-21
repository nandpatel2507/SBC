import streamlit as st
import anthropic
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Restaurant Discount Finder",
    page_icon="🍽️",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'search_results' not in st.session_state:
    st.session_state.search_results = []

# Title and description
st.title("🍽️ Restaurant Discount Finder AI Agent")
st.markdown("### Find the best restaurant deals and discounts near you!")

# Sidebar for API key and location
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        help="Enter your Anthropic API key to use the AI agent"
    )
    
    st.markdown("---")
    
    location = st.text_input(
        "📍 Your Location",
        value="Dubai, UAE",
        help="Enter your city or area"
    )
    
    cuisine_type = st.multiselect(
        "🍴 Cuisine Preferences",
        ["Italian", "Chinese", "Indian", "Japanese", "Mexican", "American", "Mediterranean", "Thai", "Arabic", "French"],
        default=[]
    )
    
    discount_min = st.slider(
        "💰 Minimum Discount %",
        min_value=0,
        max_value=70,
        value=10,
        step=5
    )
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.search_results = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**About**")
    st.markdown("This AI agent searches for restaurant discounts and deals using web search capabilities.")

# Main content area
if not api_key:
    st.warning("⚠️ Please enter your Anthropic API key in the sidebar to continue.")
    st.info("💡 Get your API key from: https://console.anthropic.com/")
    st.stop()

# Initialize Anthropic client
try:
    client = anthropic.Anthropic(api_key=api_key)
except Exception as e:
    st.error(f"Error initializing API client: {str(e)}")
    st.stop()

# Function to call Claude with web search
def search_restaurants(query, location, cuisine_prefs, min_discount):
    """Search for restaurants with discounts using Claude's web search"""
    
    # Build the search prompt
    cuisine_text = f" focusing on {', '.join(cuisine_prefs)}" if cuisine_prefs else ""
    discount_text = f" with at least {min_discount}% discount" if min_discount > 0 else ""
    
    full_query = f"""Search for restaurants near {location}{cuisine_text}{discount_text}. 
    
User query: {query}

Please search for:
1. Current restaurant deals and discounts
2. Special offers from food delivery apps (Zomato, Swiggy, Uber Eats, Deliveroo, Talabat, etc.)
3. Restaurant promotions and happy hour deals
4. Credit card or bank offers for dining

Provide a comprehensive list with:
- Restaurant name
- Type of cuisine
- Discount/offer details
- How to avail the offer
- Validity period (if available)
- Source/app where the offer is available"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            tools=[
                {
                    "type": "web_search_20250305",
                    "name": "web_search"
                }
            ],
            messages=[
                {"role": "user", "content": full_query}
            ]
        )
        
        return response
    except Exception as e:
        st.error(f"Error calling Claude API: {str(e)}")
        return None

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_query = st.chat_input("Ask me to find restaurant deals... (e.g., 'Find Italian restaurants with discounts')")

if user_query:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    with st.chat_message("user"):
        st.markdown(user_query)
    
    # Show loading spinner
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching for the best restaurant deals..."):
            response = search_restaurants(user_query, location, cuisine_type, discount_min)
            
            if response:
                # Extract text from response
                assistant_message = ""
                for block in response.content:
                    if block.type == "text":
                        assistant_message += block.text
                
                # Display the response
                st.markdown(assistant_message)
                
                # Add assistant message to chat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
                # Store search results
                st.session_state.search_results.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "query": user_query,
                    "location": location,
                    "response": assistant_message
                })

# Quick action buttons
st.markdown("---")
st.markdown("### 🚀 Quick Search Options")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🍕 Pizza Deals"):
        st.session_state.messages.append({"role": "user", "content": "Find pizza restaurants with discounts"})
        st.rerun()

with col2:
    if st.button("🍔 Burger Offers"):
        st.session_state.messages.append({"role": "user", "content": "Find burger restaurants with special offers"})
        st.rerun()

with col3:
    if st.button("🍱 Lunch Specials"):
        st.session_state.messages.append({"role": "user", "content": "Find restaurants with lunch specials and discounts"})
        st.rerun()

with col4:
    if st.button("🌮 Weekend Deals"):
        st.session_state.messages.append({"role": "user", "content": "Find restaurants with weekend special offers"})
        st.rerun()

# Display search history in an expander
if st.session_state.search_results:
    with st.expander("📊 Search History"):
        for idx, result in enumerate(reversed(st.session_state.search_results)):
            st.markdown(f"**Search {len(st.session_state.search_results) - idx}** - {result['timestamp']}")
            st.markdown(f"*Query:* {result['query']}")
            st.markdown(f"*Location:* {result['location']}")
            st.markdown("---")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Powered by Claude AI | Built with Streamlit</p>
        <p>💡 Tip: Be specific with your search to get better results!</p>
    </div>
    """,
    unsafe_allow_html=True
)