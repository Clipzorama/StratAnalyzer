import sqlite3
# Connect to the SQLite database
conn = sqlite3.connect('password.db')

# Create a cursor object
cursor = conn.cursor()

# Query the users table
cursor.execute('SELECT username, hashed_password FROM users')

# Fetch all rows
users = cursor.fetchall()

# Print the rows
for user in users:
    print(user)

# Close the database connection
conn.close()


#Stored password

# Salt: 39540dbd566e6fbc
# Stored hash: e16cccd62034997cfb7650eff3dac1506c9632e612d907b6d4eaaeae4cc7aa9196efa50f66a06fc0


# Password from the database with username --> Clipzorama (salt + hash)
# ('Clipzorama', '39540dbd566e6fbce16cccd62034997cfb7650eff3dac1506c9632e612d907b6d4eaaeae4cc7aa9196efa50f66a06fc0')