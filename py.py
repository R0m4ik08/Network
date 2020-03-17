import os,sys,glob
import numpy as np
from PIL import Image, ImageDraw
from keras.models import load_model
path = os.getcwd()

#Подгрузк сетей
Net =[]
Net.append(load_model(path + "/net/Зд.ул.h5")) ## Неправильная сеть
Net.append(load_model(path + "/net/Зд.ул.h5"))
Net.append(load_model(path + "/net/Д.н.h5"))
Net.append(load_model(path + "/net/Л.н.h5"))
Net.append(load_model(path + "/net/Од.мн.h5"))


# Сосздания белого холста
def im_in_white(im):
    draw = ImageDraw.Draw(im)
    width = im.size[0]
    height = im.size[1]
    pix = im.load()
    for i in range(width):
        for j in range(height):
            draw.point((i,j),(255,255,255))
    return(im)

# Подгон изображения в рамки размера
def podgon(path,size):
    imge = Image.open(path)
    imge.show()
    shape = imge.size
    if shape[0]>=shape[1]: 
        k = size[0]/shape[0]
    else:
         k = size[1]/shape[1]
    height = round(shape[0]*k)
    widht  = round(shape[1]*k)
    out_imge = imge.resize((height , widht))
    return(out_imge)

# Вставка изображения в холст
def past_im(holst,path_im,im):
    if im == None:  im = Image.open(path_im)
    draw = ImageDraw.Draw(holst)
    width = im.size[0]
    height = im.size[1]
    pix = im.load()
    for i in range(width):
        for j in range(height):
            r = pix[i,j][0] 
            g = pix[i,j][1] 
            b = pix[i,j][2]
            draw.point((i,j),(r,g,b))
    return(holst)

def predict_(inp):
    if inp[0]>= inp[1]:
        v = round(inp[0]*100)
        return [1,v]
    else:
        v = round(inp[1]*100)
        return[0,v];  
    
def selecting_photos(n):
    path_ = path +"/test/1 ({}).jpg".format(n);
    predict = []
    size = (400,400,3)
    holst = im_in_white(Image.new("RGB",size[:2]))
    imge = past_im(holst,'',im=podgon(path_,size[:2]))
    tabe = np.array(imge)/255
    tabe = tabe.reshape(1,400,400,3)
    
    #Net = load_model(path + "net/Те.h5")
    predict.append(predict_([0,100]))#(Net.predict(tabe)))
    if predict[0][0] == 1: 
        print("На фотографии текст с вероятностью {}_%".format(predict[0][1]))
    else:
        #Net = load_model(path + "net/Зд.ул.h5")
        predict.append(predict_(Net[1].predict(tabe)[0]))
        if predict[1][0] == 1: 
            print("Фотография сделана в здании с вероятностью {}_%".format(predict[1][1]))
        else:    
            print("Фотография сделана на улице с вероятностью {}_%".format(predict[1][1]))
        #Net = load_model(path + "net/Д.н.h5")
        predict.append(predict_(Net[2].predict(tabe)[0]))
        if predict[2][0] == 1: 
            print("Фотография сделана днём с вероятностью {}_%".format(predict[2][1]))
        else:    
            print("Фотография сделана ночью с вероятностью {}_%".format(predict[2][1]))
        #Net = load_model(path + "net/Л.н.h5")
        predict.append(predict_(Net[3].predict(tabe)[0]))
        if predict[3][0] == 1: 
            print("На фотографии присутствуют люди с вероятностью {}_%".format(predict[3][1]))
            #Net = load_model(path + "net/Од.мн.h5")
            predict.append(predict_(Net[4].predict(tabe)[0]))
            if predict[4][0] == 0: 
                    print("На фотографии более одного человека с вероятностью {}_%".format(predict[4][1]))
            else:    
                    print("На фотографии один человек с вероятностью {}_%".format(predict[4][1]))
        else:    
            print("На фотографии нет людей с вероятностью {}_%".format(predict[3][1]))
            predict.append(predict_([0,0]))                   
    holst = im_in_white(holst)

print("Выберите функцию \n 0 - Выбрать фотографию\n 1 - Выход")
a = int(input("Функция --"))
while a != 1:
    n = input("Номер теста ———>>> ");
    selecting_photos(n);
    print("Выберите функцию --\n 0 - Выбрать фотографию\n 1 - Выход")
    a = int(input("Функция -- "))