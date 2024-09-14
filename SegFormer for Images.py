from transformers import SegformerFeatureExtractor, SegformerForSemanticSegmentation
import numpy as np
import cv2
from PIL import Image
import gc

# using SegFormers feature extractor and model. code provided from https://huggingface.co/docs/transformers/en/model_doc/segformer
feature_extractor = SegformerFeatureExtractor.from_pretrained("nvidia/segformer-b5-finetuned-cityscapes-1024-1024")
model = SegformerForSemanticSegmentation.from_pretrained("nvidia/segformer-b5-finetuned-cityscapes-1024-1024")

# Example Image
filePath = "FOLDER PATH" 

# Image Segmentation process
image = cv2.imread(filePath)
imageRGB = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
PIL_Image = Image.fromarray(imageRGB)
inputs = feature_extractor (images = PIL_Image, return_tensors = "pt")
outputs = model(**inputs)
logits = outputs.logits[0]
segmentationMap = logits.argmax(dim=0).detach().cpu().numpy()
TheBuildingMask = (segmentationMap == 2)
height, width, _ = image.shape
TheBuildingMaskResized = cv2.resize(TheBuildingMask.astype(np.uint8), (width, height), interpolation=cv2.INTER_NEAREST)
TheSegmentedImage = np.zeros_like(imageRGB)
TheSegmentedImage[TheBuildingMaskResized == 1] = [57, 255, 20]
# Combining the segmentation
combinedImage = np.where(TheBuildingMaskResized[..., None], TheSegmentedImage, imageRGB)
# Convert the combined image to BGR for OpenCV compatibility
combinedImageBGR = cv2.cvtColor(combinedImage.astype(np.uint8), cv2.COLOR_RGB2BGR)
# Save or display the processed image
outputPath = "OUTPUT PATH"
cv2.imwrite(outputPath, combinedImageBGR)
# Converting using OpenCV image (BGR) to RGB format for PIL
combinedImageForPIL = cv2.cvtColor(combinedImageBGR, cv2.COLOR_BGR2RGB)
PILImageToSave = Image.fromarray(combinedImageForPIL)
# Saving the image with PIL
PILImageToSave.save(outputPath)
# Collect garbage
gc.collect()
print("Building segmentation complete.")
