import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """Looping over drop_table_queries which is a list of DROP statements which drops existing tables created on redshift db."""
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """Looping over create_table_queries which is a list of CREATE statements which creates the staging tables, fact table and dimension tables on redshift db."""
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    This is the MAIN function which creates the connection to the redshift cluster and calls functions to Drop and Create the Staging/Fact/Dimensions tables. It opens up a connection to the cluster and creates a cursor for the connection. It then passes the connection and the cursor as argument of the other functions.
    """
    config = configparser.ConfigParser()
    #Read configuration parameter values from dwh.cfg configuratio file. 
    config.read('dwh.cfg')

    #creates a connections to th redshift cluster using the config values.
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    
    #Creates a cursor for the redshift connecton.     
    cur = conn.cursor()

    #Calls a function with Connction and Cursor as arguments to Drop the existing tables on Redshift
    drop_tables(cur, conn)
    
    #Calls a function with Connection and Cursor as arguments to create staging tables and Fact/Dimension tables on Redshift.
    create_tables(cur, conn)

    #Closes the connection.
    conn.close()


if __name__ == "__main__":
    main()