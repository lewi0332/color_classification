#import time
import argparse
import json
from collections import Counter

import cv2
import numpy as np
from sklearn.cluster import KMeans, MiniBatchKMeans
import urllib

# Code adjusted from Adam Spannbauer: https://adamspannbauer.github.io/2018/03/02/app-icon-dominant-colors/

# >>>'python hsv_classify_from_url.py -i <image path> 

#start = time.time()
def get_dominant_color(image, k, image_processing_size=(50, 50)):
    """
    takes an image as input
    returns the dominant 3 colors of the image as three lists

    dominant color is found by running k means on the 
    pixels & returning the centroid of the 6 clusters

    processing time is sped up by working with a smaller image; 
    images is forced to be 25 x 25 below

    """

    # reshape the image to be a list of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    # cluster and assign labels to the pixels
    clt = MiniBatchKMeans(n_clusters = k).fit(image)
    #clt = KMeans(n_clusters = k).fit(image) <-- slower method with more steps in finding true cluster centers
    labels = clt.predict(image)

    # count labels to find most popular
    label_counts = Counter(labels)

    # subset out most popular centroid
    dominant_color_1 = clt.cluster_centers_[label_counts.most_common(1)[0][0]]
    dominant_color_2 = clt.cluster_centers_[label_counts.most_common(2)[1][0]]
    dominant_color_3 = clt.cluster_centers_[label_counts.most_common(3)[2][0]]
    dominant_color_4 = clt.cluster_centers_[label_counts.most_common(4)[3][0]]
    dominant_color_5 = clt.cluster_centers_[label_counts.most_common(5)[4][0]]
    dominant_color_6 = clt.cluster_centers_[label_counts.most_common(6)[5][0]]

    return list(dominant_color_1), list(dominant_color_2), list(dominant_color_3), list(dominant_color_4), list(dominant_color_5), list(dominant_color_6)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imagePath", type=str, required=True,
                help="Path to image to find dominant color of")
ap.add_argument("-k", "--clusters", default=3, type=int,
                help="Number of clusters to use inhsv    kmeans when finding dominant color")
args = vars(ap.parse_args())

# read in image of interest
url_response = urllib.request.urlopen(args['imagePath'])
img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
bgr_image = cv2.imdecode(img_array, -1)

# convert to HSV; this is a better representation of how we see color
hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

# extract 3 most dominant colors
# (aka the centroid of the most popular k means cluster)
# K-means set to 35 clusters. Given the complexity of our images.
# Change K-means below and the image processing size above to adjust accuracy
dom_color_1, dom_color_2, dom_color_3, dom_color_4, dom_color_5, dom_color_6 = get_dominant_color(hsv_image, k=6)

# create a square showing dominant color of equal size to input image for testing
dom_color_1_hsv = np.full(bgr_image.shape, dom_color_1, dtype='uint8')
# convert to bgr color space for display in testing
dom_color_1_rgb = cv2.cvtColor(dom_color_1_hsv, cv2.COLOR_HSV2RGB)

dom_color_2_hsv = np.full(bgr_image.shape, dom_color_2, dtype='uint8')
dom_color_2_rgb = cv2.cvtColor(dom_color_2_hsv, cv2.COLOR_HSV2RGB)

dom_color_3_hsv = np.full(bgr_image.shape, dom_color_3, dtype='uint8')
dom_color_3_rgb = cv2.cvtColor(dom_color_3_hsv, cv2.COLOR_HSV2RGB)

dom_color_4_hsv = np.full(bgr_image.shape, dom_color_4, dtype='uint8')
dom_color_4_rgb = cv2.cvtColor(dom_color_4_hsv, cv2.COLOR_HSV2RGB)

dom_color_5_hsv = np.full(bgr_image.shape, dom_color_5, dtype='uint8')
dom_color_5_rgb = cv2.cvtColor(dom_color_5_hsv, cv2.COLOR_HSV2RGB)

dom_color_6_hsv = np.full(bgr_image.shape, dom_color_6, dtype='uint8')
dom_color_6_rgb = cv2.cvtColor(dom_color_6_hsv, cv2.COLOR_HSV2RGB)

#concat input image and dom color square side by side for display
#output_image = np.hstack((bgr_image[:,:,::-1], dom_color_1_rgb, dom_color_2_rgb, dom_color_3_rgb))

hex1 = '#%02x%02x%02x' % (
    dom_color_1_rgb[0][0][0], dom_color_1_rgb[0][0][1], dom_color_1_rgb[0][0][2])
hex2 = '#%02x%02x%02x' % (
    dom_color_2_rgb[0][0][0], dom_color_2_rgb[0][0][1], dom_color_2_rgb[0][0][2])
hex3 = '#%02x%02x%02x' % (
    dom_color_3_rgb[0][0][0], dom_color_3_rgb[0][0][1], dom_color_3_rgb[0][0][2])
hex4 = '#%02x%02x%02x' % (
    dom_color_4_rgb[0][0][0], dom_color_4_rgb[0][0][1], dom_color_4_rgb[0][0][2])
hex5 = '#%02x%02x%02x' % (
    dom_color_5_rgb[0][0][0], dom_color_5_rgb[0][0][1], dom_color_5_rgb[0][0][2])
hex6 = '#%02x%02x%02x' % (
    dom_color_6_rgb[0][0][0], dom_color_6_rgb[0][0][1], dom_color_6_rgb[0][0][2])

# return json string
color_dict = {'first_color': {'red': int(dom_color_1_rgb[0][0][0]), 'green': int(dom_color_1_rgb[0][0][1]), 'blue': int(dom_color_1_rgb[0][0][2]),
                              'hex': hex1}, 'second_color': {'red': int(dom_color_2_rgb[0][0][0]), 'green': int(dom_color_2_rgb[0][0][1]), 'blue: ': int(dom_color_2_rgb[0][0][2]), 'hex': hex2},
              'third_color': {'red': int(dom_color_3_rgb[0][0][0]), 'green': int(dom_color_3_rgb[0][0][1]), 'blue': int(dom_color_3_rgb[0][0][2]),
                              'hex': hex3}, 'fourth_color': {'red': int(dom_color_4_rgb[0][0][0]), 'green': int(dom_color_4_rgb[0][0][1]), 'blue': int(dom_color_4_rgb[0][0][2]),
                              'hex': hex4}, 'fifth_color': {'red': int(dom_color_5_rgb[0][0][0]), 'green': int(dom_color_5_rgb[0][0][1]), 'blue': int(dom_color_5_rgb[0][0][2]),
                              'hex': hex5}, 'sixth_color': {'red': int(dom_color_6_rgb[0][0][0]), 'green': int(dom_color_6_rgb[0][0][1]), 'blue': int(dom_color_6_rgb[0][0][2]),
                              'hex': hex6}}

print(json.dumps(color_dict))
#print('time: {:.3f}s'.format(time.time()-start))
