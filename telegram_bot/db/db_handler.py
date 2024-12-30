import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
import os
import structlog

class DbHandler:
    _pool = None 

    @staticmethod
    def initialize_pool(pool_size=10):
        """
        Initializes the connection pool. This should be called once when the application starts.
        """
        if not DbHandler._pool:
            try:
                DbHandler._pool = MySQLConnectionPool(
                    pool_name="db_pool",
                    pool_size=pool_size,
                    pool_reset_session=True,
                    host=os.environ.get("MYSQL_HOST"),
                    user=os.environ.get("MYSQL_USER"),
                    password=os.environ.get("MYSQL_PASSWORD"),
                    database=os.environ.get("MYSQL_DATABASE"),
                )
                structlog.get_logger().info("Connection pool initialized", pool_size=pool_size)
            except mysql.connector.Error as err:
                structlog.get_logger().error("Failed to initialize connection pool", error=str(err))
                raise RuntimeError("Connection pool initialization failed") from err

    def __init__(self):
        self.logger = structlog.get_logger()
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Retrieves a connection from the pool.
        """
        try:
            if not DbHandler._pool:
                raise RuntimeError("Connection pool is not initialized")
            self.connection = DbHandler._pool.get_connection()
            self.cursor = self.connection.cursor(dictionary=True)  # Dictionary cursor
            return self.cursor
        except mysql.connector.Error as err:
            self.logger.error("Failed to retrieve connection from pool", error=str(err))
            raise RuntimeError("Failed to retrieve connection from pool") from err

    def execute(self, query: str, params=None):
        """
        Executes a given SQL query with optional parameters.
        """
        try:
            if not self.cursor:
                raise RuntimeError("Database connection is not established")
            self.cursor.execute(query, params or ())
            return self.cursor
        except mysql.connector.Error as err:
            self.logger.error("Query execution failed", query=query, params=params, error=str(err))
            raise RuntimeError("Database query failed") from err

    def commit(self):
        """
        Commits the current transaction.
        """
        try:
            if self.connection:
                self.connection.commit()
        except mysql.connector.Error as err:
            self.logger.error("Failed to commit transaction", error=str(err))
            raise RuntimeError("Transaction commit failed") from err

    def close(self):
        """
        Closes the database connection and the cursor.
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            self.logger.debug("Database connection closed")
        except mysql.connector.Error as err:
            self.logger.error("Error while closing the connection", error=str(err))
            raise RuntimeError("Failed to close the database connection") from err
