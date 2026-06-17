#!/bin/bash
API="http://localhost:8000/dinos/"

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Tyrannosaurus Rex","period":"Cretácico","diet":"carnívoro","length_m":"12","description":"El depredador más icónico del Cretácico, con una mordida descomunal.","fun_fact":"Su mordida era tan fuerte que podía triturar huesos."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Velociraptor","period":"Cretácico","diet":"carnívoro","length_m":"2","description":"Pequeño cazador veloz e inteligente, vivía en grupos.","fun_fact":"Tenía plumas, no era escamoso como en las películas."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Stegosaurus","period":"Jurásico","diet":"herbívoro","length_m":"9","description":"Reconocible por las placas óseas en su espalda y la cola con púas.","fun_fact":"Su cerebro era del tamaño de una nuez."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Triceratops","period":"Cretácico","diet":"herbívoro","length_m":"9","description":"Tres cuernos faciales y un gran escudo óseo en el cuello.","fun_fact":"Sus cuernos podían medir más de un metro de largo."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Diplodocus","period":"Jurásico","diet":"herbívoro","length_m":"33","description":"Uno de los dinosaurios más largos, con cuello y cola extremadamente alargados.","fun_fact":"Podía mover su cola como un látigo para defenderse."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Allosaurus","period":"Jurásico","diet":"carnívoro","length_m":"9","description":"Depredador dominante del Jurásico, antecesor evolutivo de los grandes carnívoros del Cretácico.","fun_fact":"Cazaba en grupos para derribar presas más grandes."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Ankylosaurus","period":"Cretácico","diet":"herbívoro","length_m":"7","description":"Acorazado con placas óseas y una maza en la punta de la cola.","fun_fact":"Su maza caudal podía romper huesos de un depredador."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Pteranodon","period":"Cretácico","diet":"carnívoro","length_m":"6","description":"Reptil volador (no era técnicamente un dinosaurio) con una envergadura enorme.","fun_fact":"No tenía dientes, se alimentaba como un pelícano."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Compsognathus","period":"Jurásico","diet":"carnívoro","length_m":"1","description":"Uno de los dinosaurios más pequeños conocidos, del tamaño de un pollo.","fun_fact":"Cazaba insectos y pequeños lagartos."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Parasaurolophus","period":"Cretácico","diet":"herbívoro","length_m":"10","description":"Reconocible por la cresta tubular en su cráneo, posiblemente usada para emitir sonidos.","fun_fact":"Su cresta funcionaba como una trompeta natural."}'

echo "Listo, 10 dinosaurios cargados"
