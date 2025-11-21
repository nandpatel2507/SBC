import streamlit as st
import random
import json
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Restaurant Discount Finder",
    page_icon="🍽️",
    layout="wide"
)

# Synthetic Restaurant Data
RESTAURANTS = [
    # Italian
    {"name": "La Bella Italia", "cuisine": "Italian", "location": "Downtown Dubai", "rating": 4.5, "discount": 25, "app": "Zomato", "offer": "25% off on entire menu", "valid_until": "2025-12-31", "card_offer": "Additional 10% with HSBC cards"},
    {"name": "Olive Garden Express", "cuisine": "Italian", "location": "JBR", "rating": 4.2, "discount": 30, "app": "Deliveroo", "offer": "30% off on orders above AED 100", "valid_until": "2025-11-30", "card_offer": None},
    {"name": "Pizza Paradise", "cuisine": "Italian", "location": "Marina", "rating": 4.7, "discount": 20, "app": "Talabat", "offer": "Buy 1 Get 1 on all pizzas", "valid_until": "2025-12-15", "card_offer": "15% cashback with Emirates NBD"},
    
    # Chinese
    {"name": "Dragon Wok", "cuisine": "Chinese", "location": "Bur Dubai", "rating": 4.3, "discount": 35, "app": "Zomato", "offer": "35% off on dim sum platters", "valid_until": "2025-12-20", "card_offer": None},
    {"name": "Golden Palace", "cuisine": "Chinese", "location": "Deira", "rating": 4.6, "discount": 40, "app": "Noon Food", "offer": "40% off weekday lunch specials", "valid_until": "2025-12-31", "card_offer": "20% with Mashreq cards"},
    {"name": "Kung Pao Kitchen", "cuisine": "Chinese", "location": "Business Bay", "rating": 4.4, "discount": 15, "app": "Uber Eats", "offer": "15% off + free delivery", "valid_until": "2025-11-25", "card_offer": None},
    
    # Indian
    {"name": "Spice Route", "cuisine": "Indian", "location": "Karama", "rating": 4.8, "discount": 30, "app": "Talabat", "offer": "30% off on all biryani orders", "valid_until": "2025-12-31", "card_offer": "Extra 10% with FAB cards"},
    {"name": "Tandoor Nights", "cuisine": "Indian", "location": "Al Barsha", "rating": 4.5, "discount": 25, "app": "Zomato", "offer": "25% off dinner buffet", "valid_until": "2025-12-10", "card_offer": None},
    {"name": "Curry House", "cuisine": "Indian", "location": "Discovery Gardens", "rating": 4.3, "discount": 45, "app": "Deliveroo", "offer": "45% off lunch combo meals", "valid_until": "2025-11-28", "card_offer": "Buy 1 Get 1 with ADCB cards"},
    
    # Japanese
    {"name": "Sakura Sushi Bar", "cuisine": "Japanese", "location": "DIFC", "rating": 4.9, "discount": 20, "app": "Deliveroo", "offer": "20% off on sushi platters", "valid_until": "2025-12-31", "card_offer": None},
    {"name": "Ramen Kingdom", "cuisine": "Japanese", "location": "JLT", "rating": 4.6, "discount": 30, "app": "Zomato", "offer": "30% off ramen bowls after 8 PM", "valid_until": "2025-12-15", "card_offer": "25% cashback with Citi cards"},
    {"name": "Tokyo Grill", "cuisine": "Japanese", "location": "Palm Jumeirah", "rating": 4.7, "discount": 15, "app": "Talabat", "offer": "15% off teppanyaki sets", "valid_until": "2025-12-20", "card_offer": None},
    
    # Mexican
    {"name": "Taco Fiesta", "cuisine": "Mexican", "location": "Motor City", "rating": 4.4, "discount": 35, "app": "Uber Eats", "offer": "35% off + free nachos", "valid_until": "2025-11-30", "card_offer": None},
    {"name": "El Mariachi", "cuisine": "Mexican", "location": "JBR", "rating": 4.5, "discount": 25, "app": "Deliveroo", "offer": "25% off on orders above AED 80", "valid_until": "2025-12-31", "card_offer": "Extra 15% with RAK Bank cards"},
    
    # American
    {"name": "Burger Bros", "cuisine": "American", "location": "Dubai Mall", "rating": 4.6, "discount": 40, "app": "Talabat", "offer": "40% off on combo meals", "valid_until": "2025-12-05", "card_offer": None},
    {"name": "Smokehouse BBQ", "cuisine": "American", "location": "Al Quoz", "rating": 4.7, "discount": 30, "app": "Zomato", "offer": "30% off weekend BBQ platter", "valid_until": "2025-12-31", "card_offer": "20% with Standard Chartered cards"},
    {"name": "The Diner", "cuisine": "American", "location": "City Walk", "rating": 4.5, "discount": 20, "app": "Noon Food", "offer": "20% off breakfast menu", "valid_until": "2025-11-27", "card_offer": None},
    
    # Mediterranean
    {"name": "Zeus Taverna", "cuisine": "Mediterranean", "location": "Jumeirah", "rating": 4.8, "discount": 25, "app": "Deliveroo", "offer": "25% off mezze platters", "valid_until": "2025-12-31", "card_offer": None},
    {"name": "Olive & Lemon", "cuisine": "Mediterranean", "location": "Marina Walk", "rating": 4.5, "discount": 30, "app": "Zomato", "offer": "30% off lunch specials", "valid_until": "2025-12-15", "card_offer": "Buy 1 Get 1 dessert with DIB cards"},
    
    # Thai
    {"name": "Bangkok Street Food", "cuisine": "Thai", "location": "Karama", "rating": 4.6, "discount": 35, "app": "Talabat", "offer": "35% off on curry dishes", "valid_until": "2025-12-20", "card_offer": None},
    {"name": "Thai Orchid", "cuisine": "Thai", "location": "Barsha Heights", "rating": 4.4, "discount": 20, "app": "Uber Eats", "offer": "20% off + free spring rolls", "valid_until": "2025-11-30", "card_offer": None},
    
    # Arabic
    {"name": "Al Safadi", "cuisine": "Arabic", "location": "Deira", "rating": 4.7, "discount": 30, "app": "Talabat", "offer": "30% off mixed grill platters", "valid_until": "2025-12-31", "card_offer": "Extra 10% with CBD cards"},
    {"name": "Shawarma Palace", "cuisine": "Arabic", "location": "Satwa", "rating": 4.5, "discount": 25, "app": "Deliveroo", "offer": "Buy 2 Get 1 free on shawarmas", "valid_until": "2025-12-10", "card_offer": None},
    {"name": "Lebanese Nights", "cuisine": "Arabic", "location": "Jumeirah Beach Residence", "rating": 4.8, "discount": 40, "app": "Zomato", "offer": "40% off family meal deals", "valid_until": "2025-12-31", "card_offer": "25% cashback with NBF cards"},
]

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {
        'location': 'Dubai',
        'cuisines': [],
        'min_discount': 0,
        'budget': 'Any',
        'dietary': []
    }

