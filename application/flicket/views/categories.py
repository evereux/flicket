#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import flash, redirect, url_for, render_template
from flask_login import login_required

from . import flicket_bp
from application import app, db
from application.flicket.forms.flicket_forms import CategoryForm
from application.flicket.models.flicket_models import FlicketCategory, FlicketDepartment


# create ticket
@flicket_bp.route(app.config['FLICKET'] + 'categories/<int:department_id>/', methods=['GET', 'POST'])
@login_required
def categories(department_id=False):
    form = CategoryForm()
    categories = FlicketCategory.query.filter_by(department_id=department_id)
    department = FlicketDepartment.query.filter_by(id=department_id).first()

    form.department_id.data = department_id

    if form.validate_on_submit():
        add_category = FlicketCategory(category=form.category.data, department=department)
        db.session.add(add_category)
        db.session.commit()
        flash('New category {} added.'.format(form.category.data))
        return redirect(url_for('flicket_bp.categories', department_id=department_id))

    return render_template('flicket_categories.html',
                           title='Categories',
                           form=form,
                           categories=categories,
                           department=department)


@flicket_bp.route(app.config['FLICKET'] + 'category_edit/<int:category_id>/', methods=['GET', 'POST'])
@login_required
def category_edit(category_id=False):
    if category_id:

        form = CategoryForm()
        category = FlicketCategory.query.filter_by(id=category_id).first()
        form.department_id.data = category.department_id

        if form.validate_on_submit():
            category.category = form.category.data
            db.session.commit()
            flash('Category {} edited.'.format(form.category.data))
            return redirect(url_for('flicket_bp.departments'))

        form.category.data = category.category

        return render_template('flicket_category_edit.html',
                               title='Edit Category',
                               form=form,
                               category=category,
                               department=category.department.department
                               )

    return redirect(url_for('flicket_bp.departments'))
