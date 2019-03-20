def con():
    import pyodbc
    from pathlib import Path
    from dotenv import load_dotenv
    import os
    env_path = Path('.') / '.env'
    load_dotenv(env_path)
    server = 'DESKTOP-HROK9FV\\SQLEXPRESS01'
    database = 'WebAnalyzer'
    username = os.getenv('ID')
    password = os.getenv('PASSWORD')
    print(server,database,username,password)
    cnxn = pyodbc.connect('DRIVER=SQL Server Native Client 11.0;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn