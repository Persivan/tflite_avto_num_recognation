
# https://www.kaggle.com/code/paulojunqueira/yolo-v8-vehicles-detecting-counting
#


import cv2
from ultralytics import YOLO

#basics
import pandas as pd
import numpy as np
from tqdm import tqdm

model = YOLO('yolov8x.pt')
dict_classes = model.model.names
def risize_frame(frame, scale_percent):
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    # dim = (1024, 576)                                  # <<<<<<<<<< CHANGE OUTPUT SIZE

    # resize image
    resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    return resized


### Configurations
# Verbose during prediction
verbose = False
# Scaling percentage of original frame
scale_percent = 50

def yolo_car_checker(frame):
        """
        На вход ожидает Mat img
        На выходе выдает [[lable],[crop_car_img]] и Mat img
        """
    # # Objects to detect Yolo
        class_IDS = [range(0, 79)]
    # # Auxiliary variables
    # centers_old = {}
    # centers_new = {}
    # obj_id = 0
    # veiculos_contador_in = dict.fromkeys(class_IDS, 0)
    # veiculos_contador_out = dict.fromkeys(class_IDS, 0)
    # end = []
    # frames_list = []
    # cy_linha = int(1500 * scale_percent / 100)
    # cx_sentido = int(2000 * scale_percent / 100)
    # offset = int(8 * scale_percent / 100)
    # contador_in = 0
    # contador_out = 0
    # print(f'[INFO] - Verbose during Prediction: {verbose}')

    # # Original informations of video
    # height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    # fps = video.get(cv2.CAP_PROP_FPS)
    # print('[INFO] - Original Dim: ', (width, height))

    # # Scaling Video for better performance
    # if scale_percent != 100:
    #     print('[INFO] - Scaling change may cause errors in pixels lines ')
    #     width = int(width * scale_percent / 100)
    #     height = int(height * scale_percent / 100)
    #     print('[INFO] - Dim Scaled: ', (width, height))

    # for i in tqdm(range(int(video.get(cv2.CAP_PROP_FRAME_COUNT)))):
    #     # Return values
    #     # truk = False
        res_lables = []
        sqr_arr = []

    #     # reading frame from video
    #     _, frame = video.read()

    #     # Applying resizing of read frame
    #     frame = risize_frame(frame, scale_percent)

    #     if verbose:
    #         print('Dimension Scaled(frame): ', (frame.shape[1], frame.shape[0]))

        # Getting predictions
        y_hat = model.predict(frame, conf=0.7, classes=class_IDS, verbose=False)
        # print(f"!!!!!{y_hat[0]}")

        # Getting the bounding boxes, confidence and classes of the recognize objects in the current frame.
        boxes = y_hat[0].boxes.xyxy.cpu().numpy()
        conf = y_hat[0].boxes.conf.cpu().numpy()
        classes = y_hat[0].boxes.cls.cpu().numpy()


        # Storing the above information in a dataframe
        positions_frame = pd.DataFrame(y_hat[0].cpu().numpy().boxes.data,
                                       columns=['xmin', 'ymin', 'xmax', 'ymax', 'conf', 'class'])
        #print(positions_frame)
        # Translating the numeric class labels to text
        labels = [dict_classes[i] for i in classes]
        # print(f"!!!!!!!!!!!!!!\n{labels}")
        for ix, row in enumerate(positions_frame.iterrows()):
            # Getting the coordinates of each vehicle (row)
            xmin, ymin, xmax, ymax, confidence, category, = row[1].astype('int')

            # Calculating the center of the bounding-box
            center_x, center_y = int(((xmax + xmin)) / 2), int((ymax + ymin) / 2)

            # drawing center and bounding-box of vehicle in the given frame
            crop = frame.copy()
            crop = crop[ymin:ymax, xmin:xmax]
            res_lables.append(labels[ix])
            sqr_arr.append([(xmin, ymin), (xmax, ymax)])

            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 0), 3)  # box

        for ix, row in enumerate(positions_frame.iterrows()):
            # Getting the coordinates of each vehicle (row)
            xmin, ymin, xmax, ymax, confidence, category, = row[1].astype('int')

            # Calculating the center of the bounding-box
            center_x, center_y = int(((xmax + xmin)) / 2), int((ymax + ymin) / 2)

            # if labels[ix] == 'truck':
            #     cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 3)
            #     cv2.putText(img=frame, text=labels[ix] + ' '+  str(np.round(conf[ix], 2)),
            #                 org=(xmin, ymin - 30), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 255),
            #                 thickness=2)
            #     # truk = True
            #     break
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 0), 3)
            cv2.putText(img=frame, text=labels[ix] + ' '+  str(np.round(conf[ix], 2)),
                            org=(xmin, ymin - 30), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 0, 0),
                            thickness=2)

            # Checking if the center of recognized vehicle is in the area given by the transition line + offset and transition line - offset
            # if (center_y < (cy_linha + offset)) and (center_y > (cy_linha - offset)):
            #     if (center_x >= 0) and (center_x <= cx_sentido):
            #         contador_in += 1
            #         veiculos_contador_in[category] += 1
            #     else:
            #         contador_out += 1
            #         veiculos_contador_out[category] += 1
        return  res_lables, frame, sqr_arr