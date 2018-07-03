
# coding: utf-8

# In[ ]:


import numpy as np
import cv2
import os
import math
class FaceAlign:
    def set_info(self, result) :
        self.result = result
    def align(self, image) :
        self.image = image
        left = self.result['keypoints']['left_eye']
        right = self.result['keypoints']['right_eye']
        angle = math.degrees(math.atan((right[1]-left[1])/abs(right[0]-left[0])))
        ih, iw = self.image.shape[:2]
        M1 = cv2.getRotationMatrix2D((iw/2, ih/2), angle, 1)
        self.image = cv2.warpAffine(self.image, M1, (iw,ih))
        return self.image

