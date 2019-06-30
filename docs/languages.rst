Adding Additional Languages
---------------------------

Flicket now supports additional languages through the use of Flask Babel.
To add an additional local:

* Edit `SUPPORTED_LANGUAGES` in `config.py` and add an additional entry to
  the dictionary. For example: `{'en': 'English', 'fr': 'Francais',
  'de': 'German'}`


* Whilst in the project root directory you now need to initialise
  the new language to generate a template file for it.

.. code-block::

    pybabel init -i messages.pot -d application/translations -l de


* In the folder `application/translations` there should now be a new folder
  `de`.


* Edit the file `messages.po` in that folder. For example:

.. code-block::

    msgid "403 Error - Forbidden"
    msgstr "403 Error - Verboten"


* Compile the translations for use:

.. code-block::

    pybabel compile -d application/translations


* If any python or html text strings have been newly tagged for translation
  run:

.. code-block::

    pybabel extract -F babel.cfg -o messages.pot .


* To get the new translations added to the .po files:

.. code-block::

    pybabel update -i messages.pot -d application/translations
