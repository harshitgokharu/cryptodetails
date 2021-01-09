from flask import Flask, render_template
#import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import investpy

app =  Flask(__name__)


app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def ref():
    end_date = datetime.today().strftime('%d/%m/%Y')
    start_date = datetime.now() - timedelta(days=2*365)
    start_date = start_date.strftime('%d/%m/%Y')

    data_bitcoin = investpy.get_crypto_historical_data(crypto='bitcoin', from_date=start_date, to_date=end_date)

    data_bitcoin.rename(columns={"Close": "Price"},inplace=True)
    data_bitcoin = data_bitcoin.iloc[::-1]


    data_ether = investpy.get_crypto_historical_data(crypto='ethereum', from_date=start_date, to_date=end_date)
    data_ether.rename(columns={"Close": "Price"},inplace=True)
    data_ether = data_ether.iloc[::-1]


    data_xrp = investpy.get_crypto_historical_data(crypto='xrp', from_date=start_date, to_date=end_date)
    data_xrp.rename(columns={"Close": "Price"},inplace=True)
    data_xrp = data_xrp.iloc[::-1]

            
    data_comb = pd.DataFrame(index= data_bitcoin.index)
    data_comb["BTC"] = data_bitcoin['Price']
    data_comb["ETH"] = data_ether['Price']  
    data_comb["XRP"] = data_xrp['Price'] 


    dates_list = []
    dates_list_label = []
    months_list = []

    reverse_data_comb = data_comb.index[::-1]
    for i in range(0,len(reverse_data_comb)):
            if reverse_data_comb[i].strftime('%m/%Y') not in months_list:
                months_list.append(reverse_data_comb[i].strftime('%m/%Y'))
                dates_list.append(reverse_data_comb[i])
                dates_list_label.append(reverse_data_comb[i].strftime('%d/%m/%Y'))

    data_comb = data_comb.assign(Perc_BTC = lambda x:((x['BTC']-x['BTC'].mean())/(x["BTC"].mean())* 100))
    data_comb = data_comb.assign(Perc_ETH = lambda x:((x['ETH']-x['ETH'].mean())/(x["ETH"].mean())* 100))
    data_comb = data_comb.assign(Perc_XRP = lambda x:((x['XRP']-x['XRP'].mean())/(x["XRP"].mean())* 100))


    plt.figure(figsize=(100, 40))
    plt.plot(data_comb.index,data_comb['Perc_BTC'], label="Percentage from mean BTC",linewidth=6.0)
    plt.plot(data_comb.index,data_comb['Perc_ETH'], label="Percentage from mean ETH",linewidth=6.0)
    plt.plot(data_comb.index,data_comb['Perc_XRP'], label="Percentage from mean XRP",linewidth=6.0)
    plt.axhline(y=0, color='black', linestyle='-')
    plt.yticks([-50,0,50,100,150,200,250,300,350],fontsize=50)
    plt.xticks(dates_list,dates_list_label,fontsize=50,rotation=40)
    plt.legend(loc=0, prop={'size': 60})
    
    plt.savefig('static/images/crypto_perc.png')


    global btc_mean
    global eth_mean
    global xrp_mean
    
    global btc_today
    global eth_today
    global xrp_today

    btc_mean= '%.2f'%data_comb["BTC"].mean()
    eth_mean= '%.2f'%data_comb["ETH"].mean()
    xrp_mean= '%.2f'%data_comb["XRP"].mean()

    btc_today= '%.2f'%data_comb["BTC"][0]
    eth_today= '%.2f'%data_comb["ETH"][0]
    xrp_today= '%.2f'%data_comb["XRP"][0]
    
    return True



@application.route('/')
def home():
    ref()
    return render_template('index.html',btc_mean= btc_mean, eth_mean= eth_mean, xrp_mean= xrp_mean, btc_today= btc_today, eth_today= eth_today, xrp_today= xrp_today, url1='../static/images/crypto_perc.png')

@app.route("/twitter")
def twitter():
  return render_template("twitter.html")

@app.route("/news")
def news():
  return render_template("news.html")



if __name__ == "__main__":
    app.run(debug=True)
    
    
