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
        output_path='temp',
        disable_logging=True,
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
        line_pos = rng.randint(0, image_array.shape[1])
        background[:, line_pos, :] = background_color

    # convert noise overlay to an image
    noise_overlay = Image.fromarray(background.astype(np.uint8))

    # add the noise layer with transparency on top of the receipt image
    noisy_image = Image.alpha_composite(im, noise_overlay)

    # make the colors more natural by scaling them to be between 75-200
    noisy_image = Image.fromarray((np.array(noisy_image, dtype=np.float32) / 255.0 * 165.0 + 35.0).astype(np.uint8))

    img = cv2.cvtColor(np.array(noisy_image), cv2.COLOR_RGB2BGR)

    background = cv2.imread('images/background.jpg', cv2.IMREAD_COLOR)

    height, width = img.shape[:2]
    background_height, background_width = background.shape[:2]

    x_offset = (background_width - width) // 2
    y_offset = (background_height - height) // 2

    background[y_offset:y_offset+height, x_offset:x_offset+width] = img

    dsize = (1736, 2312)

    zoom = rng.randint(-10, 11)
    rotation = rng.randint(-14, 15)
    forward_tilt = rng.randint(-8, 9)
    sideways_tilt = rng.randint(-8, 9)

    pos_from, pos_to = get_to_transformation(
        background_width,
        background_height,
        dsize,
        zoom=zoom,
        rotation=rotation,
        forward_tilt=forward_tilt,
        sideways_tilt=sideways_tilt,
    )

    matrix = cv2.getPerspectiveTransform(pos_from, pos_to)
    result = cv2.warpPerspective(background, matrix, dsize, borderMode=cv2.BORDER_TRANSPARENT)

    h, w = result.shape[:2]
    sigma = rng.randint(0, 30)
    gauss = np.random.normal(0, sigma, (h, w, 3)).astype(np.int16)
    noisy = cv2.add(result.astype(np.int16), gauss)
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)

    return noisy


def has_off_screen_corner(corners, dsize):
    for corner in corners:
        if corner[0] < 0 or corner[0] > dsize[0]:
            return True
        if corner[1] < 0 or corner[1] > dsize[1]:
            return True
    return False


def get_to_transformation(width, height, dsize, zoom=0, rotation=0, forward_tilt=0, sideways_tilt=0):
    cx = width // 2
    cy = height // 2

    # change center to center of receipt
    object_points = np.array([
        [-cx, -cy, 0],
        [cx, -cy, 0],
        [cx, cy, 0],
        [-cx, cy, 0]
    ], dtype=np.float32)

    # camera matrix
    focal_length = 1000
    camera_matrix = np.array([
        [focal_length, 0, 0],
        [0, focal_length, 0],
        [0, 0, 1]
    ], dtype=np.float64)

    # define transformation variables
    tilt_deg = forward_tilt
    yaw_deg = sideways_tilt
    roll_deg = rotation
    distance = 1000 * (1 - zoom / 40)

    # convert degrees to radians
    tilt = np.deg2rad(tilt_deg)
    yaw = np.deg2rad(yaw_deg)
    roll = np.deg2rad(roll_deg)

    # create rotation matrix
    rotation_x = cv2.Rodrigues(np.array([tilt, 0, 0]))[0]
    rotation_y = cv2.Rodrigues(np.array([0, yaw, 0]))[0]
    rotation_z = cv2.Rodrigues(np.array([0, 0, roll]))[0]
    rotation_matrix, _ = cv2.Rodrigues(rotation_z @ rotation_y @ rotation_x)

    tvec = np.array([[0], [0], [distance]], dtype=np.float64)
    dist_coeffs = np.zeros((4, 1))

    # project points on the 2D plane
    dst_pts, _ = cv2.projectPoints(object_points, rotation_matrix, tvec, camera_matrix, dist_coeffs)
    dst_pts = dst_pts.reshape(-1, 2).astype(np.float32)

    # shift projected points to center of canvas
    canvas_center = np.array([dsize[0] / 2, dsize[1] / 2], dtype=np.float32)
    dst_pts += canvas_center

    # shift points with a random offset
    offset = np.array([rng.randint(0, 150), rng.randint(0, 150)], dtype=np.float32)
    dst_pts += offset

    # source of the image points
    src_pts = np.array([
        [0, 0],
        [width, 0],
        [width, height],
        [0, height]
    ], dtype=np.float32)

    return src_pts, dst_pts

