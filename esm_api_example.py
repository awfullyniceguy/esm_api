import esm_api
####Import getpass for password input
import getpass


####McAfee ESM IP Address
esm_ipaddress = "192.168.0.14"

####Ask User for username and password
usr = input('Username: ')
pswd = getpass.getpass('Password:')
####Base64 Encode username and password
usr = esm_api.base64encoder(usr)
pswd = esm_api.base64encoder(pswd)

####Assigned authenticated header to a variable
authenticated_header = esm_api.login_esm(usr, pswd, esm_ipaddress)

####Define files to read
filename = "MD5.txt"
filename2 = "SHA1.txt"
####Modify two watchlists with the filenames specified above
esm_api.add_sysAddWatchlistValues(filename, 9, authenticated_header, esm_ipaddress)
esm_api.add_sysAddWatchlistValues(filename2, 10, authenticated_header, esm_ipaddress)

#Logout
esm_api.logout_esm(authenticated_header, esm_ipaddress)
