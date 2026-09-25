from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st

@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()

def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as e:
        st.toast(icon="⚠️", body="Voice Recognition Error")
        return None

def identify_speaker(new_embedding, candidate_dict):
    if new_embedding is None or not candidate_dict:
        return None, 0.0

    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidate_dict.items():
        if stored_embedding:
            similarity = np.dot(new_embedding, stored_embedding)
            if similarity > best_score:
                best_score = similarity
                best_sid = sid

    if best_score >= 0.65: #threshold
        return best_sid, best_score
    return None, best_score

def process_bulk_audio(audio_bytes, candidate_dict):
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)
        identified_results = {}

        valid_segments = [s for s in segments if (s[1] - s[0]) >= sr * 0.5]
        if not valid_segments:
            valid_segments = [(0, len(audio))]

        for start, end in valid_segments:
            if (end - start) < sr * 0.3:
                continue
            wav = preprocess_wav(audio[start:end])
            embedding = encoder.embed_utterance(wav)
            sid, score = identify_speaker(embedding, candidate_dict)

            if sid is not None and (sid not in identified_results or score > identified_results[sid]):
                identified_results[sid] = score

        return identified_results

    except Exception as e:
        print(f"Error in process_bulk_audio: {e}")
        st.toast(icon="⚠️", body=f"Voice Recognition Error: {str(e)}")
        return {}