import sqlite3
import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser("recipe_import")
    parser.add_argument('db_file', help="The exported recipe db file")
    parser.add_argument('out_file', help="The generated python file")
    parser.add_argument('-f', '--force', action='store_true')
    
    parser.parse_args(sys.argv)
    
    db_file = Path(parser.db_file)
    out_file = Path(parser.out_file)
    
    if not db_file.exists():
        print(f"ERROR: Invalid db path, file {db_file} does not exist")
        exit(1)
        
    with sqlite3.connect(str(db_file)) as db:
        
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()

if __name__ == "__main__":
    main()