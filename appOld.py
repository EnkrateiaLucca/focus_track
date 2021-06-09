# good streamlit source: https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace
# USE THE ALWAYS RERUN FEATURE ON STREAMLIT!!!!!!!!!!!!!!
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json_lines
import altair as alt
sns.set()
import difflib
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from natsort import natsorted
from utils import *
from visualizations import *
from preprocessing import *


if __name__ == '__main__':
    # Loading data #
    # dateTags = loadDates()
    timeWindows,dateWindows,windows = loadWindows()
    timeFocus,dateFocus,focus = loadFocus()
    typingData = loadTypingPerformance()
    # tasks = loadTasks()
    bootDates,bootTimes = loadSystemBootLog()
    ############################################################
    # Creating the Dashboard app #
    st.title("Self-Track")
    # SIDEBAR #
    viewType = st.sidebar.selectbox('',('Single Day', 'Overview'))
    # create a button in the side bar that will move to the next page/radio button choice
    next = st.sidebar.button('Next')
    prev = st.sidebar.button('Previous')
    dateInput = st.sidebar.text_input("Date (format: YYYY-mm-dd):", "")
    # will use this list and next button to increment page
    # new_choice = dates # Dates not implemented yet
    dates = natsorted(list(set(dateWindows))) # Put the dates here for the single view!
    day = handleDatesNextPreviousBtn(dates,nextBtn=next,prevBtn=prev)
    if dateInput!="":
        try:
            day = dateInput
        except: 
            pass
    # Preprocessing the data to visualize
    df_focus = prepFocus(focus,timeFocus,dateFocus,day=day)
    df_wpmAcc = prepTyping(typingData,viewType,day)
    df_window_usage = prepWindowUsage(windows,timeWindows,dateWindows,viewType,day=day)
    df_systemBootLog = prepSystemBoot(bootDates,bootTimes)
    ######################################################
    
    # Visualizing Focus,Window Usage & System Boot times
    ## Generating the Plots
    year,month,dayDt = split_date(day)
    focusBar,focusTrend,total_focus_time = plotFocus(df_focus,viewType,dayDt,month,year,day)
    sysBootLog = plotSystemBoot(df_systemBootLog,viewType,day)
    pie_chart,eventWindows = plotWindowUsage(df_window_usage,windows,viewType,day)

    ## Writing the Figures to the Streamlit app
    if st.sidebar.checkbox("Focus & Desktop Usage",value=True):
        fig_focus_windows_fig = create_figure_focus_windowEvents(focusBar,focusTrend,eventWindows,viewType,total_focus_time,year,month,dayDt)
        st.write(fig_focus_windows_fig)
    
    if st.sidebar.checkbox("Desktop Pie Chart"):
        window_usage_fig = create_figure_desktop_usage_pieChart(pie_chart,viewType,total_focus_time,year,month,dayDt)
        st.write(window_usage_fig)
    
    if st.sidebar.checkbox("System Boot Times"):
        sysBoot_fig = create_figure_sysBootTimes(sysBootLog,viewType,total_focus_time,year,month,dayDt)
        st.write(sysBoot_fig)

    if st.sidebar.checkbox("Show typing performance"):
        fig = plotTyping(df_wpmAcc)
        st.write(fig)

    



    