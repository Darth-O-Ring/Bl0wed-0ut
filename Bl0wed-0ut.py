#!/usr/bin/env python2

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

# Imports
import smtplib
import getpass
import time
import sys
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import argparse
import re

# Constants
VERSION = 'v0.2.2'

def bl0w_0ut(args):
	"""
	Sets up an smtp server connection using TLS, 
	then sends the passed in message n times.

	Params:
		@args - dictionary containing all the
				parsed command line arguments
	"""
	try:
		# Connect to the SMTP server
		server = smtplib.SMTP(args['s'], args['port'])
		server.ehlo()
		server.starttls()
		# Authenticate to the server
		server.login( args['u']
		            , getpass.getpass('Enter Your Password: ')
		            )

		# Print a banner and break 0-rings
		print('\nBl0wed-0ut %s by Darth_O-Ring running...' % VERSION)
		for n in range(args['n']):
			server.sendmail( args['u']
			               , args['ph']
			               , args['msg']
			               )
			time.sleep(args['sleep'])
		
		# Closing remarks	
		print('\nText bomb has finished.\n\n'
			  '%s has just been bl0wn 0ut!\n' % args['ph'])
		server.quit()
	
	# Handle each error	
	except smtplib.SMTPConnectError:
		sys.exit('\nError: Cannot connect to server.\n')
	except smtplib.SMTPServerDisconnected:
		sys.exit('\nError: Server connection disconnected.\n')
	except smtplib.SMTPRecipientsRefused:
		print("\nError: Recipient's refused.  May not be a valid "
			  "gateway.  Check that -ph == phone#@gateway.\nSee "
			  "https://en.wikipedia.org/wiki/List_of_SMS_gateways "
			  "for examples.\n")
	except smtplib.SMTPDataError:
		sys.exit('\nError:  Server refused to accept data.  This '
			     'happens when sending over a certain amount of data.'
			     '\nLook for captcha on login screen in browser.\n')
	except smtplib.SMTPAuthenticationError:
		sys.exit('\nError: Login failed.  Check username and password.\n'
				'If a data error occurred before, try login using a '
		        'browser and look for captcha.\n')

def build_msg(text, photo):
	'''build_msg(text, photo)
	Return the message portion of the
	text to bl0w someone 0ut with.
	'''
	# See if there's a photo
	if photo:
		try:
			# Start a multi part MIME message
			msg = MIMEMultipart()
			
			# Attach the photo to it
			image = MIMEImage( open(photo, 'rb').read()
							 , name=os.path.basename(photo)
							 )
			msg.attach(image)
			
			# Attach text if appropriate
			if text:
				msg.attach(MIMEText(text))	
				
			return msg		
		except IOError:
			sys.exit('\nCheck -pic/--photo option format.\n')
	# Otherwise, plain SMS
	else:
		return text

def parse_args(parser):
	'''parse_args(parser)
	Check for errors in user input;
	if no errors occur, return a
	dictionary with the arguments
	required for bl0w_0ut.
	
	Args:
		@parser - ArgumentParser object
	'''
	# Parse the arguments
	args = parser.parse_args()

	# Check for errors
	if args.ntimes < 1:
		sys.exit("\nError:  n must not be less than 1\n")

	if args.port < 0:
		sys.exit('\nError:  port numbers cannot be negative.\n')

	if args.sleep < 0:
		sys.exit('\nError:  why are you assigning a negative value '
			     'to --sleep?\n')

	if not args.photo and not args.text:
		sys.exit("\nIf you don't want to use a photo, you must provide "
				 "text to send.\nEither a text or photo option must be "
			     "given.\n")

	# Return a dictionary of 
	# args to pass to bl0w_0ut
	return { 's'     : args.server
		   , 'port'  : args.port
		   , 'u'     : args.username
		   , 'ph'    : ' '.join(re.findall( r'\d{10}@\w+\.\w+'
			                              , args.phone
			                              )
			                    )
		   , 'n'     : args.ntimes
		   , 'sleep' : args.sleep
		   , 'msg'   : build_msg(args.text, args.photo)
		   }

def build_parser():
	'''build_parser()
	Create and return an ArgumentReader object
	for parsing the Bl0wed-0ut command line args.
	'''
	parser = argparse.ArgumentParser(description='SMTP and IMAGE '
												 'function options.')
												 
	# SMTP Server FQDN
	parser.add_argument( '-s', '--server' 
	                   , default='smtp.gmail.com' 
			           , type=str, required=False 
			           , help='SMTP Server(Optional).' 
			           , metavar='SMTPServer(Default=smtp.gmail.com)'
			           )
	# SMTP Server Port
	parser.add_argument( '--port'
	                   , default=587 
					   , type=int, required=False
		               , help='SMTP Server port(Optional).'
		               , metavar='SMTP Port number(Default=587)'
		               )
	# SMTP Server Username											 
	parser.add_argument( '-u', '--username'
	                   , type=str, required=True
	                   , help='Gmail username(Required).'
	                   , metavar='username'
	                   )
		
	# Phone number
	parser.add_argument( '-ph', '--phone'
	                   , type=str, required=True 
		               , help='Phone # as e-mail address(Required).'
		               , metavar='phone_number'
		               )
	# Text to send
	parser.add_argument( '-txt', '--text'
	                   , type=str, required=False
	                   , help='Text to send(Optional if -pic given).'
	                   , metavar='text_message'
	                   )
	# Number of messages to send
	parser.add_argument( '-n', '--ntimes'
	                   , default=1
	                   , type=int, required=False
	                   , help='Number of times to send text(Optional).'
	                   , metavar='n_times_to_send_text/photo(Default=1)'
	                   )
	# Picture to attach
	parser.add_argument( '-pic', '--photo'
	                   , type=str, required=False
	                   , help='Pathname of photo to send(Optional).'
	                   , metavar='photo to send'
	                   )
	# Delay between sends
	parser.add_argument( '--sleep'
	                   , default=10
	                   , type=int, required=False
	                   , help='Time to sleep between sends(Optional).'
	                   , metavar='sleep time(Default=10)'
	                   )

	# Parser now built
	return parser

def main():
	'''main()
	Parse the command line args and call bl0w_0ut.
	'''
	# Deal with the command line arguments
	args = parse_args(build_parser())
	
	# Start bl0wing 0ut 
	bl0w_0ut(args)
	
if __name__ == '__main__':
	main()
