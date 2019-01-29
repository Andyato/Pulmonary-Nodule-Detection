from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

tf.app.flags.DEFINE_string(
    'dataset_tfrecord',
    '../data/tfrecords',
    'tfrecord of fruits dataset'
)
tf.app.flags.DEFINE_integer(
    'shortside_size',
    512,
    'the value of new height and new width, new_height = new_width'
)

###########################
#  data batch
##########################
tf.app.flags.DEFINE_integer(
    'num_classes',
    1,
    'num of classes'
)
tf.app.flags.DEFINE_integer(
    'batch_size',
    1, #64
    'num of imgs in a batch'
)

###############################
# optimizer-- MomentumOptimizer
###############################
tf.app.flags.DEFINE_float(
    'momentum',
    0.9,
    'accumulation = momentum * accumulation + gradient'
)

############################
#  train
########################
tf.app.flags.DEFINE_integer(
    'max_steps',
    70000,
    'max iterate steps'
)

tf.app.flags.DEFINE_string(
    'pretrained_model_path',
    'gdrive/My\ Drive/FPN_TensorFlow-master/data/pretrained_weights/resnet_v1_50.ckpt',
    'the path of pretrained weights'
)
tf.app.flags.DEFINE_float(
    'weight_decay',
    0.0001,
    'weight_decay in regulation'
)
################################
# summary and save_weights_checkpoint
##################################
tf.app.flags.DEFINE_string(
    'summary_path',
    'res50_summary',
    'the path of summary write to '
)
tf.app.flags.DEFINE_string(
    'trained_checkpoint',
    'res50_trained_weights',
    'the path to save trained_weights'
)
FLAGS = tf.app.flags.FLAGS