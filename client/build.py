import PyInstaller.__main__
import requests
import os
import zipfile
import sys
import shutil


def getTorExpertBundle():
	# create directory for the tor expert bundle
	os.mkdir('torbundle')
	os.chdir('torbundle')
	
	# download tor expert bundle
	torURL = 'https://www.torproject.org/dist/torbrowser/10.0.12/tor-win32-0.4.5.6.zip'
	fileData = requests.get(torURL, allow_redirects=True)

	# write downloaded tor expert bundle
	try:
		file = open('tor.zip', 'wb')
		file.write(fileData.content)
	except Exception as error:
		print('[-] Error while writing tor expert bundle: {}'.format(error))
		sys.exit(1)
	else:
		print('[*] Wrote tor expert bundle to file')
	
	# unzip tor expert bundle
	try:
		file = zipfile.ZipFile('tor.zip')
		file.extractall('.')
	except Exception as error:
		print("[-] Error while unpacking tor library: {}".format('error'))
		sys.exit(1)
	else:
		print("[*] Unpacked Tor expert bundle")

	# change directory back to \client
	os.chdir('..')



def main():
	# create payload directory 
	os.mkdir(os.path.join('..', 'payloads'))

	if os.name == 'nt':
		# dont download everytime
		if not os.path.isdir('torbundle'):
			getTorExpertBundle()

		PyInstaller.__main__.run([
		    'client.py',
		    '--onefile',
		    '--add-data=torbundle;torbundle'
		])

		shutil.copy(os.path.join('dist', 'client.exe'), os.path.join('..', 'payloads'))

if __name__ == '__main__':
	main()