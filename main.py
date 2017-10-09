from utils import to_categorical_4d, to_categorical_4d_reverse
from matplotlib import pyplot as plt
from skimage import io
from model4 import RedNet 
import tensorflow as tf
import numpy as np
import ear_pen

if __name__ == '__main__':
    (train_img, train_ann), (test_img, test_ann) = ear_pen.load_data()
    train_ann = np.asarray(train_ann) / 255
    train_ann, _map = to_categorical_4d(train_ann)
    
    img_ph = tf.placeholder(tf.float32, [None, 104, 78, 3])
    ann_ph = tf.placeholder(tf.int32, [None, 104, 78, 1])
    net = RedNet(img_ph, ann_ph)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for i in range(50):
            feed_dict = {
                img_ph: train_img[0:2],
                ann_ph: train_ann[0:2] 
            }
            _loss, _, _img = sess.run([net.loss, net.train_op, net.prediction], feed_dict=feed_dict)
            _img = np.asarray(to_categorical_4d_reverse(_img, _map)[0, :, :, :] * 255, dtype=int)            
            if i % 5 == 0:
                io.imsave(str(i)+'.png', _img)
                print('iter: ', i, '\tloss: ', _loss)