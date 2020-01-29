import postgresql

def get_connection():
	db = postgresql.open('pq://postgres:postgres@localhost:5432/mydb')