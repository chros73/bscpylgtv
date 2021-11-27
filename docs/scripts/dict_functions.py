from sqlitedict import SqliteDict

class DictFunctions:
    def __init__(self, db_path, table="unnamed"):
        self.db_path = db_path
        self.table = table
        self.db = None

    @classmethod
    async def create(cls, *args, **kwargs):
        dict = cls(*args, **kwargs)
        await dict.async_init()
        return dict

    async def async_init(self):
        """Create db."""
        self.db = SqliteDict(self.db_path, self.table)

    async def write_key(self, key, val):
        """Save the key value pair into table."""
        self.db[key] = val
        self.db.commit()

    async def read_key(self, key):
        """Get value of key from table."""
        return self.db.get(key)

    async def list_keys(self):
        """Display all saved key value pairs."""
        for key, value in self.db.iteritems():
            print(key, value)
