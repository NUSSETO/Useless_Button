# Useless Button - Idle Clicker Game 🎮

A sarcastic idle clicker game built with Streamlit. Click the button, earn clicks, and buy upgrades to automate your clicking. Because you clearly have nothing better to do.

## Features

### Core Gameplay
- **Manual Clicking**: Click the "DO NOT PRESS" button to earn clicks
- **Combo System**: Click within 2 seconds to build combos (up to 10x multiplier!)
- **Click Streaks**: Maintain consecutive clicks for bonus tracking
- **Lucky Clicks**: 1% chance for massive bonus clicks (2-10x multiplier)

### Shop System
Spend your clicks on upgrades with cost scaling:

**Auto-Clickers:**
- 🖱️ **Broken Mouse** (10 clicks): +1 click per press
- 👨‍💼 **Intern** (50 clicks): Auto-clicks 1 time per second
- 🤖 **ChatGPT** (200 clicks): Auto-clicks 10 times per second
- 🏭 **Click Farm** (500 clicks): Auto-clicks 50 times per second
- 🧠 **AI Overlord** (1,000 clicks): Auto-clicks 100 times per second
- ⏰ **Time Machine** (5,000 clicks): Auto-clicks 500 times per second

**Click Multipliers:**
- ⚡ **Double Click Power** (100 clicks): +2 clicks per press
- 🧲 **Click Magnet** (250 clicks): +5 clicks per press

### Power-ups
Temporary boosts to maximize your clicking power:
- ⚡ **Double Clicks**: 2x all clicks for 30 seconds
- 🔥 **Triple Clicks**: 3x all clicks for 20 seconds
- 💥 **Mega Clicks**: 5x all clicks for 15 seconds
- 🚀 **Auto Boost**: 2x auto-click rate for 60 seconds

### Special Features
- **Random Events**: Periodic events that boost your clicking power
- **Achievements**: 17 achievements to unlock with sarcastic descriptions
- **Prestige System**: Reset at 1M clicks for permanent bonuses
- **Statistics Tracking**: Track your best combos, streaks, and total clicks
- **Sarcastic Feedback**: The game judges your life choices

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run Useless_Button.py
```

## Deployment

This app is ready for Streamlit Cloud deployment. See `DEPLOYMENT.md` for detailed instructions.

## Project Structure

- `Useless_Button.py` - Main Streamlit application with UI
- `game_logic.py` - Game state management, shop items, and purchase logic
- `.streamlit/config.toml` - Streamlit configuration
- `requirements.txt` - Python dependencies

## Tools Used

- Python
- Streamlit
- The almighty Gemini (and maybe a human)

## About

Jason Huang  
Help me
