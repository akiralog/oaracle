import sqlite3

class DatabaseManager:
    def __init__(self, db_name="locations.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            town_name TEXT NOT NULL,
            location_id INTEGER NOT NULL UNIQUE,
            is_tidal BOOLEAN NOT NULL CHECK (is_tidal IN (0, 1))
        );
        """)
        self.conn.commit()

    def add_location(self, town_name: str, location_id: int, is_tidal: bool):
        self.cursor.execute("SELECT 1 FROM locations WHERE location_id = ?", (location_id,))
        if self.cursor.fetchone():
            print(f"Location ID {location_id} already exists in DB. Skipping insert.")
            return

        self.cursor.execute("""
        INSERT INTO locations (town_name, location_id, is_tidal)
        VALUES (?, ?, ?)
        """, (town_name, location_id, int(is_tidal)))
        self.conn.commit()
        print(f"Added location: {town_name} (ID: {location_id})")

    def get_all_locations(self):
        self.cursor.execute("SELECT * FROM locations")
        return self.cursor.fetchall()

    def get_location_by_location_id(self, location_id: int):
        self.cursor.execute("SELECT * FROM locations WHERE location_id = ?", (location_id,))
        return self.cursor.fetchone()
    
    def get_location_by_name(self, town_name: str):
        self.cursor.execute("SELECT * FROM locations WHERE town_name = ?", (town_name,))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
