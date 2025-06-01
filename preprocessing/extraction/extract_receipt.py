import cv2
import numpy as np

def extract_receipt(image):
    # Find edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    
    # Find contours
    closed = cv2.dilate(closed, None, iterations=2)
    closed = cv2.erode(closed, None, iterations=2)

    contours, _ = cv2.findContours(closed.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Thresholds
    min_contour_length = 600
    min_area_size = 75
    min_diameter = 400

    filtered_contours = []

    for cnt in contours:
        length = cv2.arcLength(cnt, True)
        area = cv2.contourArea(cnt)

        # Verify arclength of contour
        if length < min_contour_length or area <= min_area_size:
            continue

        # Verify diameter of contour
        diameter = max_pairwise_distance(cnt)
        if diameter <= min_diameter:
            continue

        # Passed all filters, keep it
        filtered_contours.append(cnt)

    # Only keep the 25 most promising contours
    filtered_contours = filtered_contours[:25]

    # Create an outer hull of the contours and get corners
    concatenated_contour = np.vstack(filtered_contours)
    hull = cv2.convexHull(concatenated_contour)

    peri = cv2.arcLength(hull, True)
    approx = cv2.approxPolyDP(hull, 0.015 * peri, True)

    # Compute approximate output size
    corners = order_points(approx.reshape((4, 2)))

    (tl, tr, br, bl) = corners

    width_a = np.linalg.norm(br - bl)
    width_b = np.linalg.norm(tr - tl)
    max_width = max(int(width_a), int(width_b))

    height_a = np.linalg.norm(tr - br)
    height_b = np.linalg.norm(tl - bl)
    max_height = max(int(height_a), int(height_b))

    output_width = 800

    ratio = max_width / float(output_width)
    output_height = int(max_height / ratio)

    # Warp the image to only keep the receipt
    src_pts = corners
    dst_pts = np.array([
        [0, 0],
        [output_width, 0],
        [output_width, output_height],
        [0, output_height]
    ], dtype=np.float32)

    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    result = cv2.warpPerspective(image.copy(), matrix, (output_width, output_height), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))

    # Improve text quality and contrast on the result
    result_gray = cv2.cvtColor(result.copy(), cv2.COLOR_BGR2GRAY)

    filtered = local_contrast_filter(result_gray)
    filtered[filtered > 50] = 255

    return filtered


def max_pairwise_distance(contour):
    hull = cv2.convexHull(contour, returnPoints=True)
    n = len(hull)
    if n < 2:
        return 0.0

    max_dist = 0
    j = 1
    for i in range(n):
        while True:
            d1 = np.linalg.norm(hull[i][0] - hull[j % n][0])
            d2 = np.linalg.norm(hull[i][0] - hull[(j + 1) % n][0])
            if d2 > d1:
                j += 1
            else:
                break
        max_dist = max(max_dist, np.linalg.norm(hull[i][0] - hull[j % n][0]))
    return max_dist


def order_points(pts):
    rect = np.zeros((4, 2), dtype=np.float32)

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # top-left
    rect[2] = pts[np.argmax(s)]  # bottom-right

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # top-right
    rect[3] = pts[np.argmax(diff)]  # bottom-left

    return rect


def local_contrast_filter(img):
    img = img.astype(np.float32)

    local_mean = cv2.blur(img, (15, 15))
    diff = img - local_mean

    adjusted = img + diff * 5

    adjusted_clipped = np.clip(adjusted, 0, 255)

    return adjusted_clipped.astype(np.uint8)
