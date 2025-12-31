# I use Gemini to create this code, even the notes
# So no human is involved in making this internet garbage
# Ok, maybe me
import streamlit as st
import time
from game_logic import (
    initialize_game_state,
    handle_click,
    process_auto_clicks,
    purchase_item,
    can_afford,
    get_sarcastic_message,
    get_item_cost,
    get_time_played,
    get_clicks_per_second,
    get_event_multiplier,
    activate_powerup,
    can_prestige,
    prestige,
    get_prestige_bonus,
    SHOP_ITEMS,
    ACHIEVEMENTS,
    POWERUPS,
    unlock_achievement
)

# Set page config for better layout
st.set_page_config(page_title="Useless Button Idle", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for dynamic colors and effects
st.markdown("""
<style>
    .combo-display {
        font-size: 2em;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        animation: pulse 0.5s infinite;
    }
    .event-banner {
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin: 10px 0;
    }
    .powerup-active {
        background: linear-gradient(90deg, #FFD700, #FFA500);
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        display: inline-block;
        margin: 2px;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
</style>
""", unsafe_allow_html=True)

# Set the webpage title
st.title("🎮 Do not press the button 🎮")

# Initialize game state
initialize_game_state()

# Process auto-clicks
process_auto_clicks()

# Check for new achievements
new_achievements = []
for ach_id in st.session_state.achievements:
    if ach_id not in st.session_state.get('displayed_achievements', set()):
        new_achievements.append(ach_id)
        if 'displayed_achievements' not in st.session_state:
            st.session_state.displayed_achievements = set()
        st.session_state.displayed_achievements.add(ach_id)

# Show new achievement notifications
if new_achievements:
    for ach_id in new_achievements:
        ach = ACHIEVEMENTS[ach_id]
        st.success(f"🏆 Achievement Unlocked: {ach['name']} - {ach['description']}")
        st.balloons()

# Show recent events
if st.session_state.recent_events:
    for event in st.session_state.recent_events[-3:]:  # Show last 3
        if event["type"] == "lucky":
            st.success(event["message"])
        elif event["type"] == "event":
            st.info(event["message"])

# Show active random event
event_mult = get_event_multiplier()
if event_mult > 1.0 and st.session_state.active_event:
    event = st.session_state.active_event
    remaining = int(st.session_state.event_end_time - time.time())
    if remaining > 0:
        st.markdown(f"""
        <div class="event-banner" style="background: linear-gradient(90deg, #FF6B6B, #FF8E53); color: white;">
            {event['emoji']} <strong>{event['name']}</strong> - {event['multiplier']}x clicks! ({remaining}s remaining)
        </div>
        """, unsafe_allow_html=True)

# Create main layout
col1, col2 = st.columns([1.2, 1])

# --- Left Column: Button and Score ---
with col1:
    st.header("Click Area 🖱️")
    
    # Combo display
    if st.session_state.combo_streak > 1:
        combo_mult = st.session_state.combo_multiplier
        st.markdown(f"""
        <div class="combo-display">
            🔥 COMBO x{st.session_state.combo_streak}! ({combo_mult:.1f}x multiplier) 🔥
        </div>
        """, unsafe_allow_html=True)
    
    # Active power-ups display
    active_powerups_display = []
    current_time = time.time()
    for powerup_id, end_time in st.session_state.active_powerups.items():
        if current_time < end_time:
            remaining = int(end_time - current_time)
            powerup = POWERUPS.get(powerup_id, {"name": powerup_id})
            active_powerups_display.append(f"{powerup['name']} ({remaining}s)")
    
    if active_powerups_display:
        st.markdown(f"""
        <div style="text-align: center; margin: 10px 0;">
            {' '.join([f'<span class="powerup-active">{p}</span>' for p in active_powerups_display])}
        </div>
        """, unsafe_allow_html=True)
    
    # Giant button with dynamic styling based on combo
    button_color = "#FF6B6B" if st.session_state.combo_streak > 5 else "#1f77b4"
    button_style = f"""
    <style>
    .stButton>button {{
        height: 150px;
        font-size: 24px;
        font-weight: bold;
        background-color: {button_color};
        border: 3px solid #FFD700;
        transition: all 0.3s;
    }}
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
    }}
    </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    
    clicked = st.button('DO NOT PRESS', use_container_width=True, type="primary")
    if clicked:
        clicks_gained, combo = handle_click()
        # Visual feedback
        if combo > 10:
            st.snow()  # Snow for high combos!
        st.balloons()
        if clicks_gained > st.session_state.click_multiplier * 2:
            st.success(f"💥 Gained {clicks_gained:,} clicks!")
    
    st.divider()
    
    # Stats row
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric(
            label="Current Clicks 💰", 
            value=f"{st.session_state.clicks:,}",
            delta=f"+{st.session_state.click_multiplier} per click"
        )
    
    with stat_col2:
        auto_clicks = st.session_state.auto_clicks_per_sec
        if auto_clicks > 0:
            st.metric(
                label="Auto-Clicks/sec ⚡",
                value=f"{auto_clicks:.1f}"
            )
        else:
            st.metric(
                label="Auto-Clicks/sec ⚡",
                value="0.0"
            )
    
    with stat_col3:
        cps = get_clicks_per_second()
        st.metric(
            label="Avg Clicks/sec 📈",
            value=f"{cps:.2f}"
        )
    
    with stat_col4:
        if st.session_state.prestige_level > 0:
            st.metric(
                label="Prestige Level 🌟",
                value=f"{st.session_state.prestige_level}",
                delta=f"+{get_prestige_bonus():.1f}x bonus"
            )
        else:
            st.metric(
                label="Prestige Level 🌟",
                value="0"
            )
    
    st.divider()
    
    # Click streak display
    if st.session_state.click_streak > 1:
        st.info(f"🔥 Click Streak: {st.session_state.click_streak} clicks! Keep it up!")
    
    # Progress to next milestone
    milestones = [10, 100, 1000, 10000, 100000, 1000000]
    current_clicks = st.session_state.clicks
    
    # Find current and next milestone
    next_milestone = None
    prev_milestone = 0
    for i, milestone in enumerate(milestones):
        if current_clicks < milestone:
            next_milestone = milestone
            prev_milestone = milestones[i - 1] if i > 0 else 0
            break
    
    if next_milestone:
        progress = (current_clicks - prev_milestone) / (next_milestone - prev_milestone) if (next_milestone - prev_milestone) > 0 else 1.0
        st.progress(min(progress, 1.0))
        st.caption(f"Progress to {next_milestone:,} clicks: {current_clicks:,} / {next_milestone:,} ({progress*100:.1f}%)")
    
    # Prestige button
    if can_prestige():
        st.divider()
        if st.button("🌟 PRESTIGE NOW! 🌟", use_container_width=True, type="secondary"):
            success, message = prestige()
            if success:
                st.success(message)
                st.balloons()
                st.snow()
                st.rerun()
    
    st.divider()
    
    # Sarcastic feedback
    msg_type, message = get_sarcastic_message()
    if msg_type == "info":
        st.info(message)
    elif msg_type == "warning":
        st.warning(message)
    elif msg_type == "error":
        st.error(message)
    elif msg_type == "success":
        st.balloons()
        st.success(message)

# --- Right Column: Shop and Power-ups ---
with col2:
    tab1, tab2, tab3 = st.tabs(["🛒 Shop", "⚡ Power-ups", "📊 Stats"])
    
    with tab1:
        st.header("Shop 🛒")
        st.caption("Spend your clicks on upgrades. Because you clearly have nothing better to do.")
        
        # Shop tabs for organization
        shop_tab1, shop_tab2 = st.tabs(["Auto-Clickers", "Multipliers"])
        
        with shop_tab1:
            st.subheader("Auto-Clickers 🤖")
            auto_items = {k: v for k, v in SHOP_ITEMS.items() if v["auto_clicks_per_sec"] > 0}
            for item_id, item in auto_items.items():
                with st.container():
                    owned_count = st.session_state.owned_items[item_id]
                    cost = get_item_cost(item_id)
                    
                    # Display item info
                    st.markdown(f"### {item['name']} (Owned: {owned_count})")
                    st.write(item['description'])
                    st.caption(f"Effect: +{item['auto_clicks_per_sec']} auto-clicks/sec")
                    st.caption(f"Next cost: {cost:,} clicks")
                    
                    # Purchase button
                    can_buy = can_afford(item_id)
                    button_label = f"Buy for {cost:,} clicks 💰"
                    
                    if st.button(button_label, key=f"buy_{item_id}", disabled=not can_buy, use_container_width=True):
                        success, message = purchase_item(item_id)
                        if success:
                            st.success(message)
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(message)
                    
                    st.divider()
        
        with shop_tab2:
            st.subheader("Click Multipliers ⚡")
            multiplier_items = {k: v for k, v in SHOP_ITEMS.items() if v["click_multiplier"] > 0}
            for item_id, item in multiplier_items.items():
                with st.container():
                    owned_count = st.session_state.owned_items[item_id]
                    cost = get_item_cost(item_id)
                    
                    # Display item info
                    st.markdown(f"### {item['name']} (Owned: {owned_count})")
                    st.write(item['description'])
                    st.caption(f"Effect: +{item['click_multiplier']} clicks per press")
                    st.caption(f"Next cost: {cost:,} clicks")
                    
                    # Purchase button
                    can_buy = can_afford(item_id)
                    button_label = f"Buy for {cost:,} clicks 💰"
                    
                    if st.button(button_label, key=f"buy_{item_id}_mult", disabled=not can_buy, use_container_width=True):
                        success, message = purchase_item(item_id)
                        if success:
                            st.success(message)
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(message)
                    
                    st.divider()
    
    with tab2:
        st.header("Power-ups ⚡")
        st.caption("Temporary boosts to maximize your clicking power!")
        
        for powerup_id, powerup in POWERUPS.items():
            with st.container():
                st.markdown(f"### {powerup['name']}")
                st.write(powerup['description'])
                st.caption(f"Cost: {powerup['cost']:,} clicks | Duration: {powerup['duration']}s")
                
                # Check cooldown
                can_use = True
                cooldown_msg = ""
                if powerup_id in st.session_state.powerup_cooldowns:
                    cooldown_end = st.session_state.powerup_cooldowns[powerup_id]
                    if time.time() < cooldown_end:
                        remaining = int(cooldown_end - time.time())
                        can_use = False
                        cooldown_msg = f"⏳ Cooldown: {remaining}s"
                    else:
                        can_use = True
                
                can_afford_powerup = st.session_state.clicks >= powerup['cost']
                button_disabled = not (can_use and can_afford_powerup)
                
                button_label = f"Activate for {powerup['cost']:,} clicks"
                if not can_use:
                    button_label = cooldown_msg
                elif not can_afford_powerup:
                    button_label = f"Need {powerup['cost']:,} clicks"
                
                if st.button(button_label, key=f"powerup_{powerup_id}", disabled=button_disabled, use_container_width=True):
                    success, message = activate_powerup(powerup_id)
                    if success:
                        st.success(message)
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(message)
                
                st.divider()
    
    with tab3:
        st.header("Statistics 📊")
        
        st.metric("Total Clicks Earned", f"{st.session_state.total_clicks_earned:,}")
        st.metric("Manual Clicks", f"{st.session_state.total_manual_clicks:,}")
        st.metric("Time Played", get_time_played())
        st.metric("Current Multiplier", f"{st.session_state.click_multiplier}x")
        st.metric("Best Combo", f"{st.session_state.get('best_combo', 0)}x")
        st.metric("Best Streak", f"{st.session_state.get('best_streak', 0)} clicks")
        
        if st.session_state.prestige_level > 0:
            st.divider()
            st.subheader("Prestige Stats")
            st.metric("Prestige Level", st.session_state.prestige_level)
            st.metric("Prestige Points", st.session_state.prestige_points)
            st.metric("Prestige Bonus", f"{get_prestige_bonus():.1f}x")

# --- Sidebar: Achievements ---
with st.sidebar:
    st.header("Achievements 🏆")
    achievement_count = len(st.session_state.achievements)
    total_achievements = len(ACHIEVEMENTS)
    st.progress(achievement_count / total_achievements)
    st.caption(f"{achievement_count} / {total_achievements} unlocked")
    
    # Show unlocked achievements
    if st.session_state.achievements:
        st.subheader("✅ Unlocked:")
        for ach_id in sorted(st.session_state.achievements):
            ach = ACHIEVEMENTS[ach_id]
            st.success(f"{ach['name']} - {ach['description']}")
    
    # Show locked achievements
    locked = [ach_id for ach_id in ACHIEVEMENTS.keys() if ach_id not in st.session_state.achievements]
    if locked:
        with st.expander("🔒 Locked Achievements"):
            for ach_id in locked:
                ach = ACHIEVEMENTS[ach_id]
                if ach["threshold"] > 0:
                    st.caption(f"❓ {ach['name']} - Reach {ach['threshold']:,} clicks")
                else:
                    st.caption(f"❓ {ach['name']} - {ach['description']}")
    
    st.divider()
    
    # Reset button (for testing/debugging)
    if st.button("🔄 Reset Game", type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Track best combo and streak
if st.session_state.combo_streak > st.session_state.get('best_combo', 0):
    st.session_state.best_combo = st.session_state.combo_streak
if st.session_state.click_streak > st.session_state.get('best_streak', 0):
    st.session_state.best_streak = st.session_state.click_streak

# Auto-refresh mechanism for idle clicking
# Only rerun if we have auto-clicks active and enough time has passed
if st.session_state.auto_clicks_per_sec > 0:
    # Initialize last refresh time if needed
    if 'last_refresh_time' not in st.session_state:
        st.session_state.last_refresh_time = time.time()
    
    # Check if we should auto-refresh (every 0.5 seconds for smooth updates)
    current_time = time.time()
    time_since_last_refresh = current_time - st.session_state.last_refresh_time
    
    if time_since_last_refresh >= 0.5:
        st.session_state.last_refresh_time = current_time
        st.rerun()
