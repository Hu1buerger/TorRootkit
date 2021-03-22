import PyInstaller.__main__
import requests
import os
import zipfile
import sys
import shutil


def get_tor_expert_bundle():
	# create directory for the tor expert bundle
	os.mkdir('torbundle')

	torbundle_dir = os.path.abspath('torbundle')

	# download tor expert bundle
	torURL = 'https://www.torproject.org/dist/torbrowser/10.0.12/tor-win32-0.4.5.6.zip'
	fileData = requests.get(torURL, allow_redirects=True)

	# write downloaded tor expert bundle
	try:
		file = open(os.path.join(torbundle_dir, 'tor.zip'), 'wb')
		file.write(fileData.content)
	except Exception as error:
		print('[-] Error while writing tor expert bundle: {}'.format(error))
		sys.exit(1)
	else:
		print('[*] Wrote tor expert bundle to file')
	
	# unzip tor expert bundle
	try:
		file = zipfile.ZipFile(os.path.join(torbundle_dir, 'tor.zip'))
		file.extractall('.')
	except Exception as error:
		print("[-] Error while unpacking tor library: {}".format('error'))
		sys.exit(1)
	else:
		print("[*] Unpacked Tor expert bundle")



def main(): 
	payload_dir = os.path.abspath(os.path.join('..', 'payloads'))

	if not os.path.isdir(payload_dir):
		os.mkdir(payload_dir)

	if os.name == 'nt':
		# dont download everytime
		if not os.path.isdir('torbundle'):
			get_tor_expert_bundle()

		PyInstaller.__main__.run([
		    'client.py',
		    '--onefile',
		    '--add-data=torbundle;torbundle'
		])

		executable_name = 'client.exe'
		executable_dir = os.path.join('dist', executable_name)


	if executable_name not in os.listdir(payload_dir):
		shutil.copy(executable_dir, payload_dir)


if __name__ == '__main__':
	main()