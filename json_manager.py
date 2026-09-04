import json
import os
from typing import Dict, Any, Optional, List

class JSONDataManager:
    def __init__(self, filepath: str = "data.json"):
        """Initialize the JSON Data Manager with a file path."""
        self.filepath = filepath
        self.data = self.load_data()

    def load_data(self) -> Dict[str, Any]:
        """Load data from JSON file."""
        if not os.path.exists(self.filepath):
            print(f"File '{self.filepath}' not found. Creating new file.")
            return {"entries": {}}
        
        try:
            with open(self.filepath, 'r') as file:
                data = json.load(file)
                # Support both old format (list) and new format (dict)
                if isinstance(data.get("entries"), list):
                    # Convert old format to new format
                    return {"entries": {}}
                return data
        except json.JSONDecodeError:
            print("Error: Invalid JSON format. Initializing with empty data.")
            return {"entries": {}}

    def save_data(self) -> None:
        """Save data to JSON file."""
        try:
            with open(self.filepath, 'w') as file:
                json.dump(self.data, file, indent=2)
            print(f"✅ Data saved successfully to '{self.filepath}'")
        except Exception as e:
            print(f"❌ Error saving data: {e}")

    def entry_exists(self, entry_id: str) -> bool:
        """Check if an entry with the given ID exists."""
        return entry_id in self.data.get("entries", {})

    def add_entry(self, entry_id: str) -> bool:
        """Add a new entry with custom key-value pairs."""
        entries = self.data.get("entries", {})
        
        # Check if ID already exists
        if entry_id in entries:
            print(f"\n❌ ID '{entry_id}' already exists!")
            print("\nExisting object:")
            self.display_entry(entry_id, entries[entry_id])
            return False
        
        # Collect key-value pairs
        entry = {}
        print(f"\n📝 Enter key-value pairs for ID '{entry_id}'")
        print("(Press Enter with blank key to finish)\n")
        
        while True:
            key = input("Key (or press Enter to finish): ").strip()
            
            if not key:
                if not entry:
                    print("⚠️  No data entered. Entry not added.")
                    return False
                break
            
            # Check for duplicate keys
            if key in entry:
                print(f"⚠️  Key '{key}' already exists in this entry. Use a different key.")
                continue
            
            value = input(f"Value for '{key}': ").strip()
            entry[key] = value
            print()
        
        # Save the entry
        entries[entry_id] = entry
        self.data["entries"] = entries
        self.save_data()
        print(f"✅ Entry with ID '{entry_id}' added successfully!")
        return True

    def search(self, query: str) -> List[tuple]:
        """Search entries by query string in all fields."""
        query_lower = query.lower()
        results = []
        entries = self.data.get("entries", {})
        
        for entry_id, entry in entries.items():
            found = False
            # Search in ID
            if query_lower in entry_id.lower():
                found = True
            # Search in values
            else:
                for value in entry.values():
                    if query_lower in str(value).lower():
                        found = True
                        break
            
            if found:
                results.append((entry_id, entry))
        
        return results

    def get_entry_by_id(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Get a single entry by ID."""
        entries = self.data.get("entries", {})
        return entries.get(entry_id)

    def update_entry(self, entry_id: str) -> bool:
        """Update an entry by ID with interactive prompts."""
        entries = self.data.get("entries", {})
        
        if entry_id not in entries:
            print(f"❌ Entry with ID '{entry_id}' not found.")
            return False
        
        entry = entries[entry_id]
        print(f"\n📝 Updating entry with ID '{entry_id}'")
        print("Current entry:")
        self.display_entry(entry_id, entry)
        
        print("\n🔧 Update options:")
        print("1. Modify existing key")
        print("2. Add new key")
        print("3. Delete key")
        print("4. Cancel")
        
        choice = input("\nChoose option (1-4): ").strip()
        
        if choice == '1':
            key = input("Enter key to modify: ").strip()
            if key not in entry:
                print(f"❌ Key '{key}' not found in this entry.")
                return False
            
            new_value = input(f"Enter new value for '{key}': ").strip()
            entry[key] = new_value
            self.data["entries"][entry_id] = entry
            self.save_data()
            print(f"✅ Key '{key}' updated successfully!")
            return True
        
        elif choice == '2':
            key = input("Enter new key: ").strip()
            if not key:
                print("⚠️  Key cannot be empty.")
                return False
            
            if key in entry:
                print(f"❌ Key '{key}' already exists. Use modify option to change it.")
                return False
            
            value = input(f"Enter value for '{key}': ").strip()
            entry[key] = value
            self.data["entries"][entry_id] = entry
            self.save_data()
            print(f"✅ Key '{key}' added successfully!")
            return True
        
        elif choice == '3':
            key = input("Enter key to delete: ").strip()
            if key not in entry:
                print(f"❌ Key '{key}' not found in this entry.")
                return False
            
            confirm = input(f"Are you sure you want to delete '{key}'? (yes/no): ").lower().strip()
            if confirm == 'yes':
                del entry[key]
                self.data["entries"][entry_id] = entry
                self.save_data()
                print(f"✅ Key '{key}' deleted successfully!")
                return True
            else:
                print("Deletion cancelled.")
                return False
        
        else:
            print("Update cancelled.")
            return False

    def delete_entry(self, entry_id: str) -> bool:
        """Delete an entry by ID."""
        entries = self.data.get("entries", {})
        
        if entry_id not in entries:
            print(f"❌ Entry with ID '{entry_id}' not found.")
            return False
        
        print(f"\n🗑️  Entry to delete (ID: '{entry_id}'):")
        self.display_entry(entry_id, entries[entry_id])
        
        confirm = input("Are you sure you want to delete this entry? (yes/no): ").lower().strip()
        if confirm == 'yes':
            del entries[entry_id]
            self.data["entries"] = entries
            self.save_data()
            print(f"✅ Entry with ID '{entry_id}' deleted successfully!")
            return True
        else:
            print("Deletion cancelled.")
            return False

    def list_all_entries(self) -> Dict[str, Dict[str, Any]]:
        """Return all entries."""
        return self.data.get("entries", {})

    def display_entry(self, entry_id: str, entry: Dict[str, Any]) -> None:
        """Display a single entry."""
        print(f"\n{'='*60}")
        print(f"ID: {entry_id}")
        for key, value in entry.items():
            print(f"  {key}: {value}")
        print(f"{'='*60}")

    def display_entries(self, entries: Optional[Dict[str, Dict[str, Any]]] = None) -> None:
        """Display multiple entries."""
        entries_to_display = entries if entries is not None else self.list_all_entries()
        
        if not entries_to_display:
            print("\n❌ No entries found.")
            return
        
        print(f"\n{'='*60}")
        print(f"Total entries: {len(entries_to_display)}")
        print(f"{'='*60}")
        
        for entry_id, entry in entries_to_display.items():
            self.display_entry(entry_id, entry)
