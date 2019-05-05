#! usr/bin/python3
# -*- coding: utf-8 -*-

import os


def nt_log_on(domain, username, password):
    """

    This feature is experimental for windows hosts that want to authenticate on the
    local machines domain running this application.

    # todo: This will eventually be changed to use ldap but I don't currently have a means to test this.
    :param domain:
    :param username:
    :param password:
    :return:
    """

    valid_os = False
    authenticated = False

    if os.name == 'nt':
        try:
            import pywintypes
            import win32security
            valid_os = True
        except ModuleNotFoundError:
            raise ModuleNotFoundError('Is pywin32 installed?')

    if valid_os:

        try:
            token = win32security.LogonUser(
                username,
                domain,
                password,
                win32security.LOGON32_LOGON_NETWORK,
                win32security.LOGON32_PROVIDER_DEFAULT)
            authenticated = bool(token)
        except pywintypes.error:
            pass

    return authenticated
