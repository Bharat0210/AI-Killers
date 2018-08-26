

# Imports
import tensorflow as tf

# Object detection imports
from utils import backbone
from api import object_counting_api

if tf.__version__ < '1.4.0':
  raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')

input_video = "crowd2.mp4"


detection_graph, category_index = backbone.set_model('faster_rcnn_resnet101_kitti_2018_01_28')



targeted_objects = "person" 
fps = 23.98 
width = 426 
height = 240 
is_color_recognition_enabled = 0

object_counting_api.targeted_object_counting(input_video, detection_graph, category_index, is_color_recognition_enabled, targeted_objects, fps, width, height) # targeted objects counting

