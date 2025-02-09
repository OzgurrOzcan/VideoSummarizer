import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
load_dotenv()

import os 

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))


st.set_page_config(layout="wide", page_title="Video Summarizer", page_icon="🎥")




st.markdown(
     """
    <style>
    body {
        background-color: #222222;  /* Dark Gray */
        color: white;  /* White Text */
    }
    .stApp {
        background-color: #222222;
    }
    h1, h2, h3, h4, h5, h6, p, div {
        color: white !important;
    }

   .stImage > img {
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
    
    
    h1 {
        text-align: center !important;
        padding: 20px 0 !important;
    }
    
    
    .stTextInput {
        max-width: 800px !important;
        margin: 0 auto !important;
    }
    
    
    .stImage > img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    
    
    .block-container {
        max-width: 1000px !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        margin: 0 auto !important;
    }
    
    .summary-text {
        color: white !important;
        font-size: 18px !important;
        line-height: 1.6 !important;
    }

    .stButton > button {
        color: black !important;
        background-color: white !important;
        border: 2px solid white !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        transition: background-color 0.3s ease, color 0.3s ease;
        display: block !important;
        margin: 0 auto !important;  /* Center the button */
    }
    
    .stButton > button p,
    .stButton > button span,
    .stButton > button div,
    .stButton > button * {
        color: black !important;
    }

    .stButton > button:hover {
        background-color: #ddd !important;
        color: black !important;
        border: 2px solid #ddd !important;
    }

    .stButton > button:active {
        background-color: black !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.markdown("<h1 style='color: white;'>▶ Youtube Video Summarizer</h1>", unsafe_allow_html=True)




def get_transcript(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="https://img.youtube.com/vi/{video_id}/0.jpg" width="500">
        </div>
        """,
        unsafe_allow_html=True
    )
     

        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
            
        return transcript    
    except Exception as e:
        raise e
   
prompt = ''' You are a YouTube Video Summarizer. Your task is to analyze the transcript of a video and generate a concise yet comprehensive summary that captures the key points, insights, and takeaways.

Instructions:
Summarize the entire video clearly and effectively within 250 words.
Highlight key arguments, important details, and actionable insights in bullet points.
Ensure the summary covers the main topics, supporting details, and final conclusions.
Use clear, structured, and informative language to maintain readability.
Omit unnecessary details while retaining essential information. Please provide the summary of the text given here: '''


def generate_gemini_content(transcript_text , prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(transcript_text + prompt)
    return response.text
    
#st.title("▶ Youtube Video Summarizer")
youtube_link = st.text_input("Enter the Youtube Video link here: ")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    #st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg",width=500)

if st.button("Get Summary"):
    transcript_text = get_transcript(youtube_link)
    if transcript_text:
        summary = generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Summary")
        st.write(summary)


