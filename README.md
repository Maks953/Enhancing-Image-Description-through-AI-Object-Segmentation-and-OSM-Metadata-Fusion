# Final-Year-Project-2023-2024
Enhancing Image Description through AI Object Segmentation and OSM Metadata Fusion

In today's time , we have plenty of images as we are living in the so called digital world now, but separating specific objects from those images or real time camera integration can
be overwhelming as there is many factors in play like shadows and other obstructing objects. 
For this project I will be investigating combining AI for segmenting automatically buildings in combination to using Open Street Map(OSM) and Metadata to provide a useful description of the images.

The goal is to use AI segmentation to automatically identify and  isolate buildings within metadata and OSM. OSM will be used to provide an integration of context rich info about buildings.
This will be a fusion of object segmentation and OSM data and will be used to accurately label buildings. There will be an additional algorithm which will be an additional algorithm which will generate meaningful descriptions of the 
buildings.

Due to ethical consideration, there will be an emphasis on privacy and ethical reasons.

# The Neural Network
At the beginning I did research first. The first step was the neural
network. I researched neural networks and strategies/architectures I could use. The first neural network
I had looked at was R-CNN, but I found issues with it that could prolong the training on it. It is a great
neural network, but I felt there must be a better one out there. I tried yolov3. I researched Hugging
Face, an ai community website. I had used hugging face open-source neural networks and found that
yolov3 is appropriate for me to use. Yolo is very fast and accurate. Yolo also has implemented real time
through webcam. Although of how good it was, I decided to research other neural networks Aswell. I
investigated amazon cloud if I for real time and image storage for users.
I had also gone back to a neural network I was familiar with which is a conditional generative adversarial
network used with a paper called Pix2Pix. I also looked at cycle Gans, but I felt it wasn’t efficient enough
for real time orientation. I had investigated yolo and Pix2Pix and I wanted to retrain yolo on campus
buildings or repurpose Pix2Pix so it can do object orientation on buildings as Pix2Pix GAN is more of an
image-to-image translation rather than object orientation. So, this transition would’ve been
problematic. Pix2Pix also operates in 2D rather than 3D. Pix2Pix is excellent for image translating but
might struggle in a new scenario especially if there would be a 3D object. I decided to focus my time on
a different neural network.
I decided to do some research on annotating images. I investigated tools like labellmg and CVAT. As
every image needs to be annotated, which involves drawing boundaries around (in my case) buildings.
At the start it would have label ‘building’, but after osm integration it would have name of building.
Preparing data would be step two but more on that in problems Encountered.
I had looked at different types of segmentation. I am doing computer vision, and I am learning methods
along with practically putting them into my research/project. Firstly, I looked at instance segmentation.
It is useful if I want to distinguish between two buildings that are, for example, next to each other.
Semantic segmentation is another. Semantic works by classifying each pixel into a predefined class (so in
my case building). My supervisor suggested to me to look at hugging faces and we found that Segformer
which uses Semantic segmentation and operates with a transformers backbone for feature extraction,
and it also diverges from common CNNs. Also, Segformer comes pretrained already.
I used my machine, final year lab machine and google Collab to work on Segformer neural network. My
first step was to see how accurate it would be for only building segmentation. I used visual studio code
to work on python scripts for Segformer. The guide to install Segformer and test it was easy and not
complicated. I used git and Py torch. I had to install transformers on my machine and open cv. When I
finished my script, I did a quick demo on Temple bar street and the pub. The first demo I made is on Gitlab for image segmentation.
As of now I am investigating AWS (Amazon web services) for image segmentation and implementing this on iOS platform using AWS console. I have decided not to use AWS as I find Segformer to be more unique with OSM integration. Segformer is working quite well it does have some issues when it comes to tree branches and objects in the way of the building. Of course this is natural but Segformer takes big chunks away of each segmentation. For example tree branches in the way so Segformer does not segment that area but it dodges these obstacles by alot of pixels therefore making big jumps between building and obstacle.

# Open Street Map integration
I had researched ways to incorporate OSM.

Extract geographic information(Need to ensure that photo includes GPS Metadata such as Latitude and Longtitude) It needs to be
embedded in photo EXIF data. Use of Pillow, exiread, pixif.
Query OpenStreetMap


- Overpass API
- Nominatin API

Overpass allows for queying specific data like finding buildings in a vicinity.
Nominatin uses reverse geocoding. Given latitude and longitude, it can return nearest address => can/might include building names.
Using overpass API, I have learned how storing data and accessing it is like on OSM. At the moment the procedure is showing good results with giving the building names in the vicinity I wish to explore upon that so I can have even more info on each segmentation. This will provide rich description of each building segmentation image. To do this I plan to manipulate the JSON code.

# The Final Product
The final product can segment a building in any image. Then the application extracts latitude and longitude from the exif metadata. Using the metadata the script then uses overpass API and querying it using JSON comes back and returns the name of the building that has been segmented. At the beginning of the project it was only a name but at the end the plan is to have multiple descriptions such as architect, build date, does the building have wheelchair access? and description.


