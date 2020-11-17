# Crypto_Sense  

### Project
Hosted at : cryptosense.herokuapp.com  
A college project simulating realtime CryptoCurrency Trading.  
Users can signup for an account and can trade different cryptocurrencies supported by system.  

### Technologies Used
Flask  
Python   
HTML  
CSS  
Javascript(Chart.js library for displaying graphs and other cryptocurrency data for efficient crypto purchase.)  

### Install Requirements
First, create a python virtual environment. Then install requirements as-
```
pip install -r requirements.txt
```

### Setup Sending Mail 
The settings file is currently set to send mails using **Gmail**.
If you want to setup some other email provider or API key, one can modify accordingly.  
> For **Gmail**  
> Create a .env environment file and set the following environment variables
  MAIL_USERNAME = 'your email'  
  MAIL_PASSWORD = 'your email password'  
  MAIL_DEFAULT_SENDER = 'your email'  

### Run in development Mode  
```
python wsgi.py  
```
The code for initializing the app configurations lies in __init__.py in app folder.  

### Detailed Usage Instructions  
1. Create a Login Id and Password using an E-mail ID. Register Now  
2. Verify your Email by clicking on the activation link sent on registered E-mail.  
3. Login to your Account Login  
4. You will be given an initial credit of 1000 $  
5. Click on Check Prices button to know about the prices of cryptocurrencies and purchase them  
6. Purchase a crypto currency  
7. Now you can check the profits earned on the dashboard and also check the currencies you have on Current Status button  
8. To sell a currency click on sell button on dashboard and sell the currency you like  
9. You check the trends of Currencies on the Data tab of our Navigation bar for reference on the prices fluctuations on various days and range of days  
10. You can also check the supported currencies and their symbol,ID and Market Cap from the Data tab  
11. Compare your profits with our all time best profiters on Standings tab!  
You can also read these instructions at our website [Graphs Help](https://cryptosense.herokuapp.com/help)  

### CryptoCurrency Data
For seeing detailed cryptocurrency data head over to [CryptoCurrency Data](https://cryptosense.herokuapp.com/graphs/g_main)  
The links are self explanatory.  
