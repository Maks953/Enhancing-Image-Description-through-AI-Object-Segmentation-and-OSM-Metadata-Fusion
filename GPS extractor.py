# Gps Exif metadata extractor - this function transforms Exif metadata to decimal
# ChatGPT 3.5 was used to incorporate the formula, to convert EXIF into decimal
import exifread
filePath =  "FOLDER PATH"

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
 
latitude, longitude = GPSCoordinates(filePath)

if latitude and longitude:
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print("GPS coordinates not found.")
