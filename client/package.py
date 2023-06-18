import shutil,os.path

version = os.popen("/opt/Artisan/client/manager/artisan_manage.py --version-cli").read().rstrip() # version 2.60 pull the version number from the artisan manager script. also write it to the version.ar
with open("/opt/Artisan/client/version.ar", 'w') as file:
   file.write(version)

package = 'Manager'

packagename = f"Artisan{package}_v{version}"
packagelocation = "/var/www/updater/software"
packagepath = f"{packagelocation}/{packagename}"
package = shutil.make_archive(f'{packagepath}', 'zip', '/opt/Artisan/client')

if os.path.exists(f"{packagepath}.zip"):
   print(package) 
else: 
   print("ZIP file not created")


# Note the folders that should be packaged

# confirmed tests have been ran 
