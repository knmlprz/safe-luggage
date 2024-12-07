import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision import transforms
import cv2
import time
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Load the pretrained Faster R-CNN model
model = fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Define the transformation to convert OpenCV image to tensor
transform = transforms.Compose([
    transforms.ToTensor()
])

def get_prediction(image, threshold=0.5):
    """ Get predictions from the model """
    image = transform(image)
    image = image.unsqueeze(0)  # Add a batch dimension
    with torch.no_grad():
        predictions = model(image)
    return predictions[0]

def visualize(image, boxes, labels, scores, threshold=0.5):
    """ Visualize the results """
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    ax = plt.gca()
    for box, label, score in zip(boxes, labels, scores):
        if score > threshold:
            x_min, y_min, x_max, y_max = box
            rect = patches.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, linewidth=2, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            ax.text(x_min, y_min, f'{label.item()}: {score:.2f}', bbox=dict(facecolor='yellow', alpha=0.5))
    plt.axis('off')
    plt.show()

# Open a connection to the camera
cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert the frame from BGR to RGB (OpenCV uses BGR by default)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert frame to PIL Image
        pil_image = Image.fromarray(frame_rgb)

        # Get predictions
        predictions = get_prediction(pil_image)

        # Extract the boxes, labels, and scores
        boxes = predictions['boxes']
        labels = predictions['labels']
        scores = predictions['scores']

        # Convert PIL image back to numpy array for visualization
        np_image = np.array(pil_image)

        # Visualize the results
        visualize(np_image, boxes, labels, scores, threshold=0.5)

        # Wait for 1 second
        time.sleep(1)

finally:
    # Release the camera
    cap.release()
    cv2.destroyAllWindows()
