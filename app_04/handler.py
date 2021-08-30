import sys
from collections import namedtuple
import cv2
import numpy as np
from pose_estimator import PoseEstimator

#=========================
class ROISelector(object): 
    def __init__(self, win_name, init_frame, callback_func): 
        self.callback_func = callback_func 
        self.selected_rect = None 
        self.drag_start = None 
        self.tracking_state = 0
        event_params = {"frame": init_frame}
        cv2.namedWindow(win_name)
        cv2.setMouseCallback(win_name, self.mouse_event, event_params)

    def mouse_event(self, event, x, y, flags, param):
        x, y = np.int16([x, y]) 

        # Detecting the mouse button down event 
        if event == cv2.EVENT_LBUTTONDOWN: 
            self.drag_start = (x, y) 
            self.tracking_state = 0 

        if self.drag_start:
            if event == cv2.EVENT_MOUSEMOVE:
                h, w = param["frame"].shape[:2] 
                xo, yo = self.drag_start 
                x0, y0 = np.maximum(0, np.minimum([xo, yo], [x, y])) 
                x1, y1 = np.minimum([w, h], np.maximum([xo, yo], [x, y])) 
                self.selected_rect = None 

                if x1-x0 > 0 and y1-y0 > 0:
                    self.selected_rect = (x0, y0, x1, y1) 

            elif event == cv2.EVENT_LBUTTONUP:
                self.drag_start = None 
                if self.selected_rect is not None: 
                    self.callback_func(self.selected_rect)
                    self.selected_rect = None
                    self.tracking_state = 1

    def draw_rect(self, img, rect): 
        if not rect: return False 
        x_start, y_start, x_end, y_end = rect
        cv2.rectangle(img, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2) 
        return True
#===================


#==========================
import sys 
from collections import namedtuple 

import cv2 
import numpy as np

class VideoHandler(object): 
    def __init__(self, capId, scaling_factor, win_name): 
        self.cap = cv2.VideoCapture(capId)
        self.pose_tracker = PoseEstimator() 
        self.win_name = win_name
        self.scaling_factor = scaling_factor

        ret, frame = self.cap.read()
        self.rect = None
        self.frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
        self.roi_selector = ROISelector(win_name, self.frame, self.set_rect) 

    def set_rect(self, rect): 
        self.rect = rect
        self.pose_tracker.add_target(self.frame, rect) 

    def start(self):
        paused = False
        while True:
            if not paused or self.frame is None: 
                ret, frame = self.cap.read()
                scaling_factor = self.scaling_factor
                frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA) 
                if not ret: break 
                self.frame = frame.copy() 

            img = self.frame.copy() 
            if not paused and self.rect is not None: 
                tracked = self.pose_tracker.track_target(self.frame) 
                for item in tracked: 
                    cv2.polylines(img, [np.int32(item.quad)], True, (255, 255, 255), 2) 
                    for (x, y) in np.int32(item.points_cur): 
                        cv2.circle(img, (x, y), 2, (255, 255, 255)) 

            self.roi_selector.draw_rect(img, self.rect) 
            cv2.imshow(self.win_name, img) 
            ch = cv2.waitKey(1) 
            if ch == ord(' '): paused = not paused 
            if ch == ord('c'): self.pose_tracker.clear_targets() 
            if ch == 27: break

if __name__ == '__main__': 
    VideoHandler(0, 0.9, 'Tracker').start()
#===============================================================


