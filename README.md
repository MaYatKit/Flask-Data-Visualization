# Flask-Data-Visualization

This project is a promising showcase about data visualization for industrial manufacture factories, being affordable, intuitive and easy to conduct.<br/>
<img title="Screen display of the Web application" width="700" src="gif.gif"><br/><br/>
Zoom & drag and displaying other field data when hovering: (**21.08.2020 update**)<br/>
<img title="Screen display of the Web application" width="700" src="zoom.gif">

Live demo: https://data-visualization-flask.herokuapp.com<br/> 
### Description of two main components are the following: <br/>
[data_persistence.py](https://github.com/MaYatKit/Flask-Data-Visualization/blob/master/data_persistence.py): Automatically periodically data persisting from constantly increased CSVs onto Google G Suite location. Normally, PLCs of industrial machinery are capable to spew out data constantly, no matter what format it is, this script is adaptive to fit in with slightly changes; Also, we choose SQLite to storage data, which is a standalone file with [free tool](https://sqlitebrowser.org/) to open and view data directly, and SQLite is simple to populate with; Finally, Google G Suite are choosed by many traditional manufacture factories to share and manage files, which is suitable to storage the DB file with an automatic synchronization 

[Web application](https://data-visualization-flask.herokuapp.com/rock_roll_charts.html): We utilize Flask and Chart.js to conduct this web application, retrieving data from a SQLite DB file which is storaged on Google G Suite location. You can look into charts of manufacture data by date, recipe and which time in a day; also, you can dig in points of data by hovering on the curve; and normally, one machinery might have different recipes to manufacture in one day, so that we add recipe marker on the start point of each cycle.

### Update
**21.08.2020:** Added a zooming function for graphs and code for displaying other fields when hovering on a field such as display mould temperature when hovering on oven temperature with the nearest timestamp.


### Future work
A zooming function for graphs is scheduled and we plan to display other fields when hovering on a field such as display mould temperature when hovering on oven temperature with the nearest timestamp; also, a CSV export function which can be choosed field and range is being considered.<br/>
**21.08.2020:** We plan to optimize the speed of zooming.
