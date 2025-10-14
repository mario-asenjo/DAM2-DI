personas = {"51227201Z":"Mario Asenjo", "12345678A":"Ana Belén", "98765432B":"Luis Cifuentes"}
print(personas)
print(personas["51227201Z"])
print(personas.get("12345678A"))
print(personas.get("00000000X","No encontrado"))
personas["00000000X"]="Pepe Delgado"
print(personas.keys())
print(personas.values())
print(personas.items())

for key in personas.keys():
    print(key, personas.get(key))

for key, value in personas.items():
    print(key, value)

for key in personas:
    print(key, personas[key])

mitupla = tuple(personas.items())
print(mitupla)

mitupla = mitupla + (("11111111H","Juana García"),)
print(mitupla)