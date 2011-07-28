Requirements
============
	* ``django-forms-builder >= 0.4.7`` (probably?)
Installation
===========
	* Add ``django_forms_builder.forms`` to ``INSTALLED_APPS``
	* Add ``cmsplugin_forms_builder`` to ``INSTALLED_APPS``
	* ``python manage.py syncdb``
	* Add a page in your CMS with App hook for ``Forms Builder``
	* Restart Application

It is not necessary to add urls to your urls.py
