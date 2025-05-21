import duckdb
import pandas as pd


class DuckdbUtils:
    def __init__(self, database_path: str = "../data/nyc_parking_violations.db"):
        self.database_path = database_path
        
    def run_sql_query_and_return_df(
            self,
            query: str,
            database_path: str = "data/nyc_parking_violations.db"
            ) -> pd.DataFrame:
        """
        Executes a provided SQL query against a DuckDB database and returns the
        results as a Pandas DataFrame.

        Due to DuckDB's limitation of allowing only one active database connection
        per database file at a time, this function explicitly opens a new
        connection for each query execution and closes it immediately afterward,
        enabling sequential access by multiple applications or processes.

        Parameters:
            query (str): The SQL query to execute.
            database_path (str, optional): Path to the DuckDB database file.
                Defaults to "data/nyc_parking_violations.db".

        Returns:
            pd.DataFrame: DataFrame containing the query results.

        Example:
            >>> df = run_sql_query_and_return_df(
            ...     "SELECT * FROM violations LIMIT 10;"
            ... )
            >>> print(df.head())
        """
        try:
            con = duckdb.connect(database=self.database_path)
            result = con.sql(query).df()
        except Exception as e:
            try:
                con.close()
                con = duckdb.connect(database=self.database_path)
                result = con.sql(query).df()
            except Exception as e2:
                print(f"Error executing SQL query: {str(e)}")
                raise
        finally:
            # This block always executes, whether an exception occurred or not
            con.close()
        
        return result

    def load_csv_file_to_db(
            self,
            csv_path: str,
            database_path: str = "data/nyc_parking_violations.db",
            ) -> None:
        """
        Loads a CSV file into a DuckDB database table.

        This function creates a new table in the DuckDB database with the name
        specified in the csv_path parameter. It then reads the CSV file and
        inserts the data into the table.
        """
        sql_query_import_1 = f"""
        CREATE OR REPLACE TABLE parking_violation_codes AS
        SELECT *
        FROM
        read_csv_auto(
        '{csv_path}/dof_parking_violation_codes.csv',
        normalize_names=True
        )
        """

        sql_query_import_2 = f"""
        CREATE OR REPLACE TABLE parking_violations_2023 AS
        SELECT *
        FROM read_csv_auto(
        '{csv_path}/parking_violations_issued_fiscal_year_2023_sample.csv',
        normalize_names=True
        )
        """
        try:
            con = duckdb.connect(database=self.database_path)
            con.sql(sql_query_import_1)
            con.sql(sql_query_import_2)
        except Exception as e:
            try:
                con.close()
                con = duckdb.connect(database=self.database_path)
                con.sql(sql_query_import_1)
                con.sql(sql_query_import_2)
            except Exception as e2:
                print(f"Error executing SQL query: {str(e)}")
                raise
        finally:
            con.close()

        return None


if __name__ == "__main__":
    None
