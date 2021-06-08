import numpy as np
import pandas as pd
import cv2
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
class DataLoader:

    def __init__ (self, train_dataframe, validation_dataframe, image_dir):

        self.train_dataframe =train_dataframe
        self.validation_dataframe = validation_dataframe
        self.image_dir = image_dir


        return

    def CreateImageGenerator(self):

        #Normalize the image and perform angle rotation as a data augmentation techinique
        self.train_image_generator = ImageDataGenerator(

            rescale = 1.0/255.0,
            rotation_range= 30,
            fill_mode = 'nearest'

        )

        self.validation_image_generator = ImageDataGenerator(

            rescale = 1.0/255.0

        )

    def CreateDataLoader(self):

        self.train_data_loader = self.train_image_generator.flow_from_dataframe(
            
            dataframe=self.train_dataframe,
            directory = self.image_dir,
            x_col = "filename",
            y_col = "finding",
            class_mode="binary",
            batch_size=2, #images per batch
            shuffle=True,
            target_size= (416,416) 

        )

        self.validation_data_loader = self.train_image_generator.flow_from_dataframe(
            dataframe=self.train_dataframe,
            directory = self.image_dir,
            x_col = "filename",
            y_col = "finding",
            class_mode="binary",
            batch_size=1, #images per batch
            shuffle=True,
            target_size= (416,416) 

        )

        return

if __name__ == '__main__':


 pass