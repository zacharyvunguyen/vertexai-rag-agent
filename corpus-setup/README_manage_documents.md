# Document Management Script

## Overview
The `manage_documents.py` script allows you to list, view details, and delete documents from your Student Report Card RAG corpus.

## Prerequisites
```bash
# Activate your conda environment
conda activate student-rag

# Source service account credentials
source keys/service-account.env
```

## Usage

### 1. List All Documents
```bash
python manage_documents.py --list
```
This will show all documents in the corpus with their resource names, creation dates, and sizes.

### 2. Interactive Management Mode (Default)
```bash
python manage_documents.py
```
This opens an interactive menu where you can:
- View document details by entering the document number (1, 2, 3, etc.)
- Delete specific documents by entering `d1`, `d2`, `d3`, etc.
- Delete ALL documents by entering `dall`
- Refresh the document list by entering `r`
- Quit by entering `q`

### 3. Delete Specific Document by Index
```bash
python manage_documents.py --delete 2
```
This will delete the document at index 2 (with confirmation prompt).

### 4. Delete All Documents
```bash
python manage_documents.py --delete-all
```
This will delete ALL documents from the corpus (with double confirmation).

### 5. Use with Different Corpus
```bash
python manage_documents.py --corpus "different-corpus-name" --list
```

## Command-Line Options

| Option | Description |
|--------|-------------|
| `--list` | List all documents and exit |
| `--delete INDEX` | Delete document by index number |
| `--delete-all` | Delete all documents from corpus |
| `--corpus NAME` | Use specific corpus (default: configured corpus) |
| `--interactive` | Interactive management mode (default) |

## Safety Features

1. **Confirmation Prompts**: All delete operations require confirmation
2. **Double Confirmation**: Deleting all documents requires typing "DELETE ALL"
3. **Error Handling**: Graceful error handling with clear error messages
4. **Non-destructive by Default**: Script defaults to listing/viewing, not deleting

## Examples

### Interactive Session Example
```
📚 Student Report Card RAG - Document Management
============================================================

📁 Retrieving documents from corpus...
   Found 3 documents:

   📄 [1] grading-standards.txt
       Resource: projects/.../ragFiles/...
       Created: 2025-05-26 17:15:28.739596+00:00

   📄 [2] report-card-1.pdf
       Resource: projects/.../ragFiles/...
       Size: 2.5 MB
       Created: 2025-05-26 22:44:34.396339+00:00

   📄 [3] report-card-2.pdf
       Resource: projects/.../ragFiles/...
       Size: 3.1 MB
       Created: 2025-05-27 15:50:31.651522+00:00

📋 Management Options:
   [1-3] View details for document
   [d1-d3] Delete specific document
   [dall] Delete ALL documents
   [r] Refresh document list
   [q] Quit

Enter your choice: 1
```

### Quick List and Delete
```bash
# List documents
python manage_documents.py --list

# Delete document #2
python manage_documents.py --delete 2
```

## Integration with Other Scripts

This script works alongside the other corpus management scripts:
- `add_documents.py` - Add new documents to the corpus
- `query_corpus.py` - Query the corpus
- `corpus_info.py` - View corpus statistics
- `check_corpus.py` - Create and check corpus status

## Note on Document Indexing

Document indices are assigned dynamically based on the current corpus state. After deleting documents, the indices may change. Always run `--list` first to see current indices before deleting. 