import json
import os
from typing import List, Dict, Any, Optional

class JSONDataManager:
    def __init__(self, filepath: str = "data.json"):
        """Initialize the JSON Data Manager with a file path."""
        self.filepath = filepath
        self.data = self.load_data()

    def load_data(self) -> Dict[str, Any]:
        """Load data from JSON file."""
        if not os.path.exists(self.filepath):
            print(f"File '{self.filepath}' not found. Creating new file.")
            return {"entries": []}
        
        try:
            with open(self.filepath, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format. Initializing with empty data.")
            return {"entries": []}

    def save_data(self) -> None:
        """Save data to JSON file."""
        try:
            with open(self.filepath, 'w') as file:
                json.dump(self.data, file, indent=2)
            print(f"Data saved successfully to '{self.filepath}'")
        except Exception as e:
            print(f"Error saving data: {e}")

    def add_entry(self, entry: Dict[str, Any]) -> None:
        """Add a new entry to the data."""
        if "entries" not in self.data:
            self.data["entries"] = []
        
        # Auto-generate ID if not provided
        if "id" not in entry:
            entry["id"] = max([e.get("id", 0) for e in self.data["entries"]], default=0) + 1
        
        self.data["entries"].append(entry)
        self.save_data()
        print(f"Entry added successfully with ID: {entry.get('id')}")

    def search(self, query: str, fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Search entries by query string in specified fields or all fields."""
        query_lower = query.lower()
        results = []
        
        for entry in self.data.get("entries", []):
            if fields:
                # Search only in specified fields
                for field in fields:
                    if field in entry and query_lower in str(entry[field]).lower():
                        results.append(entry)
                        break
            else:
                # Search in all fields
                for value in entry.values():
                    if query_lower in str(value).lower():
                        results.append(entry)
                        break
        
        return results

    def get_entry_by_id(self, entry_id: int) -> Optional[Dict[str, Any]]:
        """Get a single entry by ID."""
        for entry in self.data.get("entries", []):
            if entry.get("id") == entry_id:
                return entry
        return None

    def update_entry(self, entry_id: int, updates: Dict[str, Any]) -> bool:
        """Update an entry by ID."""
        entry = self.get_entry_by_id(entry_id)
        if entry:
            entry.update(updates)
            self.save_data()
            print(f"Entry {entry_id} updated successfully")
            return True
        else:
            print(f"Entry {entry_id} not found")
            return False

    def delete_entry(self, entry_id: int) -> bool:
        """Delete an entry by ID."""
        entries = self.data.get("entries", [])
        for i, entry in enumerate(entries):
            if entry.get("id") == entry_id:
                entries.pop(i)
                self.save_data()
                print(f"Entry {entry_id} deleted successfully")
                return True
        print(f"Entry {entry_id} not found")
        return False

    def list_all_entries(self) -> List[Dict[str, Any]]:
        """Return all entries."""
        return self.data.get("entries", [])

    def display_entries(self, entries: Optional[List[Dict[str, Any]]] = None) -> None:
        """Display entries in a formatted way."""
        entries_to_display = entries if entries is not None else self.list_all_entries()
        
        if not entries_to_display:
            print("No entries found.")
            return
        
        print("\n" + "="*80)
        for entry in entries_to_display:
            print(f"\nID: {entry.get('id')}")
            for key, value in entry.items():
                if key != 'id':
                    print(f"  {key}: {value}")
        print("="*80 + "\n")
