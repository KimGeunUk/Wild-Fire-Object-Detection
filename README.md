
## Wild-Fire-Detect

산불은 초기에 진압하지 않으면 걷잡을 수 없이 사태가 심각해진다.

이를 방지하고자 카메라를 통해 산불을 Detection 할 수 있는 인공지능 모델을 개발하고자 한다.


## 학습 환경

- Ubunt 18.04

- GPU GeForce 3090 * 2 | Driver 470.82.01 | CUDA 11.04 | CUDNN 8.2.2

- OpenCV 4.4.0

- Darknet (AlexeyAB)

- Ultralytic


## Darknet 정리

- 설치 과정

https://geunuk.tistory.com/48?category=900416

- Darknet 사용법

https://repeated-canvas-49b.notion.site/How-to-use-Darknet-febd450b63b141b0be66a121f816daee

- 데이터 버전별 Train 결과 정리 (~ing)

https://repeated-canvas-49b.notion.site/Train-Result-bee4fa45f8864c648fbaf543e467d32e

#### 파일 설명

- getbbox.py

데이터를 수집한 후 학습시키기 위해 Labeling 을 진행하는데, 수작업으로 진행하기에는 너무 많은 파일들이 있다.
먼저 앞서 수집한 데이터를 학습시킨 후 학습된 모델을 사용하여 이미지를 Input 하면 Bounding Box 만 추출하도록 하였다.
이후 추출한 Bounding Box 를 직접 확인하여 수정이 필요한 부분이 있으면 수정하고, 없으면 넘어간다.

- get_train_txt.py

Darknet 환경에서 train 하기 위해 train.txt 파일에 학습시키는 이미지의 dir이 모두 적혀있어야 한다. 이를 자동화 하였다.

#### 디렉토리 구조

<details> <summary>Directory</summary>

- darknet
  - backup
    - yolov3-fireV1
      - yolov3-custom_best.weights
    - yolov3-fireV2
  - custom
    - fireV1
      - obj
      - obj.data
      - obj.names
      - train.txt
      - valid.txt
    - fireV2    
    - yolov3-custom.cfg
    - yolov3.weights
</details>

## Pytorch YOLO - ultralytics 정리

#### 모델의 구조와 학습 결과를 확인하기 위해 wandb를 사용하고 싶어서 변경하였습니다.

- 정리

  https://repeated-canvas-49b.notion.site/YOLO-v3-Fire-Smoke-Detection-33331e6a9bc747039305593188521d4a
  
 - 직접 수집한 데이터 결과 정리
   
   https://repeated-canvas-49b.notion.site/Train-Result-a86be2dc6b9e46b1aef5a3a36b0c0ba5
   
 - AI-hub 데이터 결과
  
    https://repeated-canvas-49b.notion.site/Train-Result-13ffdc3faaa0496bbc85693d2fa9dc26
  
    
