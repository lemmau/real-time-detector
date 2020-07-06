# Real Time detector

This project is developing as a thesis for our careers of Systems Information Engineer at the Univesidad Tecnológica Nacional (UTN - FRBA) - Argentina.

Members:

- Leandro Mauro (mimauro@est.frba.utn.edu.ar)
- Tomas Agustin De Pietro (tomas94depi@gmail.com)
- Lucas Martín Cepeda (lucascepeda007@gmail.com)
- Guillermo Basaldúa (guillermobasaldua@yahoo.com.ar)
- Agustin Bellorini Mansilla (belloriniagustin@gmail.com)

# Dependencies Installation
We encourage to use python virtual environments for dependencies
```
$ sudo apt install python3-venv 
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install -r requirements.txt
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