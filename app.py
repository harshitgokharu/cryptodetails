from flask import Flask, request,  render_template
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



@app.route('/')
def home():
    ref()
    return render_template('index.html',btc_mean= btc_mean, eth_mean= eth_mean, xrp_mean= xrp_mean, btc_today= btc_today, eth_today= eth_today, xrp_today= xrp_today, url1='../static/images/crypto_perc.png', url2='../static/images/btc.png', url3='../static/images/eth.png', url4='../static/images/xrp.png')

@app.route("/twitter")
def twitter():
  return render_template("twitter.html")

@app.route("/news")
def news():
  return render_template("news.html")

@app.route('/invretresult', methods=['GET', 'POST'])
def invretresult():

    
    
    start_date = str(datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').strftime('%d/%m/%Y'))
    end_date = str(datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').strftime('%d/%m/%Y'))
    daily_amt = float(request.form.get('daily_amt'))
    crypto_name = request.form.get('crypto_name')


     
    
    data_bitcoin = investpy.get_historical_data(commodity='gold', from_date=start_date, to_date=end_date)
    data_bitcoin.rename(columns={"Close": "Price"},inplace=True)
    data_bitcoin = data_bitcoin.iloc[::-1]
    
    data_comb = pd.DataFrame(index= data_bitcoin.index)
    
    data_comb["BTC"] = data_bitcoin['Price']

    data_ether = investpy.get_crypto_historical_data(crypto='ethereum', from_date=start_date, to_date=end_date)
    data_ether.rename(columns={"Close": "Price"},inplace=True)
    data_ether = data_ether.iloc[::-1]
    data_comb["ETH"] = data_ether['Price']
    
    data_xrp = investpy.get_crypto_historical_data(crypto='xrp', from_date=start_date, to_date=end_date)
    data_xrp.rename(columns={"Close": "Price"},inplace=True)
    data_xrp = data_xrp.iloc[::-1]
    data_comb["XRP"] = data_xrp['Price']
    
    data_doge = investpy.get_crypto_historical_data(crypto='dogecoin', from_date=start_date, to_date=end_date)
    data_doge.rename(columns={"Close": "Price"},inplace=True)
    data_doge = data_doge.iloc[::-1]
    data_comb["DOGE"] = data_doge['Price']
        

    data_usdinr = investpy.get_currency_cross_historical_data(currency_cross='USD/INR', from_date=start_date, to_date=end_date)
    data_usdinr.rename(columns={"Close": "USDINR"},inplace=True)
    data_usdinr = data_usdinr.iloc[::-1]
    data_comb["USDINR"] = data_usdinr['USDINR']
    
    data_comb.fillna(method='bfill', inplace=True)
    data_comb.fillna(method='ffill', inplace=True)

    data_comb = data_comb.assign(Qty_BTC = lambda x:((1/(x["BTC"]*x["USDINR"]))* daily_amt))
    data_comb = data_comb.assign(Qty_ETH = lambda x:((1/(x["ETH"]*x["USDINR"]))* daily_amt))
    data_comb = data_comb.assign(Qty_XRP = lambda x:((1/(x["XRP"]*x["USDINR"]))* daily_amt))
    data_comb = data_comb.assign(Qty_DOGE = lambda x:((1/(x["DOGE"]*x["USDINR"]))* daily_amt))


    if(crypto_name == "BTC"):
            crypto_qty= data_comb["Qty_BTC"].sum() 
            crypto_ret= data_comb["Qty_BTC"].sum() * data_comb["BTC"][0] * data_comb["USDINR"][0]

    if(crypto_name == "ETH"):
            crypto_qty= data_comb["Qty_ETH"].sum() 
            crypto_ret= data_comb["Qty_ETH"].sum() * data_comb["ETH"][0] * data_comb["USDINR"][0]
    
    if(crypto_name == "XRP"):
            crypto_qty= data_comb["Qty_XRP"].sum()
            crypto_ret= data_comb["Qty_XRP"].sum() * data_comb["XRP"][0] * data_comb["USDINR"][0]
            
    if(crypto_name == "DOGE"):
            crypto_qty= data_comb["Qty_DOGE"].sum()
            crypto_ret= data_comb["Qty_DOGE"].sum() * data_comb["DOGE"][0] * data_comb["USDINR"][0]

    total_invest = len(data_comb) * daily_amt
    
    daily_amt = "Investment each day: ₹ "+ str(daily_amt)
    duration = "Duration: " + start_date + " to " + end_date
    total_invest = "Total Investment: ₹ "+ str(total_invest)  
    crypto_ret = "Current Amount: ₹ "+ str("%.2f" % crypto_ret)
    crypto_qty = "Current Quantity: " + str(crypto_qty) 
    
    return render_template('invret.html',crypto_name = crypto_name, daily_amt = daily_amt, duration = duration,  crypto_ret= crypto_ret , crypto_qty=crypto_qty, total_invest=total_invest)



@app.route('/invret')
def invret():
    return render_template('invret.html')



if __name__ == "__main__":
    app.run(debug=True)
    
    
