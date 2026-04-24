from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import io
import pickle

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("Backend/pneumonia_model.pkl", "rb") as f:
    model = pickle.load(f)

class_names = ["NORMAL", "PNEUMONIA"]
IMG_SIZE = 128

def preprocess_image(image):
    image = image.convert("RGB")
    image = image.resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(image) / 255.0
    return np.expand_dims(img_array, axis=0)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        processed = preprocess_image(image)

        prediction = model.predict(processed)
        class_index = np.argmax(prediction)

        return {
            "prediction": class_names[class_index],
            "confidence": float(np.max(prediction))
        }

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}