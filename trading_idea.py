# coding=utf-8
from random import seed
from random import random
import math as m
from random import randrange
import quantumrandom 
import numpy as np
from bitarray import bitarray
from bitarray.util import int2ba
import streamlit as st
import pandas as pd
import altair as alt
import base64
import xlsxwriter
from io import BytesIO
from scipy.stats import norm

output = BytesIO()


st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")
#st.write("""
    # Meine App
    #Hello *world!*
    #""")
hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.write("""# Vergleich von Buy and Hold vs. Trading""")
st.markdown("***")

#ergebnis_placeholder = st.empty()

def binary(num, pre='0b', length=12, spacer=0):   #12
    return '{{:{0}>{1}}}'.format(spacer, length).format(bin(num)[2:])


def lognorm(x,mu,sigma):
    a = (m.log(x) - mu)/m.sqrt(2*sigma**2)
    p = 0.5 + 0.5*m.erf(a)
    return p



#e = list()
#for r in range(4096):
#    b = ["0"]*12
#    for y in range(len(b)):
#        if a[r][y] == 0:
#            b[y] = "down"
#        else:
#            b[y] = "up"
#    e.append(b)
#print(e[4094])





def main():
    output = "empty"
    #my = 0.1
    #sigma = 0.2
    up = 0.0
    down = 0.0
  
    #verlaufArray = [4096][12]

    counter_trading_diskret = 0
    counter_buyAndHold_diskret = 0
    counter_indifferent_diskret = 0
    summe_trading_diskret = 0
    summe_buyAndHold_diskret = 0
    summe_indifferent_diskret = 0
    spalte1, spalte2 = st.columns(2)

    #with spalte1:

    diskret = '<p style="font-family:sans-serif; color:black; font-size: 30px;"><i>Simulation - klassisch mit Wahrscheinlichkeiten</i></p>'
    st.markdown(diskret, unsafe_allow_html=True)
    st.write("[Mehr zur Generierung echter Zufallszahlen (Quantenvakuum-Fluktuation) >](https://qrng.anu.edu.au/)")

    #st.text_input('Sigma: ')
    #st.text_input('Mu: ')
    #st.selectbox('Zufallszahlen: ', ["Echte ANU","Pseudo","Pseudo-System"])

    # Diskret - Trading vs Buy and Hold (3 up Verkauf, 3 down Kauf)

    left, right = st.columns(2)
    with left:
        #st.text_input('Sigma: ')
        sigma = st.number_input('Volatilität/Sigma σ: ', 0.0, 1.0, value=0.2)
        st.selectbox('Art der Zufallszahlen: ', ["Echte Zufallszahlen (Quantenfluktuation)","Pseudo (in Arbeit/noch nicht implementiert)","Pseudo-System (noch nicht implementiert)"])
    with right:
        #st.text_input('Mu: ')
        my = st.number_input('Drift/Mu µ: ', 0.0, 1.0, value= 0.08)
        anzahl_simulationen = st.number_input('Anzahl an Simulationsläufen: ', 1, 1000, value=100)
    #ergebnis_placeholder = st.empty()
    if st.button('Simulation durchführen'):
        my_bar = st.progress(0)
        with st.spinner('Bitte warten...'):
            #@st.cache(show_spinner=True)
            print("Numbers:")
            myList = quantumrandom.get_data(data_type='uint16', array_length=1000)
            myList2 = quantumrandom.get_data(data_type='uint16', array_length=1000)
            myList3 = quantumrandom.get_data(data_type='uint16', array_length=1000)
            myList4 = quantumrandom.get_data(data_type='uint16', array_length=1000)
            myList5 = quantumrandom.get_data(data_type='uint16', array_length=1000)
            #print(myList)
            mylist6 = myList + myList2 + myList3 + myList4 + myList5
            myInt = 65535.0
            newList  = np.divide(mylist6, myInt)
            #print(newList)
            counter1 = 0
            counter2 = 0
            counter3 = 0
            counter4 = 0
            counter5 = 0
            
            #for i in range(len(newList)):
            #    if newList[i] <= 0.5:
            #        counter1 += 1
            #    if newList[i] <=1.0:
            #        counter2 += 1
            #
            #print(max(mylist6))
            #print(min(mylist6))
            #print(str(counter1) + " : " + str(counter2) +" : " + str(counter3)+" : "  + str(counter4) +" : " + str(counter5))

            budget = 100
            price = 100.0
            t = float(1.0/52.0)
            #my = 0.08
            #sigma = 0.2
            #St = 120
            up = 0.6
            down = 0.3

            countBH = 0
            countTS = 0
            betragBH = 0
            betragTS = 0
            zf = randrange(100)
            print(zf)
            #print(norm.ppf(0.95)) entspricht StandNormInv in Excel

            for i in range(anzahl_simulationen):
                my_bar.progress((i+1)/anzahl_simulationen)
                seed(i+zf+10)

                randomNumLength = 260
                randomNum = [0] * randomNumLength      # Aray der Zufallszahlen [0;1]
                runningTime = [0.0] * randomNumLength  # Array der Laufzeit [0;5] jahre
                process = [0.0] * randomNumLength      # Array für die Aktienkurse / Prozess
                position = [0.0] * randomNumLength
                einstand = [0.0] * randomNumLength
                cash = [0.0] * randomNumLength
                prob = [0.0] * randomNumLength
                signal = [0.0] * randomNumLength
                possible = [0.0] * randomNumLength
                golden = [0.0] * randomNumLength 
                # 500 Zufallszahlen werden erzeugt
                randomNum[0] = int(1)
                #print("Hello: " + str(randomNum[0]))

                process[0] = price
                position[0] = 0
                cash[0] = 100.0
                golden[0] = 100.0
                #position[0] = 0

            #"""  
                for rand in range(len(randomNum)):
                    randomNum[rand] = random()
                    runningTime[rand] = float((rand+1) * t)
                    if rand > 0: 
                        process[rand] = process[rand-1] * m.exp((my - (sigma**2)/2) * t + sigma * m.sqrt(t) * norm.ppf(randomNum[rand]))
                        #print(process[rand])
                        #prob[rand] = norm.sf(process[rand], m.log(price)+(my+(sigma**2)/2)*rand*t, sigma * m.sqrt(rand*t))
                        prob[rand] = lognorm(process[rand], m.log(price)+(my+(sigma**2)/2)*rand*t, sigma * m.sqrt(rand*t))
                        #print(prob[rand])
                        if prob[rand] < down:
                            signal[rand] = "Kauf"
                        elif prob[rand] > up:
                            signal[rand] = "Verkauf" 
                        else:
                            signal[rand] = "-" 
                        # möglich?
                        if signal[rand] == "Kauf" and cash[rand-1] > 0:
                            possible[rand] = "möglich"
                        elif signal[rand] == "Kauf" and cash[rand-1] <= 0:
                            possible[rand] = "nicht möglich" 
                        elif signal[rand] == "Verkauf" and position[rand-1] > 0:
                            possible[rand] = "möglich"
                        elif signal[rand] == "Verkauf" and position[rand-1] <= 0:
                            possible[rand] = "nicht möglich"
                        else:
                            possible[rand] = "-"      
                        # Position
                        if signal[rand] == "Kauf" and possible[rand] == "möglich":
                            position[rand] = cash[rand-1]/process[rand]
                        elif signal[rand] == "Verkauf" and possible[rand] == "möglich":
                            position[rand] = 0
                        else: 
                            position[rand] = position[rand-1]
                        # Cash
                        if signal[rand] == "Verkauf" and possible[rand] == "möglich":
                            cash[rand] = process[rand] * position[rand-1]
                        elif signal[rand] == "Kauf" and possible[rand] == "möglich":
                            cash[rand] = 0
                        else: 
                            cash[rand] = cash[rand-1]
                        # Golden
                        if position[rand] > 0:
                            golden[rand] = position[rand] * process[rand]
                        else:
                            golden[rand] = cash[rand] 
                        #print(str(signal[rand]) + " | " + str(prob[rand]) + " | " + str(possible[rand]) + " | " + str(golden[rand]))
                        #print(str(process[rand]) + " | " + str(golden[rand]))
                        #print(signal[rand])
                        #print(prob[rand])  
                        #print(possible[rand])    

                print(str(process[259]) + " | " + str(golden[259]))
                betragBH += round(golden[259],2)
                betragTS += round(process[259],2)
                if golden[259] > process[259]:
                    countTS = countTS +1
                else:
                    countBH = countBH +1

            #"""   # first Prozess / Kurs
                #price = price * m.exp((my - (sigma**2)/2) * t + sigma * m.sqrt(t) * norm.ppf(randomNum[0]))
                #print(price)
            print("Trading: " + str(countTS) + " | Buy_And_Hold: " + str(countBH))
            output = "Trading: " + str(countTS) + " | Buy_And_Hold: " + str(countBH)
            #original_title = '<p style="font-family:Courier; color:Blue; font-size: 20px;">Überschrift</p>'
            #st.markdown(original_title, unsafe_allow_html=True)
            #st.text(output)
            #ergebnis_text = "Trading: " + str(countTS) + " | Buy_And_Hold: " + str(countBH)
        #st.write(output)
            #ergebnis_placeholder.text_area("Ergebnis: ",ergebnis_text, height = 50)
            #ergebnis_placeholder.text("Ergebnis: " + ergebnis_text)
            #st.write(output)
            ergebnis_text = 'start'
            #ergebnis_placeholder.text("Ergebnis: " + ergebnis_text)
            betragBH_rund = round(betragBH,2)
            betragTS_rund = round(betragTS,2)
            #st.success("Vergleich höherer Schlusskurs (Häufigkeit) --> Trading: " + str(countTS) + "  |  Buy_And_Hold: " + str(countBH))
            #st.success("Vergleich höherer Schlusskurs (kummuliert) --> Trading: " + str(betragTS_rund) + "  |  Buy_And_Hold: " + str(betragBH_rund))
            daten = np.array([[countBH, countTS], [betragBH_rund, betragTS_rund]])
            index_values = ['Vergleich höherer Schlusskurs (Häufigkeit)', 'Vergleich höherer Schlusskurs (kummuliert)']
            df = pd.DataFrame(data = daten, 
                index = index_values, 
                columns = ('Buy and Hold', 'Trading'))
            df.round(2)
            output = '<p style="font-family:sans-serif; color:black; font-size: 18px;"><i>Ergebnis:</i></p>'
            st.markdown(output, unsafe_allow_html=True)
            st.dataframe(df.style.format(subset=['Buy and Hold', 'Trading'], formatter="{:.2f}"))
            #st.dataframe(df.style.format("{:.2%}"))
            #st.table(df)

        #st.text(output)
        # zw1a =  m.log(100)+(0.08+(0.2**2)/2)*1*float(1.0/52.0)
        # zw2a = 0.2 * m.sqrt(1*float(1.0/52.0))
        # print(lognorm(97.6796,zw1a,zw2a)) mit Excel überprüft
        # print(lognorm(25,1.744,2.0785)) ditot




    #with spalte2:
    
    st.markdown("***")
    diskret = '<p style="font-family:sans-serif; color:black; font-size: 30px;"><i>Simulation - Diskret (abzählbar)</i></p>'
    st.markdown(diskret, unsafe_allow_html=True)
    #anzahl_basis = st.number_input('Basis T (Anzahl Bewegungen, Quartalsweise, Monatsweise...)', 1, 20, value=12)
    #start_kapital = st.number_input('Startkapital (in €)', 1, 10000, value=50)

    left_input, right_input = st.columns(2)
    with left_input:
        anzahl_basis = st.number_input('Basis T (Anzahl Bewegungen, Quartalsweise, Monatsweise...)', 1, 20, value=12)
        anzahl_down = st.number_input('Kaufen bei X Abwärtsbewegungen hintereinander', 0, 12)
    with right_input:
        start_kapital = st.number_input('Startkapital (in €)', 1, 10000, value=50)
        anzahl_up = st.number_input('Verkaufen bei X Aufwärtsbewegungen hintereinander',0,12)

    basis = 1/(anzahl_basis) #12
    startKapital = start_kapital
    
    if st.button('SImulation durchführen'):
        with st.spinner('Bitte warten...'):
            laenge = np.power(2,anzahl_basis)
            print(laenge)
            verlaufArray = np.zeros(shape=(laenge,anzahl_basis)) # 4096,12
            ergebnis_array_diskret = np.zeros(shape=(laenge,2)) # 4096
            #st.write("""
            #*Button klicken zum ausführen der Simulation*
            #""")

            a = np.zeros(shape=(laenge,anzahl_basis)) #4096, 12
            b = ["0"]*12
            c = [b]*4096
            #print(c)

            rr = binary(11)
            bitArray = ["up"] * 12               

            for t in range(laenge): #4096
                x = str(binary(t))
                #print(x)
                #print(t)
                for index, letter in enumerate(x):
                    if letter == "0":
                        a[t][index] = 0 
                        #c[t][index] = 'down'
                    else:
                        a[t][index] = 1
                        #c[t][index] = 'up'
                    #print(index, letter)
                #print(c[t])
                
            print(a)

            up = kursentwicklung_up(sigma, basis)
            down = kursentwicklung_down(sigma, basis)

            print(laenge)

            for t in range(laenge): #4096
                x = str(binary(t))
                #print(x)
                #print(t)
                for index, letter in enumerate(x):
                    if letter == "0":
                        a[t][index] = 0 
                    else:
                        a[t][index] = 1
            #print(a)


            # alle Kurse (4096 x 12) zu jedem Zeitpunkt berechnen
            endwerte = [0.0] * laenge #4096
            for t in range(laenge): #4096
                for d in range(anzahl_basis): #12
                    if a[t][d] == 0:
                        if d == 0:
                            verlaufArray[t][d] = startKapital * down 
                        else:
                            verlaufArray[t][d] = verlaufArray[t][d-1] * down 
                    else:
                        if d == 0:
                            verlaufArray[t][d] = startKapital * up 
                        else:
                            verlaufArray[t][d] = verlaufArray[t][d-1] * up 
                endwerte[t] = round(verlaufArray[t][anzahl_basis-1], 2)  # 11, 2  Hier muss gerundet werden, evtl. schon früher da sonst mehr als 12 Entwerte herauskommen
            moegliche_endwerte = list(dict.fromkeys(endwerte, 2))

            for z in range(laenge): #4096
                comp = algoTrading(a[z], verlaufArray[z], anzahl_up, anzahl_down, anzahl_basis, start_kapital)
                ergebnis_array_diskret[z][0] = comp
                ergebnis_array_diskret[z][0] = endwerte[z]
                summe_buyAndHold_diskret += endwerte[z]
                summe_trading_diskret += comp
                if comp > endwerte[z]:
                    counter_trading_diskret += 1
                if comp < endwerte[z]:
                    counter_buyAndHold_diskret += 1
                if comp == endwerte[z]:
                    counter_indifferent_diskret += 1
                    summe_indifferent_diskret += comp
                print("Vergleich: " + str(comp) + " vs. " + str(endwerte[z]))
            
            #print("a: " + str(a[500]) + "  verlauf: " + str(verlaufArray[500]) + "  endwerte: " + str(endwerte[500]))
            #st.success('Done!' + " --> Ergebnis: " + str(up) + " | " + str(down))
            #st.write("Anzahl der Möglichkeiten für die Endwerte: " + str(moegliche_endwerte))
            #st.write("Up: " + str(up))
            #st.write("Down: " + str(down))
            #st.write("Diskret Häufigkeit --> Trading: " + str(counter_trading_diskret) + " Buy and Hold: " + str(counter_buyAndHold_diskret) + " Indifferent: " + str(counter_indifferent_diskret))
            #st.write("Diskret Summe-Kapital --> Trading: " + str(round(summe_trading_diskret,2)) + " Buy and Hold: " + str(round(summe_buyAndHold_diskret,2)) + " Indifferent: " + str(round(summe_indifferent_diskret,2)))
            #st.write(a)
            daten_diskret = np.array([[counter_buyAndHold_diskret, counter_trading_diskret], [summe_buyAndHold_diskret, summe_trading_diskret]])
            index_values2 = ['Vergleich höherer Schlusskurs (Häufigkeit):', 'Vergleich höherer Schlusskurs (kummuliert in €):']
            df2 = pd.DataFrame(data = daten_diskret, 
                index = index_values2, 
                columns = ('Buy and Hold', 'Trading'))
            df2.round(2)
            output = '<p style="font-family:sans-serif; color:black; font-size: 18px;"><i>Ergebnis:</i></p>'
            spalte_1, spalte_2 = st.columns(2)
            chart_data = pd.DataFrame(
            data = np.array([summe_buyAndHold_diskret, summe_trading_diskret]),
            columns=["kummulierte Schlusskurse"],
            index= ('Buy and Hold', 'Trading'))
   
           # csv = df2.to_excel("output.xlsx")
            #df2.to_csv().encode('utf-8')
            csv = df2.to_csv().encode('utf-8')

            #c = alt.Chart(chart_data).mark_bar()
            #st.altair_chart(c, use_container_width=True)

            with spalte_1:
                st.markdown(output, unsafe_allow_html=True)
                st.dataframe(df2.style.format(subset=['Buy and Hold', 'Trading'], formatter="{:.2f}"))
                st.download_button(
                "Press to Download the Result as CSV/Excel",
                csv,
                "file.csv",
                "text/csv",
                key='download-csv'
                )
            with spalte_2:
                st.bar_chart(chart_data)
                #st.markdown(get_table_download_link(df2), unsafe_allow_html=True)
               
     

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_excel("output.xlsx")
    #b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/xlsx;base64,{csv}">Download csv file</a>'
    return href



