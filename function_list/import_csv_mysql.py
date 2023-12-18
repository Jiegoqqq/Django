# Import necessary libraries and the function
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, VARCHAR


# def csv2mysql(df, table_name):
#     # Create a connection to the MySQL database
#     engine = create_engine('mysql+pymysql://jienan:624001479@localhost:3306/WEB1')
    
#     # If replace_inf is True, replace "inf" values with inf_value or None
#     df = df.replace([np.inf, -np.inf], np.nan)
    
#     # Insert the DataFrame into the MySQL table
#     df.to_sql(table_name, con=engine, if_exists='replace', index=False)

# # Read the CSV file, specifying the first row as column names
# df = pd.read_csv('/home/cosbi/Downloads/WT_CRISPR_WAGO_1_FLAG_IP_sRNA_seq_bedgraph.csv', header=0)

# # Call the function to insert the DataFrame into the MySQL table
# csv2mysql(df, 'WT_CRISPR_WAGO_1_FLAG_IP_sRNA_seq_bedgraph')

#匯入sql檔建立column 的格式要像這樣
# START TRANSACTION;

# CREATE TABLE IF NOT EXISTS `Gene` (
#     `Gene_ID` VARCHAR(255), -- Use an appropriate length
#     `Transcript_ID` TEXT,
#     `numbers` INTEGER,
#     PRIMARY KEY (`Gene_ID`)
# );
# COMMIT;



def modify_data_types(df):
    data_types = {}  # Create an empty dictionary to store data types

    # Determine the maximum length for each column
    for column_name in df.columns:
        max_length = df[column_name].astype(str).str.len().max()
        data_types[column_name] = VARCHAR(max_length)

    return data_types

def csv2mysql(df, table_name):
    # Create a connection to the MySQL database
    engine = create_engine('mysql+pymysql://jienan:624001479@localhost:3306/WEB1')

    # Modify data types based on the maximum length
    data_types = modify_data_types(df)
    df = df.replace([np.inf, -np.inf], np.nan)
    # Insert the DataFrame into the MySQL table with the specified data types
    df.to_sql(table_name, con=engine, if_exists='replace', index=False, dtype=data_types)

# Read the CSV file, specifying the first row as column names
df = pd.read_csv('/home/cosbi/Downloads/Lbarbarum_table.csv', header=0)

# Call the function to insert the DataFrame into the MySQL table with the specified data types
csv2mysql(df, 'Lbarbarum')
