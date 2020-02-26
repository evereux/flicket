#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import os
import string
import random

from flask import flash
from werkzeug.utils import secure_filename

from application import app, db
from application.flicket.models.flicket_models import FlicketUploads
from application.flicket.models.flicket_user import FlicketUser
from application.flicket_admin.models.flicket_config import FlicketConfig


class UploadFile:

    def __init__(self, file):
        """
        Takes a file object from form submission.
        :param file: 
        """

        self.file = file
        self.file_extension = self.get_extension()

        if self.file_extension:
            self.file_name = self.random_filename(self.file.filename, characters=8)
        else:
            self.file_name = None
        self.upload_folder = None
        self.target_file = None

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

    def upload_file(self):
        """
        Method to upload the file. Returns True on success, otherwise False.
        :return: Boolean
        """

        if self.file_name and self.upload_folder:
            self.target_file = os.path.join(self.upload_folder, self.file_name)
        else:
            # print('Problem with file_name {} or upload_folder {}.'.format(self.file_name, self.upload_folder))
            return False

        if FlicketConfig.extension_allowed(self.file_name):
            self.file.save(self.target_file)
            return self.file
        else:
            # print('There was a problem with the files extension.')
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
        
        :return: nowt
        
        """

        # Find filename in the database.
        _user = FlicketUser.query.filter_by(id=self.user.id).one()
        # remove the file if it exists
        if _user.avatar:
            os.remove(os.path.join(self.upload_folder, _user.avatar))
            # null the database entry.
            _user.avatar = None
            db.session.commit()


class UploadAttachment(object):
    """
    
    Class created for the uploading of attachments to tickets and comments.
    
    Initialised with a list of file objects from form submission.
    
    """

    def __init__(self, files):
        self.files = files
        self.upload_folder = app.config['ticket_upload_folder']
        self.new_files = None

    def are_attachments(self):
        """
        Check self.files to see if any files were added to the upload form. Return True if there were.
        :return: Boolean
        """

        if len(self.files) == 0:
            return False

        if self.files[0].filename == '':
            return False

        return True

    def upload_files(self):
        """
        Upload files to self.upload_upload. 
        :return: list[str(original_filename), str(new_filename)]
        """

        # Were any files added to form?
        if not self.are_attachments():
            return False

        self.new_files = list()
        for file in self.files:
            uploaded_file = UploadFile(file)
            uploaded_file.upload_folder = self.upload_folder

            new_file_name = False
            if uploaded_file.upload_file():
                new_file_name = uploaded_file.file_name
            self.new_files.append((file.filename, new_file_name))

        return self.new_files

    def populate_db(self, flicketobject):
        topic = None
        post = None
        if type(flicketobject).__name__ == 'FlicketTicket':
            topic = flicketobject
        if type(flicketobject).__name__ == 'FlicketPost':
            post = flicketobject
        if self.new_files:
            for new_file in self.new_files:
                if new_file[1] is False:
                    flash('There was a problem uploading one or more of the files.', category='warning')
                else:
                    # all looks good, so add file to the database.
                    new_image = FlicketUploads(
                        topic=topic,
                        post=post,
                        filename=new_file[1],
                        original_filename=new_file[0]
                    )
                    db.session.add(new_image)
