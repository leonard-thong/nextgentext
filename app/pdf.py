import fitz
import unicodedata
import os
import re

import textspeech, flamebase

userID = None


def set_user_id(user_id):
    global userID
    userID = user_id


def mkdir() -> None:
    if not os.path.exists('image'):
        os.makedirs('image')
    if not os.path.exists('audio'):
        os.makedirs('audio')
    if not os.path.exists('text'):
        os.makedirs('text')


def delFiles(dir) -> None:
    path = os.getcwd()
    path = os.path.join(path, dir)
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))


def rm(fname=None) -> None:
    try:
        os.remove(fname)
    except OSError:
        pass
    if os.path.exists('image'):
        try:
            os.rmdir('image')
        except:
            delFiles('image')
            os.rmdir('image')
    if os.path.exists('audio'):
        try:
            os.rmdir('audio')
        except:
            delFiles('audio')
            os.rmdir('audio')
    if os.path.exists('text'):
        try:
            os.rmdir('text')
        except:
            delFiles('text')
            os.rmdir('text')


def save_image(doc) -> None:
    pix = doc[0].getPixmap()
    pix.writeImage(f"image/{doc.metadata['title']}.png")


#
# def save_html(doc, page_start: int, page_end: int) -> None:
#     with open(f"text/{page_start}.txt", 'w') as f:
#         for page in doc.pages(page_start, page_end, 1):
#             f.write(page.getText('html'))


def add_files_to_database(document, filename):
    global userID
    title = document.metadata['title'] if document.metadata['title'] else filename.split(".")[0]
    # Add all text
    for doc in os.listdir("text"):
        flamebase.put_to_database(userID, title, "text", doc)

    # Add all images
    for doc in os.listdir("image"):
        flamebase.put_to_database(userID, title, "image", doc)

    # Add all audio
    for doc in os.listdir("audio"):
        flamebase.put_to_database(userID, title, "audio", doc)


def save_text(doc, page_name: str, page_start: int, page_end: int, counter: int = 1) -> None:
    with open(f"text/Chapter - {counter}.txt", 'w', encoding='utf-8') as f:
        for page in doc.pages(page_start, page_end, 1):
            text = page.getText()
            text = re.sub(r'\n\s*\n', '\n', text)
            text = text.strip()
            if text:
                f.write(text)


def save_audio(voice_name: str):
    for doc in os.listdir("text"):
        try:
            with open(f"text/{doc}", 'r', encoding='utf-8') as f:
                text = f.read()[:4999]
            if text:
                docname = doc.split(".")[0]
                textspeech.text_to_wav(voice_name, text, docname)
        except:
            pass


def process_doc(filename: str, audio_name: str) -> None:
    mkdir()
    doc = fitz.open(filename)

    temp = list(map(lambda x: [x[0], unicodedata.normalize("NFKD", x[1]), x[-1]], doc.getTOC()))
    content = {}
    for each in temp:
        content[each[1]] = each[-1] if each[-1] >= 0 else 0

    # print(content)

    save_image(doc)

    counter = 0
    f_count = 1
    pgs = list(content.values())
    for counter in range(len(pgs) - 1):
        # save_html(doc, pgs[counter], pgs[counter + 1])
        save_text(doc, "Chapter - " + str(counter + 1),
                  pgs[counter], pgs[counter + 1], f_count)
        f_count += 1
    save_text(doc, "Chapter - " + str(counter + 1), pgs[counter + 1], doc.pageCount, f_count + 1)

    save_audio(audio_name)

    add_files_to_database(doc, filename)

    doc.close()
    rm(filename)


if __name__ == '__main__':
    # set_user_id("lYit13ukCtWRiC0tv6gROLaVscX2")
    set_user_id("tRUWglgOoARsRLizILq6nh5eUnA3")
    mkdir()
    process_doc("../BusinessLaw.pdf")
    # rm()
