# globle-game-solver

Solver for the game [globle-game.com](https://globle-game.com/)

Please don't mind the dirty code. That was more a proof of concept than anything serious. Nevertheless, feel free to improve the code if you feel like it (there's plenty of space for optimization!)

### Requirements :
- Python3+
- Python module `numpy`

### Installation : 

`pip install -r requirements.txt`

### Usage : 

Give in first argument the tested country name, and in second parameter it's distance to the target country.

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