import sqlite3

def create_and_seed_db():
    """Connects to the database, creates tables if they don't exist, and populates them with initial data."""
    # Connect to the SQLite database
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # Create the users table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        join_date TEXT NOT NULL
    )
    ''')
    
    # Create the transactions table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        amount REAL NOT NULL,
        transaction_date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    # Add sample users to the table
    users = [
        (1, 'Amit Kumar', 'amit.kumar@example.com', '2023-01-15'),
        (2, 'Priya Sharma', 'priya.sharma@example.com', '2023-02-20'),
        (3, 'Raj Patel', 'raj.patel@example.com', '2023-03-10'),
        (4, 'Neha Singh', 'neha.singh@example.com', '2023-04-05'),
        (5, 'Arjun Rao', 'arjun.rao@example.com', '2023-05-25'),
        (6, 'Sita Devi', 'sita.devi@example.com', '2023-06-15'),
        (7, 'Ravi Kumar', 'ravi.kumar@example.com', '2023-07-20'),
        (8, 'Meera Joshi', 'meera.joshi@example.com', '2023-08-10'),
        (9, 'Vikram Singh', 'vikram.singh@example.com', '2023-09-05'),
        (10, 'Anita Desai', 'anita.desai@example.com', '2023-10-15'),
        (11, 'Karan Malhotra', 'karan.malhotra@example.com', '2023-11-05'),  # No transaction
    (12, 'Sunita Verma', 'sunita.verma@example.com', '2023-12-10'),      # No transaction
    (13, 'Pooja Mehta', 'pooja.mehta@example.com', '2024-01-15'),        # No transaction
    (14, 'Dev Anand', 'dev.anand@example.com', '2024-02-20')
    ]
    
    # Add sample transactions to the table
    transactions = [
        (1, 1, 120.50, '2023-01-25'),
        (2, 1, 75.00, '2023-02-10'),
        (3, 1, 200.00, '2023-03-20'),
        (4, 2, 150.00, '2023-03-15'),
        (5, 2, 85.00, '2023-04-01'),
        (6, 2, 60.00, '2023-05-10'),
        (7, 3, 90.00, '2023-05-05'),
        (8, 3, 55.00, '2023-06-10'),
        (9, 3, 40.00, '2023-07-15'),
        (10, 4, 300.00, '2023-07-15'),
        (11, 4, 150.00, '2023-08-25'),
        (12, 5, 60.00, '2023-08-20'),
        (13, 5, 40.00, '2023-09-10'),
        (14, 5, 75.00, '2023-10-05'),
        (15, 6, 100.00, '2023-09-15'),
        (16, 6, 200.00, '2023-10-20'),
        (17, 7, 300.00, '2023-11-05'),
        (18, 7, 250.00, '2023-12-01'),
        (19, 8, 120.00, '2023-12-10'),
        (20, 8, 180.00, '2024-01-15'),
        (21, 9, 90.00, '2024-01-05'),
        (22, 9, 70.00, '2024-02-10'),
        (23, 10, 85.00, '2024-02-20'),
        (24, 10, 150.00, '2024-03-15')
    ]
    
    # Insert users and transactions into the tables
    cursor.executemany('INSERT OR IGNORE INTO users (user_id, name, email, join_date) VALUES (?, ?, ?, ?)', users)
    cursor.executemany('INSERT OR IGNORE INTO transactions (transaction_id, user_id, amount, transaction_date) VALUES (?, ?, ?, ?)', transactions)
    
    # Save changes and close the database connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_and_seed_db()
