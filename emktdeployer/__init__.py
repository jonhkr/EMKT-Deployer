#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description='Upload to FTP and litmus your email marketing.')
parser.add_argument('-c', '--config', metavar='Config file')
parser.add_argument('-f', '--folder', metavar='Email marketing folder')

args = parser.parse_args()

if not args.config or not args.folder:
  parser.print_help()
  exit()

folder = args.folder

foldersplit = folder.split('-')
if len(foldersplit) < 3:
  raise NameError('Invalid folder name, should be like this PRE-YEAR-EMKTID')

prefix = foldersplit[0].upper()
year = foldersplit[1]
emktid = '-'.join(foldersplit[2:]).lower()

folders = [prefix, year, 'emkt', emktid]

from ConfigParser import ConfigParser

config = ConfigParser()

with open(args.config) as f:
  config.readfp(f)

from ftputil import FTPHost

httphost = config.get('FTP', 'httphost')
ftphost = config.get('FTP', 'host')
ftpuser = config.get('FTP', 'username')
ftppasswd = config.get('FTP', 'password')

ftp = FTPHost(ftphost, ftpuser, ftppasswd)
ftp.chdir('/')


for f in folders:
  if ftp.path.exists(f):
    if not ftp.path.isdir(f):
      raise Exception('%s exists on ftp server, but is not a directory' % f)
    print('Dir exists %s' % f)
  else:
    print('Creating dir %s' % f)
    ftp.mkdir(f)
  ftp.chdir(f)
  print('chdir to %s' % f)

print 'Starting upload in dir %s' % ftp.getcwd()

# Start uploding
import os

def uploadfiles(localpath, ftppath):
  for entry in os.listdir(localpath):
    localentrypath = '%s/%s' % (localpath, entry)
    ftpentrypath = '%s/%s' % (ftppath, entry)
    if os.path.isdir(localentrypath):
      if ftp.path.exists(ftpentrypath):
        if not ftp.path.isdir(ftpentrypath):
          raise Exception('%s exists on ftp server, but is not a directory' % ftpentrypath)
      else:
        print 'Creating dir %s' % ftpentrypath
        ftp.mkdir(ftpentrypath)
      uploadfiles(localentrypath, ftpentrypath)
      continue
    print('Uploading file %s' % ftpentrypath)
    ftp.upload_if_newer(localentrypath, ftpentrypath)

uploadfiles(folder.rstrip('/'), ftp.getcwd())

print('Upload done: %s%s' % (httphost, ftp.getcwd()))
