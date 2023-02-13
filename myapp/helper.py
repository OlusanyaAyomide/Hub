import string
import random

QuestionAnswer = [
    ("A","A"),
    ("B","B"),
    ("C","C"),
    ("D","D")
]

def generator():
    N = 8
    res = ''.join(random.choices(string.ascii_uppercase +string.digits, k=N))
    return f'#{res}'

def hashgenerator():
    N =  50
    res = ''.join(random.choices(string.ascii_uppercase +string.digits, k=N))
    return res

QuestionYear =[
    ("2011","2011"),
    ("2012","2012"),
    ("2013","2013"),
    ("2014","2014"),
    ("2015","2015"),
    ("2016","2016"),
    ("2017","2017"),
    ("2018","2018"),
    ("2019","2019"),
    ("2020","2020"),
    ("2021","2021"),
    ("2022","2022"),
    ("2023","2023"),
]

def randumNumber():
    myList = ""
    for i in range(6):
        randomstr = random.randint(1, 6)
        myList += str(randomstr)
    return int(myList)
