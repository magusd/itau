# setup python env
```
python -m virtualenv venv
source venv/bin/activate
pip install selenium
```

# setup selenium firefox webdriver
```
tar -xzf geckodriver-v0.29.0-linux64.tar.gz
# or
tar -xzf geckodriver-v0.29.0-macos.tar.gz

mv geckodriver venv/bin/
```

# export your credentials
```
export ITAU_AGENCY=''
export ITAU_ACCOUNT=''
export ITAU_PASSWORD=''
```

# download transactions by month
```
python extrato.py

```