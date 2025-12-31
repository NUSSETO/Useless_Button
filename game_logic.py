# Game logic for the useless button idle clicker
# Handles state management, shop items, and purchase logic

import time
import streamlit as st
import random

# Shop item definitions with cost scaling
SHOP_ITEMS = {
    "broken_mouse": {
        "name": "Broken Mouse 🖱️",
        "base_cost": 10,
        "click_multiplier": 1,
        "auto_clicks_per_sec": 0,
        "description": "Gives +1 click per press. Because your mouse is broken, I guess?",
        "cost_multiplier": 1.15  # 15% increase per purchase
    },
    "intern": {
        "name": "Intern 👨‍💼",
        "base_cost": 50,
        "click_multiplier": 0,
        "auto_clicks_per_sec": 1,
        "description": "Auto-clicks 1 time per second. They're not very efficient.",
        "cost_multiplier": 1.2
    },
    "chatgpt": {
        "name": "ChatGPT 🤖",
        "base_cost": 200,
        "click_multiplier": 0,
        "auto_clicks_per_sec": 10,
        "description": "Auto-clicks 10 times per second. Still more useful than you.",
        "cost_multiplier": 1.25
    },
    "click_farm": {
        "name": "Click Farm 🏭",
        "base_cost": 500,
        "click_multiplier": 0,
        "auto_clicks_per_sec": 50,
        "description": "Auto-clicks 50 times per second. Exploiting workers since forever.",
        "cost_multiplier": 1.3
    },
    "double_click": {
        "name": "Double Click Power ⚡",
        "base_cost": 100,
        "click_multiplier": 2,
        "auto_clicks_per_sec": 0,
        "description": "Doubles your click power. Now you're twice as useless!",
        "cost_multiplier": 1.4
    },
    "ai_overlord": {
        "name": "AI Overlord 🧠",
        "base_cost": 1000,
        "click_multiplier": 0,
        "auto_clicks_per_sec": 100,
        "description": "Auto-clicks 100 times per second. Skynet is here, and it clicks buttons.",
        "cost_multiplier": 1.35
    },
    "click_magnet": {
        "name": "Click Magnet 🧲",
        "base_cost": 250,
        "click_multiplier": 5,
        "auto_clicks_per_sec": 0,
        "description": "+5 clicks per press. Magnets, how do they work?",
        "cost_multiplier": 1.5
    },
    "time_machine": {
        "name": "Time Machine ⏰",
        "base_cost": 5000,
        "click_multiplier": 0,
        "auto_clicks_per_sec": 500,
        "description": "Auto-clicks 500 times per second. You've traveled back in time to click more.",
        "cost_multiplier": 1.4
    }
}

# Achievement definitions
ACHIEVEMENTS = {
    "first_click": {"name": "First Click 🎯", "threshold": 1, "description": "You clicked once. Congratulations?"},
    "ten_clicks": {"name": "Double Digits 🔟", "threshold": 10, "description": "10 clicks. Still pathetic."},
    "hundred_clicks": {"name": "Century Club 💯", "threshold": 100, "description": "100 clicks. You're committed to wasting time."},
    "thousand_clicks": {"name": "Kilo Clicker 📊", "threshold": 1000, "description": "1,000 clicks. This is getting sad."},
    "ten_thousand": {"name": "Decamillionaire 🏆", "threshold": 10000, "description": "10,000 clicks. You need help."},
    "hundred_thousand": {"name": "Click Master 👑", "threshold": 100000, "description": "100,000 clicks. You've achieved nothing."},
    "million": {"name": "Millionaire (of Clicks) 💰", "threshold": 1000000, "description": "1,000,000 clicks. Seriously, get help."},
    "first_upgrade": {"name": "First Purchase 🛒", "threshold": -1, "description": "Bought your first upgrade. The addiction begins."},
    "auto_clicker": {"name": "Automation 🏭", "threshold": -1, "description": "Unlocked auto-clicking. You're officially lazy."},
    "speed_demon": {"name": "Speed Demon ⚡", "threshold": -1, "description": "100+ auto-clicks per second. You've peaked."},
    "combo_master": {"name": "Combo Master 🔥", "threshold": -1, "description": "Achieved a 50x combo streak!"},
    "lucky_click": {"name": "Lucky Clicker 🍀", "threshold": -1, "description": "Got a lucky click bonus!"},
    "power_up_user": {"name": "Power User ⚡", "threshold": -1, "description": "Used your first power-up."},
    "prestige_master": {"name": "Prestige Master 🌟", "threshold": -1, "description": "Prestiged for the first time!"},
    "secret_clicker": {"name": "Secret Clicker 🕵️", "threshold": -1, "description": "Found the secret! (Click 777 times)"},
    "streak_king": {"name": "Streak King 👑", "threshold": -1, "description": "Maintained a 100-click streak!"}
}

