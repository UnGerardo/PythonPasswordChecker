import requests
import hashlib
import sys

# optional improvement: instead of reading from command line (because commands are saved (up arrow)) read from a text file


# This function gets the hashed passwords that start with the first 5 chars of an input password
def request_api_data(query_char):
    # stores apiurl with the first 5 chars to search
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    # gets response from url
    res = requests.get(url)
    # catches response errors
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again.')
    return res


# This function takes in the response data and finds the hashed strings that match the rest of the input hashed password
def get_password_leaks_count(hashes, hash_to_check, password_string):
    # creates a generator which produces a hashed string and the amount of times it has been leaked
    hashes = (line.split(':') for line in hashes.text.splitlines())
    # goes through the generator to find the hashed string that matches the input and prints the amount of times the password was leaked
    for h, count in hashes:
        if h == hash_to_check:
            print(f"Your password: '{password_string}' has been leaked {count} times!")
            return
    print(f"Congrats! Your password: '{password_string}' has not been leaked yet!")


# Calls the necessary functions to return how many times the input password has been leaked
def pwned_api_check(password):
    # runs the password through the hashing SHA1 algorithm
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    # splits the hashed password into the first 5 chars and the rest
    first5_chars, tail = sha1password[:5], sha1password[5:]
    # calls response function to get the hashed passwords whose first 5 chars match
    response = request_api_data(first5_chars)
    # calls a function to get the amount of times a password has been leaked
    return get_password_leaks_count(response, tail, password)


if __name__ == '__main__':

    # takes in multiple input passwords
    passwords_to_check_list = sys.argv[1:]

    # loops through all input passwords and gets how many times they were leaked
    for password in passwords_to_check_list:
        pwned_api_check(password)