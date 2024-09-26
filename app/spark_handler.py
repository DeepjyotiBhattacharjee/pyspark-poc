from pyspark.sql import SparkSession, DataFrame
import pymysql

class SparkHandler:
    """
    A class to handle PySpark operations and database connections for CRUD operations.
    """

    def __init__(self):
        """
        Initializes the Spark session and JDBC properties.
        """
        self.spark = self.create_spark_session()
        self.jdbc_url = "jdbc:mysql://127.0.0.1:3306/my_schema"
        self.db_properties = {
            "user": "root",
            "password": "Snape@1993",
            "driver": "com.mysql.cj.jdbc.Driver"
        }

    def create_spark_session(self) -> SparkSession:
        """
        Creates a Spark session with the necessary configuration, suppressing unnecessary warnings.
        
        Returns:
            SparkSession: Configured Spark session instance.
        """
        try:
            # Suppressing unnecessary logging related to garbage collection and warnings
            spark = SparkSession.builder \
                .appName("SimpleCRUDApp") \
                .config("spark.jars", "app/mysql-connector-j-9.0.0.jar") \
                .config("spark.executor.memory", "4g") \
                .config("spark.driver.memory", "4g") \
                .config("spark.driver.maxResultSize", "2g") \
                .config("spark.executor.cores", "2") \
                .config("spark.sql.shuffle.partitions", "10") \
                .getOrCreate()

            print("Spark session created successfully with garbage collection optimizations.")
            return spark
        except Exception as e:
            print(f"Error creating Spark session: {e}")
            raise

    def read_from_mysql(self, table_name: str, condition: str = "") -> DataFrame:
        """
        Reads data from MySQL using Spark JDBC.

        Args:
            table_name (str): The name of the MySQL table.
            condition (str): Optional WHERE condition for filtering.

        Returns:
            DataFrame: PySpark DataFrame with the results.
        """
        query = f"(SELECT * FROM {table_name} {condition}) as tmp"
        try:
            df = self.spark.read.jdbc(self.jdbc_url, query, properties=self.db_properties)
            return df
        except Exception as e:
            print(f"Error reading data from MySQL: {e}")
            raise

    def write_to_mysql(self, df: DataFrame, table_name: str, mode: str = "append"):
        """
        Writes a PySpark DataFrame to a MySQL table.

        Args:
            df (DataFrame): The PySpark DataFrame to be written.
            table_name (str): The MySQL table where data will be written.
            mode (str): The write mode (append, overwrite, etc.).
        """
        try:
            df.write.jdbc(self.jdbc_url, table_name, mode=mode, properties=self.db_properties)
            print(f"Data written successfully to {table_name}")
        except Exception as e:
            print(f"Error writing data to MySQL: {e}")
            raise

    def execute_query(self, query: str,parameters=None):
        """
        Executes a non-returning SQL query (INSERT, UPDATE, DELETE) on MySQL using PyMySQL.

        Args:
            query (str): SQL query to execute.
        """
        try:
            connection = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='Snape@1993',
                database='my_schema'
            )
            with connection.cursor() as cursor:
                cursor.execute(query,parameters)
                connection.commit()
                print(f"Query executed successfully: {query}")
        except Exception as e:
            print(f"Error executing query: {e}")
        finally:
            connection.close()

    def close_spark_session(self):
        """
        Stops the Spark session.
        """
        self.spark.stop()
        print("Spark session stopped successfully.")
