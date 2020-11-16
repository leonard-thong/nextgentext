import json
import pprint

import pyrebase
from typing import *

config = {
    "apiKey": "AIzaSyA72hmmNga4xOEC3V1LJ4bbOwNsoJ97cuI",
    "authDomain": "book2audio-be677.firebaseapp.com",
    "databaseURL": "https://book2audio-be677.firebaseio.com",
    "projectId": "book2audio-be677",
    "storageBucket": "book2audio-be677.appspot.com",
    "messagingSenderId": "74814148576",
    "appId": "1:74814148576:web:0ac07bc85fad2b598de585",
    "measurementId": "G-8RH3T8WTND"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

user = None

storage = firebase.storage()
db = firebase.database()


# def sign_in(email: str, password: str):
#     global user
#     user = auth.sign_in_with_email_and_password(email, password)


def put_to_database(userID: str, bookName: str, category: str, name: str) -> bool:
    try:
        storage.child(f"{userID}/{bookName}/{category}/{name}").put(f"{category}/{name}")
        if name.split(".")[-1] == "txt":
            db.child("Audiobooks").child(userID).update({bookName: ""})
            db.child("Chapters").child(bookName).update({name.split(".")[0]: ""})
        return True
    except Exception as e:
        print(e)
        return False


def get_all_audiobooks(userID: str) -> List:
    try:
        result = []
        res = db.child("Audiobooks").child(userID).get()
        for each in res.each():
            result.append(each.key())
        return result
    except Exception as e:
        print(e)
        return []


def get_all_audiobook_chapters(bookName: str) -> List:
    try:
        result = []
        res = db.child("Chapters").child(bookName).get()
        for each in res.each():
            result.append(each.key())
        return result
    except Exception as e:
        print(e)
        return []


def download_file(filename: str):
    storage.child("temp/temp.pdf").download(filename)


def get_database_url(userID: str, bookName: str, category: str, number: str, extension: str = "mp3") -> str:
    try:
        if category != "image":
            link = storage.child(f"{userID}/{bookName}/{category}/Chapter - {number}.{extension}").get_url(None)
        else:
            link = storage.child(f"{userID}/{bookName}/{category}/{number}.{extension}").get_url(None)
        return link
    except Exception as e:
        print(e)
        return "ERROR"
