#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# Title of the app
st.title("Physics: The Art and Science of Thinking clearly")

# Instructions for users
st.write("Let's get started with the basics, shall we?")

# Embed lecture with responsive design
st.components.v1.html(
    """
<div style="max-width: 640px"><div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;"><iframe src="https://guidetoiit-my.sharepoint.com/personal/atmandeshmane_guidetoiit_onmicrosoft_com/_layouts/15/embed.aspx?UniqueId=9db68098-d664-4a99-a24c-6e5e82c90b8b&embed=%7B%22ust%22%3Atrue%2C%22hv%22%3A%22CopyEmbedCode%22%7D&referrer=StreamWebApp&referrerScenario=EmbedDialog.Create" width="640" height="360" frameborder="0" scrolling="no" allowfullscreen title="Vectors Part 1.mp4" style="border:none; position: absolute; top: 0; left: 0; right: 0; bottom: 0; height: 100%; max-width: 100%;"></iframe></div></div>    """,
    height=360,
)

