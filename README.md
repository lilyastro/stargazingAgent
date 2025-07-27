# 🌠 Stargazing Assistant

An intelligent conversational assistant for stargazing enthusiasts built with LangChain and Streamlit. Get real-time information about celestial events, weather conditions, satellite passes, and more for any location and date.

## ✨ Features

- **Moon Phase Information** - Get current moon phase and illumination percentage
- **Sky Events** - View visible planets, bright stars, and constellations for any location
- **Weather Data** - Check weather conditions for optimal stargazing
- **Satellite Tracking** - Track visible passes of ISS, Hubble, and other satellites
- **Location-Based** - Works with any city or address worldwide
- **Interactive Chat** - Natural language conversation with context memory
- **Real-Time Data** - Up-to-date astronomical and weather information

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- API Keys (see Configuration section)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/lilyastro/stargazingAgent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (see Configuration section)

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 🔧 Configuration

Create a `.env` file in the project root with the following API keys:

```env
# Required: OpenAI API key for the LangChain agent
OPENAI_API_KEY=your_openai_api_key_here

# Required: N2YO API key for satellite tracking
N2YO_API_KEY=your_n2yo_api_key_here

```

### Getting API Keys

1. **OpenAI API Key**
   - Visit [OpenAI API](https://platform.openai.com/api-keys)
   - Create an account and generate an API key

2. **N2YO API Key**
   - Visit [N2YO.com](https://www.n2yo.com/api/)
   - Register for a free account
   - Generate your API key in your profile

3. **Weather API Key** (optional)
   - Visit your preferred weather API provider
   - Follow their registration process

## 📁 Project Structure

```
stargazing-assistant/
├── app/
│   └──app.py                 # Main Streamlit application
├── agents/                # LangChain agent configuration
│   ├── agent.py   
│   ├── prompt.py  
│   └── tools.py        
├── stargaze/
│   └── utils/
│       ├── astronomy.py  # Astronomical calculations
│       ├── weather.py    # Weather data functions
│       └── satellites.py # Satellite tracking functions
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in repo)
└── README.md            # This file
```

## 🛠️ Available Tools

The assistant has access to the following tools:

- **`fetch_moon_phase`** - Get moon phase for any date
- **`fetch_sky_events`** - View visible celestial objects from any location
- **`fetch_weather`** - Get weather conditions for stargazing
- **`fetch_satellite_passes`** - Track ISS and other satellite passes

## 💬 Usage Examples

Try asking the assistant questions like:

- "What's the moon phase tonight?"
- "What can I see in the sky from New York City?"
- "When will the ISS be visible from London this week?"
- "What's the weather like for stargazing in Tokyo tomorrow?"
- "Show me the brightest stars visible from my location"
- "What planets are visible tonight?"

## 🔬 Technical Details

### Dependencies

- **Streamlit** - Web application framework
- **LangChain** - AI agent framework
- **OpenAI** - Language model for conversations
- **Skyfield** - Astronomical calculations
- **Astral** - Moon phase calculations
- **Geopy** - Location geocoding
- **Requests** - API calls

### Astronomical Data Sources

- **Hipparcos Catalog** - Star positions and magnitudes
- **JPL DE421** - Planetary ephemeris data
- **N2YO API** - Real-time satellite tracking
- **Astral Library** - Moon phase calculations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Adding New Tools

To add a new tool to the assistant:

1. Create the function in the appropriate utils module
2. Add the tool decorator in `tools.py`
3. Import and register the tool in `agents/agent.py`

## 🐛 Troubleshooting

### Common Issues

1. **"API key not configured" errors**
   - Ensure all required API keys are set in your `.env` file
   - Check that the `.env` file is in the project root directory

2. **Location not found**
   - Try using more specific location names (e.g., "New York, NY" instead of "NYC")
   - Include country names for international locations

3. **No satellites visible**
   - Try increasing the number of days to search
   - Check during different times of year
   - Ensure you're looking during twilight hours

4. **Slow responses**
   - The assistant makes multiple API calls for comprehensive data
   - Response time depends on network connectivity and API response times

### Debug Mode

To enable debug output, set:
```bash
export LANGCHAIN_VERBOSE=True
```

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Skyfield** - Brandon Rhodes for the excellent astronomical library
- **N2YO.com** - Free satellite tracking API
- **OpenAI** - Powerful language models for natural conversations
- **Streamlit** - Making web apps simple and beautiful

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with detailed information about your problem

---

*Happy stargazing! 🌌✨*