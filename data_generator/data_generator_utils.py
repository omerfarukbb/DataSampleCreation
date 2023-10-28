import random
import cv2
import numpy as np

from config import *

def read_image(imagePath):
    image = cv2.imread(imagePath)
    return image

def auto_canny(image, sigma=0.33): 
    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    kernel = np.ones((3, 3), np.uint8)
    return cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

def rotate_image(mat, angle):
    height, width = mat.shape[:2]
    image_center = (width/2, height/2) 
    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)
    abs_cos = abs(rotation_mat[0,0]) 
    abs_sin = abs(rotation_mat[0,1])
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]
    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h), borderValue=(255,255,255))
    return rotated_mat

def resizeImage(image, size): 
    if image.shape[0] > size[0] and image.shape[1] > size[1]: 
        return image
    elif image.shape[0] > size[0]:
        size[0] = image.shape[0]
    elif image.shape[1] > size[1]: 
        size[1] = image.shape[1]
    blank_image = np.zeros(size, np.uint8)
    blank_image[:,:] = (255, 255, 255)
    resized = blank_image.copy()
    startRow = size[0]//2 - image.shape[0]//2
    startCol = size[1]//2 - image.shape[1]//2
    resized[startRow: startRow + image.shape[0], startCol: startCol + image.shape[1]] = image
    return resized

def get_random_start_position(bg_shape, fg_shape): 
    return [random.randint(0, bg_shape[0] - fg_shape[0]), random.randint(0, bg_shape[1] - fg_shape[1])]

def get_image_contours(image): 
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_canny = auto_canny(image_gray)
    contours, _ = cv2.findContours(image_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def blur_image_from_mask(img, mask):
    blurred_img = cv2.GaussianBlur(img, (9, 9), 0)
    edge_contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    edge_mask = np.zeros(img.shape, np.uint8)
    cv2.drawContours(edge_mask, edge_contours, -1, (255,255,255), 3)
    img = np.where(edge_mask==np.array([255, 255, 255]), blurred_img, img)
    return img


def merge_image(background, foreground, black_foreground, startPos):
    if startPos == "center": 
        startPos = [background.shape[0]//2 - foreground.shape[0]//2, background.shape[1]//2 - foreground.shape[1]//2]
    startRow = startPos[0]; startCol = startPos[1]
    rows, cols, channels = foreground.shape
    roi = background[startRow: startRow + rows, startCol: startCol + cols]
    gray = cv2.cvtColor(black_foreground, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    mask_inv = cv2.bitwise_not(mask)
    foreground = cv2.GaussianBlur(foreground, (5, 5), 0)
    bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    fg = cv2.bitwise_and(foreground, foreground, mask=mask)
    dst = cv2.add(bg, fg)
    # blur dst image from merge mask: 
    dst = blur_image_from_mask(dst, mask)

    background[startRow: startRow + rows, startCol: startCol + cols] = dst
    return background

def change_image_color(image, color):
    changed = image.copy() 
    contours = get_image_contours(changed)
    contours = sorted(contours, key=cv2.contourArea)
    if len(contours) > 2: 
        cv2.fillPoly(changed, pts =[contours[-1], contours[0]], color=color)
    else: 
        cv2.fillPoly(changed, pts =[contours[-1]], color=color)
    return changed

def generate_random_number_within_range(lower_bound, upper_bound):
    mu = (lower_bound + upper_bound) / 2
    sigma = (upper_bound - lower_bound)
    while True:
        random_number = np.random.normal(mu, sigma)
        if lower_bound <= random_number <= upper_bound:
            return random_number


def get_noised_color(color, with_hsv=False):
    if not with_hsv:
        noised_color = (
            color[0] + np.random.randint(-COLOR_NOISE, COLOR_NOISE),
            color[1] + np.random.randint(-COLOR_NOISE, COLOR_NOISE),
            color[2] + np.random.randint(-COLOR_NOISE, COLOR_NOISE)
        )
        return noised_color

    upper, lower = color
    h = generate_random_number_within_range(lower[0], upper[0]) % 180
    s = np.random.randint(lower[1], upper[1]+1)
    v = np.random.randint(lower[2], upper[2]+1)
    noised_color = (int(h), int(s), int(v))
    
    return noised_color

def tile_image(image, tile_shape): 
    img_w, img_h = image.shape[:2]
    tile_w, tile_h = tile_shape[:2]
    tiles = [image[x : x + tile_w, y : y + tile_h] 
        for x in range(0, img_w, tile_w) for y in range(0, img_h, tile_h)]
    return tiles

if __name__ == "__main__": 
    for background in BACKGROUNDS: 
        bg = read_image(f"{SCRIPT_DIR}/background/{background}")
        file_name = background.split(".")[0]
        bg_tiles = tile_image(bg, (BG_WIDTH, BG_HEIGHT))
        for ind, bg_tile in enumerate(bg_tiles): 
            if bg_tile.shape[0] == BG_WIDTH and bg_tile.shape[1] == BG_HEIGHT:
                cv2.imwrite(f"{SCRIPT_DIR}/background/{file_name}-{ind}.jpg", bg_tile)