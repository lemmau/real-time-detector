# Real Time detector

This project is developing as a thesis for our careers of Systems Information Engineer at the Univesidad Tecnológica Nacional (UTN - FRBA) - Argentina.

Members:

- Leandro Mauro (leammau@gmail.com)
- Tomas Agustin De Pietro (tomas94depi@gmail.com)
- Lucas Martín Cepeda (lucascepeda007@gmail.com)
- Guillermo Basaldúa (guillermobasaldua@yahoo.com.ar)
- Agustin Bellorini Mansilla (belloriniagustin@gmail.com)

# Dependencies Installation
We encourage to use python virtual environments for dependencies
```
$ sudo apt install python3-venv 
$ python -m venv venv
$ source venv/bin/activate
$ pip install cmake 
$ pip install -r requirements.txt
```
if you want to leave the venv context just run 
```
$ deactivate
```

For node depencies run:
```
$ npm i
```
For local development run: 

```
$ npm run local
```
This will watch all changes while developing, refreshing the build and placing it in the folder where Flask can read it. Otherwise, if you just want to build once:
```
$ npm run build
```

Remember export the FLASK_APP and FLASK_ENV environment variables
```
$ export FLASK_APP=flask/app.py
$ export FLASK_ENV=development
```
In the config folder there is a config sample, rename it for "config.json"
```
$ cp config/config.json.sample config/config.json
```
And finally copy the config sample and run the webapp
```
$ flask run
 * Running on http://127.0.0.1:5000/
```
