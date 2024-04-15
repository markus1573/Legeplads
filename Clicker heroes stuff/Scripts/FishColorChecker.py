import os
import cv2
import numpy as np
os.chdir("/Users/markus/Documents/Clicker heroes stuff")

def calculate_distance(color1, color2):
    # Calculate Euclidean distance between two colors
    return np.linalg.norm(color1 - color2)

def find_common_colors(arrays, threshold):
    # Colors that are common across all arrays
    common_colors = []
    # Iterate over each color in the first array
    for color in arrays[0]:
        is_common = True  # Flag to track if color is common across arrays
        for other_array in arrays[1:]:
            found_similar_color = False
            # Check if the color is within the threshold in any other array
            for other_color in other_array:
                distance = calculate_distance(color, other_color)
                if distance <= threshold:
                    found_similar_color = True
                    break
            if not found_similar_color:
                is_common = False
                break
        if is_common:
            common_colors.append(color)
    return np.array(common_colors)


# List of arrays
arrays = []
for i in range(1,7):
    im = cv2.imread("Photos/Fishtail"+str(i)+".png")
    im = im[im[:,:,2]>200]
    im.sort(axis=0)
    im_list = np.array(im.tolist())
    arrays.append(im_list)

# Assuming threshold_value is your specified threshold
threshold_value = 6  # Adjust this threshold value based on your requirements

# Find common colors within the specified threshold
common_colors = find_common_colors(arrays, threshold_value)
unique_common_colors = np.unique(common_colors, axis=0)

print("Number of unique common colors found within the specified threshold:")
print(len(unique_common_colors))

# Calculate the median for each color channel (R, G, B) for the common colors
if len(common_colors) > 0:
    median_color = np.median(common_colors, axis=0)
    print("Median color values for common colors:")
    print(median_color)
else:
    print("No common colors found within the specified threshold.")
