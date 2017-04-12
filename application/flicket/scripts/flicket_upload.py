#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import os
import string
import random

from flask import flash
from werkzeug.utils import secure_filename

from application import app, db
from application.flicket.models.flicket_models import FlicketUploads, field_size
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.scripts.flicket_functions import random_string


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['allowed_extensions']

def allowed_avatar(filename):
    allowed_image_types = ['jpg']
    return allowed_image_types


def upload_documents(files, avatar_upload=False):
    """
    Function to upload files to the static temp folder.
    The file is given a random unique file name.
    :param files:
    :return:
    """
    new_files = []

    if avatar_upload:
        check_extension = allowed_avatar
        upload_folder = 'application/flicket/static/flicket_avatars'
    else:
        check_extension = allowed_file
        upload_folder = app.config['ticket_upload_folder']

    if len(files) == 0:
        return None

    if files[0].filename != '':

        for f in files:

            target_file = False
            if f and check_extension(f.filename):

                target_file = secure_filename(f.filename)
                target_file = os.path.join(upload_folder, target_file)
                f.save(target_file)

            # rename file
            if os.path.isfile(target_file):

                while True:
                    new_name_size = field_size['filename_max_length'] - len(
                        os.path.splitext(target_file)[1])
                    new_name = random_string(new_name_size) + os.path.splitext(target_file)[1]
                    new_name = os.path.join(upload_folder, new_name)
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


def add_upload_to_db(new_files, _object, post_type=False):
    topic = None
    post = None

    if post_type == 'Ticket':
        topic = _object
    if post_type == 'Post':
        post = _object

    if post_type is False:
        flash('There was a problem uploading images.')

    # add documents to database.
    if len(new_files) > 0:
        for f in new_files:
            new_image = FlicketUploads(topic=topic, post=post, filename=os.path.basename(f[0]), original_filename=f[1])
            db.session.add(new_image)


class UploadFile:

    def __init__(self, file):

        self.file = file
        self.file_extension = self.get_extension()

        if self.file_extension:
            self.file_name = self.random_filename(self.file.filename, characters=8)
        else:
            self.file_name = None
        self.upload_folder = None
        self.allowed_extensions = []


    def get_extension(self):
        try:
            _ext = self.file.filename.rsplit('.', 1)[1]
            return _ext
        except IndexError:
            return False

    def random_filename(self, file_name, characters=8):
        """
        Returns a random filename using lowercase letters and digits.
        :return: string 
        """
        new_file_name = secure_filename(file_name)

        while True:
            chars = string.ascii_lowercase + string.digits
            output_string = ''.join(random.choice(chars) for _ in range(characters))
            new_file_name = output_string + '.' + self.file_extension
            if not os.path.isfile(new_file_name):
                break

        return new_file_name

    def check_extension(self):
        """
        Checks that it is a valid filename with a valid extension.
        Returns True if valid
        :return: Boolean
        """
        return '.' in self.file_name and self.file_extension in self.allowed_extensions


    def upload_file(self):
        """
        Method to upload the file. Returns True on sucess, otherwise False.
        :return: Boolean
        """

        if self.file_name and self.upload_folder:
            self.target_file = os.path.join(self.upload_folder, self.file_name)
        else:
            return False

        # Is the file extension in the list of allowed extensions.
        if self.check_extension():
            self.file.save(self.target_file)
            return self.file
        else:
            return False


class UploadAvatar(UploadFile):

    def __init__(self, file, user):
        super().__init__(file)
        self.allowed_extensions = ['jpg']
        self.user = user
        self.upload_folder = app.config['avatar_upload_folder']
        self.delete_existing_avatar()

    def delete_existing_avatar(self):
        """
        Clean up old avatar before uploading new one.
        :return: 
        """
        # Find filename in the database.
        _user = FlicketUser.query.filter_by(id=self.user.id).one()
        # remove the file if it exists
        if _user.avatar:
            os.remove(os.path.join(self.upload_folder,  _user.avatar))
            # null the database entry.
            _user.avatar = None
            db.session.commit()
