import cv2
from ultralytics import YOLO
import pandas as pd
import numpy as np

model = YOLO('yolov8x.pt')
dict_classes = model.model.names

### Configurations
# Verbose during prediction
verbose = False
# Scaling percentage of original frame
scale_percent = 50

def detect_obj(frame):
    # Objects to detect Yolo
        class_IDS = [range(0, 79)]
    # Res vars
        res_lables = []
        sqr_arr = []

        # Getting prediction
        y_hat = model.predict(frame, conf=0.8, classes=class_IDS, verbose=False)

        # Getting the bounding boxes, confidence and classes of the recognize objects in the current frame.
        boxes = y_hat[0].boxes.xyxy.cpu().numpy()
        conf = y_hat[0].boxes.conf.cpu().numpy()
        classes = y_hat[0].boxes.cls.cpu().numpy()

        # Storing the above information in a dataframe
        positions_frame = pd.DataFrame(y_hat[0].cpu().numpy().boxes.data,
                                       columns=['xmin', 'ymin', 'xmax', 'ymax', 'conf', 'class'])
        labels = [dict_classes[i] for i in classes]

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

            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 0), 3)
            cv2.putText(img=frame, text=labels[ix] + ' '+  str(np.round(conf[ix], 2)),
                            org=(xmin, ymin - 30), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 0, 0),
                            thickness=2)

        return  res_lables, frame, sqr_arr