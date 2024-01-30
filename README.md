---
author: Mohammad Esmaeili
title: Simple Wallet app
---

# Sama-Wally: a simple wallet app

-   a very simple django rest framework project that each user can create multiple wallets
    and they can transfer funds through it
-  we are using django base users as user model

## Requirements  (Prerequisites)
* django
* django rest framework
* Python 3.11 and up 
* sqlite

## development setup guide:

-   setup virtual environment
```bash
 python3.11 -m venv venv && source venv/bin/activate
```

- install dependencies
```bash
pip install -r requirements.txt
```
- migrate to sqlite
```bash
python manage.py migrate
```

- run local server
```bash
python manage.py runserver
```

## Running the tests
we are using pytest as testing library so easily run pytest to run tests
```bash 
    pytest
```

## documentation:
 - you can access api documents made by swagger [here](https://github.com/momhiar/simple-wallet/blob/main/swagger/swagger.yaml)


## How to Contribute
Mention how anyone can contribute to make this project more productive or fix bugs in it.  

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate. If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.

Steps to contribute:
1. Fork this repository (link to your repository)
2. Create your feature branch (git checkout -b feature/fooBar)
3. Commit your changes (git commit -am 'Add some fooBar')
4. Push to the branch (git push origin feature/fooBar)
5. Create a new Pull Request