#!/usr/bin/env python3
"""
JSON Data Manager CLI
A simple command-line tool to store, edit, search, and manage JSON data.
Features string-based IDs and flexible key-value pair structure.
"""

import os
import subprocess

from menu_helper import MenuHelper
from json_manager import JSONDataManager
from objects.menu_item import MenuItem

def view_all(manager: JSONDataManager):
    """View all entries."""
    entries = manager.list_all_entries()
    if entries:
        manager.display_entries(entries)
    else:
        print("\n❌ No entries found in the database.")

def search_entries(manager: JSONDataManager):
    """Search entries interactively."""
    query = input("\n🔍 Enter search query: ").strip()
    if not query:
        print("⚠️  Search query cannot be empty.")
        return
    
    results = manager.search(query)
    if results:
        print(f"\n✅ Found {len(results)} result(s):")
        # Convert results list back to dict format for display
        results_dict = {entry_id: entry for entry_id, entry in results}
        manager.display_entries(results_dict)
    else:
        print(f"\n❌ No results found for '{query}'")

def add_entry(manager: JSONDataManager):
    """Add a new entry interactively with custom ID and key-value pairs."""
    print("\n" + "="*60)
    print("📝 ADD NEW ENTRY")
    print("="*60)
    
    # Get ID from user
    while True:
        entry_id = input("\nEnter unique ID (mandatory): ").strip()
        
        if not entry_id:
            print("⚠️  ID cannot be empty.")
            continue
        
        # Check if ID already exists
        if manager.entry_exists(entry_id):
            print(f"\n❌ ID '{entry_id}' already exists!")
            existing = manager.get_entry_by_id(entry_id)
            manager.display_entry(entry_id, existing)
            continue_choice = input("\nTry with a different ID? (yes/no): ").lower().strip()
            if continue_choice != 'yes':
                print("Entry creation cancelled.")
                return
            continue
        
        break
    
    # Add the entry with key-value pairs
    manager.add_entry(entry_id)

def update_entry(manager: JSONDataManager):
    """Update an entry interactively."""
    entry_id = input("\n🔧 Enter ID of entry to update: ").strip()
    
    if not entry_id:
        return
    
    if not manager.entry_exists(entry_id):
        print(f"❌ Entry with ID '{entry_id}' not found.")
        update_entry(manager)  # Prompt again for a valid ID
    else:
        manager.update_entry(entry_id)

def delete_entry(manager: JSONDataManager):
    """Delete an entry interactively."""
    entry_id = input("\n🗑️  Enter ID of entry to delete: ").strip()
    
    if not entry_id:
        return
    
    if not manager.entry_exists(entry_id):
        print(f"❌ Entry with ID '{entry_id}' not found.")
        delete_entry(manager)  # Prompt again for a valid ID
    
    manager.delete_entry(entry_id)

def view_by_id(manager: JSONDataManager):
    """View a single entry by ID."""
    entry_id = input("\n🔍 Enter entry ID: ").strip()
    
    if not entry_id:
        print("⚠️  ID cannot be empty.")
        return
    
    entry = manager.get_entry_by_id(entry_id)
    if entry:
        manager.display_entry(entry_id, entry)
    else:
        print(f"❌ Entry with ID '{entry_id}' not found.")

actions : dict[int, MenuItem] = {
    0: MenuItem("", lambda _: print("❌ Invalid choice. Please select a valid option from menu.")),
    1: MenuItem("View all entries", view_all),
    2: MenuItem("Search entries", search_entries),
    3: MenuItem("Add new entry", add_entry),
    4: MenuItem("Update entry", update_entry),
    5: MenuItem("Delete entry", delete_entry),
    6: MenuItem("View entry by ID", view_by_id),
    7: MenuItem("Exit", lambda _: print("\n👋 Goodbye! Your data has been saved."))
}

def main():
    """Main CLI loop."""
    manager = JSONDataManager()
    
    print("\n" + "🎉 " * 15)
    print("Welcome to JSON Data Manager!")
    print("🎉 " * 15)
    menu_helper = MenuHelper(actions, "📊 JSON DATA MANAGER")
    exit_program = False
    try:
        while not exit_program:
            action = menu_helper.view_menu()
            action.action(manager)
            exit_program = action.title == "Exit"
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Your data has been saved.")
    return 0

if __name__ == "__main__":
    main()
