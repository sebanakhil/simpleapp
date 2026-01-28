import os
import io
from fastapi import FastAPI, UploadFile, File
from azure.cosmos import CosmosClient, PartitionKey
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
import speech_recognition as sr
from fastapi.responses import FileResponse
app = FastAPI()

from pydub import AudioSegment
import io

@app.post("/chat/voice")
async def chat_voice(session_id: str, audio_file: UploadFile = File(...)):
    # 1. Read the raw bytes (likely WebM/Ogg from the browser)
    raw_audio_bytes = await audio_file.read()
    
    # 2. CONVERT TO WAV (Crucial step from your reference)
    try:
        audio_segment = AudioSegment.from_file(io.BytesIO(raw_audio_bytes))
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)
    except Exception as e:
        return {"error": f"Conversion failed: {str(e)}. Make sure ffmpeg is installed."}

    # 3. Transcribe using the converted WAV
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_io) as source:
        audio_data = recognizer.record(source)
        try:
            user_text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return {"error": "Could not understand audio"}

    # ... rest of your Azure AI Foundry logic ...


@app.get("/")
async def get_ui():
    # This serves your HTML file instead of the "It works" JSON
    return FileResponse("index.html")

# --- CONFIGURATION ---
COSMOS_ENDPOINT = "https://acdb-dev-in-001.documents.azure.com:443/"
COSMOS_KEY = "tpaG89BWXuCCdzubVY5N8CjvmRO3Swhe5pHLvNxjD0DCqX0PGywkxNRPr69RJpy4N2TLtKEdgjkDACDbyzLfyg=="
DATABASE_NAME = "SwimmingApp"
CONTAINER_NAME = "Sessions"

AI_ENDPOINT = "https://junimaakhil-2045-resource.services.ai.azure.com/api/projects/junimaakhil-2045"
AGENT_ID = "asst_LvmUcSVcgpRSWvF9QbecMPJP"

# --- INITIALIZE CLIENTS ---
credential = DefaultAzureCredential()
project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint="https://junimaakhil-2045-resource.services.ai.azure.com/api/projects/junimaakhil-2045")
cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
db = cosmos_client.get_database_client(DATABASE_NAME)
container = db.get_container_client(CONTAINER_NAME)

recognizer = sr.Recognizer()

@app.post("/chat/voice")
async def chat_voice(session_id: str, audio_file: UploadFile = File(...)):
    # 1. Read and Convert Audio (Crucial Step)
    raw_audio_bytes = await audio_file.read()
    try:
        audio_segment = AudioSegment.from_file(io.BytesIO(raw_audio_bytes))
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)
    except Exception as e:
        print(f"Conversion Error: {e}")
        return {"ai_response": "Audio conversion failed. Check ffmpeg.", "score": 0}

    # 2. Transcribe
    with sr.AudioFile(wav_io) as source:
        audio = recognizer.record(source)
        try:
            user_text = recognizer.recognize_google(audio)
        except:
            return {"ai_response": "I couldn't hear you clearly.", "score": 0}

    # 3. Azure AI Logic
    session_data = container.read_item(item=session_id, partition_key=session_id)
    thread_id = session_data.get("thread_id")

    project.agents.messages.create(thread_id=thread_id, role="user", content=user_text)
    project.agents.runs.create_and_process(thread_id=thread_id, agent_id=AGENT_ID)
    
    messages = project.agents.messages.list(thread_id=thread_id, order=ListSortOrder.DESCENDING)
    ai_response = messages.data[0].text_messages[-1].text.value

    # 4. Scoring logic
    new_score = calculate_persuasion_score(ai_response, session_data.get("score", 0))
    session_data["score"] = new_score
    container.upsert_item(session_data)

    return {
        "ai_response": ai_response,
        "score": int(new_score)
    }

def calculate_persuasion_score(text, current_score):
    """
    Simple logic to extract score if you tell your agent to output it,
    or a simple keyword-based mock for testing.
    """
    # Logic: If agent mentions 'fine' or 'maybe', increase score
    if "fine" in text.lower() or "ok" in text.lower():
        return min(current_score + 20, 100)
    return max(current_score - 5, 0)

@app.post("/session/start")
async def start_session():
    # Create a new thread in AI Foundry
    thread = project.agents.threads.create()
    session_id = f"user_{thread.id}"
    
    item = {
        "id": session_id,
        "thread_id": thread.id,
        "score": 0,
        "case": "Convince the guy to go swimming"
    }
    container.create_item(item)
    return {"session_id": session_id}