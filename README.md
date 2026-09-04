# JSON Data Manager

A simple yet powerful Python CLI tool to store, edit, search, and manage JSON data locally. Perfect for managing small datasets, contacts, or any structured data.

## Features

✨ **Core Functionality**
- 📖 **View All Entries** - Display all stored data in a formatted table
- 🔍 **Search** - Full or partial string matching across all fields
- ➕ **Add Entries** - Easily add new records with interactive prompts
- ✏️ **Update Entries** - Modify existing records by ID
- 🗑️ **Delete Entries** - Remove records from your database
- 🆔 **View by ID** - Quickly fetch specific entries

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/niroshan-94/json-data-manager.git
   cd json-data-manager
   ```

2. **No external dependencies required!** This project uses only Python's built-in libraries.

## Usage

### Running the CLI

```bash
python main.py
```

This will launch an interactive menu-driven interface.

### Menu Options

```
1. View all entries       - Display all records in the database
2. Search entries        - Search by full or partial string match
3. Add new entry         - Create a new record
4. Update entry          - Modify an existing record
5. Delete entry          - Remove a record
6. View entry by ID      - Fetch a specific record
7. Exit                  - Close the application
```

### Using as a Library

You can also use the `JSONDataManager` class in your own scripts:

```python
from json_manager import JSONDataManager

# Initialize manager
manager = JSONDataManager("data.json")

# Add a new entry
manager.add_entry({
    "name": "Alice Wonder",
    "email": "alice@example.com",
    "phone": "555-1234",
    "city": "Boston"
})

# Search entries
results = manager.search("alice")
manager.display_entries(results)

# Get entry by ID
entry = manager.get_entry_by_id(1)

# Update entry
manager.update_entry(1, {"city": "San Francisco"})

# Delete entry
manager.delete_entry(1)

# List all entries
all_entries = manager.list_all_entries()
```

## Data Format

Data is stored in `data.json` in the following format:

```json
{
  "entries": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "123-456-7890",
      "city": "New York"
    }
  ]
}
```

## API Reference

### JSONDataManager Class

#### Methods

**`__init__(filepath="data.json")`**
- Initialize the manager with a file path

**`load_data()`**
- Load JSON data from file

**`save_data()`**
- Save data to JSON file

**`add_entry(entry: Dict)`**
- Add a new entry (ID auto-generated if not provided)

**`search(query: str, fields: List[str] = None)`**
- Search entries by query string
- `query`: Search term (case-insensitive)
- `fields`: Optional list of fields to search in (defaults to all)

**`get_entry_by_id(entry_id: int)`**
- Retrieve a single entry by its ID

**`update_entry(entry_id: int, updates: Dict)`**
- Update specific fields of an entry

**`delete_entry(entry_id: int)`**
- Delete an entry by ID

**`list_all_entries()`**
- Get all entries as a list

**`display_entries(entries: List[Dict] = None)`**
- Pretty-print entries to console

## Examples

### Search Examples

```python
# Search for "John" in all fields
results = manager.search("john")

# Search for email containing "example"
results = manager.search("example", fields=["email"])

# Search for partial phone numbers
results = manager.search("123", fields=["phone"])
```

### Adding Entries

```python
# Using the CLI: Just follow the interactive prompts

# Using the library:
manager.add_entry({
    "name": "Eve Smith",
    "email": "eve@example.com",
    "phone": "666-5555",
    "city": "Seattle"
})
```

## File Structure

```
json-data-manager/
├── main.py              # CLI entry point
├── json_manager.py      # Core JSON manager class
├── data.json           # JSON data file (created on first run)
└── README.md           # This file
```

## Requirements

- Python 3.6+
- No external dependencies

## License

MIT License - Feel free to use this project for personal or commercial purposes.

## Contributing

Contributions are welcome! Feel free to:
- Report issues
- Submit pull requests
- Suggest improvements

## Future Enhancements

- [ ] Export to CSV/Excel
- [ ] Backup and restore functionality
- [ ] Database migration (JSON to SQLite)
- [ ] Advanced filtering options
- [ ] Batch operations
- [ ] Data validation schemas

---

Made with ❤️ by [niroshan-94](https://github.com/niroshan-94)
