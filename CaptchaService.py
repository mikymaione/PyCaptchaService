import base64
import random
import string
import uuid

import uvicorn
from captcha.image import ImageCaptcha
from fastapi import FastAPI
from pydantic import BaseModel

CAPTCHA_SIZE = 6
generated = {}

app = FastAPI()


class Answer(BaseModel):
    answer: str
    guid: str


@app.get("/")
def welcome():
    return {"Hello": "World!"}


@app.get("/generate")
def generate_captcha():
    captcha_text = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(CAPTCHA_SIZE))
    guid = str(uuid.uuid4())
    generated[guid] = captcha_text

    image = ImageCaptcha()
    img = image.generate(captcha_text)

    return {
        "guid": guid,
        "answer": captcha_text,
        "captcha": base64.b64encode(img.read())
    }


@app.post("/validate/")
def validate_captcha(answer: Answer):
    correct = answer.answer == generated[answer.guid]
    return {"Correct": correct}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
