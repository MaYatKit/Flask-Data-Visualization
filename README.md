# Flask-Data-Visualization

This project is a promising showcase about data visualization for industrial manufacture factories, being low-cost and easy to use, live demo: <br/> Two main components are the following: <br/>
[data_persistence.py](https://github.com/MaYatKit/Flask-Data-Visualization/blob/master/data_persistence.py): Automatically periodically data persisting from constantly increased CSVs onto Google G Suite location. Normally, PLCs of industrial machinery are capable to spew out data constantly, no matter what format it is, this script is adaptive to fit in with slightly changes; Also, we choose SQLite to storage data, which is a standalone file with [free tool](https://sqlitebrowser.org/) to open and view data directly, and SQLite is simple to populate with; Finally, Google G Suite are choosed by many traditional manufacture factories to share and manage files, which is suitable to storage the DB file with an automatic synchronization 

[Web application](): We utilize Flask and Chart.js to conduct this web application, retrieving data from a SQLite DB file which is storaged on Google G Suite location 
