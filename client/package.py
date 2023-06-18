import shutil,os.path

version = '2.51' # version 2.60 pull the version number from the artisan manager script. also write it to the version.ar
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
