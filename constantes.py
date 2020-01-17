import os



LOGSFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs.txt") #arquivo de logs

DCMTEMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dcmTemp/") #diretorio onde os arquivos provenientes do aparelho ficarao temporariamente antes de serem processados.

DCMRECEIVED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dcmReceived/") #diretorio onde os arquivos dcm processados serao armazenados organizados por data


