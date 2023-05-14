## Description:

The program implements a data scraper for Instagram.
It provides tools for analyzing gender and age of a selected auditory.

## Usage:

###### Setting up the local environment 

```
$> python -m venv ./venv
$> source ./venv/bin/activate 
$> pip install -r requirements.txt 
```

###### Execution with users precollection: 

```
$> python main.py login password true 10 public 29-05-23
```

`login` - Instagram login
`password` - Instagram password
`true` - complete users precollection from the specified public
`10` - the depth of parsing (total amount of users got will be 10 * 10 = 100)
`public` - the public to scrap data from 
`29-05-23` - prefix of the files in `dump` and `temp` directories  

###### Execution without users precollection:

```
$> python main.py login password false 29-05-23
```

`login` - Instagram login
`password` - Instagram password
`false` - do not complete users precollection from the specified public
`29-05-23` - prefix of the files in `dump` and `temp` directories  

