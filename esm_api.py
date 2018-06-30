
import http.client
import ssl
import re
import base64


#######Accept connection even if using self-signed certificate
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


def base64encoder(string_to_encode):
    '''
    This function will encode a string to Base64 for API authentication
    '''
    string_to_encode = string_to_encode.encode()
    string_to_encode = base64.standard_b64encode(string_to_encode)
    string_to_encode = string_to_encode.decode('UTF-8')
    return string_to_encode

####API Functions

def login_esm(usr, pswd, esm_ipaddress):
    '''
    This Function will authenticate to the ESM API
    It will return an authenticated header for future API Calls/Session Management
    Example: login_esm(username_variable, password_variable, esm_ipaddress)
    '''
    conn = http.client.HTTPSConnection(esm_ipaddress)
    payload_dict = {"username": "", "password": "", "locale": "en_US"}
    payload_dict["username"] = usr
    payload_dict["password"] = pswd
    payload_dict = str(payload_dict).replace("'", "\"")
    payload = payload_dict
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"}
    conn.request("POST", "/rs/esm/v2/login", payload, headers)
    res = conn.getresponse()
    data = res.read()
    ##Extract JWToken from Header Response for Session Management
    header_response = str(res.info())
    regex_jwauth = "(?<=Set-Cookie:)(?s)(.+?(?=;))"
    regex_xsrftok = "(?<=Xsrf-Token:)(?s)(.+?(?=Content-Type:))"
    jwttoken = re.findall(regex_jwauth,header_response)
    xsrf_token = re.findall(regex_xsrftok,header_response)
    ##Authenticated Header
    authenticated_header = {'content-type': "application/json",
                            'cache-control': "no-cache",
                            'Cookie': "",
                            'X-Xsrf-Token': ""}
    authenticated_header["Cookie"] = jwttoken[0].strip()
    authenticated_header["X-Xsrf-Token"] = xsrf_token[0].strip()
    return authenticated_header


def sysGetWatchlists(authenticated_header, esm_ipaddress):
    """
    This function will output a JSON formatted list of all watchlists in the System
    Example: sysGetWatchlists(authenticated_header_variable, esm_ipaddress)
    You can read the output by using print(sysGetWatchlists(authenticated_header_variable, esm_ipaddress))
    """
    payload = ""
    conn = http.client.HTTPSConnection(esm_ipaddress)
    conn.request("POST", "/rs/esm/v2/sysGetWatchlists?hidden=false&dynamic=false&writeOnly=false&indexedOnly=false", payload, authenticated_header)
    res = conn.getresponse()
    data = res.read()
    return data

###Submit new item to list
def sysAddWatchlistValues(list_id, list_item, authenticated_header, esm_ipaddress):
    """
    This Function will use the list id to add values.
    Example: sysAddWatchlistValues(11, "thisisatestbyjose.com")
    """
    payload = {"watchlist": 11, "values": ["thisisatestbyjose.com"]}
    payload["watchlist"] = list_id
    payload["values"] = list_item
    payload = str(payload).replace("'", "\"").replace("\"values\": ", "\"values\": [").replace("\"}", "\"]}")
    conn = http.client.HTTPSConnection(esm_ipaddress)
    conn.request("POST", "/rs/esm/v2/sysAddWatchlistValues", payload, authenticated_header)
    res = conn.getresponse()
    data = res.read().decode()
    print(data)


def add_sysAddWatchlistValues(filename, watchlist_id, authenticated_header, esm_ipaddress):
    '''
    This Function will read a file and submit each line to a specified watchlist
    Example: add_sysAddWatchlistValues("Domains.txt", 11)
    '''
    with open (filename, "r") as file:
        for line in file:
            line = line.strip()
            print(line)
            sysAddWatchlistValues(watchlist_id, line, authenticated_header, esm_ipaddress)


###Log out//Close Session
def logout_esm(authenticated_header, esm_ipaddress):
    """
    This Function will log out/terminate the active session initiated by this script
    """
    payload = ""
    conn = http.client.HTTPSConnection(esm_ipaddress)
    conn.request("DELETE", "/rs/esm/logout", payload, authenticated_header)
    res = conn.getresponse()
    data = res.read()
    print(data)
