import streamlit as st
import random

# Function to roll dice
def roll_dice(): 
    return random.randint(1, 6)

# Initialize game variables
if 'players_score' not in st.session_state:
    st.session_state.players_score = []
if 'winner_found' not in st.session_state:
    st.session_state.winner_found = False

# Input number of players
if 'players_count' not in st.session_state:
    st.title("Dice Roll Game")
    st.subheader("Welcome!")
    players_count = st.number_input("Enter the number of players (1-4):", min_value=1, max_value=4, step=1)
    if st.button("Start Game"):
        st.session_state.players_count = players_count
        st.session_state.players_score = [0 for _ in range(players_count)]

# Main game loop
if 'players_count' in st.session_state:
    n = st.session_state.players_count

    st.subheader("Game On! 🎲")
    for j in range(1, n+1):
        if st.session_state.winner_found:
            break
        if st.button(f"Player {j}: Roll Dice"):
            rolled_num = roll_dice()
            st.session_state.players_score[j-1] += rolled_num
            st.success(f"Player {j} rolled a {rolled_num}!")
            st.write(f"Current Scores: {st.session_state.players_score}")

            # Check for a winner
            if max(st.session_state.players_score) > 50:
                winner = st.session_state.players_score.index(max(st.session_state.players_score)) + 1
                st.balloons()
                st.success(f"🎉 Player {winner} is the winner of the match! 🎉")
                st.session_state.winner_found = True
                break

    # Display scores
    st.write("Scores:", st.session_state.players_score)

# Reset Button
if st.session_state.get('winner_found') and st.button("Restart Game"):
    st.session_state.clear()





