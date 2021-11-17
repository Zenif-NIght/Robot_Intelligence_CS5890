# this program will search for a hiker in a set of 4x4 images 
# use an algorithm (such as Yolov3) to do the image classification and return data upon identification

import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.type_check import imag
# this function will load in a the yolo model and return the output of the model
def load_model():
    # https://www.codespeedy.com/yolo-object-detection-from-image-with-opencv-and-python/
    #Load YOLO Algorithms\
    net=cv2.dnn.readNet("yolov3.weights","yolov3.cfg")


    #To load all objects that have to be detected
    classes=[]
    with open("coco.names","r") as f:
        read=f.readlines()
    for i in range(len(read)):
        classes.append(read[i].strip("\n"))


    #Defining layer names
    layer_names=net.getLayerNames()
    output_layers=[]
    for i in net.getUnconnectedOutLayers():
        output_layers.append(layer_names[i[0]-1])
    
    return net, classes, output_layers                                                 


# classifier function will daw the bonding box around the hiker
def classifier(images):
    net, classes, output_layers = load_model()
    # image = cv2.imread(image)
    # cv2.imshow('Image',image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    for image in images:
        # image = cv2.imread(image)
        # cv2.imshow('Image',image)
        # cv2.waitKey(0)
        #  Get the dimensions of the image
        
        #  we will use these to determine the bounding box
        height, width, channels = image.shape

        #  Create a blob from the image
        #  this will be used to determine the bounding box
        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        #  set the input to the network
        net.setInput(blob)

        #  get the output from the network
        outs = net.forward(output_layers)

        #  initialize the lists of boxes and confidences
        boxes = []
        confidences = []

        #  loop over the outputs
        for out in outs:
            #  loop over the detections
            for detection in out:
                #  extract the class id and confidence
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                #  filter out weak predictions by ensuring the
                #  confidence is greater than the minimum confidence
                if confidence > 0.5:
                    #  scale the bounding box coordinates back relative to
                    #  the size of the image, keeping in mind that YOLO
                    #  actually returns the center (x, y)-coordinates of
                    #  the bounding box followed by the boxes' width and
                    #  height
                    box = detection[0:4] * np.array([width, height, width, height])
                    (centerX, centerY, width, height) = box.astype("int")

                    #  use the center (x, y)-coordinates to derive the top
                    #  and and left corner of the bounding boxnet, classes, output_layers = load_model()

                    # draw the bounding box of the object on the image
                    image = cv2.rectangle(image, (centerX, centerY), (centerX + int(width), centerY + int(height)), (0, 0, 255), 2)
                    # label the rectangle with the class name and the confidence
                    image = cv2.putText(image, classes[class_id] + " " + str(round(confidence, 2)), (centerX, centerY - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    

# # this function will merge all 16 images from the 4x4 into one image
# def merge_images(map4x4):
#     all_images = display_map(map4x4)
#     #  merge all the images into one image
#     img_merge = np.concatenate((all_images[0],all_images[1],all_images[2],all_images[3]), axis=1)
#     img_merge = np.concatenate((img_merge,all_images[4],all_images[5],all_images[6],all_images[7]), axis=1)
#     img_merge = np.concatenate((img_merge,all_images[8],all_images[9],all_images[10],all_images[11]), axis=1)
#     img_merge = np.concatenate((img_merge,all_images[12],all_images[13],all_images[14],all_images[15]), axis=1)
#     cv2.imshow('Merged Map',img_merge)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# display the 4x4 set of images map with detections
def display_map(map):
    all_images =[]
    for i in range(len(map)):
        for j in range(len(map[i])):
            
            #  read the image from the file
            image = cv2.imread(map[i][j])
            # cv2.imshow('Map',image)
            # cv2.waitKey(1)
            
            
            all_images.append(image)
            
    # # render all the images using matplotlib
    # plt.figure(figsize=(20,20))
    # for i in range(len(all_images)):
        
    #     plt.subplot(4,4,i+1)
    #     plt.imshow(cv2.cvtColor(all_images[i], cv2.COLOR_BGR2RGB))
    #     plt.xticks([])
    #     plt.yticks([])
    #     plt.tight_layout()
    # plt.show()
    
    # cv2.destroyAllWindows()
    return all_images
            
            
def create_map():
    map = [['imgs/sec1.jpg', 'imgs/sec2.jpg', 'imgs/sec3.jpg', 'imgs/sec4.jpg'], ['imgs/sec5.jpg', 'imgs/sec6.jpg', 'imgs/sec7.jpg', 'imgs/sec8.jpg'], ['imgs/sec9.jpg', 'imgs/sec10.jpg', 'imgs/sec11.jpg', 'imgs/sec12.jpg'], ['imgs/sec13.jpg', 'imgs/sec14.jpg', 'imgs/sec15.jpg', 'imgs/sec16.jpg']]
    map[np.random.randint(0,4)][np.random.randint(0,4)] = 'imgs/AlanStringer_Hiker.jpg'
    print('Map Loaded')
    return map

map_4x4 = create_map()

display_map(map_4x4)