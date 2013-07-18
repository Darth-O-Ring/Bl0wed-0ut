#!/usr/bin/python2

__Author__ = "Darth_O-Ring"
__Email__ = "darthoring@gmail.com"
__License__ = """
Copyright (C) 2013-2015  Darth_O-Ring	<darthoring@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import smtplib
import getpass
import time
import sys
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import argparse

version = 'v0.2.1'

parser = argparse.ArgumentParser(description='SMTP and IMAGE function options.')
parser.add_argument('-u', '--username', type=str, required=True, help='Gmail username(Required).', metavar='username')
parser.add_argument('-ph', '--phone', type=str, required=True, help='Phone # to send to(Required).', metavar='phone_number')
parser.add_argument('-txt', '--text', type=str, required=False, help='Text to send(Optional if -pic not given).', metavar='text_message')
parser.add_argument('-n', '--ntimes', default=1, type=int, required=False, help='Number of times to send text(Optional).', metavar='n_times_to_send_text/photo(Default=1)')
parser.add_argument('-pic', '--photo', type=str, required=False, help='Pathname of photo to send(Optional).', metavar='photo to send')
parser.add_argument('-s', '--server', default='smtp.gmail.com', type=str, required=False, help='SMTP Server(Optional).', metavar='SMTPServer(Default=smtp.gmail.com)')
parser.add_argument('--port', default=587, type=int, required=False, help='SMTP Server port(Optional).', metavar='SMTP Port number(Default=587)')
parser.add_argument('--sleep', default=10, type=int, required=False, help='Time to sleep between sends(Optional).', metavar='sleep time(Default=10)')

args = parser.parse_args()

n = args.ntimes

u = args.username

ph = args.phone

s = args.server

port = args.port

sleep = args.sleep

if args.ntimes > 1:
	n = args.ntimes
elif args.ntimes < 1:
	print "\n-n must not be less than 1\n"
	parser.print_help()
	sys.exit(2)
if args.server:
	s = args.server
if args.port:
	port = args.port
if args.sleep:
	sleep = args.sleep

def smtp(u, ph, n, photo="", t=""):
	"""
	u: email username
	ph: phone number to send to
	n: number of times to send
	photo: path to photo being sent
	t: text to send with photo if provided
	counter:  initialized to n
	Sets up an smtp server connection using TLS, then sends text, photo, or photo with text n times.

	"""
	try:
		counter = n
		if len(photo) > 0:
			try:
				filename = photo
				img_data = open(filename, 'rb').read()
				msg = MIMEMultipart()
				if len(t) > 0:
					text = MIMEText(t)
					msg.attach(text)
				image = MIMEImage(img_data, name=os.path.basename(filename))
				msg.attach(image)
				server = smtplib.SMTP(s, port)
				server.starttls()
				p = getpass.getpass('Enter Your Password: ')
				server.login(u, p)
				print '\nBl0wed-0ut %s Running by Darth_O-Ring...\n' % version
				while counter > 0:
					server.sendmail(u, ph, msg.as_string())
					counter -= 1
					time.sleep(sleep)
				if counter == 0:
					print '\nPhoto bomb has finished.\n%s has just been blown out!\n' % ph
					server.quit()
			except IOError:
				print '\nCheck -pic/--photo option format.\n'
				return args.photo
				sys.exit(2)
		elif len(photo) == 0:
			server = smtplib.SMTP(s, port)
			server.starttls()
			p = getpass.getpass('Enter Your Password: ')
			server.login(u, p)
			print '\nBl0wed-0ut %s Running by Darth_O-Ring...\n' % version
			while counter > 0:
				server.sendmail(u, ph, txt)
				counter -= 1
				time.sleep(sleep)
			if counter == 0:
				print '\nText bomb has finished.\n%s has just been blown out!\n' % ph
				server.quit()
	except (ValueError, TypeError):
		print '\nCheck arguments passed: use -h or --help.\n'
		sys.exit(1)
	except smtplib.SMTPConnectError:
		print '\nError: Unable to establish connection with the server.\n'
	except smtplib.SMTPServerDisconnected:
		print '\nError: Server was disconnected.\n'
		sys.exit(1)
	except smtplib.SMTPRecipientsRefused:
		print "\nError: Recipient's refused.  May not be a valid gateway.  Check that -ph == phone#@gateway.\nSee https://en.wikipedia.org/wiki/List_of_SMS_gateways for examples.\n"
		sys.exit(1)
	except smtplib.SMTPDataError:
		print '\nError:  Server refused to accept data.  This happens when sending over a certain amount of data.\nLook for captcha on login screen in browser.\n'
		sys.exit(1)	
	except smtplib.SMTPAuthenticationError:
		print '\nError: Login failed.  Check username and password.\nIf a data error occurred before, try login using browser and look for captcha.\n'
		sys.exit(1)



if args.text and not args.photo:
	txt = args.text
	smtp(u, ph, n, t=txt)

elif not args.photo and not args.text:
	parser.print_help()
	print "\nIf you don't want to use a photo, you must provide a text to send.\nEither a text or photo option must be given.\n"

elif args.photo and not args.text:
	photo = args.photo
	smtp(u, ph, n, photo=photo)

elif args.photo and args.text:
	txt = args.text
	photo = args.photo
	smtp(u, ph, n, photo=photo, t=txt)
