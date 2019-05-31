# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:58:39 2019

@author: Kuldeep
"""
import glob
from tkinter import*
from PIL import ImageTk,Image
import random
from tkinter.ttk import Progressbar
import time
import threading
import xlwt
import xlrd
import datetime
import shutil
import numpy as np
import os
import xlsxwriter
from os import path
absolutepath=path.abspath(path.curdir)
print(absolutepath)

from tkinter import filedialog
dirname ="global"
number_filesinbrowse ="global"

root = Tk()
root.geometry("530x630+0+0")
root.title("Cotton Image Processing")
root.resizable(width=False, height=False)


Tops = Frame(root,relief=SUNKEN)
Tops.pack(side=TOP)



f1 = Frame(root,relief=SUNKEN)
f1.pack(side=RIGHT)

f2 = Frame(root , relief=SUNKEN)
f2.pack(side=LEFT)


f3=Frame(root,relief=SUNKEN)
f3.pack(side=BOTTOM)

localtime=time.asctime(time.localtime(time.time()))
#-----------------INFO TOP------------
lblinfo = Label(Tops, font=( 'aria' ,32, 'bold' ),text="Cotton Image Processing",fg="steel blue",bd=10,anchor='w')
lblinfo.grid(row=0,column=0)


lblinfo = Label(Tops, font=( 'aria' ,14),text="1.Browse the folder to run process by clicking Browse Folder. ",fg="black",bd=7,anchor='w')
lblinfo.grid(row=1,column=0)

lblinfo = Label(Tops, font=( 'aria' ,14),text="2.After selecting folder click on Run button to run the process.",fg="black",bd=7,anchor='w')
lblinfo.grid(row=2,column=0)


#---------------Functions------------------
def start_pro():
    perogress.start()
    lblreference.grid(row=5,column=0)
    perogress.grid(column = 1, row = 5)




#--------------------------------------------------------------
def choosefolder():
    global dirname
    dirname = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a folder')
    if len(dirname ) > 0:
       print (dirname)
       list = os.listdir(dirname) 
       number_filesinbrowse = len(list)
       
       number_filesinbrowsek= "No of files in selected folder : " + str(number_filesinbrowse)
     
       lblforfiles = Label(Tops, font=( 'aria' ,14),text=(number_filesinbrowsek), fg="cyan4",bd=7,anchor='w')
       lblforfiles.grid(row=3,column=0)
       
       
       
       
       tday=datetime.date.today()
       print(tday)
       day=(tday.strftime("%d"))
       print(day)
       
       
       datefilepath='\\Date.xls'
       givingdatefile=absolutepath+datefilepath
       
       print(givingdatefile)
       
       
       loc = (givingdatefile) 
       # To open Workbook 
       wb = xlrd.open_workbook(loc) 
       sheet = wb.sheet_by_index(0) 
       # For row 0 and column 0 
       a1=sheet.cell_value(0, 0)
       a1_as_datetime = datetime.datetime(*xlrd.xldate_as_tuple(a1, wb.datemode))
       print('%s' % a1_as_datetime)
       pday=(a1_as_datetime.strftime("%d"))
       
       print(pday)
       if(day==pday):
           list = os.listdir(dirname) 
           number_filesinbrowse = len(list)
           modellodetime=100
           timefrun=6*number_filesinbrowse+modellodetime
           ttimefrun=" Estimated time required for image processing is : " + str(timefrun) + " Sec"
           lblfortimeestimation = Label(Tops, font=( 'aria' ,14),text=ttimefrun, fg="cyan4",bd=7,anchor='w')
           lblfortimeestimation.grid(row=4,column=0)   
       
       
       return(dirname)

#-------------------------------------------------------------------------------------------------------------


        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
def run():
    
    from keras.preprocessing import image
    from keras.models import Sequential
    from keras.layers import Convolution2D
    from keras.layers import MaxPooling2D
    from keras.layers import Flatten
    from keras.layers import Dense
    
    tday=datetime.date.today()
    print(tday)
    day=(tday.strftime("%d"))
    print(day)
    
    workbookk = xlwt.Workbook()
    worksheet = workbookk.add_sheet('Today')
    
    date_format = xlwt.XFStyle()
    
    date_format.num_format_str = 'yyyy/mm/dd'
    absolutepath=path.abspath(path.curdir)
    worksheet.write(0, 0, datetime.date.today(), date_format)
    datefilepath='\\Date.xls'
    givingdatefile=absolutepath+datefilepath
    
    loc = (givingdatefile) 
    # To open Workbook 
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    # For row 0 and column 0 
    a1=sheet.cell_value(0, 0)
    a1_as_datetime = datetime.datetime(*xlrd.xldate_as_tuple(a1, wb.datemode))
    print('%s' % a1_as_datetime)
    pday=(a1_as_datetime.strftime("%d"))

    print(pday)

    
    workbook = xlsxwriter.Workbook('Cottondata.xlsx')
    worksheet = workbook.add_worksheet('Cotton Data')
    
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'S.No', bold)
    worksheet.write('B1', 'File Name', bold)
    worksheet.write('C1', 'Cotton Crop Avilability', bold)
    worksheet.write('D1','Description', bold)
    worksheet.write('E1', 'Crop State', bold)
    worksheet.write('F1', 'Next Stage', bold)
    i=0
    Sno=0
    if(day==pday):
          from keras.models import load_model
          cottonmodel_path=load_model('ficodet.h5')
          ballmodel_path=load_model('balldetection.h5')
          purpledetectionmodel_path=load_model('purpledetectionmodel.h5')
          whitemodel_path=load_model('whitedetectionmodel.h5')
          
          
          image_path= os.chdir(dirname)
          for f in os.listdir(image_path):
              if f.endswith('.jpg'):
                  imagepath=os.path.realpath(f)
                  print(imagepath)
                  i+=1
                  Sno+=1
                  k=f
                  img = image.load_img(k, target_size=(64, 64))
                  x = image.img_to_array(img)
                  x = np.expand_dims(x, axis=0)
                  
                  images = np.vstack([x])
                  classes = cottonmodel_path.predict_classes(images, batch_size=10)
                 
                  if classes[0][0] == 1:
                      print('according to my prediction',(k) ,'is not cotton')
                      nc='NotCotton'
                      worksheet.write(i,0,Sno)
                      worksheet.write(i,1,k)
                      worksheet.write(i,2,nc)
                      worksheet.write(i,3,'NA')
                      worksheet.write(i,4,'NA')
                      worksheet.write(i,5,'NA')
                       
                      other="E:\\WRM\\cotton\\other"
                      
                      if not os.path.exists(other):
                          os.mkdir(other)
                          print("Directory " , other ,  " Created ")
                      else:    
                          print("Directory " , other ,  " already exists")
                          source =imagepath
                          otherfolderpath='\\cottontraining\\other'
                          copyotherfolder=absolutepath+otherfolderpath
                          destination =copyotherfolder
                          shutil.copy(source,destination)
                   
                  
                                    
                  else:
                      print('accoding to my prediction',(k), 'is cotton')
                      c='Cotton'
                      worksheet.write(i,0,k)
                      worksheet.write(i,1,c)
                      
                      source =imagepath
                      cottonfolderpath='\\cottontraining\\cotton'
                      copycottonfolder=absolutepath+cottonfolderpath
                      destination =copycottonfolder
                      shutil.copy(source,destination)
                      
                      
                      
                      
                      
                      img = image.load_img(k, target_size=(64, 64))
                      x = image.img_to_array(img)
                      x = np.expand_dims(x, axis=0)
                      
                      images = np.vstack([x])
                      classes = ballmodel_path.predict_classes(images, batch_size=10)
                      if classes[0][0] == 1:
                                                
                          print('according to my prediction',k, 'does not have cotton boll')
                          worksheet.write(i,0,Sno)
                          worksheet.write(i,1,k)
                          worksheet.write(i,2,'Cotton')
                          worksheet.write(i,3,'Only Cotton')
                          worksheet.write(i,4,'Cotton')
                          worksheet.write(i,5,'White Flower')
                          
                          
                          source =imagepath
                          balltrainingotherfolderpath='\\Balltraining\\other'
                          copyballtrainingotherfolderpath=absolutepath+balltrainingotherfolderpath
                          destination =copyballtrainingotherfolderpath
                          shutil.copy(source,destination)
                      
                      
                          img = image.load_img(k, target_size=(64, 64))
                          x = image.img_to_array(img)
                          x = np.expand_dims(x, axis=0)
                          
                          images = np.vstack([x])
                          classes = purpledetectionmodel_path.predict_classes(images, batch_size=10)
                          
                          if classes[0][0] == 1:
                              print('according to my prediction',k,'have purple flower')
                              worksheet.write(i,0,Sno)
                              worksheet.write(i,1,k)
                              worksheet.write(i,2,'Cotton')
                              worksheet.write(i,3,'Have Purple flower')
                              worksheet.write(i,4,'Purple Flower')
                              worksheet.write(i,5,'Boll Development')
                              source =imagepath
                              purpletrainingfolderpath='\\Purpletraining\\purpelflower'
                              purpletrainingfolderpathfolderpath=absolutepath+purpletrainingfolderpath
                              destination =purpletrainingfolderpathfolderpath
                              shutil.copy(source,destination)
                          
                           
                          else:
                              print('accoding to my prediction',k, 'dont have purple flower')
                              worksheet.write(i,0,k)
                              worksheet.write(i,1,c)
                              worksheet.write(i,2,'Not have purple flower')
                              
                              source =imagepath
                              purpletrainingotherfolderpath='\\Purpletraining\\other'
                              purpletrainingotherfolderpathfolderpath=absolutepath+purpletrainingotherfolderpath
                              destination =purpletrainingotherfolderpathfolderpath
                              shutil.copy(source,destination)
                              
                              
                              
                              img = image.load_img(k, target_size=(64, 64))
                              x = image.img_to_array(img)
                              x = np.expand_dims(x, axis=0)
                              
                              images = np.vstack([x])
                              classes = whitemodel_path.predict_classes(images, batch_size=10)
                              if classes[0][0] == 1:
                                  print('according to my prediction',k,'have white flower')
                                  worksheet.write(i,0,Sno)
                                  worksheet.write(i,1,k)
                                  worksheet.write(i,2,'Cotton')
                                  worksheet.write(i,3,'Have White Flower')
                                  worksheet.write(i,4,'White Flower')
                                  worksheet.write(i,5,'purple Flower')
                                  
                                  source =imagepath
                                  whitetrainingfolderpath='\\whiteflowertraining\\white'
                                  whitetrainingfolderpathfolderpath=absolutepath+whitetrainingfolderpath
                                  destination =whitetrainingfolderpathfolderpath
                                  shutil.copy(source,destination)
                               
                                
                                
                              else:
                                  print('accoding to my prediction',k,'does not have white flower')
                                  worksheet.write(i,0,Sno)
                                  worksheet.write(i,1,k)
                                  worksheet.write(i,2,'Cotton')
                             
                       
                      else:
                           print('accoding to my prediction',k,'have cotton boll')
                           worksheet.write(i,0,Sno)
                           worksheet.write(i,1,k)
                           worksheet.write(i,2,'Cotton')
                           worksheet.write(i,3,'Cotton Ball')
                           worksheet.write(i,4,'Boll Stage')
                           worksheet.write(i,5,'Boll Busting')
                           source =imagepath
                           balltrainingfolderpath='\\Balltraining\\balls'
                           balltrainingfolderpathfolderpath=absolutepath+balltrainingfolderpath
                           destination =balltrainingfolderpathfolderpath
                           shutil.copy(source,destination)
                           
                           
                           
                           
          workbook.close()
          datefilepath='\\Date.xls'
          givingdatefile=absolutepath+datefilepath               
          workbookk.save(givingdatefile)
        
          lblreference.grid(row=5, column=0,pady=10)
          lblinfoexcelpathswo.grid(row=9,column=0)


    elif(day!=pday):
        cottonmodel = Sequential() 
        cottonmodel.add(Convolution2D(filters = 32, kernel_size = (3, 3),input_shape = (64, 64, 3),activation = 'relu'))
        
        cottonmodel.add(MaxPooling2D(pool_size = (2, 2)))
        cottonmodel.add(Convolution2D(32, 3, 3, activation = 'relu'))
        cottonmodel.add(MaxPooling2D(pool_size = (2, 2)))
        cottonmodel.add(Flatten())
        cottonmodel.add(Dense(units = 128, activation = 'relu'))
        cottonmodel.add(Dense(units = 1, activation = 'sigmoid'))
        cottonmodel.compile(optimizer = 'adam',loss = 'binary_crossentropy', metrics = ['accuracy'])
        
        from keras.preprocessing.image import ImageDataGenerator
        train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.1, zoom_range = 0.2, horizontal_flip = True) 
        test_datagen = ImageDataGenerator(rescale = 1./255)
        training_set = train_datagen.flow_from_directory('cottontraining', target_size = (64, 64),batch_size = 32,class_mode = 'binary')
        test_set = test_datagen.flow_from_directory('cottontesting',target_size = (64, 64),batch_size = 32,class_mode = 'binary')
        
        
        absolutepath=path.abspath(path.curdir)
        addcottontrainingpath='\\cottontraining\\cotton'
        cottoncounting=absolutepath+addcottontrainingpath
        list = os.listdir(cottoncounting) # dir is your directory path
        number_filestrainingcotton = len(list)
        print(number_filestrainingcotton)
        
        absolutepath=path.abspath(path.curdir)
        addcottontrainingotherpath='\\cottontraining\\other'
        cottonothercounting=absolutepath+addcottontrainingotherpath
        list = os.listdir(cottonothercounting) # dir is your directory path
        number_filestrainingcottonother = len(list)
        print(number_filestrainingcottonother)
        total_cootontraining=number_filestrainingcotton+number_filestrainingcottonother
        noofcottonepoch=int(total_cootontraining)/32
        
        cottonmodel.fit_generator(training_set, samples_per_epoch = 500,nb_epoch = noofcottonepoch,validation_data = test_set,nb_val_samples = 100)
        cottonmodel.save('ficodet.h5')   
        
        absolutepath=path.abspath(path.curdir)
        print(absolutepath)
        balldetectionmodel = Sequential() 
        balldetectionmodel.add(Convolution2D(filters = 32, kernel_size = (3, 3),input_shape = (64, 64, 3),activation = 'relu'))
                    
        balldetectionmodel.add(MaxPooling2D(pool_size = (2, 2)))
        balldetectionmodel.add(Convolution2D(32, 3, 3, activation = 'relu'))
        balldetectionmodel.add(MaxPooling2D(pool_size = (2, 2)))
        balldetectionmodel.add(Flatten())
        balldetectionmodel.add(Dense(units = 128, activation = 'relu'))
        balldetectionmodel.add(Dense(units = 1, activation = 'sigmoid'))
        balldetectionmodel.compile(optimizer = 'adam',loss = 'binary_crossentropy', metrics = ['accuracy'])
                     
        from keras.preprocessing.image import ImageDataGenerator
        train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.1, zoom_range = 0.2, horizontal_flip = True)
        test_datagen = ImageDataGenerator(rescale = 1./255)
        training_set = train_datagen.flow_from_directory('Balltraining', target_size = (64, 64), batch_size = 32,class_mode = 'binary')
        test_set = test_datagen.flow_from_directory('Balltesting',target_size = (64, 64),batch_size = 32,class_mode = 'binary')
                    
        print(absolutepath)
        absolutepath=path.abspath(path.curdir)
        addballtrainingpath='\\Balltraining\\balls'
        ballcounting=absolutepath+addballtrainingpath
        print(ballcounting)
        list = os.listdir(ballcounting) # dir is your directory path
        number_filestrainingball = len(list)
        print(number_filestrainingball)
        
        absolutepath=path.abspath(path.curdir)
        addballtrainingotherpath='\\Balltraining\\other'
        ballothercounting=absolutepath+addballtrainingotherpath
        list = os.listdir(ballothercounting) # dir is your directory path
        number_filestrainingballother = len(list)
        print(number_filestrainingballother)
        total_balltraining=number_filestrainingball+number_filestrainingballother
        noofballepoch=int(total_balltraining)/32
                    
        balldetectionmodel.fit_generator(training_set, samples_per_epoch = 500, nb_epoch =  noofballepoch, validation_data = test_set, nb_val_samples = 100)
        balldetectionmodel.save('balldetection.h5')
                    
                        
                 
        purpledetectionmodel = Sequential() 
        purpledetectionmodel.add(Convolution2D(filters = 32, kernel_size = (3, 3),input_shape = (64, 64, 3), activation = 'relu'))
        
        purpledetectionmodel.add(MaxPooling2D(pool_size = (2, 2)))
        purpledetectionmodel.add(Convolution2D(32, 3, 3, activation = 'relu'))
        purpledetectionmodel.add(MaxPooling2D(pool_size = (2, 2)))
        purpledetectionmodel.add(Flatten())
        purpledetectionmodel.add(Dense(units = 128, activation = 'relu'))
        purpledetectionmodel.add(Dense(units = 1, activation = 'sigmoid'))
        purpledetectionmodel.compile(optimizer = 'adam',loss = 'binary_crossentropy', metrics = ['accuracy'])
                        
        from keras.preprocessing.image import ImageDataGenerator
        train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.1, zoom_range = 0.2, horizontal_flip = True)
        test_datagen = ImageDataGenerator(rescale = 1./255)
        training_set = train_datagen.flow_from_directory('Purpletraining', target_size = (64, 64),batch_size = 32,class_mode = 'binary')
        test_set = test_datagen.flow_from_directory('Purpletesting',target_size = (64, 64),batch_size = 32,class_mode = 'binary')
                        
                        
        absolutepath=path.abspath(path.curdir)
        addpurpletrainingpath='\\Purpletraining\\purpelflower'
        purplecounting=absolutepath+addpurpletrainingpath
        list = os.listdir(purplecounting) # dir is your directory path
        number_filestrainingpurple = len(list)
        print(number_filestrainingpurple)
                        
        absolutepath=path.abspath(path.curdir)
        addpurpletrainingotherpath='\\Purpletraining\\other'
        purpleothercounting=absolutepath+addpurpletrainingotherpath
        list = os.listdir(purpleothercounting) # dir is your directory path
        number_filestrainingpurpleother = len(list)
        print(number_filestrainingpurpleother)
        total_purpletraining=number_filestrainingpurple+number_filestrainingpurpleother
        noofpurpleepoch=int(total_purpletraining)/32
                        
                        
        purpledetectionmodel.fit_generator(training_set, samples_per_epoch = 500, nb_epoch = noofpurpleepoch, validation_data = test_set, nb_val_samples = 100)
                        
        
                    
                        
        purpledetectionmodel.save('purpledetectionmodel.h5')
                        
        whitedetectionmodel = Sequential() 
        whitedetectionmodel.add(Convolution2D(filters = 32, kernel_size = (3, 3),input_shape = (64, 64, 3), activation = 'relu'))
        
        whitedetectionmodel.add(MaxPooling2D(pool_size = (2, 2)))
        
        whitedetectionmodel.add(Convolution2D(32, 3, 3, activation = 'relu'))
        whitedetectionmodel.add(MaxPooling2D(pool_size = (2, 2)))
        whitedetectionmodel.add(Flatten())
        whitedetectionmodel.add(Dense(units = 128, activation = 'relu'))
        whitedetectionmodel.add(Dense(units = 1, activation = 'sigmoid'))
        whitedetectionmodel.compile(optimizer = 'adam',loss = 'binary_crossentropy', metrics = ['accuracy'])
        from keras.preprocessing.image import ImageDataGenerator
        train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.1, zoom_range = 0.2, horizontal_flip = True)
        test_datagen = ImageDataGenerator(rescale = 1./255)
        
        training_set = train_datagen.flow_from_directory('whiteflowertraining', target_size = (64, 64), batch_size = 32,class_mode = 'binary')
        test_set = test_datagen.flow_from_directory('whiteflowertesting',target_size = (64, 64),batch_size = 32,class_mode = 'binary')
        
        
        absolutepath=path.abspath(path.curdir)
        addwhitetrainingpath='\\whiteflowertraining\\white'
        whitecounting=absolutepath+addwhitetrainingpath
        list = os.listdir(whitecounting) # dir is your directory path
        number_filestrainingwhite = len(list)
        print(number_filestrainingwhite)
        
        absolutepath=path.abspath(path.curdir)
        addwhitetrainingotherpath='\\whiteflowertraining\\other'
        whiteothercounting=absolutepath+addwhitetrainingotherpath
        list = os.listdir( whiteothercounting) # dir is your directory path
        number_filestrainingwhiteother = len(list)
        print(number_filestrainingwhiteother)
        total_whitetraining=number_filestrainingwhite+number_filestrainingwhiteother
        noofwhiteepoch=int(total_whitetraining)/32
        
        whitedetectionmodel.fit_generator(training_set, samples_per_epoch = 500, nb_epoch = noofwhiteepoch, validation_data = test_set, nb_val_samples = 100)
        whitedetectionmodel.save('whitedetectionmodel.h5')
        
        
        from keras.models import load_model
        cottonmodel_path=load_model('ficodet.h5')
        ballmodel_path=load_model('balldetection.h5')
        purpledetectionmodel_path=load_model('purpledetectionmodel.h5')
        whitemodel_path=load_model('whitedetectionmodel.h5')
        image_path= os.chdir(dirname)
        for f in os.listdir(image_path):
            if f.endswith('.jpg'):
                imagepath=os.path.realpath(f)
                print(imagepath)
                i+=1
                Sno+=1
                k=f
                img = image.load_img(k, target_size=(64, 64))
                x = image.img_to_array(img)
                x = np.expand_dims(x, axis=0)
                  
                images = np.vstack([x])
                classes = cottonmodel_path.predict_classes(images, batch_size=10)
                 
                
                if classes[0][0] == 1:
                    print('according to my prediction',(k) ,'is not cotton')
                    nc='NotCotton'
                    worksheet.write(i,0,Sno)
                    worksheet.write(i,1,k)
                    worksheet.write(i,2,nc)
                    worksheet.write(i,3,'NA')
                    worksheet.write(i,4,'NA')
                    worksheet.write(i,5,'NA')
                       
                    other="E:\\WRM\\cotton\\other"
                      
                    if not os.path.exists(other):
                        os.mkdir(other)
                        print("Directory " , other ,  " Created ")
                    else:
                        print("Directory " , other ,  " already exists")
                        source =imagepath
                        otherfolderpath='\\cottontraining\\other'
                        copyotherfolder=absolutepath+otherfolderpath
                        destination =copyotherfolder
                        shutil.copy(source,destination)
                   
                  
                                    
                else:
                    print('accoding to my prediction',(k), 'is cotton')
                    c='Cotton'
                    worksheet.write(i,0,k)
                    worksheet.write(i,1,c)
                    
                    source =imagepath
                    cottonfolderpath='\\cottontraining\\cotton'
                    copycottonfolder=absolutepath+cottonfolderpath
                    destination =copycottonfolder
                    shutil.copy(source,destination)
                      
                      
                      
                      
                      
                    img = image.load_img(k, target_size=(64, 64))
                    x = image.img_to_array(img)
                    x = np.expand_dims(x, axis=0)
                      
                    images = np.vstack([x])
                    classes = ballmodel_path.predict_classes(images, batch_size=10)
                    if classes[0][0] == 1:
                        print('according to my prediction',k, 'does not have cotton boll')
                        worksheet.write(i,0,Sno)
                        worksheet.write(i,1,k)
                        worksheet.write(i,2,'Cotton')
                        worksheet.write(i,3,'Only Cotton')
                        worksheet.write(i,4,'Cotton')
                        worksheet.write(i,5,'White Flower')
                          
                          
                        source =imagepath
                        balltrainingotherfolderpath='\\Balltraining\\other'
                        copyballtrainingotherfolderpath=absolutepath+balltrainingotherfolderpath
                        destination =copyballtrainingotherfolderpath
                        shutil.copy(source,destination)
                      
                                                
                        img = image.load_img(k, target_size=(64, 64))
                        x = image.img_to_array(img)
                        x = np.expand_dims(x, axis=0)
                          
                        images = np.vstack([x])
                        classes = purpledetectionmodel_path.predict_classes(images, batch_size=10)
                          
                        if classes[0][0] == 1:
                            print('according to my prediction',k,'have purple flower')
                            worksheet.write(i,0,Sno)
                            worksheet.write(i,1,k)
                            worksheet.write(i,2,'Cotton')
                            worksheet.write(i,3,'Have Purple flower')
                            worksheet.write(i,4,'Purple Flower')
                            worksheet.write(i,5,'Boll Development')
                            source =imagepath
                            purpletrainingfolderpath='\\Purpletraining\\purpelflower'
                            purpletrainingfolderpathfolderpath=absolutepath+purpletrainingfolderpath
                            destination =purpletrainingfolderpathfolderpath
                            shutil.copy(source,destination)
                          
                           
                        else:
                            print('accoding to my prediction',k, 'dont have purple flower')
                            worksheet.write(i,0,k)
                            worksheet.write(i,1,c)
                            worksheet.write(i,2,'Not have purple flower')
                            
                            source =imagepath
                            purpletrainingotherfolderpath='\\Purpletraining\\other'
                            purpletrainingotherfolderpathfolderpath=absolutepath+purpletrainingotherfolderpath
                            destination =purpletrainingotherfolderpathfolderpath
                            shutil.copy(source,destination)
                              
                              
                              
                            img = image.load_img(k, target_size=(64, 64))
                            x = image.img_to_array(img)
                            x = np.expand_dims(x, axis=0)
                              
                            images = np.vstack([x])
                            classes = whitemodel_path.predict_classes(images, batch_size=10)
                            if classes[0][0] == 1:
                                print('according to my prediction',k,'have white flower')
                                worksheet.write(i,0,Sno)
                                worksheet.write(i,1,k)
                                worksheet.write(i,2,'Cotton')
                                worksheet.write(i,3,'Have White Flower')
                                worksheet.write(i,4,'White Flower')
                                worksheet.write(i,5,'purple Flower')
                                
                                source =imagepath
                                whitetrainingfolderpath='\\whiteflowertraining\\white'
                                whitetrainingfolderpathfolderpath=absolutepath+whitetrainingfolderpath
                                destination =whitetrainingfolderpathfolderpath
                                shutil.copy(source,destination)
                               
                                
                                
                            else:
                                print('accoding to my prediction',k,'does not have white flower')
                                worksheet.write(i,0,Sno)
                                worksheet.write(i,1,k)
                                worksheet.write(i,2,'Cotton')
                             
                       
                    else:
                        print('accoding to my prediction',k,'have cotton boll')
                        worksheet.write(i,0,Sno)
                        worksheet.write(i,1,k)
                        worksheet.write(i,2,'Cotton')
                        worksheet.write(i,3,'Cotton Ball')
                        worksheet.write(i,4,'Boll Stage')
                        worksheet.write(i,5,'Boll Busting')
                        source =imagepath
                        balltrainingfolderpath='\\Balltraining\\balls'
                        balltrainingfolderpathfolderpath=absolutepath+balltrainingfolderpath
                        destination =balltrainingfolderpathfolderpath
                        shutil.copy(source,destination)
                           
                           
                           
                           
        workbook.close()
        datefilepath='\\Date.xls'
        givingdatefile=absolutepath+datefilepath               
        workbookk.save(givingdatefile)
        lblreference.grid(row=5, column=0,pady=10)
        lblinfoexcelpathswo.grid(row=9,column=0)
        return(dirname)           
        

'''++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''

lblreference = Label(f2, font=( 'aria' ,14, 'bold' ),text="Process Completed !",fg="cyan4",bd=5,anchor='w')
#lblreference.grid(row=5, column=0,pady=10)
pathshowkliye="You can view detailed image processing result in excel file \n from selected folder."                                             
lblinfoexcelpathswo = Label(f2, font=( 'aria' ,14),text= pathshowkliye,fg="cyan4",bd=4,anchor='w')
#lblinfoexcelpathswo.grid(row=9,column=0)


lblinfornote = Label(f2, font=( 'aria' ,14),text="Note- Please review Training set folders where exe placed. \n Delete if any wrong image exist there. This is important \n before starting process otherwise system will train on wrong \n dataset and predictions will be wrong.                       ",fg="red4",bd=4,anchor='w')
lblinfornote.grid(row=10,column=0)





#-----------------------------------------buttons------------------------------------------


btncf=Button(f2,padx=10,pady=5, bd=5 ,fg="black",font=('ariel' ,16,'bold'),width=10, text="Browse Folder", bg="powder blue",command=choosefolder)
btncf.grid(row=0,column=0, pady=25)



btnrun=Button(f2,padx=10,pady=5, bd=5 ,fg="black",font=('ariel' ,16,'bold'),width=8, text="Run", bg="powder blue", command= run)
btnrun.grid(row=3, column=0, padx=50)




root.mainloop()
