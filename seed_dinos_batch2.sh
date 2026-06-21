#!/bin/bash
# Carga 20 dinosaurios nuevos a la API. Ajustá la variable API si usás
# un túnel distinto (por ejemplo, si volvés a usar port-forward directo
# al backend en vez del Ingress).
API="http://dinoarchive.local:8080/dinos/"

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Yutyrannus huali","period":"Cretácico","diet":"carnívoro","length_m":"9","description":"Primo emplumado y mucho más antiguo del Tyrannosaurus, vivía en manada.","fun_fact":"Es el animal con plumas más grande jamás descubierto."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Spinosaurus","period":"Cretácico","diet":"carnívoro","length_m":"15","description":"El depredador terrestre más largo conocido, con una vela ósea en el lomo y hábitos semiacuáticos.","fun_fact":"Probablemente pasaba gran parte del tiempo nadando para cazar peces."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Giganotosaurus","period":"Cretácico","diet":"carnívoro","length_m":"12","description":"Uno de los terópodos más grandes jamás hallados, ligeramente más largo que el T-Rex.","fun_fact":"Cazaba en grupo a saurópodos mucho más grandes que él."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Brachiosaurus","period":"Jurásico","diet":"herbívoro","length_m":"22","description":"Saurópodo con patas delanteras más largas que las traseras, lo que le daba una postura inclinada hacia arriba.","fun_fact":"Su cabeza podía alcanzar más de 12 metros de altura."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Iguanodon","period":"Cretácico","diet":"herbívoro","length_m":"10","description":"Uno de los primeros dinosaurios descritos científicamente, con un característico pulgar en forma de pico.","fun_fact":"Su pulgar puntiagudo probablemente se usaba como arma defensiva."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Pachycephalosaurus","period":"Cretácico","diet":"herbívoro","length_m":"4.5","description":"Reconocible por su cráneo abovedado, extremadamente grueso y duro.","fun_fact":"Se cree que usaba su cabeza para embestir rivales, como un carnero."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Carnotaurus","period":"Cretácico","diet":"carnívoro","length_m":"8","description":"Depredador veloz con dos pequeños cuernos sobre los ojos y brazos diminutos.","fun_fact":"Sus brazos eran tan cortos que ni siquiera podía tocarse el pecho."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Brontosaurus","period":"Jurásico","diet":"herbívoro","length_m":"22","description":"Saurópodo masivo de cuello largo, confundido durante décadas con el Apatosaurus.","fun_fact":"Su nombre fue descartado y luego restaurado como especie válida en 2015."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Therizinosaurus","period":"Cretácico","diet":"herbívoro","length_m":"10","description":"Terópodo de aspecto extraño, con garras gigantes y dieta principalmente vegetal.","fun_fact":"Sus garras eran las más largas de cualquier animal conocido, hasta 1 metro."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Oviraptor","period":"Cretácico","diet":"carnívoro","length_m":"2","description":"Pequeño terópodo emplumado, injustamente acusado durante años de robar huevos ajenos.","fun_fact":"Los huevos que se creían robados eran en realidad los suyos: incubaba sus propios nidos."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Deinonychus","period":"Cretácico","diet":"carnívoro","length_m":"3","description":"Cazador ágil con una garra curva en cada pie, usada para atacar a sus presas.","fun_fact":"Su descubrimiento cambió por completo la imagen que se tenía de los dinosaurios como animales lentos."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Microraptor","period":"Cretácico","diet":"carnívoro","length_m":"1","description":"Pequeño dinosaurio con cuatro alas emplumadas, capaz de planear entre árboles.","fun_fact":"Sus plumas tenían un brillo iridiscente negro azulado, similar al de un cuervo."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Edmontosaurus","period":"Cretácico","diet":"herbívoro","length_m":"12","description":"Hadrosaurio de pico de pato, uno de los herbívoros más comunes de finales del Cretácico.","fun_fact":"Tenía cientos de dientes de repuesto organizados en baterías dentales."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Camarasaurus","period":"Jurásico","diet":"herbívoro","length_m":"18","description":"Saurópodo robusto de cuello relativamente corto, uno de los más comunes en el registro fósil de Norteamérica.","fun_fact":"Sus vértebras tenían grandes cavidades huecas que aligeraban su peso."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Kentrosaurus","period":"Jurásico","diet":"herbívoro","length_m":"5","description":"Pariente africano del Stegosaurus, con placas y espinas afiladas a lo largo del cuerpo.","fun_fact":"Tenía espinas defensivas incluso sobre los hombros, además de la cola."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Plateosaurus","period":"Triásico","diet":"herbívoro","length_m":"8","description":"Uno de los primeros grandes dinosaurios herbívoros, capaz de pararse en dos patas para alcanzar follaje alto.","fun_fact":"Se han hallado decenas de esqueletos juntos, sugiriendo que viajaban en grupo."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Coelophysis","period":"Triásico","diet":"carnívoro","length_m":"3","description":"Uno de los dinosaurios más antiguos conocidos, pequeño, veloz y de huesos huecos.","fun_fact":"Vivía y cazaba en grandes grupos, según evidencia de cientos de fósiles juntos."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Dilophosaurus","period":"Jurásico","diet":"carnívoro","length_m":"7","description":"Terópodo temprano con dos crestas óseas paralelas sobre la cabeza.","fun_fact":"A diferencia de su versión en el cine, no tenía gola ni escupía veneno."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Megalosaurus","period":"Jurásico","diet":"carnívoro","length_m":"9","description":"El primer dinosaurio descrito científicamente, en 1824, antes de que existiera siquiera la palabra dinosaurio.","fun_fact":"Su nombre significa literalmente lagarto grande."}'

curl -s -X POST $API -H "Content-Type: application/json" -d '{"name":"Styracosaurus","period":"Cretácico","diet":"herbívoro","length_m":"5.5","description":"Ceratopsio con un gran escudo óseo coronado por largas espinas a modo de corona.","fun_fact":"Podía tener hasta seis espinas largas saliendo de su escudo craneal."}'

echo "Listo, 20 dinosaurios nuevos cargados"
