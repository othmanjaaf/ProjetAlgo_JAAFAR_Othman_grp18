# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime 

data=pd.read_csv('EIVP_KM.csv', sep=';', index_col=0)


#Calcul de l'humidex et rajout aux dataframes

e=6.112*10*( 7.5*data['temp'] / (237.7+data['temp']) )*data['humidity']/100
h=5/9*(e- 10.0)
humidex=data['temp']+h
humidex.name = 'humidex'
data=pd.concat([data, humidex], axis = 1)
data=data.reindex(columns = ['noise', 'temp', 'humidity','humidex','lum','co2','sent_at']) 

#Separations en 6 tableaux pour chaque capteur

data1=data.loc['1'] #1336 rows
data2=data.loc['2'] #1345 rows
data3=data.loc['3'] #1345 rows
data4=data.loc['4'] #1344 rows
data5=data.loc['5'] #1165 rows
data6=data.loc['6'] #1345 rows se deroule 1 mois avant on le supprime de l'étude de simililarités

#Fais correspondre les dates de début et de fin de tous les capteurs
data1=data1[data1['sent_at']<data2['sent_at'].max()]
data2=data2[data2['sent_at']>data1['sent_at'].min()]
data3=data3[data3['sent_at']>data1['sent_at'].min()]
data4=data4[data4['sent_at']>data1['sent_at'].min()]
data5=data5[data5['sent_at']>data1['sent_at'].min()]

#transformation de la colonne temps en liste
timelist1= data1["sent_at"].tolist()
timelist2= data2["sent_at"].tolist() 
timelist3= data3["sent_at"].tolist() 
timelist4= data4["sent_at"].tolist()     

#fonction qui retire les mesures du 22 septembre 2020
def enlevele22(listetemp):
    L1=listetemp
    L=[]
    for i in range (len(L1)):
       if (int(L1[i][8])==2 and int(L1[i][9])==2):
           L1[i]=0
           L=L+[i]
    del L1[980:1075]
    return L1

#reindaxion des dataframes
data1.reset_index(drop = True, inplace = True) 
data2.reset_index(drop = True, inplace = True) 
data3.reset_index(drop = True, inplace = True) 
data4.reset_index(drop = True, inplace = True) 

#supprimer toutes les valeurs correspondants au 22 dans les dataframes

data1.drop([i for i in range(980,1075)], inplace=True)
data2.drop([i for i in range(980,1075)], inplace=True)
data3.drop([i for i in range(980,1075)], inplace=True)
data4.drop([i for i in range(980,1075)], inplace=True)

#trace l'evolution temporelle des variables(le capteur 1 par exemple)


plt.plot(data1['sent_at'],data1['temp'])
m=data1['temp'].mean()#Calcul de latemperature moyenne sur le capteur 1
plt.title('Courbe de la temperature en °C')
plt.show()
   
#Calcul de l'indice de corrélation pour la temperature par ex au sens de Pearson

print(data1['temp'].corr(data2['temp']))

        

    
    