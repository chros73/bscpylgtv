import os
from sqlitedict import SqliteDict

class StorageSqliteDict:
    def __init__(self, db_path=None, table="unnamed"):
        KEY_FILE_NAME = ".aiopylgtv.sqlite"
        USER_HOME = "HOME"

        self.db = None
        self.table = table

        if db_path:
            self.db_path = db_path
        else:
            if os.getenv(USER_HOME) is not None and os.access(
                os.getenv(USER_HOME), os.W_OK
            ):
                self.db_path = os.path.join(os.getenv(USER_HOME), KEY_FILE_NAME)

            self.db_path = os.path.join(os.getcwd(), KEY_FILE_NAME)

    @classmethod
    async def create(cls, *args, **kwargs):
        storage = cls(*args, **kwargs)
        await storage.async_init()
        return storage

    async def async_init(self):
        """Create db."""
        self.db = SqliteDict(self.db_path, self.table)

    async def set_key(self, key, val):
        """Set the key value pair into storage."""
        if key is None or val is None:
            return

        self.db[key] = val
        self.db.commit()

    async def get_key(self, key):
        """Get value of key from storage."""
        if key is None:
            return

        return self.db.get(key)

    async def list_keys(self):
        """Display all key value pairs from storage."""
        for key, value in self.db.iteritems():
            print(key, value)
