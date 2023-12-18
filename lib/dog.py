import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        with CONN:
            CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS dogs"
        with CONN:
            CURSOR.execute(sql)

    def save(self):
        if self.id is None:
            # Insert a new row
            sql = "INSERT INTO dogs (name, breed) VALUES (?, ?)"
            with CONN:
                CURSOR.execute(sql, (self.name, self.breed))
                self.id = CURSOR.lastrowid
        else:
            # Update existing row
            sql = "UPDATE dogs SET name=?, breed=? WHERE id=?"
            with CONN:
                CURSOR.execute(sql, (self.name, self.breed, self.id))

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, data):
        dog = cls(data[1], data[2])
        dog.id = data[0]
        return dog

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM dogs"
        with CONN:
            return [cls.new_from_db(row) for row in CURSOR.execute(sql).fetchall()]

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM dogs WHERE name=?"
        with CONN:
            result = CURSOR.execute(sql, (name,)).fetchone()
            if result:
                return cls.new_from_db(result)
            return None

    @classmethod
    def find_by_id(cls, dog_id):
        sql = "SELECT * FROM dogs WHERE id=?"
        with CONN:
            result = CURSOR.execute(sql, (dog_id,)).fetchone()
            if result:
                return cls.new_from_db(result)
            return None

    # Bonus Methods (uncomment tests in pytest file to run these)
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            return cls.create(name, breed)

    def update(self):
        self.save()  # Since save handles both insert and update

