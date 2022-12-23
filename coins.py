# Ayo Eyesan
# Coins

import requests

def dict_to_query(dictionary):
    """ (dict) -> (str)
    Returns a string containing the keys and values of the dictionary
    
    >>> dict_to_query({'email': 'jonathan.campbell@mcgill.ca', 'token': 'ABC'})
    'email=jonathan.campbell@mcgill.ca&token=ABC'
    >>> dict_to_query({'email': 'ayo.eyesan@mail.mcgill.ca', 'token': '5KhR5EK83xEo15Ac'})
    'email=ayo.eyesan@mail.mcgill.ca&token=5KhR5EK83xEo15Ac'
    >>> dict_to_query({'email': 'ayo.eyesan@mail.mcgill.ca', 'token': '5KhR5EK83xEo15Ac'}, {'balance': '250'})
    'email=ayo.eyesan@mail.mcgill.ca&token=5KhR5EK83xEo15Ac&balance=250'
    
    """
    dict_to_query_intermediatte = ''
    dict_to_query = ''
    dict_items = dictionary.items()
    for tuples in dict_items:
        for i in range(len(tuples)):
            if i == 0:
                dict_to_query_intermediatte += tuples[i] + '='
            if i == 1:
                dict_to_query_intermediatte += tuples[i] + '&'
    for i in range(len(dict_to_query_intermediatte) - 1):
        dict_to_query += dict_to_query_intermediatte[i]
    return dict_to_query

class Account:
    API_URL = 'https://coinsbot202.herokuapp.com/api/'
    def __init__(self, email, token):
        """ (str, str) -> (NoneType)
        Creates instance attributes email, token, balance, and request log
        
        >>> my_acct = Account("jonathan.campbell@mcgill.ca", "ABC")
        >>> my_acct.balance
        -1
        >>> my_acct = Account("jonathan.campbell@mcgill.ca", "ABC")
        >>> my_acct.email
        jonathan.campbell@mcgill.ca
        >>> my_acct = Account("jonathan.campbell@mgill.ca", "ABC")
        >>> my_acct.email
        AssertionError: Email must end in mcgill.ca!
        
        """
        if type(email) != str or type(token) != str:
            raise AssertionError('Types of inputs must be a string!')
        if email[len(email) - 9:] != 'mcgill.ca':
            raise AssertionError('Email must end in mcgill.ca!')
        self.email = email
        self.token = token
        self.balance = -1
        self.request_log = []
    def __str__(self):
        """ (NoneType) -> (str)
        Returns a string of the format 'EMAIL has balance BALANCE' where EMAIL and BALANCE refer
        to the appropriate instance attributes
        
        >>> my_acct = Account("jonathan.campbell@mcgill.ca", "ABC")
        >>> print(my_acct)
        jonathan.campbell@mcgill.ca has balance -1
        >>> my_acct = Account("ayo.eyesan@mail.mcgill.ca", "5KhR5EK83xEo15Ac")
        >>> print(my_acct)
        ayo.eyesan@mail.mcgill.ca has balance 130
        >>> my_acct = Account("jonathan.campbell@mcgill.ca", 6412563789)
        >>> print(my_acct)
        AssertionError: Types of inputs must be a string!
        
        """
        return self.email + ' has balance ' + str(self.balance)
    def call_api(self, endpoint, request_dictionary):
        """ (str, dict) -> (dict)
        Returns result dictionary of requests method
        
        >>> my_acct = Account("jonathan.campbell@mcgill.ca", "ABC")
        >>> my_acct.call_api("balance", {'email': my_acct.email})
        AssertionError: The token in the API request did not match the token that was sent
        over Slack.
        >>> my_acct = Account("ayo.eyesan@mail.mcgill.ca", "5KhR5EK83xEo15Ac")
        >>> my_acct.call_api("balance", {'email': my_acct.email})
        {'message': 130, 'status': 'OK'}
        >>> my_acct = Account("ayo.eyesan@mail.mcgill", "5KhR5EK83xEo15Ac")
        >>> my_acct.call_api("balance", {'email': my_acct.email})
        AssertionError: Email must end in mcgill.ca!
        
        """
        if type(endpoint) != str:
            raise AssertionError('Incorrect input type')
        if type(request_dictionary) != dict:
            raise AssertionError('Incorrect input type')
        if endpoint != 'balance' and endpoint != 'transfer':
            raise AssertionError('Invalid endpoint')
        request_dictionary['token'] = self.token
        request_url = 'https://coinsbot202.herokuapp.com/api/' + endpoint + '?' + dict_to_query(request_dictionary)
        result_dict = requests.get(url=request_url).json()
        if result_dict.get('status') != 'OK':
            raise AssertionError(str(result_dict.get('message')))
        return result_dict
    def retrieve_balance(self):
        """ (NoneType) -> (int)
        Updates the balance attribute of the current user to the given value and returns
        the integer
        >>> my_acct = Account("jonathan.campbell@mcgill.ca", "ABC")
        >>> my_acct.retrieve_balance()
        AssertionError: The token in the API request did not match the token that was sent over Slack.
        >>> my_acct = Account("ayo.eyesan@mail.mcgill.ca", "5KhR5EK83xEo15Ac")
        >>> my_acct.retrieve_balance()
        130
        >>> my_acct = Account([ayo.eyesan@mail.mcgill.ca], "5KhR5EK83xEo15Ac")
        >>> my_acct.retrieve_balance()
        AssertionError: Types of input must be a string!
        
        """
        result_dict = self.call_api('balance', {'email': self.email} )
        self.balance = int(result_dict.get('message'))
        return self.balance
    def transfer(self, coins, deposit_email):
        """ (int, str) -> (dict<message>)
        Calls the API to transfer the given amount to coins from the current user to the specified
        user. Returns the value for the key 'message' in the result dictionary.
        
        >>> my_acct = Account("ayo.eyesan@mail.mcgill.ca", "5KhR5EK83xEo15Ac")
        >>> my_acct.transfer(25, "alexa.infelise@mail.mcgill.ca")
        'You have transferred 25 coins of your balance of 25 coins to alexa.infelise@mail.
        mcgill.ca. Your balance is now 105.'
        >>> my_acct = Account("ayo.eyesan@mail.mcgill.ca", "5KhR5EK83xEo15Ac")
        >>> my_acct.transfer(-1, "alexa.infelise@mail.mcgill.ca")
        AssertionError: Balance must be different from defualt of -1
        >>> my_acct = Account("ayo.eyesan@mail.mcgill.ca", "5KhR5EK83xEo15Ac")
        >>> my_acct.transfer(130, "ayo.eyesan@mail.mcgill.ca")
        AssertionError: Deposit email must be different from user email
        
        """
        if self.balance == -1:
            raise AssertionError('Balance must be different from defualt of -1')
        if type(coins) != int or coins < 0:
            raise AssertionError('Invalid coins input')
        if deposit_email[len(deposit_email) - 9:] != 'mcgill.ca':
            raise AssertionError('Email must end in mcgill.ca!')
        if type(deposit_email) != str:
            raise AssertionError('Emaill type must be a string')
        if deposit_email == self.email:
            raise AssertionError('Deposit email must be different from user email')
        if coins < 0 or coins > self.balance:
            raise AssertionError('Coin amount must be positive and no more than current user balance')
        self.amount = str(coins)
        self.deposit_email = deposit_email
        result_dict = self.call_api('transfer', {'withdrawal_email': self.email, 'deposit_email': self.deposit_email, 'amount': self.amount})
        return result_dict.get('message')