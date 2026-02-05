from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
from tensorflow.keras.models import load_model

app = FastAPI()

model = load_model("cifar10_cnn.h5")

class_names = [
    "Airplane", "Car", "Bird", "Cat", "Deer",
    "Dog", "Frog", "Horse", "Ship", "Truck"
]

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read image
    contents = await file.read()
    np_img = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # Preprocess (same as training)
    img = cv2.resize(img, (32, 32))
    img = img / 255.0
    img = img.reshape(1, 32, 32, 3)

    # Predict
    pred = model.predict(img)
    cls = int(np.argmax(pred))
    conf = float(np.max(pred))

    return {
        "class_id": cls,
        "class_name": class_names[cls],
        "confidence": round(conf, 4)
    }
