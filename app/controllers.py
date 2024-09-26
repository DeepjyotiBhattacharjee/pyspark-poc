from fastapi import APIRouter, Request
from schemas import CreateUserRequest, UpdateUserRequest, RespValidation
from spark_handler import SparkHandler
from utils import success_200, internal_server_error_500, not_found_404
import logging
from pyspark.sql.functions import col, coalesce

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def set_responses(response_model):
    def decorator(func):
        func.response_model = response_model
        return func
    return decorator

class UserController:
    def __init__(self):
        self.router = APIRouter()
        self.spark_handler = SparkHandler()

        self.router.post("/users/create")(self.create)
        self.router.get("/users/read/{user_id}")(self.read)
        self.router.put("/users/update/{user_id}")(self.update)
        self.router.delete("/users/delete/{user_id}")(self.delete)

    @set_responses(RespValidation)
    async def create(self, request: Request, obj: CreateUserRequest):
        """Create a new user record."""
        try:
            # Create a DataFrame from the input data
            new_user_df = self.spark_handler.spark.createDataFrame([{
                "name": obj.name,
                "email": obj.email,
                "age": obj.age,
                "address": obj.address,
                "phone_number": obj.phone_number,
                "gender": obj.gender,
                "membership_status": obj.membership_status
            }])

            # Write the DataFrame to MySQL
            self.spark_handler.write_to_mysql(new_user_df, "users", mode="append")
            return success_200({"message": "User record created successfully"})
        except Exception as e:
            logger.error(f"Error creating user record: {e}")
            return internal_server_error_500("Error creating user record")

    @set_responses(RespValidation)
    async def read(self, request: Request, user_id: int):
        """Fetch a user record by ID."""
        try:
            # Read the user data from MySQL
            condition = f"WHERE id = {user_id}"
            result_df = self.spark_handler.read_from_mysql("users", condition)

            if result_df.count() == 0:
                return not_found_404("User record not found")

            # Convert DataFrame to a list of dictionaries
            result = result_df.collect()
            return success_200([row.asDict() for row in result])
        except Exception as e:
            logger.error(f"Error fetching user record: {e}")
            return internal_server_error_500("Error fetching user record")

    @set_responses(RespValidation)
    async def update(self, request: Request, user_id: int, obj: UpdateUserRequest):
        """Update an existing user record using parameterized query."""
        try:
            query = """
                UPDATE my_schema.users 
                SET 
                    name = %s, 
                    email = %s, 
                    age = %s, 
                    address = %s, 
                    phone_number = %s, 
                    gender = %s, 
                    membership_status = %s 
                WHERE id = %s
            """
            parameters = (obj.name, obj.email, obj.age, obj.address, obj.phone_number, obj.gender, obj.membership_status, user_id)

            # Execute the SQL query with parameters
            self.spark_handler.execute_query(query, parameters)

            return success_200({"message": "User record updated successfully"})
        except Exception as e:
            logger.error(f"Error updating user record: {e}")
            return internal_server_error_500("Error updating user record")


    @set_responses(RespValidation)
    async def delete(self, request: Request, user_id: int):
        """Delete a user record."""
        try:
            # Create a SQL DELETE statement
            delete_sql = f"DELETE FROM my_schema.users WHERE id = {user_id}"

            # Execute the delete operation
            # self.spark_handler.spark.sql(delete_sql)
            self.spark_handler.execute_query(delete_sql)

            return success_200({"message": "User record deleted successfully"})
        except Exception as e:
            logger.error(f"Error deleting user record: {e}")
            return internal_server_error_500("Error deleting user record")

