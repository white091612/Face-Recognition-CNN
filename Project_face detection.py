
# coding: utf-8

# In[2]:


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


# In[3]:


cr = CR.CRAWL()


# In[4]:


Project_Translate.hanrom("유아인")


# In[5]:


plist=["강다니엘","공유","박서준","정해인","고수","이진욱","전현무","유재석",
       "류준열","박보검","조정석","조진웅","육성재","차승원",
       "지성","최다니엘","장동건","송중기","유아인","마동석","오상진",#"에디킴"
       "아이유","한혜진","아이린","설현","손나은","고아라","윤아","조보아",
       "손예진","홍진영","전지현","한효주","박신혜","박민영",#"혜리","쯔위",
       "김민희","이성경","유인나","김태희","제니","박나래","화사"]
cr.set_info(plist,1001)


# In[6]:


cr.plist.append("에디킴")
cr.plist.append("혜리")
cr.plist.append("쯔위")
cr.plist.append("aoa 지민")
cr.plist_e.append("eddie kim")
cr.plist_e.append("hyeri")
cr.plist_e.append("zzuwi")
cr.plist_e.append("aoa jimin")
cr.myd = dict(zip(cr.plist,cr.plist_e))


# In[7]:


cr.myd


# In[10]:


cr.crawl()


# In[26]:


files = ["{0:0>6}".format(str(x)) for x in range(1,1001)]


# In[27]:


for file in files:
    print(file)


# In[33]:


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


# # 아래는 참고용 코드

# In[18]:


detector = MTCNN()
fa = MFA.FaceAlign()
fdir = "C:/py_src/project/test"
filen1 = fdir + "/000007.jpg"
image = cv2.imread(filen1)
result = detector.detect_faces(image)
result = result[0]
bounding_box = result['box']
x,y,w,h = bounding_box
image = cv2.rectangle(image,
              (bounding_box[0], bounding_box[1]),
              (bounding_box[0]+bounding_box[2], bounding_box[1]+bounding_box[3]),
              (0,155,255),
              2)
iw,ih = image.shape[:2]
#가능한 크게 자르기
minimum = np.min([x,y,iw-(x+w),ih-(y+h)])

image_d = image[y-minimum : minimum+y+h, x-minimum : x+minimum+w]
#image_d = image[max((y - int(h / 2)),0) : min(ih,(y + h + int(h / 2))), 
#                max((x - int(w / 2)),0) : min(iw,(x + w + int(w / 2)))]
plt.imshow(image_d)
#cv2.imwrite("no1.jpg", image_d)


# In[16]:


result['box'][0] = result['box'][0] - max((x - int(w / 2)),0)
result['box'][1] = result['box'][1] - max((y - int(h / 2)),0)
result['keypoints']['left_eye'] = (result['keypoints']['left_eye'][0] -max((x - int(w / 2)),0),
                                   result['keypoints']['left_eye'][1] -max((y - int(h / 2)),0))
result['keypoints']['right_eye'] = (result['keypoints']['right_eye'][0] - max((x - int(w / 2)),0),
                                    result['keypoints']['right_eye'][1] - max((y - int(h / 2)),0))
result['keypoints']['nose'] = (result['keypoints']['nose'][0] - max((x - int(w / 2)),0),
                               result['keypoints']['nose'][1] - max((y - int(h / 2)),0))
result['keypoints']['mouth_left'] = (result['keypoints']['mouth_left'][0] - max((x - int(w / 2)),0),
                                     result['keypoints']['mouth_left'][1] - max((y - int(h / 2)),0))
result['keypoints']['mouth_right'] = (result['keypoints']['mouth_right'][0] - max((x - int(w / 2)),0),
                                      result['keypoints']['mouth_right'][1] - max((y - int(h / 2)),0))


# In[21]:


result['box'][0] = minimum
result['box'][1] = minimum
result['keypoints']['left_eye'] = (minimum + result['keypoints']['left_eye'][0] - x,
                                   minimum + result['keypoints']['left_eye'][1] - y)
result['keypoints']['right_eye'] = (minimum + result['keypoints']['right_eye'][0] - x,
                                    minimum + result['keypoints']['right_eye'][1] - y)
result['keypoints']['nose'] = (minimum + result['keypoints']['nose'][0] - x,
                               minimum + result['keypoints']['nose'][1] - y)
result['keypoints']['mouth_left'] = (minimum + result['keypoints']['mouth_left'][0] - x,
                                     minimum + result['keypoints']['mouth_left'][1] - y)
result['keypoints']['mouth_right'] = (minimum + result['keypoints']['mouth_right'][0] - x,
                                      minimum + result['keypoints']['mouth_right'][1] - y)


# In[19]:


image_d = cv2.circle(image_d,(result['keypoints']['left_eye']), 3, (0,155,255), 2)
image_d = cv2.circle(image_d,(result['keypoints']['right_eye']), 3, (0,155,255), 2)
plt.imshow(image_d)
#cv2.imwrite("no2.jpg", image_d)


# In[20]:


left = result['keypoints']['left_eye']
right = result['keypoints']['right_eye']
angle = math.degrees(math.atan((right[1]-left[1])/abs(right[0]-left[0])))
ih, iw = image_d.shape[:2]

