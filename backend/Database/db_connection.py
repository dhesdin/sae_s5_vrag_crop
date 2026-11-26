import sqlite3
from models.Response import Response

class DatabaseConnection:

    def __init__(self) -> None:
        self.connection = sqlite3.connect("./database.db")

    def get_connection(self: DatabaseConnection) -> sqlite3.Connection:
        """ Charger une connexion à la base de données

        Returns:
            sqlite3.Connection: Connexion à la base de données
        """
        return self.connection

    def insert_data(self: DatabaseConnection, data : Response) -> None:
        """
        Insérer des données dans la base de données

        Args:
            data (Response): Les données à insérer
        """
        cursor : sqlite3.Cursor = self.get_connection().cursor()
        if not data:
            print("No data to insert.")
            return

        try:
            cursor.execute("INSERT INTO responses (user_input, bot_response) VALUES (?, ?)", (data.user_input, data.bot_response))
            self.get_connection().commit()
        except sqlite3.Error as e:
            print(f"Error occurred while inserting data: {e}")