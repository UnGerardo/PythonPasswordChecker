import requests
import hashlib
import sys

# optional improvement: instead of reading from command line (because commands are saved (up arrow)) read from a text file

if __name__ == '__main__':

    def request_api_data(query_char):
        # stores apiurl + password to check - 'password123' hashed in SHA1 = 'CBFDAC6008F9CAB4083784CBD1874F76618D2A97' - only first 5 chars for k-anonymity
        url = 'https://api.pwnedpasswords.com/range/' + query_char
        # gets response from url
        res = requests.get(url)
        if res.status_code != 200:
            raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again.')
        return res

    def get_password_leaks_count(hashes, hash_to_check, password):
        hashes = (line.split(':') for line in hashes.text.splitlines())
        for h, count in hashes:
            if h == hash_to_check:
                print(f"Your password: '{password}' has been leaked {count} times!")
                return
        print(f"Congrats! Your password: '{password}' has not been leaked yet!")

    def pwned_api_check(password):
        # check password if it exists in API response
        sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        first5_chars, tail = sha1password[:5], sha1password[5:]
        response = request_api_data(first5_chars)
        return get_password_leaks_count(response, tail, password)

    passwords_to_check_list = sys.argv[1:]

    for password in passwords_to_check_list:
        pwned_api_check(password)