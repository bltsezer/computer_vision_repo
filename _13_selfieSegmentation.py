import cv2
import mediapipe as mp
import numpy as np


class Segmentatiion():
  global mp_selfie_segmentation
  mp_drawing = mp.solutions.drawing_utils
  mp_selfie_segmentation = mp.solutions.selfie_segmentation

  IMAGE_FILES = []
  BG_COLOR = (192, 192, 192) # gray
  MASK_COLOR = (255, 255, 255) # white

  with mp_selfie_segmentation.SelfieSegmentation(
    model_selection=0) as selfie_segmentation:
    
    for idx, file in enumerate(IMAGE_FILES):
      image = cv2.imread(file)
      image_height, image_width, _ = image.shape


      condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
      fg_image = np.zeros(image.shape, dtype=np.uint8)
      fg_image[:] = MASK_COLOR
      bg_image = np.zeros(image.shape, dtype=np.uint8)
      bg_image[:] = BG_COLOR
      output_image = np.where(condition, fg_image, bg_image)
      cv2.imwrite('/tmp/selfie_segmentation_output' + str(idx) + '.png', output_image)

  def __init__(self):
    # For webcam input:
    BG_COLOR = (192, 192, 192) # gray
    cap = cv2.VideoCapture(0)
    with mp_selfie_segmentation.SelfieSegmentation(
        model_selection=1) as selfie_segmentation:
      bg_image = None
      while cap.isOpened():
        success, image = cap.read()
        if not success:
          print("empty frame.")
          continue

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = selfie_segmentation.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        condition = np.stack( (results.segmentation_mask,) * 3, axis=-1) > 0.1

        if bg_image is None:
          bg_image = np.zeros(image.shape, dtype=np.uint8)
          bg_image[:] = BG_COLOR
        output_image = np.where(condition, image, bg_image)

        cv2.imshow('Selfie Segmentation', output_image)
        if cv2.waitKey(5) & 0xFF == 27:
          break
    cap.release()

s=Segmentatiion()
s

