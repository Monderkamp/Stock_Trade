"""
bei increment 5.0 und 4 Aktien ruft er ca alle 10 Sek. die Daten ab.
d.h 1.25 Sekunden pro Abrufen (lokale Prozessor-rechenzeit nicht eingerechnet. aber die sollte minimal sein)

Nach 1:19h Laufzeit sind ca 48 kB Daten mit 4 Aktien entstanden. 
Das entspricht 36 kB pro Stunde bei 4 Aktien + Uhrzeit. 
Das sind ca 7kB pro Stunde pro Aktie und 7kB Pro Stunde fuer Uhrzeit

Daten (D) pro Stunde ca. 
D = (1 + n)*7kB,
mit n = Anzahl der Aktien 
"""
import time as tm
import numpy as np
import pandas as pd
from yahoo_fin import stock_info as si


def get_time():
  Zeit = tm.asctime(tm.localtime())
  Tag = Zeit[-4:] + '_' + Zeit[4:7]+ '_' + Zeit[8:10] +  '_' + Zeit[0:3]  
  Uhrzeit = Zeit[11:20]
  Stunde = int(Uhrzeit[0:2])
  Minute = int(Uhrzeit[3:5])
  Sekunde = int(Uhrzeit[6:8])
  return([Zeit,Tag,Uhrzeit,Stunde,Minute,Sekunde])

def calc_time_until(StundeX,MinuteX,SekundeX):
  [Zeit,Tag,Uhrzeit,Stunde,Minute,Sekunde] = get_time()
  dStunde = StundeX - Stunde
  if dStunde < 0:
    dStunde += 24
  dMinute = MinuteX - Minute
  if dMinute < 0:
    dStunde -= 1
    dMinute += 60
  dSekunde = SekundeX - Sekunde
  if dSekunde < 0:
    dMinute -= 1
    dSekunde += 60
  return [dStunde,dMinute,dSekunde]

def make_file(Data, emergency = None):
  [Zeit,Tag,Uhrzeit,Stunde,Minute,Sekunde] = get_time()
  
  if emergency == None or emergency == False:
    file_name = Tag + '_' +PC_id +'.txt'
  elif emergency == True:
    file_name = Tag + '_emergency' + '_' + PC_id + '.txt'
  else:
    print('invalid use of emergency parameter in function make_file.')

  with open(file_name,'w') as f:
    for line in AktienDaten:
      a = []
      for b in line:
        a.append(str(b))
      f.write(",".join(a))
      f.write('\n')

  if emergency == None or emergency == False:
    print('file generated')
  elif emergency == True:
    print('emergency file generated')

check = True
while check == True:
  PC_id = input('From which PC are you accessing this program?\nEnter T for Tobis PC, \
P for Pauls PC, R for Raspberri Pi and confirm with enter.\n')
  PC_id = PC_id.upper()
  if PC_id == 'T' or PC_id == 'P' or PC_id == 'R':
    print('You are accessing with PC_id = %s' % (PC_id))
    check = False
  else:
    print()
    print('Your input is invalid. Try again.\n')

companies = []
#------INPUT------
increment = 5.0  #Intervalle in denen Aktienpreise abgerufen werden in Sekunden

companies.append('TSLA') #Tesla
companies.append('AAPL') #Apple
companies.append('EA')   #Electronic Arts
companies.append('GOOG') #Google
#-----------------
sleeping = False
col_names = ['Zeit']     #names of columns in table
for company in companies:
  col_names.append(company)
print(col_names)
AktienDaten = [col_names] 

#make_file(AktienDaten)

try:
  while True:
    [Zeit,Tag,Uhrzeit,Stunde,Minute,Sekunde] = get_time()
    Reihe = [Zeit]
    for company in companies:
      Reihe.append(si.get_live_price(company))
    print(Reihe)
    AktienDaten.append(Reihe)

    if (Stunde >= 22) or (Stunde <= 14 or (Stunde == 15 and Minute <= 29)):
      [dH,dM,dS] = calc_time_until(15,30,00)
      Schlafzeit = dS + 60*dM + 3600*dH
      if len(AktienDaten) > 2: #sorgt dafuer dass er nur eine Datei schreibt, 
                               #wenn mehr als die col_names und eine Reihe in den Aktiendaten sind   
                               #sonst wuerde er auch eine Datei erstellen, wenn man ihn im Schlafmodus startet

        make_file(AktienDaten)                           
      AktienDaten = [col_names]
      print('sleeping for %s hours, %s minutes and %s seconds until 15:30' % (dH,dM,dS))
      sleeping = True
      tm.sleep(Schlafzeit)
      sleeping = False
      
    tm.sleep(increment)  

except KeyboardInterrupt:
  if sleeping == False:
    make_file(AktienDaten,True)
    print('Program aborted')
  elif sleeping == True:
    print('Program aborted.')
    print('No emergency file generated because program was sleeping.') #Programm erstellt sowieso file wenn es 
                                                                       #schlafen geht. Oder es wurde schlafend
                                                                       #gestartet und deswegen sind keine Daten
                                                                       #vorhanden