def kursentwicklung_up(sigma, basis):
    up_1 = np.exp(sigma * np.sqrt(basis))
    print(up_1)
    return up_1


def kursentwicklung_down(sigma, basis):
    down_1 = np.exp(-sigma * np.sqrt(basis))
    print(down_1)
    return down_1

def algoTrading(array1, kurs, ups, downs, anzahl_basis2, start_kapital): # 6 - 0
    #strategie = 3
    strategie_ups = ups
    strategie_downs = downs
    kapital = start_kapital #50.00 # entweder realitätsnah, indem Aktien stückelbar sind und gewinne reinvestiert werden oder man nimmt den profit/verlust immer raus und kuaft/verkauft zu dem kurs, egal wie viel gesamtkapital man hat
    anteil = 1.0
    market_in = False 
    if strategie_ups == 0 and strategie_downs == 0: # D.h. immer direkt Verkaufen und Kaufen --> 50€ 
        return round(kapital,2)

    for u in range((anzahl_basis2)): # 12
        trading_buy = True
        trading_sell = True

        # For downs --> wann kaufen  
        if u >= strategie_downs-1:
            for e in range(strategie_downs):
                if array1[u - e] == 1:
                    trading_buy = False
            if trading_buy and not market_in:
                # buy
                anteil = kapital/kurs[u]
                market_in = True

        # For ups --> wann verkaufen
        if u >= strategie_ups-1:
            for e in range(strategie_ups):
                if array1[u - e] == 0:
                    trading_sell = False
            if trading_sell and market_in:
                # sell
                market_in = False
                #kapital = kurs[u]

        if market_in:  # Platzierung evtl. oberhalb sinnvoller?
            kapital = anteil * kurs[u]

          # if u >= strategie-1:  # Old Stuff bei einer Strategie (parralell up/down)
          #      trading_buy = True
          #  trading_sell = True
          #  for e in range(strategie):
          #      if array1[u - e] == 1:
          #          trading_buy = False
          #      if array1[u - e] == 0:
          #          trading_sell = False
          #  if trading_buy and not market_in:
          #    # buy
          #      anteil = kapital/kurs[u]
           #     market_in = True
           # if trading_sell and market_in:
           #     # sell
           #     market_in = False
           #     #kapital = kurs[u]

    #print(kapital)
    return round(kapital,2) #ergebnis


if __name__ == "__main__":
    main()
