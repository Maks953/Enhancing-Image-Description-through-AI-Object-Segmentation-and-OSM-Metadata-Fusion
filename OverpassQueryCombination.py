#OSM (Using the Overpass API) and SegFormer(Hugging Face) integration
from transformers import SegformerFeatureExtractor, SegformerForSemanticSegmentation
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import exifread
import requests
import gc

# Load Segformer model and feature extractor - code provided from https://huggingface.co/docs/transformers/en/model_doc/segformer
feature_extractor = SegformerFeatureExtractor.from_pretrained("nvidia/segformer-b5-finetuned-cityscapes-1024-1024")
model = SegformerForSemanticSegmentation.from_pretrained("nvidia/segformer-b5-finetuned-cityscapes-1024-1024")

# Image input - images are selected from computer folders
filePath = "FOLDER PATH"

# Gps Exif metadata extractor - this function transforms Exif metadata to decimal
def ConvertingToDecimal(value):
    degree, minute, second = value.values
    # the formula is derived from chatgpt 3.5
    return degree.num / degree.den + (minute.num / minute.den / 60) + (second.num / second.den / 3600)

# This is a function called GPSCoordinates, this function extracts the longitude and latitude from the EXIF metadata of the image file
def GPSCoordinates(filePath):
    # the following line opens the file (image) in binary mode
    # rb allows the user compatibality with binary libraries
    with open(filePath, 'rb') as imageFile:
        # exifread library is applied in the following code line
        EXIFData = exifread.process_file(imageFile)
        # if statement to check if both GPSLatitude and GPSLongitude exist in the EXIFData
        if 'GPS GPSLatitude' in EXIFData and 'GPS GPSLongitude' in EXIFData:
            latitude = ConvertingToDecimal(EXIFData['GPS GPSLatitude'])
            # if statement to check if latitude reference is not north to indicate the latitude is in the south
            if EXIFData ['GPS GPSLatitudeRef'].values != 'N':
                # if latitude is in the south, latitude is negative
                latitude = -latitude
            longitude = ConvertingToDecimal(EXIFData['GPS GPSLongitude'])
                # similar to previous in the case of north. This if statement is to check if longitude is in the west
            if EXIFData ['GPS GPSLongitudeRef'].values != 'E' :
                    # if longitude is in the west, longitude is negative
                    longitude = -longitude
                    return latitude, longitude
                # if the function reaches here, there was no GPS data for latitude and longitude were not in EXIF Metadata.
                # return None for each latitude and longitude
    return None, None

# BuildingDetailsForImageDescriptions function has two parameters and expects for them to represent geographical coordinates
 # Chatgpt 3.5 helped with using the JSON data query
def BuildingDetailsForImageDescriptions (latitude, longitude):
    # this code line has the overpass api interpreter url
    OverpassURL = "http://overpass-api.de/api/interpreter"
    # OverpassQuery has a multi line stringwhich allows the user to send a query into overpass api
    # below overpassQuery, there is a json query, the json query looks for buildings within 30 meter radius
    OverpassQuery = f"""
    [out:json];
    (
      way(around:30,{latitude},{longitude})["building"];
    );
    out body;
    >;
    out skel qt;
    """
    response = requests.get(OverpassURL, params={'data': OverpassQuery}) #HTTP GET request to overpass api
    data = response.json()
    # below are the details I intend to have to enhance image descriptions
    BuildingDetails = {
        'name' : 'Building not identified',
        'architect' : 'Not specified',
        'construction date': 'Not specified',
        'building levels': 'Not specified',
        'description': 'Not specified',
        'wheelchair': 'N/A',
        'amenity': 'Not Specified',
        'designation': 'Not available'
    }
    # this script iterates over the elements in data[elements] list.
    # if any of the following are present, they will be stored
    for element in data['elements']:
        if 'tags' in element: # this line checks if an element contains tags key
           tags = element['tags']
           # these lines call tags to retrieve the value for the key
           BuildingDetails ['name'] = tags.get('name' , BuildingDetails ['name'])
           BuildingDetails['architect'] = tags.get('architect', BuildingDetails['architect'])
           BuildingDetails['construction date'] = tags.get('start_date', tags.get('construction date', BuildingDetails['construction date']))
           BuildingDetails['building levels'] = tags.get('building:levels', BuildingDetails['building levels'])
           BuildingDetails['description'] = tags.get('description', BuildingDetails['description'])
           BuildingDetails['wheelchair'] = tags.get('wheelchair', BuildingDetails['wheelchair'])
           BuildingDetails['amenity'] = tags.get('amenity', BuildingDetails['amenity'])
           BuildingDetails['designation'] = tags.get('designation', BuildingDetails['designation'])

    return BuildingDetails

latitude, longitude = GPSCoordinates(filePath)
if latitude is None or longitude is None:
    print("GPS Coordinates are not found")
    exit()

TheBuildingDetails = BuildingDetailsForImageDescriptions(latitude, longitude)
print(TheBuildingDetails)

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
CombinedImage = np.where(TheBuildingMaskResized[..., None], TheSegmentedImage, imageRGB)
CombinedImageBGR = cv2.cvtColor(CombinedImage.astype(np.uint8), cv2.COLOR_RGB2BGR)

# The Overlay
ThePILImageToSave = Image.fromarray(cv2.cvtColor(CombinedImageBGR, cv2.COLOR_RGB2BGR))
Draw = ImageDraw.Draw (ThePILImageToSave)
FontSize = 100  # Font size can be change to what it suits the user
Font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", FontSize)
TheBuildingInfo = "\n".join(f"{key}: {value}" for key, value in TheBuildingDetails.items())
Draw.text((80, 80), TheBuildingInfo, fill="blue", font=Font)
outputImagePath = "OUTPUT FOLDER PATH"
ThePILImageToSave.save(outputImagePath)

# Garbage Collector
gc.collect()
print("Building segmentation and identification complete.")
