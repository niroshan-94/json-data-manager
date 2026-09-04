#!/usr/bin/env python3
"""
JSON Data Manager CLI
A simple command-line tool to store, edit, search, and manage JSON data.
"""

from json_manager import JSONDataManager
import json

def print_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("     JSON DATA MANAGER")
    print("="*50)
    print("1. View all entries")
    print("2. Search entries")
    print("3. Add new entry")
    print("4. Update entry")
    print("5. Delete entry")
    print("6. View entry by ID")
    print("7. Exit")
    print("="*50)

def view_all(manager: JSONDataManager):
    """View all entries."""
    entries = manager.list_all_entries()
    if entries:
        manager.display_entries(entries)
    else:
        print("No entries found in the database.")

def search_entries(manager: JSONDataManager):
    """Search entries interactively."""
    query = input("\nEnter search query: ").strip()
    if not query:
        print("Search query cannot be empty.")
        return
    
    results = manager.search(query)
    if results:
        print(f"\nFound {len(results)} result(s):")
        manager.display_entries(results)
    else:
        print(f"No results found for '{query}'")

def add_entry(manager: JSONDataManager):
    """Add a new entry interactively."""
    print("\nEnter entry details (press Enter to skip a field):")
    entry = {}
    
    # Get field names from existing entries or use defaults
    if manager.list_all_entries():
        sample_entry = manager.list_all_entries()[0]
        fields = [k for k in sample_entry.keys() if k != 'id']
    else:
        fields = ['name', 'email', 'phone', 'city']
    
    for field in fields:
        value = input(f"  {field}: ").strip()
        if value:
            entry[field] = value
    
    if entry:
        manager.add_entry(entry)
    else:
        print("No data entered. Entry not added.")

def update_entry(manager: JSONDataManager):
    """Update an entry interactively."""
    try:
        entry_id = int(input("\nEnter entry ID to update: "))
    except ValueError:
        print("Invalid ID format.")
        return
    
    entry = manager.get_entry_by_id(entry_id)
    if not entry:
        print(f"Entry {entry_id} not found.")
        return
    
    print("\nCurrent entry:")
    manager.display_entries([entry])
    
    print("Enter new values (press Enter to keep current value):")
    updates = {}
    
    for key, current_value in entry.items():
        if key == 'id':
            continue
        new_value = input(f"  {key} (current: {current_value}): ").strip()
        if new_value:
            updates[key] = new_value
    
    if updates:
        manager.update_entry(entry_id, updates)
    else:
        print("No updates made.")

def delete_entry(manager: JSONDataManager):
    """Delete an entry interactively."""
    try:
        entry_id = int(input("\nEnter entry ID to delete: "))
    except ValueError:
        print("Invalid ID format.")
        return
    
    entry = manager.get_entry_by_id(entry_id)
    if not entry:
        print(f"Entry {entry_id} not found.")
        return
    
    print("\nEntry to delete:")
    manager.display_entries([entry])
    
    confirm = input("Are you sure you want to delete this entry? (yes/no): ").lower().strip()
    if confirm == 'yes':
        manager.delete_entry(entry_id)
    else:
        print("Deletion cancelled.")

def view_by_id(manager: JSONDataManager):
    """View a single entry by ID."""
    try:
        entry_id = int(input("\nEnter entry ID: "))
    except ValueError:
        print("Invalid ID format.")
        return
    
    entry = manager.get_entry_by_id(entry_id)
    if entry:
        manager.display_entries([entry])
    else:
        print(f"Entry {entry_id} not found.")

def main():
    """Main CLI loop."""
    manager = JSONDataManager()
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            view_all(manager)
        elif choice == '2':
            search_entries(manager)
        elif choice == '3':
            add_entry(manager)
        elif choice == '4':
            update_entry(manager)
        elif choice == '5':
            delete_entry(manager)
        elif choice == '6':
            view_by_id(manager)
        elif choice == '7':
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
