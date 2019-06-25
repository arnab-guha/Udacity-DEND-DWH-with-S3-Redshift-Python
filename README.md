# Setting up a Data Warehouse on cloud for Sparkify
#### *Creation of the data warehouse in AWS Redshift and the necessary ETL pipeline to support the same*


### Purpose:
We will be creating a Data Warehouse for Sparkify on cloud using the Event Files and Song Files stored on AWS S3. The Data warehouse will have a fact table and set of dimension tables which will help Sparkify to analyze their data in a more effective way which will in turn help them to make better business decisions. It will help them to understand user's taste in songs, their choice and listening pattern and utlizing those analytics, Sparkiy will be able to provide more quality service and gain their user base. 

### Source File Information:
There are 2 different types of Data (Event Files and Song Files) that is available for the Sparkify music streaming application amd they are stored as JSON files. Following are the paths for the files:

**Song Data**
s3://udacity-dend/song_data

**Log Data** 
s3://udacity-dend/log_data

Following are the JSON file structures:


- Song Files: It has all Songs, Albums and Artist related details. Here is one sample row:
        {   "num_songs": 1, 
            "artist_id": "ARD7TVE1187B99BFB1", 
            "artist_latitude": null, 
            "artist_longitude": null, 
            "artist_location": "California - LA", 
            "artist_name": "Casual", 
            "song_id": "SOMZWCG12A8C13C480", 
            "title": "I Didn't Mean To", 
            "duration": 218.93179, 
            "year": 0
        }

- Log Files: It has the logs of the user's music listening activity on the app. Here is one sample row:
        {   "artist":null,
            "auth":"Logged In",
            "firstName":"Walter",
            "gender":"M",
            "itemInSession":0,
            "lastName":"Frye",
            "length":null,
            "level":"free",
            "location":"San Francisco-Oakland-Hayward, CA",
            "method":"GET",
            "page":"Home",
            "registration":1540919166796.0,
            "sessionId":38,
            "song":null,
            "status":200,
            "ts":1541105830796,
            "userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"39"
        }
        
### Approach:
Here are steps we will be taking to create the data warehouse on Cloud. 

- Create a Redshift Cluster using python which will have sparkify database. 
- Create set of Staging Tables, Fact Table and Dimension tables on sparkify database.
- Access the Log Files and Song Files available on S3 and load them in the staging tables.
- Run a set of Insert queries to load data from staging tables to the Fact and Dimension tables. 

### Technical Design:
Here are the steps taken to create the sparkify data warehouse on cloud.
- Create a Redshift cluster
    - The necessary code to create Redshift cluster is available in create_cluster.ipynb notebook. The code utilize dwh.cfg configuration file which has all necessary parameters. Once the cluster is ready, the ARN and Endpoint(host) values should be noted and inserted in dwh.cfg file. 
- Create set of Staging Tables, Fact table and dimension table in Redshift. 
    - We have 2 set of python files to achieve this step. The first file sql_queries.py has all drop table, create table statements saved in variables. While the create_tables.py file has functions which trigger the table creation by importing the variables from sql_queries.py. So to achieve this step, run sql_queries.py and then create_tables.py from console. 
- Retrieve the JSON files stored in S3 bucket, transform and load them in the Fact/Dimensions tables.
    - This step can be achieved by running etl.py from the console. Sql_queries.py also have insert statements saved in the variables. The etl.py file import those variables and pass them as argument to the functions for importing data from JSON file into staging tables and from staging tables to the main tables in data warehouse. 


### Data Analysis
Several queries are executed against the newly created Fact & Dimensions tables to analyse the data. The same is stored under Analytics.ipynb