#!/usr/bin/env python3
"""
Example usage of the JSONDataManager as a library.
Shows various operations without using the CLI.
"""

from json_manager import JSONDataManager

def example_1_basic_operations():
    """Example 1: Basic CRUD operations."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic CRUD Operations")
    print("="*60)
    
    manager = JSONDataManager("data.json")
    
    # View all entries
    print("\n1. Viewing all entries:")
    manager.display_entries()
    
    # Add a new entry
    print("2. Adding a new entry:")
    manager.add_entry({
        "name": "Alice Wonder",
        "email": "alice@example.com",
        "phone": "555-1234",
        "city": "Boston"
    })
    
    # Get entry by ID
    print("3. Getting entry by ID (ID=1):")
    entry = manager.get_entry_by_id(1)
    if entry:
        print(f"   Found: {entry}")

def example_2_search_operations():
    """Example 2: Search functionality."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Search Operations")
    print("="*60)
    
    manager = JSONDataManager("data.json")
    
    # Full text search
    print("\n1. Search for 'john' in all fields:")
    results = manager.search("john")
    manager.display_entries(results)
    
    # Partial string search
    print("2. Search for 'example' in all fields:")
    results = manager.search("example")
    manager.display_entries(results)
    
    # Search in specific fields
    print("3. Search for entries in 'New York' (city field only):")
    results = manager.search("new york", fields=["city"])
    manager.display_entries(results)
    
    # Phone number search
    print("4. Search for phone numbers starting with '123':")
    results = manager.search("123", fields=["phone"])
    manager.display_entries(results)

def example_3_update_operations():
    """Example 3: Update operations."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Update Operations")
    print("="*60)
    
    manager = JSONDataManager("data.json")
    
    entry_id = 1
    print(f"\n1. Current entry (ID={entry_id}):")
    current = manager.get_entry_by_id(entry_id)
    if current:
        manager.display_entries([current])
    
    # Update the entry
    print(f"2. Updating entry {entry_id}:")
    manager.update_entry(entry_id, {
        "city": "San Francisco",
        "phone": "415-555-0123"
    })
    
    print(f"3. Entry after update:")
    updated = manager.get_entry_by_id(entry_id)
    if updated:
        manager.display_entries([updated])

def example_4_advanced_search():
    """Example 4: Advanced search scenarios."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Advanced Search Scenarios")
    print("="*60)
    
    manager = JSONDataManager("data.json")
    
    # Case-insensitive search
    print("\n1. Case-insensitive search for 'JANE':")
    results = manager.search("JANE")
    manager.display_entries(results)
    
    # Email domain search
    print("2. Search for all entries with 'example.com' email:")
    results = manager.search("example.com", fields=["email"])
    manager.display_entries(results)
    
    # Partial name search
    print("3. Partial name search for 'son':")
    results = manager.search("son", fields=["name"])
    manager.display_entries(results)

def run_all_examples():
    """Run all examples."""
    print("\n" + "🚀 " * 20)
    print("JSON Data Manager - Usage Examples")
    print("🚀 " * 20)
    
    try:
        example_1_basic_operations()
        example_2_search_operations()
        example_3_update_operations()
        example_4_advanced_search()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60 + "\n")
    except Exception as e:
        print(f"❌ Error running examples: {e}")

if __name__ == "__main__":
    run_all_examples()
