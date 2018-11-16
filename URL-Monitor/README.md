# URL Monitor
URL Montior via GET Request and dump the data to InfluxDB. 


| Variable | Value  | Description |
| :---         |     :---:      |          ---: |
|  INFLUX_URL_STRING       | URL with DB          |   Example: https://hawk-datasource.tothenew.net/write?db=hawkclient1    |
|  INFLUX_USERNAME       | Influx authentication Username        |   Influx authentication Username    |     
|  INFLUX_PASSWORD       | Influx authentication Password       |   Influx authentication Password   |


### Input
Pass URL List with an identifier in a form of key value pair to **weblist** .
**Example**
weblist={'Prod-LB': 'https://google.com',
           'Prod-Portal': 'https://google.com',
           'Prod-Api': 'https://google.com',
           'Prod-SOAP': 'https://google.com',
           'Prod-Admin': 'https://google.com'
           }

