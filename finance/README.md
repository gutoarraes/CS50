This is application was the exercise of week 9 of the 2021 Introduction to computer science course which simulated a brokerage account.

The specification of this exercise demanded that the following functions were implemented:
  - REGISTER - allowed the user to register a login and password (with validation);
  - QUOTE - get the most recent price of a company stock via API request;
  - BUY - purchase a stock, update the SQL database to reflect the new cash balance and current stock holdings
  - INDEX - the index page displays a HTML table of the user's current holdings
  - SELL - sell a stock and update the database accurately
  - HISTORY - show the history of all transactions, specifying if the trade was a purchase or a sale, the price, quantity and which stock was traded
  - PERSONAL TOUCH - student's choice of additional functionality to the website

# Technologies used #

The *Finance* webservice was developed in **Python** and used the **Flask** framework. A **SQL** database was used to manage all user's information, **HTML** to format the webpages and the styling was done with use of the **bootstrap** library 

Lastly, in order to obtain real data for the stocks, a public token from [IEX]( https://iexcloud.io/) was obtained.



