This python file must be used on computer with an active Bloomberg terminal (xbbg library requirement).

https://xbbg.readthedocs.io/en/latest/

The program uses multiple libraries among which:

- xbbg for bloomberg related functions
- easygui for options selection while running it (user interface)
- smtplib (mail protocol)
- email multipart 

The script searches for the equity tickers that the active bloomberg terminal is following,
The script then looks for potential upcoming dividends and their value.

Then every piece of information is compiled into an html table, and added to an html email, the final mail is sent to a list of receivers that the users provide.


The script would require a bit of cleaning (separating the functions from the rest)