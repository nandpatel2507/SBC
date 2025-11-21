# 🍽️ Restaurant Discount Finder AI Agent

An intelligent Streamlit dashboard powered by Claude AI that helps you discover the best restaurant deals and discounts near you.

## Features

- 🔍 **Smart Search**: AI-powered search for restaurant deals and discounts
- 🌍 **Location-Based**: Find offers specific to your area
- 🍴 **Cuisine Filters**: Filter by your preferred cuisine types
- 💰 **Discount Threshold**: Set minimum discount percentage
- 📱 **Multi-App Search**: Searches across Zomato, Swiggy, Uber Eats, Deliveroo, Talabat, and more
- 💳 **Credit Card Offers**: Discover bank and credit card dining deals
- 🚀 **Quick Actions**: One-click searches for popular categories
- 📊 **Search History**: Track your previous searches

## Setup Instructions

### For Streamlit Cloud Deployment

1. **Create a GitHub Repository**
   - Go to GitHub and create a new repository
   - Upload these files: `app.py`, `requirements.txt`, and `README.md`

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Select the repository and branch
   - Set Main file path as `app.py`
   - Click "Deploy"

3. **Get Your Anthropic API Key**
   - Visit [console.anthropic.com](https://console.anthropic.com/)
   - Create an account or sign in
   - Generate an API key
   - Enter it in the sidebar when using the app

### For Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   - The app will automatically open at `http://localhost:8501`

## How to Use

1. **Enter API Key**: Add your Anthropic API key in the sidebar
2. **Set Location**: Specify your city or area
3. **Configure Preferences**: 
   - Select cuisine types (optional)
   - Set minimum discount threshold (optional)
4. **Search**: Type your query or use quick action buttons
5. **Review Results**: The AI agent will search and present deals

## Example Queries

- "Find Italian restaurants with discounts"
- "Show me pizza deals near me"
- "What are the best lunch specials today?"
- "Find restaurants with bank offers"
- "Show weekend dining deals"

## Tech Stack

- **Frontend**: Streamlit
- **AI Model**: Claude Sonnet 4
- **API**: Anthropic API with web search capabilities
- **Language**: Python

## Requirements

- Python 3.7+
- Anthropic API key
- Internet connection

## Privacy & Security

- API keys are entered securely and not stored
- All searches are processed in real-time
- No user data is stored on servers

## Support

For issues or questions:
- Check [Streamlit Documentation](https://docs.streamlit.io)
- Review [Anthropic API Docs](https://docs.anthropic.com)

## License

This project is open source and available under the MIT License.

---

**Note**: This app requires an active Anthropic API subscription. Make sure you have credits available in your account.