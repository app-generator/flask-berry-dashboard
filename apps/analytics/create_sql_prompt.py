import pandas as pd

def create_message(conn, query, history):

    class message:
            
        def __init__(message, system, user): #, column_names, column_attr):
            message.system = system
            message.user = user
            # message.column_names = column_names
            # message.column_attr = column_attr
        
    system_template = """
    Respond to a user's request by considering the conversational history shown here {} and writing a SQL query given the following SQL table. \n
    Please consider verbs with all their tenses and assume and dates mentioned default to this year unless specified differently.

    CREATE TABLE `ldfe_jobs` ({}) \n
    """

    user_template = "Write a SQL query that returns - {}"
    
    #tbl_describe = duckdb.sql("DESCRIBE SELECT * FROM " + table_name +  ";")

    tbl_describe = pd.read_sql_query("select * from ldfe_jobs", con=conn)

    # col_attr = tbl_describe[["column_name", "column_type"]]
    # col_attr["column_joint"] = col_attr["column_name"] + " " +  col_attr["column_type"]
    # col_names = str(list(col_attr["column_joint"].values)).replace('[', '').replace(']', '').replace('\'', '')
    
    table_cols = """`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
                    `timestamp` timestamp NOT NULL DEFAULT NULL,
                    `realm` varchar(40) NOT NULL,
                    `site` varchar(4) COLLATE utf8mb4_unicode_ci NOT NULL,
                    `jobtype` varchar(40) NOT NULL,
                    `status` ENUM('success', 'fail'),
                    `note` varchar(500) DEFAULT NULL,
                    `fail reason` varchar(500) DEFAULT NULL,
                    PRIMARY KEY (`id`)"""
    system = system_template.format(history, table_cols)
    
    user = user_template.format(query)
        
    m = message(system = system, user = user) #, column_names = col_attr["column_name"], column_attr = col_attr["column_type"])
        
    return m
