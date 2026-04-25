from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import io, pickle, gc

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

with open("pneumonia_model.pkl", "rb") as f:
    model = pickle.load(f)

class_names, IMG_SIZE = ["NORMAL", "PNEUMONIA"], 128

def preprocess_image(image):
    img = image.convert("RGB")                          
    img = img.resize((IMG_SIZE, IMG_SIZE), Image.BILINEAR)
    arr = np.array(img, dtype=np.float32) / 255.0      
    return np.expand_dims(arr, axis=0)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        processed = preprocess_image(image)
        image.close()       
        del contents        

        prediction = model.predict(processed)
        del processed       
        gc.collect()        

        idx = int(np.argmax(prediction))
        return {"prediction": class_names[idx], "confidence": round(float(np.max(prediction)), 4)}

    except Exception as e:
        gc.collect()
        return {"error": str(e)}