def initialize_game_state():
    """Initialize all game state variables if they don't exist."""
    if 'clicks' not in st.session_state:
        st.session_state.clicks = 0
    
    if 'total_clicks_earned' not in st.session_state:
        st.session_state.total_clicks_earned = 0
    
    if 'click_multiplier' not in st.session_state:
        st.session_state.click_multiplier = 1  # Base: 1 click per press
    
    if 'auto_clicks_per_sec' not in st.session_state:
        st.session_state.auto_clicks_per_sec = 0
    
    if 'owned_items' not in st.session_state:
        st.session_state.owned_items = {}
        for item_id in SHOP_ITEMS.keys():
            st.session_state.owned_items[item_id] = 0
    
    if 'last_auto_click_time' not in st.session_state:
        st.session_state.last_auto_click_time = time.time()
    
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
    
    if 'achievements' not in st.session_state:
        st.session_state.achievements = set()
    
    if 'total_manual_clicks' not in st.session_state:
        st.session_state.total_manual_clicks = 0
    
    if 'last_achievement_check' not in st.session_state:
        st.session_state.last_achievement_check = 0
    
    # Combo system
    if 'combo_streak' not in st.session_state:
        st.session_state.combo_streak = 0
    if 'last_click_time' not in st.session_state:
        st.session_state.last_click_time = 0
    if 'combo_multiplier' not in st.session_state:
        st.session_state.combo_multiplier = 1.0
    
    # Power-ups
    if 'active_powerups' not in st.session_state:
        st.session_state.active_powerups = {}
    if 'powerup_cooldowns' not in st.session_state:
        st.session_state.powerup_cooldowns = {}
    
    # Random events
    if 'last_random_event' not in st.session_state:
        st.session_state.last_random_event = time.time()
    if 'active_event' not in st.session_state:
        st.session_state.active_event = None
    if 'event_end_time' not in st.session_state:
        st.session_state.event_end_time = 0
    if 'next_event_threshold' not in st.session_state:
        st.session_state.next_event_threshold = random.randint(30, 60)  # Fixed threshold for next event
    
    # Prestige
    if 'prestige_level' not in st.session_state:
        st.session_state.prestige_level = 0
    if 'prestige_points' not in st.session_state:
        st.session_state.prestige_points = 0
    
    # Click streak
    if 'click_streak' not in st.session_state:
        st.session_state.click_streak = 0
    if 'streak_start_time' not in st.session_state:
        st.session_state.streak_start_time = time.time()
    
    # Visual effects
    if 'recent_events' not in st.session_state:
        st.session_state.recent_events = []

def get_prestige_bonus():
    """Get the prestige bonus multiplier."""
    return 1.0 + (st.session_state.prestige_level * 0.1)

