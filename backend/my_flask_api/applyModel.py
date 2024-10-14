import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image
import numpy as np

def apply():
    # CONSTANT
    IMG_SIZE = 48

    # โหลดโมเดล
    model = load_model('models/model.h5')

    # เตรียมภาพสำหรับการพยากรณ์
    img_path = 'uploads/detected-face.png'
    
    # โหลดภาพและปรับเป็นขาวดำ
    img = Image.open(img_path).convert('L')
    # ปรับขนาดภาพตามที่โมเดลต้องการ
    img = img.resize((IMG_SIZE, IMG_SIZE))
    
    # แปลงภาพขาวดำเป็น RGB
    img = img.convert('RGB')
    
    # ทำ Normalization ให้อยู่ระหว่าง [0, 1]
    img_array = img_to_array(img) / 255.0
    # เพิ่มมิติให้สอดคล้องกับ input ของโมเดล
    img_array = np.expand_dims(img_array, axis=0)

    # ทำนายอารมณ์
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)

    # แสดงผลลัพธ์
    emotion_labels = ['angry', 'disgust', 'fear', 'happy',
                      'neutral', 'sad', 'surprise']

    return emotion_labels[predicted_class[0]]
