import pyrealsense2 as rs
import numpy as np
import math
import cv2

class perception:
    def __init__(self):
        #sets up depth/color data pipelines
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        # human locations
        self.humans = []
        #configs streams and HOG stuff
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.cfg = self.pipeline.start(self.config)
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.profile = self.cfg.get_stream(rs.stream.color) 
        self.intrinsics = self.profile.as_video_stream_profile().get_intrinsics()
    def __del__(self):
        self.pipeline.stop()
    def getHumans(self):
        return self.humans
    def getCoords(self,x,y,depth):
        return rs.rs2_deproject_pixel_to_point(self.intrinsics, [x, y], depth)
    def getHumanBoundingBoxes(self, frame):
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        boxes, weights = self.hog.detectMultiScale(frame, winStride=(8,8))
        boxes = np.array([[x,y,x+w,y+h] for (x,y,w,h) in boxes])
        return boxes
    def update(self):
        align_to = rs.stream.color
        align = rs.align(align_to)
        frames = self.pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not depth_frame or not color_frame:
            return
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_INFERNO)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        if depth_colormap_dim != color_colormap_dim:
            color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)

        boxes = self.getHumanBoundingBoxes(color_image)
        points = []
        for (xA, yA, xB, yB) in boxes:
            cv2.rectangle(color_image, (xA, yA), (xB, yB), (0, 255, 0), 2)
            xC, yC = math.floor((xB+xA)/2), math.floor((yB+yA)/2)
            depth = depth_frame.get_distance(xC,yC)
            location = self.getCoords(xC, yC, depth)
            points.append(location)
        self.humans = points
        images = np.hstack((color_image, depth_colormap))
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)
        
# Code for testing

#percep = perception()
#
#while(True):
#    percep.update()
#    print(percep.getHumans())