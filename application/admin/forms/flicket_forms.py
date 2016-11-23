from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired

from application.admin.models.user import User
from application.flicket.models.flicket_models import FlicketPriority, FlicketDepartment, FlicketCategory


def does_email_exist(form, field):
    """
    Username must be unique so we check against the database to ensure it doesn't
    :param form:
    :param field:
    :return True / False:
    """
    if form.email.data:
        result = User.query.filter_by(email=form.email.data).count()
        if result == 0:
            field.errors.append('Can\'t find user.')
            return False
    else:
        return False

    return True


def does_department_exist(form, field):
    """
    Username must be unique so we check against the database to ensure it doesn't
    :param form:
    :param field:
    :return True / False:
    """
    result = FlicketDepartment.query.filter_by(department=form.department.data).count()
    if result > 0:
        field.errors.append('Department already exists.')
        return False

    return True


def does_category_exist(form, field):
    """
    Username must be unique so we check against the database to ensure it doesn't
    :param form:
    :param field:
    :return True / False:
    """
    result = FlicketCategory.query.filter_by(category=form.category.data).filter_by(department_id=form.department_id.data).count()
    if result > 0:
        field.errors.append('Category already exists.')
        return False

    return True


class CreateTicket(FlaskForm):

    def __init__(self, *args, **kwargs):
        form = super(CreateTicket, self).__init__(*args, **kwargs)
        self.priority.choices = [(p.id, p.priority) for p in FlicketPriority.query.all()]
        self.category.choices = [(c.id, "{} - {}".format(c.department.department, c.category)) for c in
                                 FlicketCategory.query.all() if c.department]

    """ Log in form. """
    title = StringField('username', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    priority = SelectField('priority', validators=[DataRequired()], coerce=int)
    category = SelectField('category', validators=[DataRequired()], coerce=int)


class ContentForm(FlaskForm):
    """ Content form. Displayed when replying too end editing tickets """
    content = TextAreaField('content', validators=[DataRequired()])


class SearchTicketForm(FlaskForm):
    """ Search form. """
    email = StringField('email', validators=[does_email_exist])
    content = StringField('content', validators=[])


class SearchUserForm(FlaskForm):
    """ Search user. """
    name = StringField('name', validators=[DataRequired()])


class SearchEmailForm(FlaskForm):
    """ Search email form. """
    email = StringField('email', validators=[DataRequired(), does_email_exist])


class DepartmentForm(FlaskForm):
    """ Department form. """
    department = StringField('department', validators=[DataRequired(), does_department_exist])


class CategoryForm(FlaskForm):
    """ Category form. """
    category = StringField('category', validators=[DataRequired(), does_category_exist])
    department_id = HiddenField('department_id')
