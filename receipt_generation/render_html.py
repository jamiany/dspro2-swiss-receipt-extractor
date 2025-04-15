from uuid import uuid4

from PIL import Image
from html2image import Html2Image
import numpy as np
import numpy.random as rng
import cv2


def render_html(name):
    hti = Html2Image(
        custom_flags=[
            '--default-background-color=00000000',
            '--hide-scrollbars',
            '--headless',
        ],
        output_path='temp'
    )
    hti.screenshot(html_file=f'temp/{name}.html', css_file='templates/styles_coop.css', save_as=f'{name}.png')

    im = Image.open(f'temp/{name}.png')
    im = im.crop(im.getbbox())

    image_array = np.array(im, dtype=np.float32)

    background_color = np.array([255, 255, 255, 255])

    # create a background canvas to generate a noise from
    background = np.ones(image_array.shape)
    background[:, :] = background_color

    # generate a noise with floating point values representing the translucency of the background color
    noise_dim = (image_array.shape[0], image_array.shape[1])
    noise = rng.normal(-5, 20, noise_dim)
    noise = np.round(np.clip(noise, 0, 50) / 50 * 255)

    # apply noise as opacity to the background to create a noise in the color of the background
    background[:, :, 3] = noise[:, :]

    # add printing error lines
    for _ in range(rng.randint(0, 6)):
        line_pos = rng.randint(0, image_array.shape[1] + 1)
        background[:, line_pos, :] = background_color

    # convert noise overlay to an image
    noise_overlay = Image.fromarray(background.astype(np.uint8))

    # add the noise layer with transparency on top of the receipt image
    noisy_image = Image.alpha_composite(im, noise_overlay)

    # make the colors more natural by scaling them to be between 75-200
    noisy_image = Image.fromarray((np.array(noisy_image, dtype=np.float32) / 255.0 * 165.0 + 35.0).astype(np.uint8))

    img = cv2.cvtColor(np.array(noisy_image), cv2.COLOR_RGB2BGR)

    background = cv2.imread('images/background.jpg', cv2.IMREAD_COLOR)

    background = cv2.resize(background, (2376, 1584))
    background = background[150:150 + 1100, 750:750 + 800]

    width = img.shape[1]
    height = img.shape[0]

    pos_from = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    pos_to = np.float32([[200, 50], [600, 50], [50, 1000], [750, 1000]])

    matrix = cv2.getPerspectiveTransform(pos_from, pos_to)
    result = cv2.warpPerspective(img, matrix, (800, 1100), background, borderMode=cv2.BORDER_TRANSPARENT)

    cv2.imwrite(f'temp/{name}.png', result)
