import random
import cv2
import imutils
import numpy as np

from rotate_image import rotate_along_axis
from config import *
from data_generator_utils import *

def augment_image(image, orientation, phi, theta, width): 
    image = rotate_image(image, orientation)
    image = rotate_along_axis(image, theta, phi)
    image = imutils.resize(image, width=width)
    return image

def create_odlc(shape_ind, alpha_ind, shape_color_ind, alpha_color_ind, with_hsv=False):
    shape_path = os.path.join(SCRIPT_DIR, 'data_generator', 'shape', f'{SHAPES[shape_ind]}.png')
    alpha_path = os.path.join(SCRIPT_DIR, 'data_generator', 'alphanumeric', f'{ALPHANUMERICS[alpha_ind]}.png')

    black_shape = read_image(shape_path)
    black_alpha = read_image(alpha_path)

    if with_hsv:
        shape_color = get_noised_color(COLORS_HSV[shape_color_ind], with_hsv)
        alpha_color = get_noised_color(COLORS_HSV[alpha_color_ind], with_hsv)
    else:
        shape_color = get_noised_color(COLORS[shape_color_ind], with_hsv)
        alpha_color = get_noised_color(COLORS[alpha_color_ind], with_hsv)
    shape = change_image_color(black_shape, shape_color)
    alpha = change_image_color(black_alpha, alpha_color)

    odlc = merge_image(shape, alpha, black_alpha, startPos="center")

    orientation = random.randint(0, 360)
    theta = random.randint(*ODLC_ROTATE_RANGE)
    phi = random.randint(*ODLC_ROTATE_RANGE)
    width = random.randint(*ODLC_WIDTH_RANGE)

    odlc = augment_image(odlc, orientation, theta, phi, width)
    # We will need black odlc later
    black_odlc = augment_image(black_shape, orientation, theta, phi, width)

    return odlc, black_odlc

def create_random_odlc_props(): 
    shape = random.randint(0, len(SHAPES) - 1)
    alpha = random.randint(0, len(ALPHANUMERICS) - 1)
    shapeColor = random.randint(0, len(COLORS) - 1)
    alphaColor = random.randint(0, len(COLORS) - 1)
    while alphaColor == shapeColor: 
        alphaColor = random.randint(0, len(COLORS) - 1)
    return shape, alpha, shapeColor, alphaColor

def get_odlc_rect(odlc, start_position): 
    white_bg = 255 * np.ones((BG_HEIGHT, BG_WIDTH, 3), dtype=np.uint8)
    odlc_on_white = merge_image(white_bg, odlc, odlc, start_position)
    odlc_contour = get_image_contours(odlc_on_white)[0]
    odlc_rect = cv2.boundingRect(odlc_contour)
    return odlc_rect

def get_random_odlc_count(): 
    odlc_count = np.random.choice(list(ODLC_COUNT_PROBS.keys()), size=1, p=list(ODLC_COUNT_PROBS.values()))[0]
    return odlc_count

def create_data(data_id, with_hsv=False): 
    background = read_image(f"{SCRIPT_DIR}/background/{random.choice(BACKGROUNDS)}")
    if background.shape[0] != BG_HEIGHT or background.shape[1] != BG_WIDTH: 
        background = cv2.resize(background, (BG_WIDTH, BG_HEIGHT))

    odlc_count = get_random_odlc_count()
    # print("odlc count: ", odlc_count)
    generated_data = background
    generated_label = ""
    for i in range(odlc_count): 
        shape, alpha, shape_color, alpha_color = create_random_odlc_props()
        odlc, black_odlc = create_odlc(shape, alpha, shape_color, alpha_color, with_hsv)
        start_position = get_random_start_position(background.shape, odlc.shape)
        odlc_rect = get_odlc_rect(black_odlc, start_position)
        generated_data = merge_image(generated_data, odlc, black_odlc, start_position)
        x, y, w, h = odlc_rect
        x = x + w//2; y = y + h//2
        if SAVE_SHAPE_LABEL:
            generated_label += f"{shape} {x / BG_WIDTH} {y / BG_HEIGHT} {w / BG_WIDTH} {h / BG_HEIGHT}\n"
        alpha_w = odlc.shape[1] // 4; alpha_h = odlc.shape[0] // 4
        if SAVE_ALPHA_LABEL: 
            generated_label += f"{alpha} {x / BG_WIDTH} {y / BG_HEIGHT} {alpha_w / BG_WIDTH} {alpha_h / BG_HEIGHT}\n"
        # cv2.rectangle(generated_data, (x-w//2, y-h//2), (x+w//2, y+h//2), (0, 255, 0))
        # cv2.rectangle(generated_data, (x-alpha_w//2, y-alpha_h//2), (x+alpha_w//2, y+alpha_h//2), (0, 255, 0))
    file_name = f"{data_id}"
    cv2.imwrite(f"{SCRIPT_DIR}\\images\\{file_name}.png", generated_data)
    label_file = open(f"{SCRIPT_DIR}\\labels\\{file_name}.txt", "w")
    label_file.write(generated_label)
    label_file.close()
    # cv2.imshow("generated data", generated_data)
    # cv2.waitKey(0)

if __name__ == "__main__": 
    from tqdm import tqdm
    for data_id in tqdm(range(100)): 
        create_data(data_id, True)