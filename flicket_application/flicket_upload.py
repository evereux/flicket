import os

from werkzeug.utils import secure_filename
from flask import flash

from config import BaseConfiguration
from application import app, db
from flicket_application.flicket_models import FlicketUploads
from flicket_application.flicket_functions import random_string


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def upload_documents(files):

    new_files = []

    if len(files) == 0 :
        return None

    if files[0].filename != '':

        for f in files:

            target_file = False
            if f and allowed_file(f.filename):
                target_file = os.path.join(app.config['TICKET_UPLOAD_FOLDER'], f.filename)
                target_file = secure_filename(target_file)
                f.save(target_file)

            # rename file
            if os.path.isfile(target_file):

                new_name = False

                while True:
                    new_name_size = BaseConfiguration.db_field_size['ticket']['upload_filename'] - len(
                        os.path.splitext(target_file)[1])
                    new_name = random_string(new_name_size) + os.path.splitext(target_file)[1]
                    new_name = os.path.join(app.config['TICKET_UPLOAD_FOLDER'], new_name)
                    # make sure new name doesn't already exist
                    if not os.path.isfile(new_name):
                        break

                # rename uploaded file to unique name
                os.rename(target_file, new_name)

                new_files.append((new_name, f.filename))

            else:

                # There has been a problem uploading some documents.
                return False


    return new_files


def add_upload_to_db(new_files, object, post_type=False):

    topic = None
    post = None

    if post_type == 'Ticket':
        topic = object
    if post_type == 'Post':
        post = object

    if post_type == False:
        flash('There was a problem uploading images.')

    # add documents to database.
    # todo: need to find a way to improve this. seems repetitive.
    if len(new_files) > 0:
        # if post_type == 'Ticket':
        #     for f in new_files:
        #         new_image = FlicketUploads(topic=topic, filename=os.path.basename(f[0]), original_filename=f[1])
        #         db.session.add(new_image)
        # if post_type == 'Post':
        #     for f in new_files:
        #         new_image = FlicketUploads(post=post, filename=os.path.basename(f[0]), original_filename=f[1])
        #         db.session.add(new_image)
        for f in new_files:
            new_image = FlicketUploads(topic=topic, post=post, filename=os.path.basename(f[0]), original_filename=f[1])
            db.session.add(new_image)
