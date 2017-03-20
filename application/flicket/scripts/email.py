#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import render_template, url_for
from flask_mail import Mail, Message

from application import app
from application.flicket.models.flicket_models import FlicketPost
from application.flicket.scripts.decorators import async
from application.flicket_admin.models.flicket_config import FlicketConfig


def get_recipients(ticket):
    """
    Returns a list of emails of all users who have responded to ticket.
    :param ticket: ticket object
    :param replies: replies object
    :return: list of emails
    """

    replies = FlicketPost.query.filter_by(ticket_id=ticket.id).order_by(FlicketPost.date_added.asc())
    recipients = [ticket.user.email]
    if replies:
        for reply in replies:
            recipients.append(reply.user.email)

    recipients = list(set(recipients))

    return recipients


def pad_ticket_id(ticket):
    """
    Pad ticket.id with left zeros
    :param ticket: ticket object
    :return: string
    """

    return str(ticket.id).zfill(6)


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
        )

        self.mail = Mail(app)
        self.mail.init_app(app)

        self.base_url = app.config['base_url']

        self.sender = config.mail_default_sender

    def create_ticket(self, ticket):
        """

        Send emails for newly created tickets.

        :param ticket: ticket object
        :return:
        """
        recipients = get_recipients(ticket)

        title = 'New Ticket: {} - {}'.format(pad_ticket_id(ticket), ticket.title)
        ticket_url = self.base_url + url_for('flicket_bp.ticket_view', ticket_id=ticket.id)
        html_body = render_template('email_ticket_create.html', title=title, number=pad_ticket_id(ticket), ticket_url=ticket_url, ticket=ticket)

        self.send_email(title, self.sender, recipients, html_body)

    def reply_ticket(self, ticket):
        """
        :param ticket: ticket object
        :return:
        """
        recipients = get_recipients(ticket)
        # add the user to whom the ticket has been assigned.
        if ticket.assigned:
            if ticket.assigned.email not in recipients:
                recipients.append(ticket.assigned.email)
        title = 'Ticket Reply: {} - {}'.format(pad_ticket_id(ticket), ticket.title)
        ticket_url = self.base_url + url_for('flicket_bp.ticket_view', ticket_id=ticket.id)
        html_body = render_template('email_ticket_replies.html', title=title, number=pad_ticket_id(ticket), ticket_url=ticket_url, ticket=ticket)

        self.send_email(title, self.sender, recipients, html_body)

    def assign_ticket(self, ticket):
        """
        :param ticket: ticket object
        :return:
        """

        recipients = get_recipients(ticket)
        # add the user to whom the ticket has been assigned.
        if ticket.assigned.email not in recipients:
            recipients.append(ticket.assigned.email)

        title = 'Ticket "{} - {}" - has been assigned'.format(pad_ticket_id(ticket), ticket.title)
        ticket_url = self.base_url + url_for('flicket_bp.ticket_view', ticket_id=ticket.id)
        html_body = render_template('email_ticket_assign.html', ticket=ticket, number=pad_ticket_id(ticket),
                                    ticket_url=ticket_url)

        self.send_email(title, self.sender, recipients, html_body)

    def release_ticket(self, ticket):
        """
        :param ticket: ticket object
        :return:
        """

        recipients = get_recipients(ticket)
        # add the user to whom the ticket was been assigned.
        if ticket.assigned.email not in recipients:
            recipients.append(ticket.assigned.email)

        title = 'Ticket "{} - {}" - has been assigned'.format(pad_ticket_id(ticket), ticket.title)
        ticket_url = self.base_url + url_for('flicket_bp.ticket_view', ticket_id=ticket.id)
        html_body = render_template('email_ticket_release.html', ticket=ticket, number=pad_ticket_id(ticket),
                                    ticket_url=ticket_url)

        self.send_email(title, self.sender, recipients, html_body)


    @async
    def send_email(self, subject, sender, recipients, html_body):
        """

        :param subject:
        :param sender:
        :param recipients:
        :param html_body:
        :return:
        """
        # remove announcer from the recipients list.
        if app.config['ANNOUNCER']['email'] in recipients:
            i = recipients.index(app.config['ANNOUNCER']['email'])
            recipients.pop(i)

        message = Message(subject, sender=sender, recipients=recipients, html=html_body)

        with app.app_context():
            self.mail.send(message)