def handle_click():
    """Handle a manual button click with combo system, streaks, and random events."""
    current_time = time.time()
    
    # Combo system - clicks within 2 seconds increase combo
    if current_time - st.session_state.last_click_time < 2.0:
        st.session_state.combo_streak += 1
        # Combo multiplier caps at 10x
        st.session_state.combo_multiplier = min(1.0 + (st.session_state.combo_streak * 0.1), 10.0)
    else:
        st.session_state.combo_streak = 1
        st.session_state.combo_multiplier = 1.0
    
    st.session_state.last_click_time = current_time
    
    # Click streak tracking (clicks within 5 seconds)
    if current_time - st.session_state.streak_start_time < 5.0:
        st.session_state.click_streak += 1
    else:
        st.session_state.click_streak = 1
        st.session_state.streak_start_time = current_time
    
    # Base clicks with combo multiplier
    base_clicks = st.session_state.click_multiplier
    clicks_to_add = int(base_clicks * st.session_state.combo_multiplier)
    
    # Apply power-up multipliers
    powerup_mult = 1.0
    for powerup_id, end_time in st.session_state.active_powerups.items():
        if current_time < end_time:
            if powerup_id == "double_clicks":
                powerup_mult *= 2
            elif powerup_id == "triple_clicks":
                powerup_mult *= 3
            elif powerup_id == "mega_clicks":
                powerup_mult *= 5
    
    clicks_to_add = int(clicks_to_add * powerup_mult)
    
    # Apply random event multiplier
    event_mult = get_event_multiplier()
    clicks_to_add = int(clicks_to_add * event_mult)
    
    # Apply prestige bonus
    prestige_mult = get_prestige_bonus()
    clicks_to_add = int(clicks_to_add * prestige_mult)
    
    # Random lucky click (1% chance)
    if random.random() < 0.01:
        lucky_bonus = clicks_to_add * random.randint(2, 10)
        clicks_to_add += lucky_bonus
        st.session_state.recent_events.append({
            "type": "lucky",
            "message": f"🍀 LUCKY CLICK! +{lucky_bonus:,} bonus clicks!",
            "time": current_time
        })
        if "lucky_click" not in st.session_state.achievements:
            unlock_achievement("lucky_click")
    
    # Secret achievement check (777 clicks)
    if st.session_state.total_manual_clicks == 777 and "secret_clicker" not in st.session_state.achievements:
        unlock_achievement("secret_clicker")
        clicks_to_add *= 7  # Bonus!
    
    # Combo achievement
    if st.session_state.combo_streak >= 50 and "combo_master" not in st.session_state.achievements:
        unlock_achievement("combo_master")
    
    # Streak achievement
    if st.session_state.click_streak >= 100 and "streak_king" not in st.session_state.achievements:
        unlock_achievement("streak_king")
    
    st.session_state.clicks += clicks_to_add
    st.session_state.total_clicks_earned += clicks_to_add
    st.session_state.total_manual_clicks += 1
    
    check_achievements()
    
    return clicks_to_add, st.session_state.combo_streak

def process_auto_clicks():
    """Process auto-clicks based on time elapsed."""
    current_time = time.time()
    
    # Process random events
    process_random_events(current_time)
    
    # Clean up expired power-ups
    expired_powerups = [pid for pid, end_time in st.session_state.active_powerups.items() if current_time >= end_time]
    for pid in expired_powerups:
        del st.session_state.active_powerups[pid]
    
    # Clean up old events (keep last 5)
    st.session_state.recent_events = [
        e for e in st.session_state.recent_events 
        if current_time - e["time"] < 5.0
    ][-5:]
    
    # Reset combo if too much time passed
    if current_time - st.session_state.last_click_time > 2.0:
        st.session_state.combo_streak = 0
        st.session_state.combo_multiplier = 1.0
    
    if st.session_state.auto_clicks_per_sec <= 0:
        return
    
    elapsed = current_time - st.session_state.last_auto_click_time
    
    # Add clicks based on elapsed time (can be fractional seconds)
    if elapsed > 0:
        base_auto_clicks = st.session_state.auto_clicks_per_sec
        
        # Apply auto boost power-up
        if "auto_boost" in st.session_state.active_powerups:
            if current_time < st.session_state.active_powerups["auto_boost"]:
                base_auto_clicks *= POWERUPS["auto_boost"]["multiplier"]
        
        clicks_to_add = base_auto_clicks * elapsed
        
        # Apply prestige bonus
        prestige_mult = 1.0 + (st.session_state.prestige_level * 0.1)
        clicks_to_add *= prestige_mult
        
        # Apply random event multiplier
        event_mult = get_event_multiplier()
        clicks_to_add *= event_mult
        
        clicks_to_add_int = int(clicks_to_add)
        st.session_state.clicks += clicks_to_add_int
        st.session_state.total_clicks_earned += clicks_to_add_int
        # Update last time, accounting for any remainder
        st.session_state.last_auto_click_time = current_time
    
    # Check achievements periodically
    if current_time - st.session_state.last_achievement_check > 1.0:
        check_achievements()
        st.session_state.last_achievement_check = current_time

