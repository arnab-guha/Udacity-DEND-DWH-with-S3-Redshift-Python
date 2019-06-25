import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


#Function definition for loading staging tables from files in S3 buckets.
def load_staging_tables(cur, conn):
    """Looping over copy_table_queries which is a list of COPY statements which copies data from S3 to staging tables on redshift db."""
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

#Function definition for loading Fact & dimension tables using the staging tables. 
def insert_tables(cur, conn):
    """Looping over insert_table_queries which is a list of insert statements which inserts data into Fact and Dimnsion tables using the staging tables. """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    This is the MAIN function which creates the connection to the redshift cluster and calls functions to load staging tables and insert records to the fact and dimension tables. It opens up a connection to the cluster and creates a cursor for the connection. It then passes the connection and the cursor as argument of the other functions.
    """
    config = configparser.ConfigParser()
    
    #Read configuration parameter values from dwh.cfg configuratio file. 
    config.read('dwh.cfg')

    #creates a connections to th redshift cluster using the config values.
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))

    #Creates a cursor for the redshift connecton. 
    cur = conn.cursor()
    
    #Calls the function to load staging tables from the files in S3 buckets. Passes the cursor and connection as arguments. 
    load_staging_tables(cur, conn)
    
    #Calls the function to load data into Fact and Dimension tables using the staging tables. Passes the cursor and connection as arguments. 
    insert_tables(cur, conn)
    
    #Closes the connection.
    conn.close()


if __name__ == "__main__":
    main()