#잘려진 이미지의 중심을 기준으로 회전(이미지만)
M1 = cv2.getRotationMatrix2D((iw/2, ih/2), angle, 1)
image_d = cv2.warpAffine(image_d, M1, (iw, ih))

#x = int(r/2 * math.cos(-math.radians(angle)) - l/2 * math.sin(-math.radians(angle)))
#y = int(r/2 * math.sin(-math.radians(angle)) + l/2 * math.cos(-math.radians(angle)))
image_d = cv2.rectangle(image_d,
              (x, y),
              (x+w, y+h),
              (0,255,0),
              3)
plt.imshow(image_d)
#cv2.imwrite("no3.jpg", image_d)


# In[ ]:


detector = MTCNN()
fa = MFA.FaceAlign()
for j in range(len(cr.plist)):
    fdir = "C:/py_src/project/aligned/"+ cr.plist_e[j]
    for file in files:
        try:
            filen1 = fdir + "/" + file
            image = cv2.imread(filen1)

            result = detector.detect_faces(image)
            # for i in range(len(result)):
            # Result is an array with all the bounding boxes detected. We know that for 'ivan.jpg' 
            # there is only one.
            result = result[0]
            bounding_box = result['box']
            keypoints = result['keypoints']

            #cv2.rectangle(image,
            #              (bounding_box[0], bounding_box[1]),
            #              (bounding_box[0]+bounding_box[2], bounding_box[1]+bounding_box[3]),
            #              (0,155,255),
            #              2)
            #cv2.circle(image,(keypoints['left_eye']), 2, (0,155,255), 2)
            #cv2.circle(image,(keypoints['right_eye']), 2, (0,155,255), 2)
            #cv2.circle(image,(keypoints['nose']), 2, (0,155,255), 2)
            #cv2.circle(image,(keypoints['mouth_left']), 2, (0,155,255), 2)
            #cv2.circle(image,(keypoints['mouth_right']), 2, (0,155,255), 2)

            # x,y,w,h = bounding_box 
            # image = image[y - int(h / 10):y + h + int(h / 10), x - int(w / 10) : x + w + int(w / 10)]
            fa.set_info(result)
            image = fa.align(image)
            #result = detector.detect_faces(image)
            #bounding_box = result[0]['box']
            #keypoints = result[0]['keypoints'].
            image_d = fa.align(image)
            result_d = detector.detect_faces(image_d)
            result_d = result_d[0]
            bounding_box = result_d['box']
            keypoints = result_d['keypoints']
            #result = detector.detect_faces(image)
            #bounding_box = result[0]['box']
            #keypoints = result[0]['keypoints']
            x,y,w,h = bounding_box # 박스 시작 좌표 : (x,y) 이로부터 떨어진 거리 : w,h
            cropped = image[y - int(h / 80):y + h + int(h / 80), x - int(w / 80) : x + w + int(w / 80)]
            crdir = "C:/py_src/project/aligned/"+ cr.plist_e[j]
            if not os.path.isdir(crdir): 
                os.mkdir(crdir)
            filen2 = crdir + "/" + file
            cv2.imwrite(filen2, cropped)
            print(result)
        except :
            pass


# In[15]:


detector = MTCNN()
fa = MFA.FaceAlign()
fdir = "C:/py_src/project/Kang Daniel"
filen1 = fdir + "/000663.jpg"
image = cv2.imread(filen1)
result = detector.detect_faces(image)
result = result[2]
bounding_box = result['box']
x,y,w,h = bounding_box
#크게 자르기
image_d = image[y - int(h / 2):y + h + int(h / 2), x - int(w / 2) : x + w + int(w / 2)]
#자른거 안에서 다시 찾기
result_d = detector.detect_faces(image_d)
result_d = result_d[0]
bounding_box = result_d['box']
x,y,w,h = bounding_box
keypoints = result_d['keypoints']
# align
#left = result_d['keypoints']['left_eye']
#right = result_d['keypoints']['right_eye']
#angle = math.degrees(math.atan((right[1]-left[1])/abs(right[0]-left[0])))
#ih, iw = image_d.shape[:2]
#nosex = iw/2-result_d['keypoints']['nose'][0]
##nosey = ih/2-result_d['keypoints']['nose'][1]
#ch, cw = result_d['keypoints']['nose']
#M1 = cv2.getRotationMatrix2D((cw, ch), angle, 1)
#M2 = np.float32([[1, 0, nosex], [0, 1, nosey]])
#image_d = cv2.warpAffine(image_d, M2, (iw, ih))
#image_d = cv2.warpAffine(image_d, M1, (iw, ih))
fa.set_info(result_d)
image_d=fa.align(image_d)

#돌리고 다시 찾기
result_d = detector.detect_faces(image_d)
result_d = result_d[0]
bounding_box_d = result_d['box']
x,y,w,h = bounding_box_d
image_d=cv2.rectangle(image_d,
                              (bounding_box_d[0], bounding_box_d[1]),
                              (bounding_box_d[0]+bounding_box_d[2], bounding_box_d[1]+bounding_box_d[3]),
                              (0,155,255),
                              2)
#제대로 자르기
cropped = image_d[y - int(h / 80):y + h + int(h / 80), x - int(w / 80) : x + w + int(w / 80)]
plt.imshow(cropped)

