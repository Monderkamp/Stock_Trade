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

directories =\
{\
'L':'/home/gnadt/GitHub Repositories/Stock_Trade/stock price data/',\
'SA':'/home/gnadt/GitHub Repositories/Stock_Trade/stock price data/sechs_aktien/',\
'PB':'/home/monderkamp/Paul Monderkamp/Stock_Trade/stock price data/Daten von Uni Buero/'\
} 
#------------------------------------------------------------------------
def get_time():
  Zeit = tm.asctime(tm.localtime())
  Tag =str( Zeit[-4:] + '_' + Zeit[4:7]+ '_' + Zeit[8:10] +  '_' + Zeit[0:3]  )
  Uhrzeit = str(Zeit[11:20])
  Stunde = int(Uhrzeit[0:2])
  Minute = int(Uhrzeit[3:5])
  Sekunde = int(Uhrzeit[6:8])
  return([Zeit,Tag,Uhrzeit,Stunde,Minute,Sekunde])
#------------------------------------------------------------------------
def calc_time_until(StundeX,MinuteX,SekundeX,WochentagX = None):
  [Zeit,Tag,Uhrzeit,Stunde,Minute,Sekunde] = get_time()
  Wochentag = Tag[-3:]
  WT_to_Nr = {'Mon':0,'Tue':1,'Wed':2,'Thu':3,'Fri':4,'Sat':5,'Sun':6}

  def calc_hour_minute_until(StundeX,MinuteX,SekundeX):
    dStunde = 0
    dMinute = 0
    dSekunde = 0
  
    dSekunde += SekundeX - Sekunde

    if dSekunde < 0:
      dMinute -= 1
      dSekunde += 60

    dMinute += MinuteX - Minute

    if dMinute < 0:
      dStunde -= 1
      dMinute += 60

    dStunde += StundeX - Stunde
    if dStunde < 0:
      dStunde += 24

    return [dStunde,dMinute,dSekunde]
  [dStunde,dMinute,dSekunde] = calc_hour_minute_until(StundeX,MinuteX,SekundeX)
  if WochentagX == None:
    return [dStunde,dMinute,dSekunde]
  elif WochentagX in WT_to_Nr.keys():
    dWochentag = (WT_to_Nr[WochentagX] - WT_to_Nr[Wochentag])%7
    #print(dWochentag,dStunde)
    #print(StundeX,MinuteX,SekundeX,Stunde,Minute,Sekunde)
    if dWochentag == 0 and (3600*StundeX+60*MinuteX+SekundeX - 3600*Stunde-60*Minute-Sekunde < 0):
      dWochentag += 7
    if (3600*StundeX+60*MinuteX+SekundeX - 3600*Stunde-60*Minute-Sekunde > 0):
      #print('fall1')
      dStunde += (dWochentag) *24
    elif (3600*StundeX+60*MinuteX+SekundeX - 3600*Stunde-60*Minute-Sekunde < 0):
      #print('fall2')
      dStunde += ((dWochentag-1) *24)

    return [dStunde,dMinute,dSekunde]
  else:
    print('WochentagX in calctimeuntil does not have the correct form.')

#------------------------------------------------------------------------
def make_file(Data,PC_id,emergency = None):
  [Zeit,Tag,Uhrzeit,Stunde,Minute,Sekunde] = get_time()
  
  if emergency == None or emergency == False:
    file_name = Tag[0:11] + '_stock_data.txt'
  elif emergency == True:
    file_name = Tag[0:11] + '_emergency' + '_stock_data.txt'
  else:
    print('invalid use of emergency parameter in function make_file.')
  if PC_id in directories.keys():
    file_name = directories[PC_id] + file_name

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

#------------------------------------------------------------------------
def gleitender_Durchschnitt(Anzahl,Tabelle,Spalte):
  Tabelle = np.array(Tabelle)
  return sum(Tabelle[-Anzahl:,Spalte])/Anzahl
#------------------------------------------------------------------------
sleeping = False
while True:
  PC_id = input('From which PC are you accessing this program?\nEnter T for Tobis PC, \
PB for Pauls Uni Buero, L for Linux-PC, SA for sechs_aktien, P for Pauls PC and confirm with enter.\n')
  PC_id = PC_id.upper()
  if PC_id == 'T' or PC_id == 'PB' or PC_id == 'L' or PC_id == 'P' or PC_id == 'SA':
    print('You are accessing with PC_id = %s' % (PC_id))
    break
  else:
    print()

