#!/usr/bin/env python3
"""
JSON Data Manager CLI
A simple command-line tool to store, edit, search, and manage JSON data.
Features string-based IDs and flexible key-value pair structure.
"""

import os
import subprocess

from json_manager import JSONDataManager
from objects.menu_item import MenuItem

menuViewed = False

def print_menu():
    """Display the main menu."""
    print("="*60)
    print("     📊 JSON DATA MANAGER")
    print("="*60)
    for k in [k for k in actions if k > 0]:
        print(k, ":", actions[k].title)
    print("="*60)

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
        print("⚠️  ID cannot be empty.")
        return
    
    if not manager.entry_exists(entry_id):
        print(f"❌ Entry with ID '{entry_id}' not found.")
        return
    
    manager.update_entry(entry_id)

def delete_entry(manager: JSONDataManager):
    """Delete an entry interactively."""
    entry_id = input("\n🗑️  Enter ID of entry to delete: ").strip()
    
    if not entry_id:
        print("⚠️  ID cannot be empty.")
        return
    
    if not manager.entry_exists(entry_id):
        print(f"❌ Entry with ID '{entry_id}' not found.")
        return
    
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

actions = {
    -1 : MenuItem("", lambda _: globals().update(menuViewed=False)),
    0: MenuItem("", lambda _: print("❌ Invalid choice. Please select a valid option from menu.")),
    1: MenuItem("View all entries", view_all),
    2: MenuItem("Search entries", search_entries),
    3: MenuItem("Add new entry", add_entry),
    4: MenuItem("Update entry", update_entry),
    5: MenuItem("Delete entry", delete_entry),
    6: MenuItem("View entry by ID", view_by_id),
    7: MenuItem("Clear screen", lambda _: subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)),
    8: MenuItem("Exit", lambda _: print("\n👋 Goodbye! Your data has been saved."))
}

def validate_input(choice):
    """
    Validate user input for menu choice.
    Returns the integer choice if valid, otherwise returns 0.
    """
    try:
        if choice.lower() == 'y':
            return -1  # Special case for viewing menu again
        choice_int = int(choice)
        if(choice_int in actions):
            return choice_int
        return 0
    except (ValueError, TypeError):
        return 0


def main_menu(manager):
    global menuViewed
    w = "Choose an option from menu "
    if(menuViewed == False):
        print_menu()
    else:
        w += ". View menu (y)"
    menuViewed = True
    choice = input(f"{w}: ").strip()
    choice_int = validate_input(choice)
    action = actions[choice_int]
    action.action(manager)
    return action.title == "Exit"

def main():
    """Main CLI loop."""
    manager = JSONDataManager()
    
    print("\n" + "🎉 " * 15)
    print("Welcome to JSON Data Manager!")
    print("🎉 " * 15)

    try:
        while True:
            exit_program = main_menu(manager)
            if exit_program:
                break
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Your data has been saved.")

if __name__ == "__main__":
    main()
