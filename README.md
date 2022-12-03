
# InStock

© Chip Osur 2022

A utility for retrieving web docs and checking if an item is in stock.
This program uses XPATH expressions to search for paths indicating item availability, optionally sending an email notification via SMTP if it detects that the item may be available for order.

## Command Line Options

| Command     | Description                                    |
|------------:| -----------------------------------------------|
| `-f, -file` | Parse required and optional settings from file |
| `-h, -help` | Show utility help                              |
| `-v`        | Verbose output when running                    |

## Environment Variables

>`SMTP_SERVER_USERNAME=chip@example.com`  
>`SMTP_SERVER_PASSWORD=********`  

## Sample Settings File

>**url:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`https://www.example.com/store/products/popular-product/`  
>**notExistsXPATH:** &nbsp;&nbsp;`//span[text()="Sold out"]`  
>**cooldownMs:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`3000`  
>**email:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`chip@example.com`  
>**smtpServer:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`smtp.example.com`  
>**smtpPort:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`587`  