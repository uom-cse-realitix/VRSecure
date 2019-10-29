# Import packages
import os

import cv2
import numpy as np
import tensorflow as tf

import distance_utils
from point import point
from utils import label_map_util

import simpleaudio as sa

wave_obj = sa.WaveObject.from_wave_file("./data/alarm_sound_short.wav")

CWD_PATH = os.getcwd()
PATH_TO_CKPT = os.path.join(CWD_PATH, 'data', 'frozen_inference_graph.pb')
PATH_TO_LABELS = os.path.join(CWD_PATH, 'data', 'mscoco_label_map.pbtxt')
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)

image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# video = VideoStream(src=0).start()
video = cv2.VideoCapture(1)
video.set(3, IMAGE_WIDTH)
video.set(4, IMAGE_HEIGHT)

boundary = None
play_obj = None

while True:
    ret, image = video.read()
    frame_expanded = np.expand_dims(image, axis=0)

    if boundary:
        cv2.rectangle(image, (boundary[0], boundary[1]), (boundary[2], boundary[3]),
                      (255, 0, 0), 2)

    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: frame_expanded})

    scores_arr = np.squeeze(scores)
    classes_arr = np.squeeze(classes).astype(np.int32)
    boxes_arr = np.squeeze(boxes)

    person_location = point(IMAGE_WIDTH, IMAGE_HEIGHT)
    person_found = False
    object_locations = []

    for i in range(int(num[0])):
        if scores_arr[i] > 0.6:
            ymin, xmin, ymax, xmax = tuple(boxes_arr[i].tolist())
            if classes_arr[i] == 1 and not person_found:
                person_found = True
                person_location.set_x_coordinates(xmin, xmax)
                person_location.set_y_coordinates(ymin, ymax)
                cv2.rectangle(image, person_location.get_top_left(), person_location.get_bottom_right(), (0, 255, 0), 2)
            else:
                object_location = point(IMAGE_WIDTH, IMAGE_HEIGHT)
                object_location.set_x_coordinates(xmin, xmax)
                object_location.set_y_coordinates(ymin, ymax)
                object_locations.append(object_location)
                cv2.rectangle(image, object_location.get_top_left(), object_location.get_bottom_right(), (0, 0, 255), 2)

    if person_found:
        for object_location in object_locations:
            distance = distance_utils.calc_relative_distance(object_location, person_location)
            # distance = distance_utils.calculate_mid_distance(object_location, person_location)
            print("Distance", distance)
            # if distance < 100:
            #     if play_obj:
            #         while play_obj.is_playing():
            #             play_obj.stop()
            #     play_obj = wave_obj.play()
            # else:
            #     if play_obj:
            #         if play_obj.is_playing():
            #             play_obj.stop()
            if distance[0] == "LEFT":
                if distance[1] < 50 and \
                        person_location.y_2 < object_location.y_2 + 50 and \
                        person_location.y_2 > object_location.get_mid_point()[1]:
                    if play_obj:
                        while play_obj.is_playing():
                            play_obj.stop()
                    play_obj = wave_obj.play()
                else:
                    if play_obj:
                        if play_obj.is_playing():
                            play_obj.stop()
            elif distance[0] == "TOP":
                if distance[1] < -70:
                    if play_obj:
                        while play_obj.is_playing():
                            play_obj.stop()
                    play_obj = wave_obj.play()
                else:
                    if play_obj:
                        if play_obj.is_playing():
                            play_obj.stop()

        if boundary:
            if person_location.x_1 < boundary[0] or \
                    person_location.x_2 > boundary[2] or \
                    person_location.y_2 < boundary[1] or \
                    person_location.y_2 > boundary[3]:
                print("Out of the safe area")
                if play_obj:
                    while play_obj.is_playing():
                        play_obj.stop()
                play_obj = wave_obj.play()
            else:
                print("Inside the safe area")
                if play_obj:
                    if play_obj.is_playing():
                        play_obj.stop()

        print("=======================================")

    cv2.imshow("Frame", image)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
    elif key == ord("s"):
        b = cv2.selectROI("Frame", image, fromCenter=False, showCrosshair=True)
        boundary = (b[0], b[1], b[0] + b[2], b[1] + b[3])
        print(boundary)

video.release()
cv2.destroyAllWindows()