def process_random_events(current_time):
    """Process random events that can happen."""
    time_since_last = current_time - st.session_state.last_random_event
    rand_threshold = st.session_state.get('next_event_threshold', 45)  # Use stored threshold
    
    # Random event every 30-60 seconds (using fixed threshold)
    if time_since_last > rand_threshold:
        if st.session_state.active_event is None:
            events = [
                {"name": "Click Frenzy", "multiplier": 2.0, "duration": 10, "emoji": "⚡"},
                {"name": "Lucky Hour", "multiplier": 1.5, "duration": 15, "emoji": "🍀"},
                {"name": "Double Trouble", "multiplier": 2.5, "duration": 8, "emoji": "💥"},
                {"name": "Mega Boost", "multiplier": 3.0, "duration": 5, "emoji": "🚀"}
            ]
            event = random.choice(events)
            st.session_state.active_event = event
            st.session_state.event_end_time = current_time + event["duration"]
            st.session_state.recent_events.append({
                "type": "event",
                "message": f"{event['emoji']} {event['name']} activated! {event['multiplier']}x clicks for {event['duration']}s!",
                "time": current_time
            })
            st.session_state.last_random_event = current_time
            # Set next event threshold for future events
            st.session_state.next_event_threshold = random.randint(30, 60)
    
    # Check if event expired
    if st.session_state.active_event and current_time >= st.session_state.event_end_time:
        st.session_state.active_event = None

def get_event_multiplier():
    """Get the current random event multiplier."""
    current_time = time.time()
    
    if st.session_state.active_event:
        if current_time < st.session_state.event_end_time:
            return st.session_state.active_event["multiplier"]
    return 1.0

def get_item_cost(item_id):
    """Calculate the current cost of an item based on how many are owned."""
    item = SHOP_ITEMS[item_id]
    owned = st.session_state.owned_items[item_id]
    cost = int(item["base_cost"] * (item["cost_multiplier"] ** owned))
    return cost

def can_afford(item_id):
    """Check if the player can afford an item."""
    cost = get_item_cost(item_id)
    return st.session_state.clicks >= cost

def purchase_item(item_id):
    """Purchase an item and update game state."""
    if item_id not in SHOP_ITEMS:
        return False, "Invalid item"
    
    cost = get_item_cost(item_id)
    if not can_afford(item_id):
        return False, f"Not enough clicks! Need {cost:,} clicks."
    
    item = SHOP_ITEMS[item_id]
    st.session_state.clicks -= cost
    st.session_state.owned_items[item_id] += 1
    
    # Apply effects
    st.session_state.click_multiplier += item["click_multiplier"]
    st.session_state.auto_clicks_per_sec += item["auto_clicks_per_sec"]
    
    # Check for purchase-related achievements
    if sum(st.session_state.owned_items.values()) == 1:
        unlock_achievement("first_upgrade")
    
    if st.session_state.auto_clicks_per_sec > 0 and "auto_clicker" not in st.session_state.achievements:
        unlock_achievement("auto_clicker")
    
    if st.session_state.auto_clicks_per_sec >= 100 and "speed_demon" not in st.session_state.achievements:
        unlock_achievement("speed_demon")
    
    return True, f"Purchased {item['name']}! 💰"

def check_achievements():
    """Check and unlock achievements based on current game state."""
    clicks = st.session_state.clicks
    
    # Check click-based achievements
    # Skip achievements with threshold -1 (they are handled elsewhere) and already unlocked ones
    skip_achievements = ["first_upgrade", "auto_clicker", "speed_demon", "combo_master", 
                         "lucky_click", "power_up_user", "prestige_master", "secret_clicker", "streak_king"]
    
    for ach_id, ach in ACHIEVEMENTS.items():
        if ach_id in skip_achievements:
            continue  # These are handled elsewhere
        
        # Only check achievements with positive thresholds
        if ach["threshold"] <= 0:
            continue  # Skip achievements with invalid thresholds
        
        if ach_id not in st.session_state.achievements and clicks >= ach["threshold"]:
            unlock_achievement(ach_id)

def unlock_achievement(ach_id):
    """Unlock an achievement."""
    if ach_id not in st.session_state.achievements:
        st.session_state.achievements.add(ach_id)
        if ach_id in ACHIEVEMENTS:
            st.balloons()  # Celebrate!
            return True
    return False

