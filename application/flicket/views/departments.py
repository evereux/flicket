#! usr/bin/python3
# -*- coding: utf8 -*-

from flask import flash, redirect, url_for, render_template
from flask_login import login_required

from . import flicket_bp
from application import app, db
from application.flicket.forms.flicket_forms import DepartmentForm
from application.flicket.models.flicket_models import FlicketDepartment


# create ticket
@flicket_bp.route(app.config['FLICKET'] + 'departments/', methods=['GET', 'POST'])
@flicket_bp.route(app.config['FLICKET'] + 'departments/<int:page>/', methods=['GET', 'POST'])
@login_required
def departments(page=1):
    form = DepartmentForm()
    departments = FlicketDepartment.query

    if form.validate_on_submit():
        add_department = FlicketDepartment(department=form.department.data)
        db.session.add(add_department)
        db.session.commit()
        flash('New department {} added.'.format(form.department.data))
        return redirect(url_for('flicket_bp.departments'))

    departments = departments.paginate(page, app.config['POSTS_PER_PAGE'])

    return render_template('flicket_departments.html',
                           title='Flicket - Departments',
                           form=form,
                           page=page,
                           departments=departments)


@flicket_bp.route(app.config['FLICKET'] + 'department_edit/<int:department_id>/', methods=['GET', 'POST'])
@login_required
def department_edit(department_id=False):
    if department_id:

        form = DepartmentForm()
        department = FlicketDepartment.query.filter_by(id=department_id).first()

        if form.validate_on_submit():
            department.department = form.department.data
            db.session.commit()
            flash('Depart {} edited.'.format(form.department.data))
            return redirect(url_for('flicket_bp.departments'))

        form.department.data = department.department

        return render_template('flicket_department_edit.html',
                               title='Flicket - Edit Department',
                               form=form,
                               department=department
                               )

    return redirect(url_for('flicket_bp.departments'))
