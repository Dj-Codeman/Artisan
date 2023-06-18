import shutil,os.path

version = '2.4'
package = 'Manager'

packagename = f"Artisan{package}_v{version}"
packagelocation = "/var/www/updater/software"
packagepath = f"{packagelocation}/{packagename}"
package = shutil.make_archive(f'{packagepath}', 'zip', '/root/Artisan-Hosting/Machine-Management/client')

if os.path.exists(f"{packagepath}.zip"):
   print(package) 
else: 
   print("ZIP file not created")


# Note the folders that should be packaged

# confirmed tests have been ran 