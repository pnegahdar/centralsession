# This file is part of django-flask-sessions.
# https://github.com/pnegahdar/django-flask-sessions

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Parham Negahdar <pnegahdar@gmail.com>

test: unit

unit:
	inenv test -- py.test --cov centralsession/


