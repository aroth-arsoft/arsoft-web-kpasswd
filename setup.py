#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='arsoft-web-kpasswd',
		version='1.6.5',
		description='change Kerberos password via web',
		author='Andreas Roth',
		author_email='aroth@arsoft-online.com',
		url='http://www.arsoft-online.com/',
		packages=['arsoft.web.kpasswd'],
		scripts=[],
		data_files=[
            ('/etc/arsoft/web/kpasswd/static', ['arsoft/web/kpasswd/static/main.css']),
            ('/etc/arsoft/web/kpasswd/templates', ['arsoft/web/kpasswd/templates/home.html']),
            ]
		)
