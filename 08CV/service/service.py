import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import tensorflow as tf
import cv2 as cv
import numpy as np
import time
import math

# gpu = tf.config.experimental.list_physical_devices(device_type='GPU')
# assert len(gpu) == 1
# tf.config.experimental.set_memory_growth(gpu[0], True)


def generate_face_grid(frameW, frameH, gridW, gridH, labelFaceX, labelFaceY, labelFaceW, labelFaceH):
    scaleX = gridW / frameW
    scaleY = gridH / frameH
    grid = np.zeros((gridH, gridW))

    # Use one-based image coordinates.
    xLo = round(labelFaceX * scaleX)
    yLo = round(labelFaceY * scaleY)
    w = round(labelFaceW * scaleX)
    h = round(labelFaceH * scaleY)

    xHi = xLo + w
    yHi = yLo + h

    # Clamp the values in the range.
    xLo = int(min(gridW, max(0, xLo)))
    xHi = int(min(gridW, max(0, xHi)))
    yLo = int(min(gridH, max(0, yLo)))
    yHi = int(min(gridH, max(0, yHi)))

    faceLocation = np.ones((yHi - yLo, xHi - xLo))
    grid[yLo:yHi, xLo:xHi] = faceLocation

    # Flatten the grid.
    grid = np.transpose(grid)
    labelFaceGrid = grid.flatten()

    return labelFaceGrid


gaze_model_path = "./saved_model_itracker_basic"
emo_model_path = './saved_model_binary_rm_surprise'
emo_model = tf.keras.models.load_model(emo_model_path)
gaze_model = tf.keras.models.load_model(gaze_model_path)
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')
emo_list = []


def gaze_emo(img_path, mirror_label=True):
    # t = time.time()  # s
    img = cv.imread(img_path)
    [h, w, c] = img.shape
    ce = math.ceil(w / 2.)
    bandwidth = h * 0.5
    img = img[:, math.floor(ce - bandwidth):math.floor(ce + bandwidth), :]
    grey = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(grey, 1.3, 5)
    if len(faces) > 0:
        distance_from_center = np.array((faces[:, 0] - 320) ** 2 + (faces[:, 1] - 240) ** 2)
        cf_idx = np.argmin(distance_from_center)
        (x, y, w, h) = faces[cf_idx, :]
        faceinfo = [x, y, w, h]
        eyeinfo = []
        cv.rectangle(grey, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_grey = grey[y:np.int(y + h * 0.6), x:x + w]
        max_eye_size = np.int(w / 4.)
        min_eye_size = np.int(w / 20.)
        eyes = eye_cascade.detectMultiScale(roi_grey, 2, 5, minSize=(min_eye_size, min_eye_size),
                                            maxSize=(max_eye_size, max_eye_size))
        for (ex, ey, ew, eh) in eyes:
            eyeinfo.append([ex, ey, ew, eh])
            cv.rectangle(roi_grey, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)

        if len(eyes) == 2:
            # plty = np.ones((900, 1200, 3), dtype='uint8') * 255
            face_mask = generate_face_grid(img.shape[1], img.shape[0], 25, 25, faceinfo[0], faceinfo[1], faceinfo[2],
                                           faceinfo[3])
            if eyeinfo[0][0] > eyeinfo[1][0]:
                l_idx, r_idx = (0, 1)
            else:
                l_idx, r_idx = (1, 0)
            half_width = math.ceil(faceinfo[3] / 2.0)
            l_width = eyeinfo[l_idx][0] + eyeinfo[l_idx][2] - half_width
            r_width = half_width - eyeinfo[r_idx][0]
            side_width = max(l_width, r_width)
            l_height_pad = (side_width - eyeinfo[l_idx][3]) / 2.0
            r_height_pad = (side_width - eyeinfo[r_idx][3]) / 2.0
            eye_left = img[faceinfo[1] + eyeinfo[l_idx][1] - math.floor(l_height_pad):faceinfo[1] + eyeinfo[l_idx][1] +
                                                                                      eyeinfo[l_idx][3] + math.ceil(
                l_height_pad),
                       faceinfo[0] + half_width:faceinfo[0] + half_width + side_width]
            eye_right = img[faceinfo[1] + eyeinfo[r_idx][1] - math.floor(r_height_pad):faceinfo[1] + eyeinfo[r_idx][1] +
                                                                                       eyeinfo[r_idx][3] + math.ceil(
                r_height_pad),
                        faceinfo[0] + half_width - side_width:faceinfo[0] + half_width]
            face = img[faceinfo[1]:faceinfo[1] + faceinfo[3], faceinfo[0]:faceinfo[0] + faceinfo[2]]
            eye_left = cv.resize(eye_left, (64, 64))
            eye_right = cv.resize(eye_right, (64, 64))
            face = cv.resize(face, (64, 64))

            eye_left = eye_left[:, :, [2, 1, 0]].astype('float32') / 255. - 0.5
            eye_right = eye_right[:, :, [2, 1, 0]].astype('float32') / 255. - 0.5
            emo_face = face[:, :, [2, 1, 0]].astype('float32')
            face = emo_face / 255. - 0.5
            face_mask = np.reshape(face_mask, (face_mask.shape[0], -1)).astype('float32')
            if mirror_label:
                data1 = np.reshape(eye_right, (-1, 64, 64, 3))
                data2 = np.reshape(eye_left, (-1, 64, 64, 3))
            else:
                data1 = np.reshape(eye_left, (-1, 64, 64, 3))
                data2 = np.reshape(eye_right, (-1, 64, 64, 3))
            data3 = np.reshape(face, (-1, 64, 64, 3))
            data4 = np.reshape(face_mask, (-1, 625))
            emo_input = np.reshape(emo_face, (-1, 64, 64, 3))

            gaze_pred = gaze_model.predict([data1, data2, data3, data4])
            emo_pred = emo_model.predict(emo_input)
            print(gaze_pred[0])
            print(emo_pred[0][0, 0])
            return gaze_pred[0], emo_pred[0][0, 0], grey


gaze_emo("img.png", mirror_label=True)