yn_init = input('Input (y/n) for initial sleep timer:')
if yn_init.upper() == 'Y':
  WochentagX = input('Input target weekday as Mon/Tue/Wed/Thu/Fri/Sat/Sun: ')
  StundeX = int(input('Input target hour: '))
  MinuteX = int(input('Input target minute: '))
  SekundeX = 0
  [dStunde,dMinute,dSekunde] = calc_time_until(StundeX,MinuteX,SekundeX,WochentagX = WochentagX)
  init_sleep = 3600 * dStunde + 60*dMinute + dSekunde
  print('sleeping until {} {}:{}'.format(WochentagX,StundeX,MinuteX))
  sleeping = True
  #print(dStunde,dMinute,dSekunde)
  tm.sleep(init_sleep)

  sleeping = False
else:
  print('Starting with no initial sleep timer.') 

"""
init_sleep = int(input('set initial sleep timer in hours:'))
print('sleeping for %s hours' % (init_sleep))
tm.sleep(init_sleep*3600)
"""
companies = []

#------------------------------------------------------------------------
#---------------------------------INPUT----------------------------------
#------------------------------------------------------------------------
increment = 15.0  #Intervalle in denen Aktienpreise abgerufen werden in Sekunden
                  #sollte ca. erfuellen:
		  #increment > 1.25 * len(companies)
[H_wakeup, M_wakeup, S_wakeup] = [15,30,00]
[H_sleep, M_sleep, S_sleep] = [22,00,00]

Sommerzeit = True        #Das gilt nur so lange in den USA Sommerzeit ist (10. Maerz) und hier nicht (31. Maerz)
                         #sobald hier wieder Uhren umgestellt werden, gleicht sich das aus
if Sommerzeit == True:
  H_wakeup -= 1
  H_sleep -= 1

companies.append('TSLA') #Tesla
companies.append('AAPL') #Apple
companies.append('EA')   #Electronic Arts
companies.append('GOOG') #Google
companies.append('ADS.DU') #ADIDAS AG NA O.N.
companies.append('DAI.MU') #DAIMLER AG NA O.N.
#------------------------------------------------------------------------
if increment < 1.25*len(companies):
  print('WARNING: increment < 1.25 * len(companies). Might result in too short sleeping intervals')

col_names = ['Zeit']     #names of columns in table
for company in companies:
  col_names.append(company)
print(col_names)
AktienDaten = [col_names] 


try:
  while True:
    try:
      T_0 = tm.time()
      [Zeit,Tag,Uhrzeit,Stunde,Minute,Sekunde] = get_time()
      Reihe = [Uhrzeit]
      for company in companies:
        Reihe.append(si.get_live_price(company))
      print(Reihe)
      AktienDaten.append(Reihe)
	  #print('Tag:',Tag[-3:])
  
      if (Stunde >= H_sleep) or (Stunde <= H_wakeup-1) or (Stunde == H_wakeup and Minute <= M_wakeup-1):

        [dH,dM,dS] = calc_time_until(H_wakeup,M_wakeup,S_wakeup)

        if (Tag[-3:] == 'Fri') or (Tag[-3:] == 'Sat') or (Tag[-3:] == 'Sun'): 
          [dH,dM,dS] = calc_time_until(H_wakeup,M_wakeup,S_wakeup,'Mon')            
      
        Schlafzeit = dS + 60*dM + 3600*dH      
		#print(Schlafzeit)
        if len(AktienDaten) > 2 and not(Tag[-3:] == 'Sat' or Tag[-3:] == 'Sun'): 
          make_file(AktienDaten,PC_id,False)                           
        AktienDaten = [col_names]
        print('AktienDaten-Array (Zwischenspeicher) geleert.')
        print('sleeping for %s hours, %s minutes and %s seconds until %02d:%02d:%02d' % (dH,dM,dS,H_wakeup,M_wakeup,S_wakeup))
        sleeping = True
        tm.sleep(Schlafzeit)
        sleeping = False
      T = increment-tm.time()+T_0
      print('incremental sleep: T = {}\n'.format(T))
      if T > 0:
        tm.sleep(T)
      else: 
        print('Warning. Total processing time longer than increment.')  
    except:
      continue
	  
except KeyboardInterrupt:
  if sleeping == False:
    make_file(AktienDaten,PC_id,True)
    print('Program aborted')
  elif sleeping == True:
    print('Program aborted.')
    print('No emergency file generated because program was sleeping.') 


