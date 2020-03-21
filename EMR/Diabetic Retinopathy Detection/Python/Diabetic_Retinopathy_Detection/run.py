import numpy as np
import cv2, os
import sys
import pandas as pd
import tensorflow as tf

from model import Tensorflow_Model

class dl_model():

    EXT_TRAIN_DATA = 'train'
    EXT_TEST_DATA = 'test'
    EXT_TRAIN_CSV = 'trainLabels.csv'
    
    IMAGE_WIDTH = 512 #1536
    IMAGE_HEIGHT = 340 #1024
    N_CHANNELS = 3
    
    GENERATOR_BATCH_SIZE = 100
    NB_EPOCH_PER_BATCH = 2
    NB_EPOCH = 5
    
    def __init__(self, argv):
        print(argv)

        self.argv = argv
        self.BASE_PATH = './data'   #argv[0]
        print(self.BASE_PATH)
        self.dims_image = {'width': self.IMAGE_WIDTH, 'height': self.IMAGE_HEIGHT, 'channel': self.N_CHANNELS}
        self.dims_output = 5
    
    def get_image_name_list(self, path, train_or_not):
        if train_or_not:
            training_csv = pd.read_csv(path)
            headers = training_csv.columns
            return np.array([training_csv[headers[0]], training_csv[headers[1]]])
        else:
            return np.array([os.listdir(path)])

    def get_image_names(self):
        self.train_image_names_with_labels = self.get_image_name_list(os.path.join(self.BASE_PATH, self.EXT_TRAIN_CSV), 1) # returns a tuple
        self.test_image_names = self.get_image_name_list(os.path.join(self.BASE_PATH, self.EXT_TEST_DATA), 0) # returns just names

        print('Number of training images: {}\nNumber of testing images: {}'.format(len(self.train_image_names_with_labels[0]), len(self.test_image_names[0])))

    def image_transformation(self, image_path):
        img = cv2.imread(image_path)
        img = cv2.resize(img, (self.IMAGE_WIDTH, self.IMAGE_HEIGHT))
        return np.array(img).reshape((self.IMAGE_HEIGHT, self.IMAGE_WIDTH, self.N_CHANNELS))

    def image_batch_generator(self, array, batch_size, ext):

        print(batch_size)

        path = os.path.join(self.BASE_PATH, ext)
        # for i in range(0, len(array[0]), len(array[0])):
        for i in range(0, len(array[0]), batch_size):
        #     print(len(array[0]))
        #     print(i)
        #     print(batch_size)

            batch = array[0][i: i+batch_size]
            data_batch = []
            for j, image_name in enumerate(batch):
                try:
                    if ext == self.EXT_TRAIN_DATA:
                        image_path = '{}.jpeg'.format(os.path.join(path, image_name))
                        data_batch.append((self.image_transformation(image_path), array[1][i+j]))
                    else:
                        image_path = '{}'.format(os.path.join(path, image_name))
                        data_batch.append(self.image_transformation(image_path))
                except:
                    print('Error reading: {}'.format(image_path))

            # return data_batch;
            yield(np.array(data_batch))

    
    def execute(self):
        with tf.device('/cpu:0'):
            self.get_image_names()
            # training_batch_generator = self.image_batch_generator(self.train_image_names_with_labels,
            #                                                       len(self.train_image_names_with_labels[0]), self.EXT_TRAIN_DATA)
            training_batch_generator = self.image_batch_generator(self.train_image_names_with_labels, self.GENERATOR_BATCH_SIZE, self.EXT_TRAIN_DATA)
            tf_model = Tensorflow_Model(self.dims_image, self.dims_output) # CALCULATE dims_output
            

            # TRAINING PHASE
            for i, training_batch in enumerate(training_batch_generator):
                if i== 0:
                    tf_model.train(training_batch)


                # if not i > self.NB_EPOCH:
                #     tf_model.train(training_batch)
                # else:
                #     break


#        test_batch_generator = self.image_batch_generator(self.test_image_names, self.BATCH_SIZE, self.EXT_TEST_DATA)


if __name__ == '__main__':
    dl_model(sys.argv).execute()
