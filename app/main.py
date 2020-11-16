import os
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import flamebase, pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    max_age=5000
)


@app.get('/')
def index():
    return "Hello world!"


@app.get('/{user_id}/get-all-books')
def get_all_user_audiobooks(user_id: str):
    ans = flamebase.get_all_audiobooks(user_id)
    return ans


@app.get('/{bookName}/get-all-audiobook-chapters')
def get_all_audiobook_chapters(bookName: str):
    ans = flamebase.get_all_audiobook_chapters(bookName)
    return ans


@app.get('/{user_id}/{bookName}/get-image')
def get_audiobook_image(user_id: str, bookName: str):
    return flamebase.get_database_url(user_id, bookName, "image", bookName, "png")


@app.get('/create-pdf')
def create_pdf_and_generate_voice(user_id: str, voice_name: str):
    print(f"Voice: {voice_name}")
    try:
        os.remove("temp.pdf")
    except OSError:
        pass
    fname = str(uuid.uuid4())[:8] + ".pdf"
    print(fname)
    flamebase.download_file(fname)
    pdf.set_user_id(user_id)
    pdf.process_doc(fname, voice_name)
    return "Success"


@app.get('/{user_id}/{bookName}/{category}/{number}')
def get_from_database(user_id: str, bookName: str, category: str, number: int):
    if category == "image":
        extension = "png"
    elif category == "text":
        extension = "txt"
    else:
        extension = "mp3"
    return flamebase.get_database_url(user_id, bookName, category, str(number), extension)
