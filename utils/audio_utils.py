from faster_whisper import WhisperModel
from moviepy import VideoFileClip
import tempfile

def extract_audio(video_path):

    output_path = tempfile.mktemp(suffix=".wav")
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(output_path, codec='pcm_s16le')
    return output_path

def get_timestamped_transcript(audio_path, model_size="base"):

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_path, vad_filter=True, vad_parameters={"threshold": 0.5})

    return [
        {
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "text": seg.text.strip()
        }
        for seg in segments
    ]

def transcript_structure(segments):

    full_text=""

    for i in range(0, len(segments)-1, 2):
        
        question = segments[i]
        answer = segments[i+1]
        delay = round(answer['start'] - question['end'], 2)

        full_text +=f"{question['text']}. {delay} seconds. {answer['text']}."

    return full_text.strip()
