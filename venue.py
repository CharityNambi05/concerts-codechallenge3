class Venue:
    def __init__(self, venue_id):
        self.venue_id = venue_id

    def concerts(self, conn):
        query = "SELECT * FROM concerts WHERE venue_id = %s"
        with conn.cursor() as cur:
            cur.execute(query, (self.venue_id,))
            return cur.fetchall()

    def bands(self, conn):
        query = """
        SELECT DISTINCT bands.* FROM bands
        JOIN concerts ON concerts.bands_id = bands.id
        WHERE concerts.venue_id = %s
        """
        with conn.cursor() as cur:
            cur.execute(query, (self.venue_id,))
            return cur.fetchall()

    def concert_on(self, date, conn):
        query = "SELECT * FROM concerts WHERE venue_id = %s AND date = %s LIMIT 1"
        with conn.cursor() as cur:
            cur.execute(query, (self.venue_id, date))
            return cur.fetchone()

    def most_frequent_band(self, conn):
        query = """
        SELECT bands.*, COUNT(concerts.id) AS num_performances
        FROM concerts
        JOIN bands ON concerts.bands_id = bands.id
        WHERE concerts.venue_id = %s
        GROUP BY bands.id
        ORDER BY num_performances DESC
        LIMIT 1
        """
        with conn.cursor() as cur:
            cur.execute(query, (self.venue_id,))
            return cur.fetchone()