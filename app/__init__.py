from flask import Flask

app = Flask (__name__)
app.secret_key = '?O(8k"@AUia=*F5c?}?o(TbZ%JjKhp'

from app import routes
from app import auth