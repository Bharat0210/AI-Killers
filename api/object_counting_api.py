

import tensorflow as tf
import csv
import cv2
import numpy as np
from utils import visualization_utils as vis_util
import re
from twilio.rest import Client



def targeted_object_counting(input_video, detection_graph, category_index, is_color_recognition_enabled, targeted_object, fps, width, height):
        

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_movie = cv2.VideoWriter('the_output.avi', fourcc, fps, (width, height))
        x=0
        y=0
        # input video
        cap = cv2.VideoCapture(input_video)

        total_passed_vehicle = 0
        speed = "waiting..."
        direction = "waiting..."
        size = "waiting..."
        color = "waiting..."
        the_result = "..."
        width_heigh_taken = True
        height = 0
        width = 0
        with detection_graph.as_default():
          with tf.Session(graph=detection_graph) as sess:
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            # for all the frames that are extracted from input video
            while(cap.isOpened()):
                ret, frame = cap.read()                

                if not  ret:
                    print("end of the video file...")
                    break
                
                input_frame = frame

                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(input_frame, axis=0)

                # Actual detection.
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})

                # insert information text to video frame
                font = cv2.FONT_HERSHEY_SIMPLEX

                # Visualization of the results of a detection.        
                counter, csv_line, the_result = vis_util.visualize_boxes_and_labels_on_image_array(cap.get(1),
                                                                                                      input_frame,
                                                                                                      1,
                                                                                                      is_color_recognition_enabled,
                                                                                                      np.squeeze(boxes),
                                                                                                      np.squeeze(classes).astype(np.int32),
                                                                                                      np.squeeze(scores),
                                                                                                      category_index,
                                                                                                      targeted_objects=targeted_object,
                                                                                                      use_normalized_coordinates=True,
                                                                                                      line_thickness=4)
                if(len(the_result) == 0):
                    the_result='0'
                    cv2.putText(input_frame, "...", (10, 35), font, 0.8, (0,255,255),2,cv2.FONT_HERSHEY_SIMPLEX)                       
                else:
                    cv2.putText(input_frame, the_result, (10, 35), font, 0.8, (0,255,255),2,cv2.FONT_HERSHEY_SIMPLEX)
                
                
               # print(the_result)
                x=int(re.search(r'\d+', the_result).group())
                if(x>8):
                    y=y+1
                output_movie.write(input_frame)
                print ("writing frame")

                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                if(csv_line != "not_available"):
                        with open('traffic_measurement.csv', 'a') as f:
                                writer = csv.writer(f)                          
                                size, direction = csv_line.split(',')                                             
                                writer.writerows([csv_line.split(',')])         
            if(y>10):
               print("over crowded")
               account_sid='ACc021bfd03fdbcfd6ac7ce1e27a7f5f0e'
               auth_token='eaf3b673fd5518db71bb309b8f91d473'
               client = Client(account_sid, auth_token)
               
               message=client.messages.create(
                       body='Over Crowded!!',
                       from_='+15713395577',
                       to='+918124391974'
                       )
            cap.release()
            cv2.destroyAllWindows()



