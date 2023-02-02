# globle-game-solver

Solver for the game [globle-game.com](https://globle-game.com/)

Please don't mind the dirty code. That was more a proof of concept than anything serious. Nevertheless, feel free to improve the code if you feel like it (there's plenty of space for optimization!)

### Requirements :
- Python3+
- Python module `numpy`

### Installation : 

`pip install -r requirements.txt`

### Usage : 

Give the name of the country being tested as the first argument, and its distance from the target country as the second. The smaller the distance, the more likely it is to be the target country.

Example usage :
```bash
$ python3 distance.py Bangladesh 1055
[...]
382.5 Tajikistan
358.3 Sri Lanka
219.0 Laos
202.8 Malaysia
197.5 Singapore
172.7 Kyrgyzstan
170.8 Pakistan
 32.7 Cambodia
  5.7 Vietnam
```

> Note : The `country_data.json` file is originally taken from https://github.com/the-abe-train/globle