from wtforms.validators import ValidationError

class Unique(object):
    """validates the username field in our ClickForm so that it does not have
    duplicate usernames"""

    def __init__(self,model,field,message=u'This username already exists.'):
        self.model = model
        self.field = field

    def __call__(self,form,field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)
