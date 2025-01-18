import streamlit as st

# Configure the page
st.set_page_config(
    page_title="Learn Page",
    layout="wide",  # Optional: "centered" for a centered layout
)

# Sidebar Topics
st.sidebar.title("Topics")
topics = ["Vectors", "Motion in Straight Line"]  # Add more topics here
selected_topic = st.sidebar.radio("Select a Topic", topics)

# Subtopics for each topic
subtopics = {
    "Vectors": ["Vector Basics", "Parallelogram Law", "Vector Components",
                "Dot Product", "Cross Product", "Miscellaneous"],
    "Motion in Straight Line": ["Basic Terminologies", "Uniform Motion",
                                "Constant Acceleration", "Motion under Gravity",
                                "Miscellaneous"],
}

st.title(f"Learn: {selected_topic}")
st.write("Select a subtopic to explore modules, videos, and quizzes.")
selected_subtopics = subtopics[selected_topic]

# Display cards for subtopics
cols = st.columns(3)  # Adjust the number for more/less cards per row
selected_subtopic = st.radio("Select a subtopic:", selected_subtopics)

# Display content for the selected subtopic
if selected_subtopic:
    st.subheader(f"Content for {selected_subtopic}")
    st.write("Here is where you'll embed your videos, quizzes, and SensAI tool.")
    # Example: Embed a video
    st.components.v1.html(
        """
        <div style="max-width: 640px">
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
                <iframe src="https://guidetoiit-my.sharepoint.com/personal/atmandeshmane_guidetoiit_onmicrosoft_com/_layouts/15/embed.aspx?UniqueId=9db68098-d664-4a99-a24c-6e5e82c90b8b&embed=%7B%22ust%22%3Atrue%2C%22hv%22%3A%22CopyEmbedCode%22%7D&referrer=StreamWebApp&referrerScenario=EmbedDialog.Create" 
                        width="640" 
                        height="360" 
                        frameborder="0" 
                        scrolling="no" 
                        allowfullscreen 
                        title="Video Content" 
                        style="border:none; position: absolute; top: 0; left: 0; right: 0; bottom: 0; height: 100%; max-width: 100%;">
                </iframe>
            </div>
        </div>
        """,
        height=360,
    )