# Helper functions
def filter_restaurants(cuisine=None, min_discount=0, location=None, sort_by='discount'):
    """Filter restaurants based on criteria"""
    filtered = RESTAURANTS.copy()
    
    if cuisine:
        filtered = [r for r in filtered if r['cuisine'] in cuisine]
    
    if min_discount > 0:
        filtered = [r for r in filtered if r['discount'] >= min_discount]
    
    if location and location != 'Any':
        filtered = [r for r in filtered if location.lower() in r['location'].lower()]
    
    # Sort results
    if sort_by == 'discount':
        filtered.sort(key=lambda x: x['discount'], reverse=True)
    elif sort_by == 'rating':
        filtered.sort(key=lambda x: x['rating'], reverse=True)
    
    return filtered

def generate_response(user_input):
    """Generate AI-like response based on user input"""
    user_input_lower = user_input.lower()
    
    # Extract intent from user input
    cuisines = []
    for cuisine in ['italian', 'chinese', 'indian', 'japanese', 'mexican', 'american', 'mediterranean', 'thai', 'arabic']:
        if cuisine in user_input_lower:
            cuisines.append(cuisine.capitalize())
    
    # Check for specific requests
    if 'pizza' in user_input_lower:
        cuisines = ['Italian']
    elif 'burger' in user_input_lower:
        cuisines = ['American']
    elif 'sushi' in user_input_lower or 'ramen' in user_input_lower:
        cuisines = ['Japanese']
    elif 'biryani' in user_input_lower or 'curry' in user_input_lower:
        cuisines = ['Indian']
    elif 'shawarma' in user_input_lower:
        cuisines = ['Arabic']
    
    # Extract discount requirements
    min_discount = st.session_state.user_preferences['min_discount']
    if '30%' in user_input_lower or 'thirty percent' in user_input_lower:
        min_discount = 30
    elif '40%' in user_input_lower or 'forty percent' in user_input_lower:
        min_discount = 40
    elif '50%' in user_input_lower or 'fifty percent' in user_input_lower:
        min_discount = 50
    
    # Extract location
    location = None
    locations = ['downtown', 'marina', 'jbr', 'deira', 'karama', 'difc', 'jlt', 'palm']
    for loc in locations:
        if loc in user_input_lower:
            location = loc
            break
    
    # Get filtered results
    results = filter_restaurants(
        cuisine=cuisines if cuisines else None,
        min_discount=min_discount,
        location=location
    )
    
    # Generate response
    if not results:
        return "I couldn't find any restaurants matching your exact criteria. Let me show you some similar options!", filter_restaurants(min_discount=10)
    
    if cuisines:
        cuisine_text = ' or '.join(cuisines)
        response = f"Great choice! I found {len(results)} {cuisine_text} restaurants with amazing deals for you! "
    else:
        response = f"I've found {len(results)} fantastic restaurants with great discounts! "
    
    if min_discount > 0:
        response += f"All have at least {min_discount}% off. "
    
    if location:
        response += f"Located in the {location.title()} area. "
    
    response += "Here are the top picks:"
    
    return response, results[:10]  # Return top 10 results

