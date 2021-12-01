from typing import Protocol, runtime_checkable

@runtime_checkable
class StorageProto(Protocol):
    async def set_key(self, key, val):
        """Set the key value pair into storage."""

    async def get_key(self, key):
        """Get value of key from storage."""

    async def list_keys(self):
        """Display all key value pairs from storage."""
