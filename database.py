import streamlit as st
import psycopg2
import os
import json
from dotenv import load_dotenv


load_dotenv()

# Set up PostgreSQL database credentials
db_credentials = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT")
}

# Function to execute SQL query
def execute_query(query):
    try:
        conn = psycopg2.connect(**db_credentials)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]  # Get column names
        cursor.close()
        conn.close()
        return column_names, result
    except psycopg2.Error as e:
        st.error(f"Error executing SQL query: {e}")
        return None, None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None

# Function to handle database-related prompts
def handle_database_prompt(prompt):
    return execute_query(prompt)

# Main Streamlit app
def main():
    st.title("AI Chatbot")

    # Connect to PostgreSQL database
    try:
        conn = psycopg2.connect(**db_credentials)
        cur = conn.cursor()
    except psycopg2.Error as e:
        st.error(f"Error connecting to the database: {e}")
        return

    # Load data from the database
    try:
        cur.execute("SELECT * FROM products;")
        column_names, rows = execute_query("SELECT * FROM products;")  # Fetch column names and data
    except psycopg2.Error as e:
        st.error(f"Error executing the query: {e}")
        return
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    # Display the loaded data
    st.write("Data loaded from the PostgreSQL database:")
    if rows:
        for row in rows:
            st.write(row)
    else:
        st.warning("No records found.")

    # Convert data to JSON and save to file
    json_data = {}
    if rows:
        for index, row in enumerate(rows):
            record = {}
            for i, col in enumerate(column_names):
                record[col] = row[i]
            json_data[f"record_{index+1}"] = record

        # Write JSON data to a file
        with open("database_data.json", "w") as json_file:
            json.dump(json_data, json_file, indent=4)
        st.success("JSON file created successfully!")

if __name__ == "__main__":
    main()
