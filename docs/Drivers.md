# Data Drivers

Return data in the format :

```json
[
	{
		"Name": "Sophia Walker",
		"RollNo": "1",
		"Email": "sophia@localhost",
		"Conduct": "Good",
		"Subjects": {
			"Math": 50,
			"English": 58,
			"Physics": 56,
			"Chemistry": 46,
			"CS": 65
		},
		"TotalMarksObtained": 275,
		"MaxMarks": 370,
		"Percentage": 74.32
	},
	{
		"Name": "Adele Reed",
		"RollNo": "2",
		"Email": "adele@localhost",
		"Conduct": "Excellent",
		"Subjects": {
			"Math": 68,
			"English": 65,
			"Physics": 54,
			"Chemistry": 45,
			"Biology": 68
		},
		"TotalMarksObtained": 300,
		"MaxMarks": 370,
		"Percentage": 81.08
	},
	{
		"Name": "Edgar Barrett",
		"RollNo": "3",
		"Email": "edgar@localhost",
		"Conduct": "Mediocre",
		"Subjects": {
			"Math": 68,
			"English": 58,
			"Physics": 54,
			"Chemistry": 54,
			"Biology": 29
		},
		"TotalMarksObtained": 263,
		"MaxMarks": 370,
		"Percentage": 71.08
	},
	{
		"Name": "Honey Walker",
		"RollNo": "4",
		"Email": "honey@localhost",
		"Conduct": "Good",
		"Subjects": {
			"Math": 78,
			"English": 48,
			"Physics": 56,
			"Chemistry": 65,
			"CS": 47
		},
		"TotalMarksObtained": 294,
		"MaxMarks": 370,
		"Percentage": 79.46
	}
]
```

Structure of Database:

```
create table details(
	Name text NOT NULL,
	RollNo int NOT NULL,
	Email varchar(255),
	Conduct text,
	Math float,
	English float,
	Physics float,
	Chemistry float,
	Biology float,
	CS float,
);

+-----------+--------------+------+-----+---------+-------+
| Field     | Type         | Null | Key | Default | Extra |
+-----------+--------------+------+-----+---------+-------+
| Name      | text         | NO   |     | NULL    |       |
| RollNo    | int          | NO   |     | NULL    |       |
| Email     | varchar(255) | YES  |     | NULL    |       |
| Conduct   | text         | YES  |     | NULL    |       |
| Math      | float        | YES  |     | NULL    |       |
| English   | float        | YES  |     | NULL    |       |
| Physics   | float        | YES  |     | NULL    |       |
| Chemistry | float        | YES  |     | NULL    |       |
| Biology   | float        | YES  |     | NULL    |       |
| CS        | float        | YES  |     | NULL    |       |
+-----------+--------------+------+-----+---------+-------+
```


| Field     | Type         | Null | Key | Default | Extra |
|-----------|--------------|------|-----|---------|-------|
| Name      | text         | NO   |     | NULL    |       |
| RollNo    | int          | NO   |     | NULL    |       |
| Email     | varchar(255) | YES  |     | NULL    |       |
| Conduct   | text         | YES  |     | NULL    |       |
| Math      | float        | YES  |     | NULL    |       |
| English   | float        | YES  |     | NULL    |       |
| Physics   | float        | YES  |     | NULL    |       |
| Chemistry | float        | YES  |     | NULL    |       |
| Biology   | float        | YES  |     | NULL    |       |
| CS        | float        | YES  |     | NULL    |       |