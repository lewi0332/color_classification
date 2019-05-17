from sklearn.cluster import KMeans
from collections import Counter
import cv2 #for resizing image
import numpy as np
import argparse
import json

def get_dominant_color(image, k=4, image_processing_size = (50, 50)):
    """
    takes an image as input
    returns the dominant 3 colors of the image as three lists
    
    dominant color is found by running k means on the 
    pixels & returning the centroid of the largest 3 clusters

    processing time is sped up by working with a smaller image; 
    this resizing can be done with the image_processing_size param 
    which takes a tuple of image dims as input

    get_dominant_color(my_image, k=4, image_processing_size = (25, 25))
    [56.2423442, 34.0834233, 70.1234123]
    """
    #resize image if new dims provided
	#image = cv2.imread(image)
    if image_processing_size is not None:
        image = cv2.resize(image, image_processing_size, 
                            interpolation = cv2.INTER_AREA)
    
    #reshape the image to be a list of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    #cluster and assign labels to the pixels 
    clt = KMeans(n_clusters = k)
    labels = clt.fit_predict(image)

    #count labels to find most popular
    label_counts = Counter(labels)

    #subset out most popular centroid
    dominant_color_1 = clt.cluster_centers_[label_counts.most_common(1)[0][0]]
    dominant_color_2 = clt.cluster_centers_[label_counts.most_common(2)[1][0]]
    dominant_color_3 = clt.cluster_centers_[label_counts.most_common(3)[2][0]]

    return list(dominant_color_1), list(dominant_color_2), list(dominant_color_3)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imagePath", required=True,
	help="Path to image to find dominant color of")
ap.add_argument("-k", "--clusters", default=3, type=int,
	help="Number of clusters to use in kmeans when finding dominant color")
args = vars(ap.parse_args())

#read in image of interest
bgr_image = cv2.imread(args['imagePath'])
#convert to HSV; this is a better representation of how we see color
hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
    
#extract 3 most dominant colors
# (aka the centroid of the most popular k means cluster)
dom_color_1, dom_color_2, dom_color_3 = get_dominant_color(hsv_image, k=35)
    
#create a square showing dominant color of equal size to input image
dom_color_1_hsv = np.full(bgr_image.shape, dom_color_1, dtype='uint8')
#convert to bgr color space for display
dom_color_1_rgb = cv2.cvtColor(dom_color_1_hsv, cv2.COLOR_HSV2RGB)
    
#create a square showing dominant color of equal size to input image
dom_color_2_hsv = np.full(bgr_image.shape, dom_color_2, dtype='uint8')
#convert to bgr color space for display
dom_color_2_rgb = cv2.cvtColor(dom_color_2_hsv, cv2.COLOR_HSV2RGB)
    
#create a square showing dominant color of equal size to input image
dom_color_3_hsv = np.full(bgr_image.shape, dom_color_3, dtype='uint8')
#convert to bgr color space for display
dom_color_3_rgb = cv2.cvtColor(dom_color_3_hsv, cv2.COLOR_HSV2RGB)
    
#concat input image and dom color square side by side for display
output_image = np.hstack((bgr_image[:,:,::-1], dom_color_1_rgb, dom_color_2_rgb, dom_color_3_rgb))

hex1 = '#%02x%02x%02x' % (dom_color_1_rgb[0][0][0], dom_color_1_rgb[0][0][1], dom_color_1_rgb[0][0][2])
hex2 = '#%02x%02x%02x' % (dom_color_2_rgb[0][0][0], dom_color_2_rgb[0][0][1], dom_color_2_rgb[0][0][2])
hex3 = '#%02x%02x%02x' % (dom_color_3_rgb[0][0][0], dom_color_3_rgb[0][0][1], dom_color_3_rgb[0][0][2])

#return json string
color_dict = {'first_color':{'red': int(dom_color_1_rgb[0][0][0]), 'green': int(dom_color_1_rgb[0][0][1]), 'blue': int(dom_color_1_rgb[0][0][2]), 
'hex': hex1}, 'second_color':{'red': int(dom_color_2_rgb[0][0][0]), 'green':int(dom_color_1_rgb[0][0][1]), 'blue: ': int(dom_color_2_rgb[0][0][2]), 'hex': hex2}, 
              'third_color':{'red': int(dom_color_3_rgb[0][0][0]), 'green': int(dom_color_1_rgb[0][0][1]), 'blue': int(dom_color_3_rgb[0][0][2]), 
'hex': hex3}}

print(json.dumps(color_dict))

