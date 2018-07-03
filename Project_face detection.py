from __future__ import print_function

import os
os.environ['GLOG_minloglevel'] = '2'  # Hide caffe debug info.
import sys
import math
import time

import cv2
import caffe

import numpy as np
import matplotlib.pyplot as plt

import Project_Translate
import Project_Crawl as CR
import Project_MyFaceAlign as MFA

from mtcnn.mtcnn import MTCNN

cr = CR.CRAWL()
plist=["강다니엘","공유","박서준","정해인","고수","이진욱","전현무","유재석",
       "류준열","박보검","조정석","조진웅","육성재","차승원",
       "지성","최다니엘","장동건","송중기","유아인","마동석","오상진",#"에디킴"
       "아이유","한혜진","아이린","설현","손나은","고아라","윤아","조보아",
       "손예진","홍진영","전지현","한효주","박신혜","박민영",#"혜리","쯔위",
       "김민희","이성경","유인나","김태희","제니","박나래","화사"]
cr.set_info(plist,1001)

cr.plist.append("에디킴")
cr.plist.append("혜리")
cr.plist.append("쯔위")
cr.plist.append("aoa 지민")
cr.plist_e.append("eddie kim")
cr.plist_e.append("hyeri")
cr.plist_e.append("zzuwi")
cr.plist_e.append("aoa jimin")
cr.myd = dict(zip(cr.plist,cr.plist_e))

cr.crawl()

files = ["{0:0>6}".format(str(x)) for x in range(1,1001)]

detector = MTCNN()
fa = MFA.FaceAlign()
for j in range(len(cr.plist)):
    fdir = "C:/py_src/project/" + cr.plist_e[j]
    for file in files:
        try:
            filen1 = fdir + "/" + file + ".jpg"
            image = cv2.imread(filen1)
            result = detector.detect_faces(image)
            for i in range(len(result)):
                #x,y,w,h,result 변수 설정
                result_d = result[i]
                bounding_box = result_d['box']
                x,y,w,h = bounding_box
                #가능한 크게 자르기
                minimum = np.min([x,y,iw-(x+w),ih-(y+h)])
                image_d = image[y-minimum : minimum+y+h, x-minimum : x+minimum+w]
                #자른 이미지 기준 result 재설정
                result_d['box'][0] = minimum
                result_d['box'][1] = minimum
                result_d['keypoints']['left_eye'] = (minimum + result_d['keypoints']['left_eye'][0] - x,
                                                   minimum + result_d['keypoints']['left_eye'][1] - y)
                result_d['keypoints']['right_eye'] = (minimum + result_d['keypoints']['right_eye'][0] - x,
                                                    minimum + result_d['keypoints']['right_eye'][1] - y)
                result_d['keypoints']['nose'] = (minimum + result_d['keypoints']['nose'][0] - x,
                                               minimum + result_d['keypoints']['nose'][1] - y)
                result_d['keypoints']['mouth_left'] = (minimum + result_d['keypoints']['mouth_left'][0] - x,
                                                     minimum + result_d['keypoints']['mouth_left'][1] - y)
                result_d['keypoints']['mouth_right'] = (minimum + result_d['keypoints']['mouth_right'][0] - x,
                                                      minimum + result_d['keypoints']['mouth_right'][1] - y)
                # 돌리기
                fa.set_info(result_d)
                image_d = fa.align(image_d)
                # x,y,w,h 재설정(result_d가 변했으므로)
                x,y,w,h = result_d['box']
                #제대로 자르기
                cropped = image_d[y+int(h/30):y+h-int(h/30),x+int(w/30):x+w-int(w/30)]
                #이미지 저장
                crdir = "C:/py_src/project/cropped_aligned/"+ cr.plist_e[j]
                if not os.path.isdir(crdir): 
                    os.mkdir(crdir)
                filen2 = crdir + "/" + file + "_" + str(i) + ".jpg"
                cv2.imwrite(filen2, cropped)
                print(result)
        except :
            pass
