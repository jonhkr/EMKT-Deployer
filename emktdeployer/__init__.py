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

from ConfigParser import ConfigParser

config = ConfigParser()

with open(args.config) as f:
  config.readfp(f)

from ftputil import FTPHost

ftphost = config.get('FTP', 'host')
ftpuser = config.get('FTP', 'username')
ftppasswd = config.get('FTP', 'password')

ftp = FTPHost(ftphost, ftpuser, ftppasswd)
ftp.chdir('/')

# TODO: Clean this up
if ftp.path.exists(prefix):
  if ftp.path.isdir(prefix):
    ftp.chdir(prefix)
    
  else:
    raise Exception('Prefix exists but is not a directory')
else:
  print('Creating dir %s' % prefix)
  ftp.mkdir(prefix)