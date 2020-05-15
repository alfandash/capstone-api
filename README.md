# API Documentation
This API contain chinook.db data with some data wrangling. You can check data folder to get `chinook.db` to look RAW data before process in this end point

Where full URLs are provided in responses they will be rendered as if service is running on 'https://algoritma-api-capstone.herokuapp.com/'.

___
## Open Endpoints : 
Open endpoints require no Authentication.

**List of Country** : 
> `GET /country`    

Return list of Country you can use to other endpoints

**Total frequencies by Country** : 

> `GET /invoice/total/freq/<country>`    

Return total frequencies selected `<country>`. Available country you can found from `GET /country`

**Total amount invoice by Year** : 

> `GET /invoice/total/<year>`  

Return total amount where selected `<year>`, year limited from 2009 - 2013

**List of Customer** : 

> `GET /customer`    

Return full data customer

**Most favorite Artist by User** : 

> `GET /customer/topbuy/<customerid>`    

Return list of Artists, Albums, Total Invoice where `<customerid>`. You can get customer id from other endpoint `GET /customer`
___
## Example :

I want get list of county 

**Request** :  

Method = GET  
URL =  https://algoritma-api-capstone.herokuapp.com/

**Response** : 
```json
{
    "0": {
        "0": "Brazil",
        "1": "Germany",
        "2": "Canada",
        "3": "Norway",
        "4": "Czech Republic",
        "5": "Austria",
        "6": "Belgium",
        "7": "Denmark",
        "8": "USA",
        "9": "Portugal",
        "10": "France",
        "11": "Finland",
        "12": "Hungary",
        "13": "Ireland",
        "14": "Italy",
        "15": "Netherlands",
        "16": "Poland",
        "17": "Spain",
        "18": "Sweden",
        "19": "United Kingdom",
        "20": "Australia",
        "21": "Argentina",
        "22": "Chile",
        "23": "India"
    }
}
```
