from wtforms import Form, BooleanField,TextField,validators


class LoginForm(Form):
    user = TextField("user",[validators.Length(1,64)])
    pwd = TextField("pwd",[validators.Length(1,64)])