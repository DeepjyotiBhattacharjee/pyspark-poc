# FastAPI + PySpark CRUD Application

## Overview

This project is a **CRUD API** built using **FastAPI** and **PySpark**. It provides basic functionalities to create, read, update, and delete user records stored in a MySQL database. The application integrates FastAPI for API development and PySpark for handling data operations, making it efficient for large-scale data manipulation.

## Features

- **User Management**: Create, Read, Update, and Delete (CRUD) operations on user records.
- **PySpark Integration**: Handles data processing using PySpark DataFrames.
- **MySQL Support**: Connects to and manipulates user records in a MySQL database using PySpark and PyMySQL.
- **CORS Support**: Cross-origin resource sharing enabled to allow requests from any origin.
- **Response Validation**: API responses are validated using Pydantic models.

## Prerequisites

- **Python 3.11.8** or higher.
- **Java 8+** (required for PySpark).
- **MySQL** database.
- **Apache Spark**.
- **MySQL Connector JAR** file for Spark (`mysql-connector-j-9.0.0.jar`).

Ideally you'd want to keep the mysql-connector-j-9.0.0.jar file in .gitignore file, since we don't want git to track it.

## 4. Set up MySQL
- Create a MySQL schema named my_schema.
- update spark_handler.py in the app/ directory with your MySQL credentials if needed:

self.jdbc_url = "jdbc:mysql://127.0.0.1:3306/my_schema"
self.db_properties = {
    "user": "your_mysql_user",
    "password": "your_mysql_password",
    "driver": "com.mysql.cj.jdbc.Driver"
}


## Set up PySpark on Windows

1. Install Java Development Kit (JDK)
PySpark requires Java 8 or higher. You can install it from [Oracle's](https://www.oracle.com/java/technologies/javase-downloads.html) website or use an open-source alternative like OpenJDK.

After installation, add the JDK bin path to your system's PATH environment variable.

2. Add the following environment variables:

SPARK_HOME: Path to your Spark installation directory (e.g., C:\spark).
HADOOP_HOME: Set this to the same value as SPARK_HOME or download Hadoop binaries.
JAVA_HOME: Path to your JDK installation directory (e.g., C:\Program Files\Java\jdk1.8.0_241).
PATH: Add %SPARK_HOME%\bin and %JAVA_HOME%\bin to your system's PATH variable.

3. Configure winutils.exe (for Hadoop)
Download the winutils.exe binary for the Hadoop version you are using and place it in a bin directory within your Hadoop installation path (e.g., C:\hadoop\bin). Add this path to the HADOOP_HOME environment variable.
Note : I have attached the winutils.exe file here for you to download. In practice, it shouldn't be there in the code-base.

4. Verify Installation
To verify Spark is set up properly, run the following in a terminal or command prompt:
    pyspark
This should open an interactive PySpark shell.

5. Run the application
Start the FastAPI server using Uvicorn:

uvicorn app.main:app --host localhost --port 5001 --reload

## Usage
Once the server is running, you can interact with the API. Below are the available endpoints:

**Endpoints**
POST /users/create - Create a new user.
GET /users/read/{user_id} - Read a user's information by ID.
PUT /users/update/{user_id} - Update a user's information by ID.
DELETE /users/delete/{user_id} - Delete a user by ID.

**Sample Request**
Create User (POST /users/create):

{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "age": 30,
  "address": "123 Main St",
  "phone_number": "123-456-7890",
  "gender": "Male",
  "membership_status": "Active"
}


**Project Structure**

.
├── app/
│   ├── main.py                           # FastAPI app setup
│   ├── controllers.py                    # API routes and business logic
│   ├── spark_handler.py                  # PySpark and MySQL integration
│   ├── schemas.py                        # Pydantic models for request validation
│   ├── utils.py                          # Utility functions for response handling
│   ├── mysql-connector-j-9.0.0.jar       # MySQL JDBC Driver for PySpark
└── requirements.txt                      # Python dependencies


# Resources

PySpark Documentation (https://spark.apache.org/docs/latest/api/python/index.html)
Youtube (https://www.youtube.com/watch?v=_C8kWso4ne4)