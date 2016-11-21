from flask import flash, redirect, url_for, render_template
from flask_login import login_required

from application import app, db
from flicket_application.flicket_forms import DepartmentForm
from flicket_application.flicket_models import FlicketDepartment


# create ticket
@app.route(app.config['FLICKETHOME'] + 'departments/', methods=['GET', 'POST'])
@app.route(app.config['FLICKETHOME'] + 'departments/<int:page>/', methods=['GET', 'POST'])
@login_required
def departments(page=1):

    form = DepartmentForm()
    departments = FlicketDepartment.query

    if form.validate_on_submit():

        add_department = FlicketDepartment(department=form.department.data)
        db.session.add(add_department)
        db.session.commit()
        flash('New department {} added.'.format(form.department.data))
        return redirect(url_for('departments'))


    departments = departments.paginate(page, app.config['POSTS_PER_PAGE'])

    return render_template('flicket/flicket_departments.html',
                           title='Flicket - Departments',
                           form=form,
                           page=page,
                           departments=departments)


@app.route(app.config['FLICKETHOME'] + 'department_edit/<int:department_id>/', methods=['GET', 'POST'])
@login_required
def department_edit(department_id=False):

    if department_id:

        form = DepartmentForm()
        department = FlicketDepartment.query.filter_by(id=department_id).first()


        if form.validate_on_submit():
            department.department = form.department.data
            db.session.commit()
            flash('Depart {} edited.'.format(form.department.data))
            return redirect(url_for('departments'))

        form.department.data = department.department


        return render_template('flicket/flicket_department_edit.html',
                               title='Flicket - Edit Department',
                               form=form,
                               department=department
                               )

    return redirect(url_for('departments'))