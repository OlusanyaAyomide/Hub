URL 
/create-user
METHOD :[POST]
REQUIRED:{
    email : string,
    password:string,
    username:string
}
SUCESS RESPONSE:{
    "email": "test@gmail.com",
    "username": "tester"
}
SUCESS CODE:200

ERROR CODEL:400
ERROR RESPONSE:[
    "email": [
        "This field is required."
    ],
    "password": [
        "This field is required."
    ],
    "non_field_errors": [
        "username field is missing"
    ]
]