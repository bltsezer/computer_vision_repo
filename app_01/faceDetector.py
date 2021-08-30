import time
import cv2
import mediapipe as mp


class FaceDetector:

    def __init__(self, minDetectionCon=0.5):

        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)

    def findFaces(self, img, draw=True):
       
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        bboxs = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                       int(bboxC.width * iw), int(bboxC.height * ih)
                cx, cy = bbox[0] + (bbox[2] // 2), \
                         bbox[1] + (bbox[3] // 2)
                bboxInfo = {"id": id, "bbox": bbox, "score": detection.score, "center": (cx, cy)}
                bboxs.append(bboxInfo)
                if draw:
                    img = cv2.rectangle(img, bbox, (50, 50, 250), 2)

                    cv2.putText(img, f'{int(detection.score[0] * 100)}%',
                                (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                                2, (50, 50, 250), 2)
        return img, bboxs

    def __test__(self,param):
        cap = cv2.VideoCapture(param)
        pTime = 0
        while True:
            success, img = cap.read()
            img, bboxs = self.findFaces(img)


            try:
                x_p=bboxs[0]["bbox"][0]
                y_p=bboxs[0]["bbox"][1]
                cv2.putText(img, f'Tanimlama Oran', (x_p, y_p-50), cv2.FONT_HERSHEY_PLAIN, 2, (50, 250, 50), 2)
            except IndexError:
                cv2.putText(img, f'Yuz Tespit edilemedi', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                print("Yuz Tespit edilemedi")
                _, bboxs = self.findFaces(img)
                
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (250, 50, 50), 2)
            
            cv2.imshow("Image", img)
            cv2.waitKey(1)

fd=FaceDetector()
fd.__test__(0)
