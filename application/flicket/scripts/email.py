#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import render_template, url_for
from flask_mail import Mail, Message

from application import app
from application.flicket.scripts.decorators import send_async_email
from application.flicket_admin.models.flicket_config import FlicketConfig


class FlicketMail:
    """
    FlicketMail class to send emails.
    """

    def __init__(self):
        """
        Upon initialisation the mail configuration settings are retrieved from the database and
        self.mail is intialised.
        """

        config = FlicketConfig.query.first()

        app.config.update(
            MAIL_SERVER=config.mail_server,
            MAIL_PORT=config.mail_port,
            MAIL_USE_TLS=config.mail_use_tls,
            MAIL_USE_SSL=config.mail_use_ssl,
            MAIL_DEBUG=config.mail_debug,
            MAIL_USERNAME=config.mail_username,
            MAIL_PASSWORD=config.mail_password,
            MAIL_MAX_EMAILS=config.mail_max_emails,
            MAIL_SUPPRESS_SEND=config.mail_suppress_send,
            MAIL_ASCII_ATTACHMENTS=config.mail_ascii_attachments,
            base_url=config.base_url,
        )

        self.mail = Mail(app)
        self.mail.init_app(app)

        self.sender = config.mail_default_sender

    def create_ticket(self, ticket):
        """"""
        # todo: send email to department heads
        pass

    def reply_ticket(self, ticket=None, reply=None, user=None):
        """
        :param ticket: ticket object
        :param reply: reply object
        :param user: user object
        :return:
        """
        recipients = ticket.get_subscriber_emails()
        # remove user who actually replied.
        recipients = [r for r in recipients if r != user.email]
        if len(recipients) > 0:
            title = f'Ticket #{ticket.id_zfill} - "{ticket.title}" has new replies.'
            ticket_url = app.config['base_url'] + url_for('flicket_bp.ticket_view', ticket_id=ticket.id)
            html_body = render_template('email_ticket_replies.html', title=title, number=ticket.id_zfill,
                                        ticket_url=ticket_url, ticket=ticket, reply=reply)

            self.send_email(title, self.sender, recipients, html_body)

    def assign_ticket(self, ticket):
        """
        :param ticket: ticket object
        :return:
        """

        recipients = ticket.get_subscriber_emails()
        title = f'Ticket #{ticket.id_zfill} - "{ticket.title}" has been assigned to {ticket.assigned.name}.'
        ticket_url = app.config['base_url'] + url_for('flicket_bp.ticket_view', ticket_id=ticket.id)
        html_body = render_template('email_ticket_assign.html', ticket=ticket, number=ticket.id_zfill,
                                    ticket_url=ticket_url)

        self.send_email(title, self.sender, recipients, html_body)

    def department_category_ticket(self, ticket):
        """
        Change ticket department or category email notification

        :param ticket: ticket object
        :return:
        """

        recipients = ticket.get_subscriber_emails()
        title = f'Ticket #{ticket.id_zfill} - "{ticket.title}" has changed department and/or category.'
        ticket_url = app.config['base_url'] + url_for('flicket_bp.ticket_view', ticket_id=ticket.id)
        html_body = render_template('email_ticket_department_category.html', ticket=ticket, number=ticket.id_zfill,
                                    ticket_url=ticket_url)

        self.send_email(title, self.sender, recipients, html_body)

    def release_ticket(self, ticket):
        """
        :param ticket: ticket object
        :return:
        """

        recipients = ticket.get_subscriber_emails()
        title = f'Ticket #{ticket.id_zfill} - "{ticket.title}" has been released.'
        ticket_url = app.config['base_url'] + url_for('flicket_bp.ticket_view', ticket_id=ticket.id)
        html_body = render_template('email_ticket_release.html', ticket=ticket, number=ticket.id_zfill,
                                    ticket_url=ticket_url)

        self.send_email(title, self.sender, recipients, html_body)

    def close_ticket(self, ticket):
        """
        :param ticket: ticket object
        :return:
        """

        recipients = ticket.get_subscriber_emails()
        title = f'Ticket #{ticket.id_zfill} - "{ticket.title}" has been closed.'
        ticket_url = app.config['base_url'] + url_for('flicket_bp.ticket_view', ticket_id=ticket.id)
        html_body = render_template('email_ticket_close.html', ticket=ticket, ticket_url=ticket_url)

        self.send_email(title, self.sender, recipients, html_body)

    def tickets_not_closed(self, user, tickets):
        """
        Sends email to user notifying them that tickets they have created or have been assigned
        that are
        :return:
        """

        recipient = [user.email]
        title = 'Outstanding Ticket Notifications'
        html_body = render_template('email_ticket_not_closed.html', tickets=tickets,
                                    title="Tickets Still Awaiting Resolution", base_url=app.config['base_url'])

        self.send_email(title, self.sender, recipient, html_body)

    def password_reset(self, user, new_password):
        """
        Sends email to user notifying of password reset.
        :param user:
        :param new_password:
        :return:
        """

        recipient = [user.email]
        title = 'Password Reset'
        html_body = render_template('email_password_reset.html', title=title, new_password=new_password)

        self.send_email(title, self.sender, recipient, html_body)

    def test_email(self, recipients):
        """
        :return:
        """

        html_body = render_template('email_test.html')

        self.send_email('Flicket Test Email', self.sender, recipients, html_body)

    @send_async_email
    def send_email(self, subject, sender, recipients, html_body):
        """
        Sends email via async thread.

        :param subject: string
        :param sender: string
        :param recipients: list()
        :param html_body: string
        :return: nowt
        """

        if not app.config['MAIL_SUPPRESS_SEND']:
            with app.app_context():
                message = Message(subject, sender=sender, recipients=recipients, html=html_body)
                self.mail.send(message)
