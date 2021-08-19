import cv2
import mediapipe as mp
import time
import math


class PoseDetector():
  def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):
    self.mode = mode
    self.upBody = upBody
    self.smooth = smooth
    self.detectionCon = detectionCon
    self.trackCon = trackCon

    self.mpDraw = mp.solutions.drawing_utils
    self.mpPose = mp.solutions.pose
    self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,
                                  self.detectionCon, self.trackCon)

  def findPose(self, img, draw=True):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    self.results = self.pose.process(imgRGB)
    if self.results.pose_landmarks:
        if draw:
            self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                        self.mpPose.POSE_CONNECTIONS)
    return img

  def findPosition(self, img, draw=True):
    self.lmList = []
    if self.results.pose_landmarks:
        for id, lm in enumerate(self.results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            self.lmList.append([id, cx, cy])
            if draw:
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
    return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):
        
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle

class CamDetectElbowFromPose():
  def __init__(self,dev):
    self.cap = cv2.VideoCapture(dev)
    self.pTime = 0
    self.detector = PoseDetector()
    self.start()

  def start(self):
    while True:
      success, img = self.cap.read()
      img = self.detector.findPose(img)
      lmList = self.detector.findPosition(img, draw=False)
      if len(lmList) !=0:
          print(lmList[14])
          cv2.circle(img, (lmList[13][1], lmList[13][2]), 12, (250, 0, 50), cv2.FILLED)
          cv2.circle(img, (lmList[14][1], lmList[14][2]), 12, (0, 50, 250), cv2.FILLED)
          cv2.circle(img, (lmList[26][1], lmList[26][2]), 14, (250, 50, 0), cv2.FILLED)
          cv2.circle(img, (lmList[25][1], lmList[25][2]), 14, (0, 250, 50), cv2.FILLED)

      cTime = time.time()
      fps = 1 / (cTime - self.pTime)
      self.pTime = cTime

      cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                  (255, 0, 0), 3)

      cv2.imshow("Image", img)
      cv2.waitKey(1)

ss=CamPoseEstimate(0)
ss
