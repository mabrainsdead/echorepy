import time
from pydicom.tag import Tag
import os
from datetime import datetime

from constantes import LOGSFILE, DCMTEMP, DCMRECEIVED #arquivo de log



def logger(msg): #funcao de log na tela e no arquivo logs.txt
    
    a = open(LOGSFILE, 'a')
    a.write(time.strftime("%d-%m-%Y  %H:%M:%S")+ " : " + str(msg) + "\n")  
    print(time.strftime("%d-%m-%Y  %H:%M:%S")+ " : " + str(msg) + "\n")
    a.close
    
def getTag(ds, group, element): #funcao para pegar as tags
    val = ''
    if Tag("0x" + group, "0x" + element) in ds:
        val = ds["0x" + group, "0x" + element].value
    else:
        val = ""
    return (val)

def dcmToMp4(file, folder):
    os.system("dcmj2pnm +Fa +oj +Jq 100 " + DCMTEMP + file + " "  + folder + "/frame" ) #fatia o video dicom em multiplos jpeg no diretorio mp4
    
    os.chdir(folder )    #muda o cursor para o diretorio folder/mp4
    for filename in os.listdir("."):
        if filename.startswith("frame."):
            os.rename(filename, filename[6:]) #tira o frame do nome do arquivo deixa so o numero do quadro
            
    for filename in os.listdir("."): #acrescenta 0s no nome do arquivo jpeg
        if filename.endswith("jpg"):
            if len(filename) == 6: 
                os.rename(filename, "0"+filename)
            elif len(filename) == 5:
                os.rename(filename, "00"+filename)
                
    os.system("ffmpeg -r 24 -i %03d.jpg -vcodec libx264 -pix_fmt yuv420p -b:v 5000k " + folder +"/"+ file + ".mp4")
    
    for filename in os.listdir("."):
        if filename.endswith("jpg"):
            os.remove(filename)
    
                
                
def dcmToJpg(dcmfile, jpgfolder):
    os.system("dcmj2pnm +oj +Jq 100 " + DCMTEMP +  dcmfile + " "  + jpgfolder)                
                
    
def dcm2xml(dcmFile, folder):
    os.system("dsr2xml -v " + folder + dcmFile + " > " + folder + "sr/" + dcmFile + ".xml" )