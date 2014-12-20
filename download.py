# Auto install script for downstream-farmer
# Thanks PabloG for downloading with progress bar (http://stackoverflow.com/a/22776)
import shutil, urllib2, os, tarfile, sys, subprocess

url = 'https://github.com/Storj/downstream-farmer/archive/v0.1.4-alpha.tar.gz'

def main():
  os.makedirs("./downstream-farmer")

  print "Installing dependencies"
  os.system("apt-get install -y git libcrypto++-dev python python3 python-pip")

  file_name = "df-%s" % url.split('/')[-1]
  u = urllib2.urlopen(url)
  f = open("./downstream-farmer/%s" % file_name, 'wb')
  meta = u.info()
  file_size = int(meta.getheaders("Content-Length")[0])
  print "Downloading: %s Bytes: %s" % (file_name, file_size)

  file_size_dl = 0
  block_sz = 8192
  while True:
      buffer = u.read(block_sz)
      if not buffer:
          break

      file_size_dl += len(buffer)
      f.write(buffer)
      status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
      status = status + chr(8)*(len(status)+1)
      print status,

  f.close()

  os.chdir("./downstream-farmer")
  downloaded_tar_name = "./df-v0.1.4-alpha.tar.gz"

  print "Extracting %s" % downloaded_tar_name
  downloaded_tar = tarfile.open(downloaded_tar_name)
  downloaded_tar.extractall(path=".")

  os.chdir("./downstream-farmer-0.1.4-alpha")
  df_folder = "."
  print "Executing setup.py"
  subprocess.call(['python', '%s/setup.py' % df_folder, 'install'])

  print "! downstream-farmer is now installed"
  print "! run downstream-farmer with downstream"
  print "! or python downstream.py in %s" % df_folder

if __name__ == "__main__":
  if not os.geteuid() == 0:
    sys.exit('Script must be run as root')
  main()
