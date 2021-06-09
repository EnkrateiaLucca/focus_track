import streamlit as st
from datetime import datetime
from track_focus import *


# Creating the Dashboard app #
st.title("Focus Tracker")

df_focus = create_focus_df()

fig = plotFocus(df_focus)

st.write(fig)












