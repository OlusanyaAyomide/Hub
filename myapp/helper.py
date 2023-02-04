import string
import random

QuestionAnswer = [
    ("optionA","A"),
    ("optionB","B"),
    ("optionC","C"),
    ("optionD","D")
]

def generator():
    N = 8
    res = ''.join(random.choices(string.ascii_uppercase +string.digits, k=N))
    return f'#{res}'


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


