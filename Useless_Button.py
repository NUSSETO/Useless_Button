# I use Gemini to create this code, even the notes
# So no human is involved in making this internet garbage
# Ok, maybe me
import streamlit as st
import random

# Set the webpage title and subtitle
st.title("Do not press the button")

# --- Core Logic: Initialize Session State ---
# Check if 'count' exists in session_state, if not, initialize it to 0.
# This ensures the variable persists across reruns.
if 'count' not in st.session_state:
    st.session_state.count = 0

# --- Button Logic ---
# Increment the counter by 1 each time the button is clicked.
if st.button('DO NOT PRESS'):
    st.session_state.count += 1

# --- Display Results & Sarcastic Feedback ---
st.divider() # Draw a visual separator
st.metric(label = "How many time you've clicked that stupid button", value = st.session_state.count)

# Define logic for sarcastic messages based on the click count
count = st.session_state.count

if count == 0:
    st.info("Good, nothing has changed.")
elif count < 10:
    st.warning(f"You've pressed the button {count} times, is it worth it?")
elif count < 25:
    st.warning("Serious? Can you find something better to do?")
elif count < 100:
    st.error("Enough is enough.")
elif count == 100:
    st.balloons() # Trigger balloon animation
    st.success("Congrats! You've wasted so much time in your life!")
else:
    # Give up on the user if they click too many times
    st.write("That's it. I am not going to say anything else anymore.")