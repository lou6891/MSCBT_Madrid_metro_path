# Individual assignment - Moving Around Madrid

### <a name='Rubric'></a>Rubric

| Section    | Max points |
|------------|------------|
| Exercise | 2 points   |
| Code quality | 1 points   |


## <a name='Problem'></a>Problem

In this workgroup exercise you'll be working with the Metro de Madrid stations data.

In order to solve these problems you can create as much auxiliary code as you need, and distribute it in the project as you see fit.  You can create auxiliary packages and modules if you need them.

### <a name='Exercise4-findingaroute'></a>Exercise 4 - finding a route

Create a function `exercise_4` in `main.py` that receives the names of two Metro stations as parameters, and returns a way to go from one to another, in case there's a way.

The returned data should be a list containing all Metro stations one would need to go through from start to finish.

```python
exercise_4("Concha Espina", "Pirámides")
# Would return something like
# ["Concha Espina", "Cruz del Rayo", "Avenida de América", "Núñez de Balboa", "Príncipe de Vergara", "Retiro", "Banco de España", "Sevilla", "Sol", "Opera", "La Latina", "Puerta de Toledo", "Acacias", "Pirámides"]
```