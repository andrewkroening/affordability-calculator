"""This is the main app module"""

import streamlit as st

st.set_page_config(
    page_title="Affordability Calculator",
    page_icon="💲",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.title("Welcome to Fun Money Tools")
st.write(
    "Learning about finance is hard, and sometimes it can be really intimidating. This is a collection of tools to help you manage your money and learn some practices along the way. It's set up to help you answer some common questions that you might have while you navigate some potentially sticky situations."
)

st.write("You can use the sidebar to navigate to the tools you want to use, or scroll down to walkthrough some of the features.")

st.markdown("---")
st.write("Figuring out how to manage your money can be really hard. Coming soon, I'll be rolling out a budgeting tool to help you learn how to distribute your earnings and what your money can do for you.")
c1, c2 = st.columns(2)

with c1:
    st.header("Budgeting Tools (Coming Soon)")

with c2:
    st.markdown("")

st.markdown("---")
st.write("Buying a home is a big decision, and it's important to know what you can afford. This tool will help you figure out how much you can afford to spend on a home, and how much you can expect to pay each month based on a few parameters.")

c3, c4 = st.columns(2)

with c3:
    st.markdown("")

with c4:
    st.header("Home Buying Power Calculator")
    