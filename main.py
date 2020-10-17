import requests

if __name__ == '__main__':

    def request_api_data(query_char):
        # stores apiurl + password to check - 'password123' hashed in SHA1 = 'CBFDAC6008F9CAB4083784CBD1874F76618D2A97' - only first 5 chars for k-anonymity
        url = 'https://api.pwnedpasswords.com/range/' + query_char
        # gets response from url
        res = requests.get(url)
        if res.status_code != 200:
            raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again.')

    def pwned_api_check(password):
        # check password if it exists in API response
        pass

    request_api_data('hello')