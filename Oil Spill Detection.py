import cv2
import numpy as np

def resize_image(image, max_width, max_height):
    height, width = image.shape[:2]
    aspect_ratio = width / height
    if width > max_width or height > max_height:
        if aspect_ratio > 1:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
        resized_image = cv2.resize(image, (new_width, new_height))
    else:
        resized_image = image
    return resized_image

# Load the image
image = cv2.imread('SAR 7.jpg')

# Define a broad color range from black to dark gray (in BGR format)
lower_bound = np.array([0, 0, 0], dtype="uint8")
upper_bound = np.array([40, 40, 40], dtype="uint8")

# Create a mask for the specified color range
mask = cv2.inRange(image, lower_bound, upper_bound)

# Detect edges on the masked image
edges = cv2.Canny(mask, 100, 200)

# Check if edges are detected
if np.count_nonzero(edges) > 0:
    detection_text = "Oil Spill Detected"
else:
    detection_text = "No Oil Spill Detected"

# Create a black background image of the same size as the original image
black_background = np.zeros_like(image)

# Draw the edges on the black background (white lines)
edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
black_edges = cv2.bitwise_or(black_background, edges_colored)

# Get screen size (using a common screen resolution for demonstration)
screen_width, screen_height = 1920, 1080  # Adjust this to match your screen resolution

# Calculate the maximum allowed width and height for each image
max_width = screen_width // 2
max_height = screen_height

# Resize both images to fit within the screen
resized_original = resize_image(image, max_width, max_height)
resized_edges = resize_image(black_edges, max_width, max_height)

# Combine original and result images side by side
combined_image = np.hstack((resized_original, resized_edges))

# Add a black rectangle at the top for the text background
text_height = 50
combined_image_with_text = np.vstack((np.zeros((text_height, combined_image.shape[1], 3), dtype=np.uint8), combined_image))

# Add detection text at the top of the combined image
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1  # Subheading size
font_thickness = 2
text_size = cv2.getTextSize(detection_text, font, font_scale, font_thickness)[0]

# Calculate text position to be centered at the top
text_x = (combined_image_with_text.shape[1] - text_size[0]) // 2
text_y = text_size[1] + 10  # Slightly below the top edge

# Add text to the combined image
cv2.putText(combined_image_with_text, detection_text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)

# Display the result in full screen
cv2.namedWindow('Original and Edges on Black Background', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Original and Edges on Black Background', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow('Original and Edges on Black Background', combined_image_with_text)
cv2.waitKey(0)
cv2.destroyAllWindows()