def display_restaurant_card(restaurant):
    """Display restaurant as a card"""
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### 🍽️ {restaurant['name']}")
            st.markdown(f"**{restaurant['cuisine']}** • 📍 {restaurant['location']}")
            st.markdown(f"⭐ {restaurant['rating']}/5.0")
        
        with col2:
            st.markdown(f"<h2 style='color: #FF4B4B; text-align: right;'>{restaurant['discount']}% OFF</h2>", unsafe_allow_html=True)
        
        st.markdown(f"**🎁 Offer:** {restaurant['offer']}")
        st.markdown(f"**📱 Available on:** {restaurant['app']}")
        st.markdown(f"**📅 Valid until:** {restaurant['valid_until']}")
        
        if restaurant['card_offer']:
            st.markdown(f"**💳 Bank Offer:** {restaurant['card_offer']}")
        
        st.markdown("---")

# Title and header
st.title("🍽️ AI Restaurant Discount Finder")
st.markdown("### Your personal assistant for finding the best restaurant deals!")

# Sidebar - User Preferences
with st.sidebar:
    st.header("⚙️ Your Preferences")
    
    location = st.selectbox(
        "📍 Location",
        ["Any", "Downtown Dubai", "Marina", "JBR", "Deira", "Karama", "DIFC", "JLT", "Business Bay", "Palm Jumeirah"]
    )
    
    cuisines = st.multiselect(
        "🍴 Favorite Cuisines",
        ["Italian", "Chinese", "Indian", "Japanese", "Mexican", "American", "Mediterranean", "Thai", "Arabic"]
    )
    
    min_discount = st.slider(
        "💰 Minimum Discount",
        min_value=0,
        max_value=50,
        value=0,
        step=5,
        help="Filter restaurants with at least this discount percentage"
    )
    
    budget = st.selectbox(
        "💵 Budget per Person",
        ["Any", "Under AED 50", "AED 50-100", "AED 100-200", "Above AED 200"]
    )
    
    dietary = st.multiselect(
        "🥗 Dietary Preferences",
        ["Vegetarian", "Vegan", "Halal", "Gluten-Free"]
    )
    
    # Update preferences
    st.session_state.user_preferences = {
        'location': location,
        'cuisines': cuisines,
        'min_discount': min_discount,
        'budget': budget,
        'dietary': dietary
    }
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### 📊 Available Deals")
    st.metric("Total Restaurants", len(RESTAURANTS))
    st.metric("Avg. Discount", f"{sum(r['discount'] for r in RESTAURANTS) // len(RESTAURANTS)}%")
    st.metric("Best Offer", f"{max(r['discount'] for r in RESTAURANTS)}% OFF")
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Chat with AI Assistant")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for chat in st.session_state.chat_history:
            if chat['role'] == 'user':
                st.markdown(f"**You:** {chat['message']}")
            else:
                st.markdown(f"**AI Assistant:** {chat['message']}")
                if 'restaurants' in chat:
                    with st.expander(f"📋 View {len(chat['restaurants'])} Recommendations", expanded=False):
                        for restaurant in chat['restaurants']:
                            display_restaurant_card(restaurant)
            st.markdown("---")
    
    # Chat input
    user_input = st.text_input(
        "Ask me anything...",
        placeholder="e.g., Find me Italian restaurants with good discounts",
        key="chat_input"
    )
    
    if st.button("Send") and user_input:
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'message': user_input
        })
        
        # Generate AI response
        response, restaurants = generate_response(user_input)
        
        # Add AI response
        st.session_state.chat_history.append({
            'role': 'assistant',
            'message': response,
            'restaurants': restaurants
        })
        
        st.rerun()

