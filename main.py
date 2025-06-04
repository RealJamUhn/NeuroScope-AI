import streamlit as st
import tempfile
from llm.history import HistoryAgent
from llm.audioanalyze import AudioAgent
from llm.videoanalyze import VisionAgent
from llm.diagnosisagent import DiagnosisAgent
from utils.DSM5MCP import DSM5_ASD_DATA
from utils.audio_utils import extract_audio, get_timestamped_transcript, transcript_structure

history_agent = HistoryAgent()
audio_agent = AudioAgent()
video_agent = VisionAgent()
diagnosis_agent = DiagnosisAgent()

st.set_page_config(page_title="NeuroScope AI", layout="centered")

st.markdown("*⚠️DISCLAIMER* This tool should not be used as a substitute for professional medical advice")

st.title("AI Autism Spectrum Disorder Diagnosis Tool (NeuroScope AI)")

age_input = st.number_input(
    "Enter the patient's age", value=None, step=1, placeholder=""
)

history_input = st.text_area(
    label="Enter the patient's behavioral, developmental, and medical history:",
    placeholder="e.g., Learned speech fundamentals at 5, could rarely keep eye contact, seizures during infancy...",
    height=200
)

video_file = st.file_uploader("Upload a patient video for behavioral analysis", type=["mp4", "mov", "avi", "webm"])

if video_file is not None:
    
    st.video(video_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_file.read())
        temp_video_path = temp_video.name

if st.button("Submit For Diagnosis"):
    if age_input is None:
        st.warning("Please enter an age before submitting.")
    if not history_input.strip():
        st.warning("Please enter history before submitting.")
    if video_file is None:
        st.warning("Please upload a video before submiting.")
    
    if history_input.strip():
        if video_file is not None:
            if age_input is not None:
                st.success("Submitted For Diagnosis.")
                with st.spinner("Analyzing Medical History and Behavior", show_time=True):
                    history_analyze = history_agent.analyze(history_input)
                with st.spinner("Analyzing Visual Features", show_time=True):
                    video_analyze = video_agent.analyze(temp_video_path)
                with st.spinner("Extracting, Transcribing and Structuring Audio...", show_time=True):
                    audio_path = extract_audio(temp_video_path)
                    segments = get_timestamped_transcript(audio_path)
                    transcript = transcript_structure(segments)
                with st.spinner("Analyzing Audible Features", show_time=True):
                    audio_analyze = audio_agent.analyze(transcript)
                with st.spinner("Generating Final Diagnosis", show_time=True):
                    diagnose = diagnosis_agent.analyze(age_input, history_analyze, video_analyze, audio_analyze, DSM5_ASD_DATA)
                st.text_area("Diagnosis", diagnose, height=500)