def get_sarcastic_message():
    """Get a sarcastic message based on click count."""
    clicks = st.session_state.clicks
    
    if clicks == 0:
        return ("info", "Good, nothing has changed.")
    elif clicks < 10:
        return ("warning", f"You've clicked {clicks} times. Is it worth it?")
    elif clicks < 25:
        return ("warning", "Serious? Can you find something better to do?")
    elif clicks < 100:
        return ("error", "Enough is enough.")
    elif clicks == 100:
        return ("success", "Congrats! You've wasted so much time in your life!")
    elif clicks < 1000:
        return ("info", "Still clicking? Really?")
    elif clicks < 10000:
        return ("warning", "You know you can stop anytime, right?")
    else:
        return ("error", "That's it. I am not going to say anything else anymore. (But you'll keep clicking anyway.)")

def get_time_played():
    """Get the time played in a readable format."""
    elapsed = time.time() - st.session_state.start_time
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def get_clicks_per_second():
    """Calculate average clicks per second."""
    elapsed = time.time() - st.session_state.start_time
    if elapsed > 0:
        return st.session_state.total_clicks_earned / elapsed
    return 0

# Power-up definitions
POWERUPS = {
    "double_clicks": {
        "name": "Double Clicks ⚡",
        "cost": 1000,
        "duration": 30,
        "description": "Double all clicks for 30 seconds",
        "multiplier": 2.0
    },
    "triple_clicks": {
        "name": "Triple Clicks 🔥",
        "cost": 5000,
        "duration": 20,
        "description": "Triple all clicks for 20 seconds",
        "multiplier": 3.0
    },
    "mega_clicks": {
        "name": "Mega Clicks 💥",
        "cost": 20000,
        "duration": 15,
        "description": "5x all clicks for 15 seconds",
        "multiplier": 5.0
    },
    "auto_boost": {
        "name": "Auto Boost 🚀",
        "cost": 10000,
        "duration": 60,
        "description": "Double auto-click rate for 60 seconds",
        "multiplier": 2.0
    }
}

def activate_powerup(powerup_id):
    """Activate a power-up."""
    if powerup_id not in POWERUPS:
        return False, "Invalid power-up"
    
    powerup = POWERUPS[powerup_id]
    
    # Check cooldown
    if powerup_id in st.session_state.powerup_cooldowns:
        if time.time() < st.session_state.powerup_cooldowns[powerup_id]:
            remaining = int(st.session_state.powerup_cooldowns[powerup_id] - time.time())
            return False, f"On cooldown for {remaining} more seconds"
    
    # Check if can afford
    if st.session_state.clicks < powerup["cost"]:
        return False, f"Not enough clicks! Need {powerup['cost']:,}"
    
    st.session_state.clicks -= powerup["cost"]
    current_time = time.time()
    
    if powerup_id == "auto_boost":
        # Special handling for auto boost - store multiplier
        st.session_state.active_powerups[powerup_id] = current_time + powerup["duration"]
    else:
        st.session_state.active_powerups[powerup_id] = current_time + powerup["duration"]
    
    # Set cooldown (2x duration)
    st.session_state.powerup_cooldowns[powerup_id] = current_time + (powerup["duration"] * 2)
    
    if "power_up_user" not in st.session_state.achievements:
        unlock_achievement("power_up_user")
    
    return True, f"Activated {powerup['name']}! 🎉"

def can_prestige():
    """Check if player can prestige (at 1M clicks)."""
    return st.session_state.clicks >= 1000000

def prestige():
    """Prestige - reset progress for permanent bonus."""
    if not can_prestige():
        return False, "Need 1,000,000 clicks to prestige!"
    
    # Calculate prestige points (1 point per 1M clicks)
    prestige_points_earned = st.session_state.clicks // 1000000
    st.session_state.prestige_points += prestige_points_earned
    st.session_state.prestige_level += 1
    
    # Reset game state but keep prestige
    st.session_state.clicks = 0
    st.session_state.click_multiplier = 1
    st.session_state.auto_clicks_per_sec = 0
    st.session_state.owned_items = {item_id: 0 for item_id in SHOP_ITEMS.keys()}
    st.session_state.combo_streak = 0
    st.session_state.combo_multiplier = 1.0
    st.session_state.active_powerups = {}
    st.session_state.total_manual_clicks = 0
    # Keep total_clicks_earned for stats
    
    if "prestige_master" not in st.session_state.achievements:
        unlock_achievement("prestige_master")
    
    return True, f"Prestiged! Gained {prestige_points_earned} prestige points! 🌟"