with col2:
    st.markdown("### 🚀 Quick Actions")
    
    if st.button("🍕 Pizza Deals", use_container_width=True):
        response, restaurants = generate_response("Find pizza restaurants")
        st.session_state.chat_history.append({'role': 'user', 'message': 'Find pizza restaurants'})
        st.session_state.chat_history.append({'role': 'assistant', 'message': response, 'restaurants': restaurants})
        st.rerun()
    
    if st.button("🍔 Burger Specials", use_container_width=True):
        response, restaurants = generate_response("Show me burger places")
        st.session_state.chat_history.append({'role': 'user', 'message': 'Show me burger places'})
        st.session_state.chat_history.append({'role': 'assistant', 'message': response, 'restaurants': restaurants})
        st.rerun()
    
    if st.button("🍱 Asian Cuisine", use_container_width=True):
        response, restaurants = generate_response("Find Chinese or Japanese restaurants")
        st.session_state.chat_history.append({'role': 'user', 'message': 'Find Asian restaurants'})
        st.session_state.chat_history.append({'role': 'assistant', 'message': response, 'restaurants': restaurants})
        st.rerun()
    
    if st.button("💰 Best Discounts", use_container_width=True):
        response, restaurants = generate_response("Show restaurants with highest discounts")
        st.session_state.chat_history.append({'role': 'user', 'message': 'Show best discounts'})
        st.session_state.chat_history.append({'role': 'assistant', 'message': response, 'restaurants': restaurants})
        st.rerun()
    
    if st.button("🌮 Weekend Deals", use_container_width=True):
        response, restaurants = generate_response("Show me weekend special offers")
        st.session_state.chat_history.append({'role': 'user', 'message': 'Weekend deals'})
        st.session_state.chat_history.append({'role': 'assistant', 'message': response, 'restaurants': restaurants})
        st.rerun()
    
    st.markdown("---")
    
    # Sample queries
    st.markdown("### 💡 Try asking:")
    st.markdown("""
    - "Find Italian restaurants near Marina"
    - "Show me places with 40% discount"
    - "I want Chinese food with good offers"
    - "Best sushi places in DIFC"
    - "Cheap eats with big discounts"
    - "Show me Arabic restaurants"
    """)

# Footer section
st.markdown("---")

# Browse all restaurants
with st.expander("🔍 Browse All Available Restaurants"):
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        browse_cuisine = st.multiselect("Filter by Cuisine", ["Italian", "Chinese", "Indian", "Japanese", "Mexican", "American", "Mediterranean", "Thai", "Arabic"], key="browse_cuisine")
    
    with filter_col2:
        browse_discount = st.slider("Minimum Discount %", 0, 50, 0, 5, key="browse_discount")
    
    with filter_col3:
        sort_option = st.selectbox("Sort By", ["Discount", "Rating"], key="sort_option")
    
    filtered = filter_restaurants(
        cuisine=browse_cuisine if browse_cuisine else None,
        min_discount=browse_discount,
        sort_by=sort_option.lower()
    )
    
    st.markdown(f"**Showing {len(filtered)} restaurants**")
    
    for restaurant in filtered:
        display_restaurant_card(restaurant)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p><strong>🎉 Prototype Mode</strong> - Using synthetic data for demonstration</p>
        <p>💡 This is a working prototype showing how an AI agent can help you find restaurant deals</p>
        <p>Built with ❤️ using Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
