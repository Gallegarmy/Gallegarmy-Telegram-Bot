import mysql.connector
import os
import structlog

class db_handler:
    def __init__(self):
        self.logger = structlog.get_logger()
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Establishes a connection to the database and handles any connection errors.
        """
        try:
            self.connection = mysql.connector.connect(
                host=os.environ.get("MYSQL_HOST"),
                user=os.environ.get("MYSQL_USER"),
                password=os.environ.get("MYSQL_PASSWORD"),
                database=os.environ.get("MYSQL_DATABASE"),
            )
            self.cursor = self.connection.cursor(dictionary=True)  # Dictionary cursor
            return self.cursor
        except mysql.connector.Error as err:
            self.logger.error("Failed to connect to the database", error=str(err))
            raise RuntimeError("Database connection failed") from err

    def execute(self, query, params=None):
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
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.logger.debug("Database connection closed")