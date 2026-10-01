import psycopg2

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="retailpulse",
        user="postgres",
        password="adigs234"  # Replace with your actual password
    )
    
    print("Successfully connected to the retailpulse database!")
    
    # Close the connection
    connection.close()

except Exception as error:
    print(f"Failed to connect to database: {error}")