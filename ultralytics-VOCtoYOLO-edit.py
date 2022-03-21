import os
import json

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return [x,y,w,h]

# classes = {0: 'None', 1: 'Black smoke', 2:'Gray smoke', 3: 'White smoke', 4: 'Fire', 5: 'Cloud', 6: 'Fog', 7: 'Light', 8: 'Sunlight', 9: 'Shake object', 10: 'Shake leaf'}
# classes_convert = {'11': 0, '01': 1, '02': 2, '03': 3, '04': 4, '05': 5, '06': 6, '07': 7, '08': 8, '09': 9, '10': 10}
classes = {0: 'Black smoke', 1:'Gray smoke', 2: 'White smoke', 3: 'Fire', 4: 'Cloud'}
classes_convert = {'01': 0, '02': 1, '03': 2, '04': 3, '05': 4}

obj_path = r'D:/STUDY/UNID/data/aihub'

files = os.listdir(obj_path + '/labels-json')

print('Convert Start !!')

for file in files:
    json_f = open(obj_path + '/labels-json/' + file, 'r', encoding='utf-8-sig')
    r = json.load(json_f)
    
    filename = r['image']['filename']
    w = r['image']['resolution'][0]
    h = r['image']['resolution'][1]
    
    annotations = r['annotations']
    
    for annotation in annotations:
        try:
            annotation_box = annotation['box']
        except KeyError:
            # print('Polygon detect')
            continue
        
        xmin, ymin, xmax, ymax = annotation_box[0], annotation_box[1], annotation_box[2], annotation_box[3]
        annotation_class = annotation['class']
         
        yolo_class = classes_convert[annotation_class]     
        yolo_box = convert((w,h), (xmin,xmax,ymin,ymax))
                    
        txt_f = open(obj_path + '/labels/' + file[:-5] + '.txt', 'a')
        result = [yolo_class, '{:.8f}'.format(yolo_box[0]), '{:.8f}'.format(yolo_box[1]), '{:.8f}'.format(yolo_box[2]), '{:.8f}'.format(yolo_box[3]), '\n']
        result = list(map(str, result))
        txt_f.write(' '.join(result))
        
        txt_f.close()
            
    json_f.close()

print('Convert End !!')