from flask import Flask, render_template
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from datetime import datetime
from datetime import timedelta
import investpy

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
script_path = os.path.dirname(os.path.realpath(__file__))
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


data_sp500 = investpy.get_index_historical_data(index='S&P 500',
                                        country='United States',
                                        from_date=start_date,
                                        to_date=end_date)

data_sp500.rename(columns={"Close": "Price"},inplace=True)
data_sp500 = data_sp500.iloc[::-1]


data_comb = pd.DataFrame(index= data_sp500.index)
list_bitcoin = []
list_ether = []
list_xrp = []
for date1 in data_sp500.index:
    for date2 in data_bitcoin.index:
        if date1 == date2:
            list_bitcoin.append(data_bitcoin.loc[date1,'Price'])
            continue
    for date3 in data_ether.index:
        if date1 == date3:
            list_ether.append(data_ether.loc[date1,'Price'])
            continue
    for date4 in data_xrp.index:
        if date1 == date4:
            list_xrp.append(data_xrp.loc[date1,'Price'])
            continue
            
data_comb["S&P 500"] = data_sp500['Price']
data_comb["BTC"] = list_bitcoin  
data_comb["ETH"] = list_ether  
data_comb["XRP"] = list_xrp   


data_comb = data_comb.assign(Std_SP500 = lambda x:((x['S&P 500']-x['S&P 500'].min())/(x['S&P 500'].max()-x['S&P 500'].min())* 100))
data_comb = data_comb.assign(Std_BTC = lambda x:((x['BTC']-x['BTC'].min())/(x['BTC'].max()-x['BTC'].min())* 100))
data_comb = data_comb.assign(Std_ETH = lambda x:((x['ETH']-x['ETH'].min())/(x['ETH'].max()-x['ETH'].min())* 100))
data_comb = data_comb.assign(Std_XRP = lambda x:((x['XRP']-x['XRP'].min())/(x['XRP'].max()-x['XRP'].min())* 100))

dates_list = []
dates_list_label = []
months_list = []

reverse_data_comb = data_comb.index[::-1]
for i in range(0,len(reverse_data_comb)):
   if reverse_data_comb[i].strftime('%m/%Y') not in months_list:
         months_list.append(reverse_data_comb[i].strftime('%m/%Y'))
         dates_list.append(reverse_data_comb[i])
         dates_list_label.append(reverse_data_comb[i].strftime('%d/%m/%Y'))

plt.figure(figsize=(100, 40))
plt.plot(data_comb.index,data_comb['Std_SP500'], label="Standardized S&P 500",linewidth=6.0)
plt.plot(data_comb.index,data_comb['Std_BTC'], label="Standardized BTC",linewidth=6.0)
plt.plot(data_comb.index,data_comb['Std_ETH'], label="Standardized ETH",linewidth=6.0)
plt.plot(data_comb.index,data_comb['Std_XRP'], label="Standardized XRP",linewidth=6.0)
plt.yticks([0,10,20,30,40,50,60,70,80,90,100], fontsize=50)
plt.xticks(dates_list,dates_list_label,fontsize=50,rotation=40)
plt.legend(loc=0, prop={'size': 60})
    
plt.savefig('static/images/crypto_std.png')



@app.route('/')
def home():
    return render_template('index.html',name = 'hello', url='../static/images/crypto_std.png')


@app.route('/disp',methods=['POST'])
def disp():
    '''
    For rendering results on HTML GUI
    ''' 

    return render_template('index.html',name = 'hello', url='../static/images/crypto_std.png')


if __name__ == "__main__":
    app.run(debug=True)
    
    