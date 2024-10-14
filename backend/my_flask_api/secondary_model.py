import pickle
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Path to the image and the model
image_path = 'uploads/detected-face.png'
model_path = 'models/model.pkl'
# model_path = 'models/model-2.pkl'

# Load the model
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Preprocess the image
def preprocess_image(image_path, target_size=(48, 48)):
    # Load the image
    image = load_img(image_path, target_size=target_size)
    # Convert the image to an array
    image_array = img_to_array(image)
    # Scale the pixel values to [0, 1]
    image_array = image_array / 255.0
    # Expand dimensions to match the model's expected input shape
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

# Preprocess the input image
preprocessed_image = preprocess_image(image_path)

# Make a prediction
prediction = model.predict(preprocessed_image)

# Output the prediction
print("Prediction:", prediction)

# Class labels
class_labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

# Find the index of the highest confidence score
predicted_index = np.argmax(prediction)

# Get the corresponding emotion label
predicted_emotion = class_labels[predicted_index]

# Output the result
print(f"The predicted emotion is: {predicted_emotion}")