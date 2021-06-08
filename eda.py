'''
EDA - Exploratory Data Analysis
(limpar os dados)
'''
import os
import glob
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
from IPython.display import display



def CreateDataFrame(data_path):

    data_frame = pd.read_csv(
        data_path,
        sep=',',  # ver separador dos dados
        header=0  # First row corresponds to the headers
    )
    return data_frame

# .gz sao imagens de ressonância, nao quero usar.


def FilterDataFrame(data_frame):

    # remove all lines that contain .gz
    filter_images = data_frame['filename'].str.contains('.jpg|.png|.jpeg|.JPG')
    data_frame = data_frame[filter_images]
    # filtering coluns
    data_frame = data_frame[['patientid', 'finding', 'filename']]

    return data_frame


def ShowInfo(data_frame):

    print('---------------------------------')

    # Identify how many and which diseases the dataset contains
    print(
        f"This dataset has {len(data_frame['finding'].unique())} unique diseases and they are: \n{data_frame['finding'].unique()}")
    # Identify how many unique patients the dataset contains
    print(
        f"This dataset has {len(data_frame['patientid'].unique())} unique patients")

    print('---------------------------------')

    # show some images
    cv2.namedWindow('T', 0)  # 0 é a tela padrao

    for i in range(5):
        image_path = data_frame['filename'][i]
        # read images in colors RGB
        # 1 para imagem colorida e 0 para imagem preto e branco
        image = cv2.imread(os.path.join('images', image_path), 1)

        # Show image on widow 'T'
        
        cv2.imshow('T', image)
        # OpenCV wait for the user to close the widow (parametro em milisegundos)
        cv2.waitKey(0)
    
    return

def FilterClasses2Bool(data_frame):
    print('---------------------------------')

    filter_classes = data_frame['finding'].str.contains("COVID")
    
    data_frame.finding = filter_classes
     

    # Show how many covid cases have in finding colum

    print(filter_classes.value_counts())
    
    print('---------------------------------')
    return data_frame

def PlotClassFrequency(data_frame):
    filter_positive_cases = data_frame["finding"] == True
    # Valuecounts return a list with true and false values, we want only true (in positive cases)
    # and false (in nagative cases), so we need to acess the index of this lists, using [0], [1]...etc
    num_positive_cases = filter_positive_cases.value_counts()[1]
    num_negative_cases = filter_positive_cases.value_counts()[0]
    
    frequency_pos_cases = 100*num_positive_cases/ (num_negative_cases + num_positive_cases)
    frequency_neg_cases = 100*num_negative_cases/ (num_negative_cases + num_positive_cases)
    

    plt.bar(

        x = ["Positive Cases", "Negative Cases"],
        height= [frequency_pos_cases, frequency_neg_cases],
        width=0.8,
        color = "#CD4446",
        bottom = 0,
        align = 'center',

        edgecolor= "#113759")
           
    
    plt.show()
    return


    
    





def SplitDataSetByPatientID(data_frame):
    print('---------------------------------')
    
    
    patientids = data_frame['patientid'].unique()

    
    train_dataset = data_frame['patientid'].sample(frac=0.95, random_state=0)
    validation_dataset = data_frame['patientid'].drop(train_dataset.index)    

    print(train_dataset.to_list())
    print(validation_dataset.to_list())


    print('---------------------------------')
    return data_frame


if __name__ == '__main__':  # se este arquivo for importado em outro arquivo, esse script nao será executado

    # list all images on ..\images\
    # using the glob and os modules

    # caminho relativo até a pasta (sempre melhor usar ao inves do absoluto, evita de mostar nome do user, etc)
    folder_path = '..\images'

    # glob.glob pega todos os arquivos de um caminho
    # os.path.join concateca os caminhos
    images_list = glob.glob(os.path.join(folder_path, '*.jpg'))
    images_list += glob.glob(os.path.join(folder_path, '*.jpeg'))
    images_list += glob.glob(os.path.join(folder_path, '*.png'))
    images_list += glob.glob(os.path.join(folder_path, '*.JPG'))

    print(images_list[:10])  # listando até o numero 10

    # -------------------------------------- --- ------------------------------


    data_path = 'metadata.csv'
    data_frame = CreateDataFrame(data_path)
    data_frame = FilterDataFrame(data_frame)
    #ShowInfo(data_frame)
    data_frame = FilterClasses2Bool(data_frame)
    print(data_frame)
    #PlotClassFrequency(data_frame)
    SplitDataSetByPatientID(data_frame)
    
    

    pass
