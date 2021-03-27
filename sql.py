import mysql.connector


def connect_database():
	database = mysql.connector.connect(
		# host='145.89.166.209',
		host='localhost',
		user='tom',
		password='broer'
	)
	return database


def get_PoI(database):
	database = database
	try:
		cursor = database.cursor()

		cursor.execute('use tomsbroer;')
		cursor.execute('select * from points_of_interest order by searched desc;')

		data = dict()

		for x in cursor:
			data[x[1]] = eval(x[2])
		print(data)
	except:
		get_PoI()
	return data


def one_upper(q):
	update = "update points_of_interest set searched = searched + 1 where name = '{}' ".format(q)
	print(update)
	database = connect_database()
	cursor = database.cursor()
	
	cursor.execute('use tomsbroer;')
	cursor.execute(update)
	database.commit()