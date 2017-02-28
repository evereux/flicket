#! usr/bin/python3
# -*- coding: utf8 -*-

from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, HiddenField, SubmitField, FileField
from wtforms.fields import SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.widgets import ListWidget, CheckboxInput

from application.flicket.models.flicket_models import (FlicketCategory,
                                                       FlicketDepartment,
                                                       FlicketPriority,
                                                       FlicketTicket)
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.scripts.upload_choice_generator import generate_choices

form_class_button = {'class': 'btn btn-primary'}


def does_email_exist(form, field):
    """
    Username must be unique so we check against the database to ensure it doesn't
    :param form:
    :param field:
    :return True / False:
    """
    if form.email.data:
        result = FlicketUser.query.filter_by(email=form.email.data).count()
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
    result = FlicketCategory.query.filter_by(category=form.category.data).filter_by(
        department_id=form.department_id.data).count()
    if result > 0:
        field.errors.append('Category already exists.')
        return False

    return True


class CreateTicketForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        form = super(CreateTicketForm, self).__init__(*args, **kwargs)
        self.priority.choices = [(p.id, p.priority) for p in FlicketPriority.query.all()]
        self.category.choices = [(c.id, "{} - {}".format(c.department.department, c.category)) for c in
                                 FlicketCategory.query.all() if c.department]

    """ Log in form. """
    title = StringField('username', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    priority = SelectField('priority', validators=[DataRequired()], coerce=int)
    category = SelectField('category', validators=[DataRequired()], coerce=int)
    file = FileField('Upload Documents', render_kw={'multiple': True})
    submit = SubmitField('Submit', render_kw=form_class_button, validators=[DataRequired()])


class MultiCheckBoxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class EditTicketForm(CreateTicketForm):
    def __init__(self, ticket_id, *args, **kwargs):
        self.form = super(EditTicketForm, self).__init__(*args, **kwargs)
        # get ticket data from ticket_id
        ticket = FlicketTicket.query.filter_by(id=ticket_id).first()

        # define the multi select box for document uploads
        uploads = []
        for u in ticket.topic_uploads:
            uploads.append((u.id, u.filename, u.original_filename))
        self.uploads.choices = []
        for x in uploads:
            uri = url_for('flicket_bp.view_ticket_uploads', filename=x[1])
            uri_label = '<a href="' + uri + '">' + x[2] + '</a>'
            self.uploads.choices.append((x[0], uri_label))

    uploads = MultiCheckBoxField('Label', coerce=int)
    submit = SubmitField('Edit Ticket', render_kw=form_class_button, validators=[DataRequired()])


class ReplyForm(FlaskForm):
    """ Content form. Displayed when replying too end editing tickets """
    content = TextAreaField('Reply', validators=[DataRequired()])
    file = FileField('Upload Documents', render_kw={'multiple': True})
    submit = SubmitField('submit reply', render_kw=form_class_button)


class EditReplyForm(ReplyForm):
    def __init__(self, post_id, *args, **kwargs):
        self.form = super(EditReplyForm, self).__init__(*args, **kwargs)
        self.uploads.choices = generate_choices('Post', id=post_id)

    uploads = MultiCheckBoxField('Label', coerce=int)
    submit = SubmitField('Edit Ticket', render_kw=form_class_button, validators=[DataRequired()])


class SearchUserForm(FlaskForm):
    """ Search user. """
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('search user', render_kw=form_class_button)


class SearchEmailForm(FlaskForm):
    """ Search email form. """
    email = StringField('email', validators=[DataRequired(), does_email_exist])
    submit = SubmitField('assign', render_kw=form_class_button)


class DepartmentForm(FlaskForm):
    """ Department form. """
    department = StringField('Department', validators=[DataRequired(), does_department_exist])
    submit = SubmitField('add department', render_kw=form_class_button)


class CategoryForm(FlaskForm):
    """ Category form. """
    category = StringField('Category', validators=[DataRequired(), does_category_exist])
    department_id = HiddenField('department_id')
    submit = SubmitField('add category', render_kw=form_class_button)
