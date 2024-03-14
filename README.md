## Instagram Data Scraper

This program implements a data scraper for Instagram, providing a toolset to collect Instagram logins of people based on specific gender and age groups.

### Usage:

#### Setting up a Local Environment

```bash
$ python -m venv ./venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```

#### Collecting Accounts from an Instagram Channel and Analyzing Them

```bash
$ python main.py login password true 10 channel 29-05-23
```

- `login`: Instagram login
- `password`: Instagram password
- `true`: Identify whether to collect user logins
- `10`: Depth of parsing (total amount of users will be n * 10, e.g., 10 * 10 = 100), only when collecting user logins
- `channel`: Channel to collect user logins from, only when collecting user logins
- `29-05-23`: Prefix of the temp files in `temp` directory and the output file in `dump` directory containing Instagram logins that match a gender-age criterion

#### Analyzing Instagram Accounts Without Collecting User Logins

```bash
$ python main.py login password false 29-05-23
```

- `login`: Instagram login
- `password`: Instagram password
- `false`: Does not collect user logins, but reads them from `temp` directory
- `29-05-23`: Prefix of the temp files in `temp` directory and the output file in `dump` directory containing Instagram logins that match a gender-age criterion

