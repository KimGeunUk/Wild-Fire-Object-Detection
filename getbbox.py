from copyreg import pickle
from unittest import result
from unittest.mock import patch
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
import time

def get_detected_img(cv_net, img_array, conf_threshold, nms_threshold, use_copied_array=True, is_print=True):
    rows = img_array.shape[0]
    cols = img_array.shape[1]
    
    layer_names = cv_net.getLayerNames()
    outlayer_names = [layer_names[i - 1] for i in cv_net.getUnconnectedOutLayers()]
    
    # 로딩한 모델은 Yolov3 416 x 416 모델 원본 이미지 배열을 사이즈 (416, 416)으로, BGR을 RGB로 변환하여 배열 입력
    cv_net.setInput(cv2.dnn.blobFromImage(img_array, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False))
    start = time.time()
    
    # Object Detection 수행하여 결과를 cvout으로 반환 
    cv_outs = cv_net.forward(outlayer_names)
    layerOutputs = cv_net.forward(outlayer_names)

    class_ids = []
    confidences = []
    boxes = []
    boxes_yolo = []
    result_yolo = []

    # 3개의 개별 output layer별로 Detect된 Object들에 대해서 Detection 정보 추출 및 시각화 
    for ix, output in enumerate(cv_outs):
        # Detected된 Object별 iteration
        for jx, detection in enumerate(output):
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            # confidence가 지정된 conf_threshold보다 작은 값은 제외 
            if confidence > conf_threshold:
                # print('ix:', ix, 'jx:', jx, 'class_id', class_id, 'confidence:', confidence)
                # detection은 scale된 좌상단, 우하단 좌표를 반환하는 것이 아니라, detection object의 중심좌표와 너비/높이를 반환
                # 원본 이미지에 맞게 scale 적용 및 좌상단, 우하단 좌표 계산
                center_x = int(detection[0] * cols)
                center_y = int(detection[1] * rows)
                width = int(detection[2] * cols)
                height = int(detection[3] * rows)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                # 3개의 개별 output layer별로 Detect된 Object들에 대한 class id, confidence, 좌표정보를 모두 수집
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])
                boxes_yolo.append([str(class_id) , str(detection[0]), str(detection[1]), str(detection[2]), str(detection[3])])
    
    # NMS로 최종 filtering된 idxs를 이용하여 boxes, classes, confidences에서 해당하는 Object정보를 추출하고 시각화.
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    idxs_label = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    
    if len(idxs_label) > 0:
        for i in idxs_label.flatten():
            box = boxes_yolo[i]
            # center_x = boxes_yolo[1]
            # center_y = boxes_yolo[2]
            # width = boxes_yolo[3]
            # height = boxes_yolo[4]            
            # labels_to_names 딕셔너리로 class_id값을 클래스명으로 변경. opencv에서는 class_id + 1로 매핑해야함.
            caption = "{}: {:.4f}".format(label[class_ids[i]], confidences[i])
            #print("lable[", class_ids[i] , "]", label[class_ids[i]], '\t=', "box : ", box)
            result_yolo.append(box)            

    if is_print:
        print('Detection time:',round(time.time() - start, 2),"초")
    #return draw_img
    return result_yolo

# main
import os
import shutil

# define path
cur_path = os.getcwd()
obj_path = cur_path + '/custom/fireV4/obj/'
if not os.path.exists(cur_path + '/custom/fireV4/no_detect/'):
    os.makedirs(cur_path + '/custom/fireV4/no_detect/')
no_dectect_path = cur_path + '/custom/fireV4/no_detect/'

# weights, cfg path
weights_path = cur_path + '/backup/yolov3-fireV1V2V3/obj2/yolov3-custom_best.weights'
config_path =  cur_path + '/custom/yolov3-custom.cfg'

# Model Load
cv_net_yolo = cv2.dnn.readNetFromDarknet(config_path, weights_path)
    
conf_threshold = 0.25
nms_threshold = 0.2

label = ['fire', 'likefire', 'smoke', 'likesmoke']

file_list = os.listdir(obj_path)

for i in file_list:
    # image Load    
    if i[-4:] == '.jpg' or i[-5:] == '.jpeg':
        if i[-4:] == '.jpg':
            img_file = i[:-4] + '.jpg'
        else:
            img_file = i[:-5] + '.jpeg'
            
        img = cv2.imread(obj_path + img_file)
        
        # Visualization
        # draw_img = get_detected_img(cv_net_yolo, img, conf_threshold=conf_threshold, nms_threshold=nms_threshold, use_copied_array=True, is_print=True)
        lines = get_detected_img(cv_net_yolo, img, conf_threshold=conf_threshold, nms_threshold=nms_threshold, use_copied_array=True, is_print=True)
        
        if len(lines) == 0:
            shutil.move(obj_path + img_file, no_dectect_path + img_file)
        else:           
            with open(obj_path + img_file[:6] + '.txt', 'w') as file:
                for line in lines:
                    file.write(' '.join(line))
                    file.write('\n')
