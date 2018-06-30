

# McAfee ESM 10.x and up REST API for Python 3.6

Python 3.6 code for McAfee® Enterprise Security Manager (ESM) API watchlist manipulation

## Getting Started

I am by no means a programmer, I've put together this Python Script due to the lack of examples I found online for McAfee ESM API. I am not associated to McAfee in any way, just use their products, had a need to automate procedures and so I wrote this.

I'm not responsible for any issues that may arise from executing this code in production. Use at your own risk (Go through the code first, you should never just copy/paste code off the internet without understanding what will happen once you run it).

### Prerequisites

These would be needed in order to run the Module

```
http.client
ssl
re
base64
```

The imports are already performed in the esm_api.py file

You may want to use getpass for secure password input from users.

### Installing

Just copy the esm_api.py script to the same folder as your scripts and import it using:

```
import esm_api
```

Call the functions using esm_api.<name_of_function>

## Authenticating to ESM

Authentication happens through the REST API.

You'd need to specify a username and password, have those encoded using Base64 and submitted as a POST Request.

```
##Specify the ESM IP Address
esm_ipaddress = "192.168.0.14"
##User Credentials in Plain Text for example purposes
usr = "NGCP"
pswd = "security.4u"
##Encode the Username and Password into Base64 Format
usr = esm_api.base64encoder(usr)
pswd = esm_api.base64encoder(pswd)
```

The only time this is used is during initial authentication, all the subsequent API calls during that session use the Header for authentication.

### Authenticated Header

To facilitate session management you'd need to assign the response from initial authentication to a variable and use that in all other API Calls.

```
authenticated_header = esm_api.login_esm(usr, pswd, esm_ipaddress)
```

### Watchlist Manipulation

You'd need to specify a file to read as a variable and then call it in the "esm_api.add_sysAddWatchlistValues" function

```
filename = "MD5.txt"
filename2 = "SHA1.txt"
esm_api.add_sysAddWatchlistValues(filename, 9, authenticated_header, esm_ipaddress)
esm_api.add_sysAddWatchlistValues(filename2, 10, authenticated_header, esm_ipaddress)
```

The other arguments are "watchlist ID", the authenticated header from the example in the previous section and the IP Address of the ESM Server.

## Identifying Lists IDs

I wrote a function to get the JSON output for all your watchlists, you'll need this to identify which lists to call.

```
output = esm_api.sysGetWatchlists(authenticated_header, esm_ipaddress)
print(output.decode())
```

The output would need to be decoded as in the example above since it's a JSON Format reply.

The ID is specified next to the first "id", the name of the list is at the bottom of that object.

For example, in the example below the "Malicious FileNames" watchlist has the "id" : 5 and "Malicious SHA1 Hashes" has the "id" : 10.

```
[ {
  "id" : 5,
  "dynamic" : false,
  "scored" : false,
  "valueCount" : 109,
  "active" : true,
  "errorMsg" : "",
  "customType" : {
    "id" : 0,
    "name" : "4259843"
  },
  "hidden" : false,
  "source" : 5,
  "type" : {
    "id" : 0,
    "name" : "Filename"
  },
  "name" : "Malicious FileNames"
}, {
  "id" : 6,
  "dynamic" : false,
  "scored" : false,
  "valueCount" : 812,
  "active" : true,
  "errorMsg" : "",
  "customType" : {
    "id" : 0,
    "name" : "3"
  },
  "hidden" : false,
  "source" : 5,
  "type" : {
    "id" : 0,
    "name" : "DomainID"
  },
  "name" : "Malicious Domains"
}, {
  "id" : 7,
  "dynamic" : false,
  "scored" : false,
  "valueCount" : 1030,
  "active" : true,
  "errorMsg" : "",
  "customType" : {
    "id" : 0,
    "name" : "65548"
  },
  "hidden" : false,
  "source" : 5,
  "type" : {
    "id" : 0,
    "name" : "Mail_ID"
  },
  "name" : "Malicious E-Mail Address''''s"
}, {
  "id" : 8,
  "dynamic" : false,
  "scored" : false,
  "valueCount" : 22251,
  "active" : true,
  "errorMsg" : "",
  "customType" : {
    "id" : 0,
    "name" : "IPAddress"
  },
  "hidden" : false,
  "source" : 5,
  "type" : {
    "id" : 0,
    "name" : "IPAddress"
  },
  "name" : "Malicious IP List"
}, {
  "id" : 9,
  "dynamic" : false,
  "scored" : false,
  "valueCount" : 9,
  "active" : true,
  "errorMsg" : "",
  "customType" : {
    "id" : 0,
    "name" : "262159"
  },
  "hidden" : false,
  "source" : 5,
  "type" : {
    "id" : 0,
    "name" : "File_Hash"
  },
  "name" : "Malicious MD5 Hashes"
}, {
  "id" : 10,
  "dynamic" : false,
  "scored" : false,
  "valueCount" : 9,
  "active" : true,
  "errorMsg" : "",
  "customType" : {
    "id" : 0,
    "name" : "65619"
  },
  "hidden" : false,
  "source" : 5,
  "type" : {
    "id" : 0,
    "name" : "SHA1"
  },
  "name" : "Malicious SHA1 Hashes"
}, {
  "id" : 11,
  "dynamic" : false,
  "scored" : false,
  "valueCount" : 38827,
  "active" : true,
  "errorMsg" : "",
  "customType" : {
    "id" : 0,
    "name" : "4259841"
  },
  "hidden" : false,
  "source" : 5,
  "type" : {
    "id" : 0,
    "name" : "URL"
  },
  "name" : "Malicious URL''s"
} ]
```


## Logging out

Sessions will timeout eventually but it's a best practice to close them after you've made your changes.

For this use the logout_esm functon

```
esm_api.logout_esm(authenticated_header, esm_ipaddress)
```

The Function uses the Authenticated Header to identify the session and close it.

## Working Example

This Code will ask for user credentials, Authenticate to ESM, modify two watchlists and log out

```
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
```


## Written With

* [README Template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2) - Used this as a Template to write this README

## Contributing

Like I said before, I am by no means a programmer.
Feel free to use this code and tweak it to your own needs.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

* [Self Signed Certificates Workaround](https://community.netapp.com/t5/Software-Development-Kit-SDK-and-API-Discussions/Python-How-to-disable-SSL-certificate-verification/td-p/113697) - Used this to allow API Calls using self-signed certificates to ESM.
