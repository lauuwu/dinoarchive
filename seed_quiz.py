"""
Carga preguntas de quiz para los dinosaurios ya existentes en la API.
Busca cada dinosaurio por nombre (no asume IDs fijos).

Cada dinosaurio recibe 2 preguntas fáciles (10 puntos) y 1 difícil (25 puntos).
El campo 'fact' es un dato curioso PROPIO de cada pregunta, distinto al
fun_fact que ya se muestra en la ficha del dinosaurio.

IMPORTANTE: este script vuelve a insertar TODAS las preguntas. Si ya habías
corrido una versión anterior de este seed, primero vaciá la tabla para
evitar duplicados:

    kubectl exec -it deployment/postgres -n dinoarchive -- \\
        psql -U dino -d dinoarchive -c "TRUNCATE TABLE quiz_questions;"

Uso:
    python3 seed_quiz.py
"""
import json
import urllib.request
import urllib.error

API_BASE = "http://dinoarchive.local:8080"

# (nombre_dino, pregunta, correcta, incorrecta_1, incorrecta_2, dato_curioso, dificultad, puntos)
QUESTIONS = [
    # ---------- Tyrannosaurus Rex ----------
    ("Tyrannosaurus Rex", "¿En qué período vivió el Tyrannosaurus Rex?", "Cretácico", "Jurásico", "Triásico", "Vivió en los últimos millones de años antes de la gran extinción.", "easy", 10),
    ("Tyrannosaurus Rex", "¿Qué característica de su mordida lo hacía único?", "Podía triturar huesos", "No tenía dientes", "Mordía muy débil", "Sus dientes podían medir hasta 30 cm contando la raíz.", "easy", 10),
    ("Tyrannosaurus Rex", "¿Cuál era aproximadamente la fuerza de mordida estimada del T-Rex?", "Más de 8.000 kg", "Apenas 50 kg", "Igual a la de un perro", "Es una de las mordidas más fuertes calculadas para cualquier animal terrestre conocido.", "hard", 25),

    # ---------- Velociraptor ----------
    ("Velociraptor", "¿Qué tenía el Velociraptor que casi nunca se muestra en el cine?", "Plumas", "Branquias", "Caparazón", "Medía apenas un metro de largo, mucho menos que en las películas.", "easy", 10),
    ("Velociraptor", "¿Cómo solía cazar el Velociraptor?", "En grupos", "Siempre solo", "Bajo el agua", "Su garra curva en el segundo dedo se usaba para sujetar presas, no para abrir el vientre como se suele mostrar.", "easy", 10),
    ("Velociraptor", "¿En qué formación geológica se halló el famoso fósil 'luchando' con un Protoceratops?", "Formación Djadochta, Mongolia", "Formación Hell Creek, EE.UU.", "Formación Morrison, EE.UU.", "Ambos animales quedaron sepultados juntos, posiblemente por el colapso de una duna.", "hard", 25),

    # ---------- Stegosaurus ----------
    ("Stegosaurus", "¿Qué tenía el Stegosaurus en la espalda?", "Placas óseas", "Branquias", "Aletas", "Las placas no estaban fusionadas al esqueleto, sino incrustadas en la piel.", "easy", 10),
    ("Stegosaurus", "¿Cómo era el cerebro del Stegosaurus en relación a su tamaño corporal?", "Muy pequeño, como una nuez", "Enorme", "Inexistente", "A pesar de su tamaño, su cerebro pesaba apenas unos 80 gramos.", "easy", 10),
    ("Stegosaurus", "¿Cuál era la función principal que hoy se cree que tenían sus placas?", "Regular la temperatura corporal y exhibición visual", "Volar", "Respirar bajo el agua", "Estaban llenas de vasos sanguíneos, lo que sugiere un rol térmico además de visual.", "hard", 25),

    # ---------- Triceratops ----------
    ("Triceratops", "¿Cuántos cuernos faciales tenía el Triceratops?", "Tres", "Uno", "Cinco", "Su nombre significa justamente 'cara de tres cuernos'.", "easy", 10),
    ("Triceratops", "¿Para qué se usaba probablemente su escudo óseo?", "Defensa y exhibición", "Para volar", "Para nadar", "Algunos fósiles muestran marcas de mordidas de T-Rex en el escudo, evidencia de enfrentamientos reales.", "easy", 10),
    ("Triceratops", "¿Con qué otro género se lo relaciona tan de cerca que algunos paleontólogos los consideran la misma especie en distintas edades?", "Torosaurus", "Stegosaurus", "Iguanodon", "Esta hipótesis sigue siendo debatida activamente en la comunidad científica.", "hard", 25),

    # ---------- Diplodocus ----------
    ("Diplodocus", "¿Qué lo hacía uno de los dinosaurios más largos?", "Su cuello y cola extremadamente largos", "Su altura", "Su peso extremo", "A pesar de su longitud, era relativamente liviano para su tamaño gracias a huesos huecos.", "easy", 10),
    ("Diplodocus", "¿Cómo podía usar su cola para defenderse?", "Como un látigo", "Como una maza", "Como una lanza", "Se estima que la punta de la cola pudo alcanzar velocidades supersónicas al chasquearla.", "easy", 10),
    ("Diplodocus", "¿Cuántas vértebras caudales llegaba a tener aproximadamente su cola?", "Alrededor de 80", "Apenas 10", "Más de 500", "Es una de las colas con más vértebras de todo el reino animal conocido.", "hard", 25),

    # ---------- Allosaurus ----------
    ("Allosaurus", "¿En qué período dominó el Allosaurus?", "Jurásico", "Cretácico", "Triásico", "Fue uno de los depredadores más comunes de su época en Norteamérica.", "easy", 10),
    ("Allosaurus", "¿Cómo cazaba presas más grandes que él?", "En grupos", "Siempre solo", "Con veneno", "Se han hallado varios individuos juntos cerca de restos de saurópodos grandes.", "easy", 10),
    ("Allosaurus", "¿En qué famosa formación geológica de EE.UU. se hallaron la mayoría de sus fósiles?", "Formación Morrison", "Formación Hell Creek", "Formación Djadochta", "Esa misma formación también contiene fósiles de Diplodocus y Stegosaurus.", "hard", 25),

    # ---------- Ankylosaurus ----------
    ("Ankylosaurus", "¿Qué tenía el Ankylosaurus en la punta de la cola?", "Una maza ósea", "Espinas venenosas", "Garras", "Esa maza podía pesar varios kilos y romper huesos de un golpe certero.", "easy", 10),
    ("Ankylosaurus", "¿Cómo estaba protegido su cuerpo?", "Con placas óseas", "No tenía protección", "Con escamas blandas", "Incluso sus párpados estaban protegidos por placas óseas.", "easy", 10),
    ("Ankylosaurus", "¿De qué material biológico estaban hechas sus placas de armadura, según estudios histológicos?", "Hueso dérmico (osteodermos)", "Queratina pura, como las uñas", "Cartílago blando", "Estas placas se desarrollaban directamente en la piel, no en el esqueleto interno.", "hard", 25),

    # ---------- Pteranodon ----------
    ("Pteranodon", "¿El Pteranodon era técnicamente un dinosaurio?", "No, era un reptil volador", "Sí, un dinosaurio típico", "Era un ave moderna", "Los pterosaurios son un grupo de reptiles voladores, primos de los dinosaurios pero no dinosaurios en sí.", "easy", 10),
    ("Pteranodon", "¿Cómo se alimentaba?", "Como un pelícano, sin dientes", "Masticando con muelas", "Filtrando plancton", "Su nombre significa justamente 'ala sin diente'.", "easy", 10),
    ("Pteranodon", "¿Qué envergadura alar podía alcanzar?", "Hasta 7 metros", "Apenas 50 centímetros", "Más de 20 metros", "Eso lo hacía uno de los animales voladores más grandes conocidos de su época.", "hard", 25),

    # ---------- Compsognathus ----------
    ("Compsognathus", "¿Qué tamaño tenía aproximadamente?", "El de un pollo", "El de un elefante", "El de una ballena", "Es uno de los dinosaurios no aviares más pequeños jamás descubiertos.", "easy", 10),
    ("Compsognathus", "¿Qué solía cazar?", "Insectos y pequeños lagartos", "Grandes saurópodos", "Peces de mar abierto", "Un fósil famoso fue hallado con los restos de una lagartija aún en el estómago.", "easy", 10),
    ("Compsognathus", "¿En qué país europeo se hallaron sus fósiles más famosos?", "Alemania", "Argentina", "China", "Provienen de las mismas calizas de grano fino donde se halló el Archaeopteryx.", "hard", 25),

    # ---------- Parasaurolophus ----------
    ("Parasaurolophus", "¿Qué tenía en la cabeza?", "Una cresta tubular", "Cuernos retorcidos", "Una placa frontal", "La cresta era hueca por dentro, conectada a las fosas nasales.", "easy", 10),
    ("Parasaurolophus", "¿Para qué se cree que usaba su cresta?", "Para emitir sonidos", "Para volar", "Para nadar mejor", "Investigadores recrearon digitalmente el sonido que pudo producir, similar a un cuerno grave.", "easy", 10),
    ("Parasaurolophus", "¿Qué grupo de dinosaurios herbívoros integra, caracterizado por su pico de pato?", "Hadrosaurios", "Ceratopsios", "Anquilosaurios", "Este grupo fue extremadamente exitoso y diverso a finales del Cretácico.", "hard", 25),

    # ---------- Yutyrannus huali ----------
    ("Yutyrannus huali", "¿Qué tenía de especial el Yutyrannus?", "Estaba cubierto de plumas", "Tenía branquias", "Era acuático", "Su nombre significa 'tirano emplumado hermoso'.", "easy", 10),
    ("Yutyrannus huali", "¿Qué relación tenía con el Tyrannosaurus?", "Era un pariente mucho más antiguo", "Era su presa habitual", "No tenía relación", "Vivió unos 60 millones de años antes que el T-Rex.", "easy", 10),
    ("Yutyrannus huali", "¿Aproximadamente cuánto pesaba un adulto?", "Alrededor de 1.400 kg", "Apenas 20 kg", "Más de 10.000 kg", "Eso lo convierte en el animal emplumado más pesado conocido hasta la fecha.", "hard", 25),

    # ---------- Spinosaurus ----------
    ("Spinosaurus", "¿Qué tenía en el lomo el Spinosaurus?", "Una vela ósea", "Placas acorazadas", "Una joroba de grasa", "La vela estaba sostenida por largas espinas neurales que partían de la columna.", "easy", 10),
    ("Spinosaurus", "¿Dónde pasaba probablemente buena parte del tiempo?", "Nadando en busca de peces", "Bajo tierra", "En la copa de los árboles", "Estudios de densidad ósea sugieren un estilo de vida semiacuático.", "easy", 10),
    ("Spinosaurus", "¿Cómo se compara su longitud estimada con la del Tyrannosaurus Rex?", "Era más largo", "Era mucho más corto", "Eran idénticos", "Se estima que pudo superar los 15 metros, más que cualquier T-Rex conocido.", "hard", 25),

    # ---------- Giganotosaurus ----------
    ("Giganotosaurus", "¿Cómo se compara su tamaño con el T-Rex?", "Era ligeramente más largo", "Era mucho más pequeño", "Eran idénticos", "Algunos estudios lo ubican como uno de los terópodos carnívoros más grandes conocidos.", "easy", 10),
    ("Giganotosaurus", "¿Cómo cazaba presas grandes?", "En grupo", "Siempre en solitario", "Con trampas", "Se hallaron varios individuos cerca entre sí, sugiriendo comportamiento social.", "easy", 10),
    ("Giganotosaurus", "¿En qué país sudamericano se descubrió?", "Argentina", "Brasil", "Perú", "Fue hallado en la Patagonia, en la provincia de Neuquén.", "hard", 25),

    # ---------- Brachiosaurus ----------
    ("Brachiosaurus", "¿Qué característica tenían sus patas?", "Las delanteras eran más largas", "Las traseras eran más largas", "Todas iguales", "Esto le daba una postura inclinada hacia arriba, poco común entre saurópodos.", "easy", 10),
    ("Brachiosaurus", "¿Qué altura podía alcanzar su cabeza?", "Más de 12 metros", "Apenas 2 metros", "Nunca se levantaba del suelo", "Eso le permitía alimentarse de follaje que otros herbívoros no alcanzaban.", "easy", 10),
    ("Brachiosaurus", "¿Qué problema fisiológico habría tenido que resolver su corazón, según los científicos?", "Bombear sangre hasta una cabeza muy elevada", "No tenía corazón", "Bombear agua de mar", "Se estima que su corazón debió pesar cientos de kilos para lograrlo.", "hard", 25),

    # ---------- Iguanodon ----------
    ("Iguanodon", "¿Qué tenía de particular su pulgar?", "Tenía forma de pico, usado como arma", "Era igual al resto de los dedos", "No tenía pulgar", "Durante años los científicos no supieron bien dónde ubicarlo en el esqueleto.", "easy", 10),
    ("Iguanodon", "¿Qué importancia histórica tiene el Iguanodon?", "Fue de los primeros descritos científicamente", "Fue descubierto este siglo", "Nunca se halló un fósil completo", "Fue nombrado en 1825, basado inicialmente solo en algunos dientes.", "easy", 10),
    ("Iguanodon", "¿Con qué animal actual se compararon erróneamente sus dientes al nombrarlo?", "La iguana", "El perro", "El tiburón", "De ahí viene su nombre, que significa 'diente de iguana'.", "hard", 25),

    # ---------- Pachycephalosaurus ----------
    ("Pachycephalosaurus", "¿Qué tenía de especial su cráneo?", "Era abovedado y muy grueso", "Era plano y frágil", "No tenía cráneo óseo", "El domo podía tener hasta 25 cm de espesor.", "easy", 10),
    ("Pachycephalosaurus", "¿Para qué se cree que usaba su cabeza?", "Para embestir como un carnero", "Para excavar túneles", "Para filtrar agua", "Estudios recientes debaten si los embistes eran de frente o más bien laterales.", "easy", 10),
    ("Pachycephalosaurus", "¿Qué significa su nombre científico?", "Lagarto de cabeza gruesa", "Lagarto sin cabeza", "Lagarto volador", "Hace referencia directa al grosor inusual de su cráneo.", "hard", 25),

    # ---------- Carnotaurus ----------
    ("Carnotaurus", "¿Qué tenía sobre los ojos?", "Pequeños cuernos", "Una cresta de plumas", "Una placa transparente", "Es uno de los pocos terópodos grandes con cuernos bien desarrollados.", "easy", 10),
    ("Carnotaurus", "¿Cómo eran sus brazos?", "Diminutos", "Extremadamente largos", "Con seis dedos", "Eran proporcionalmente más cortos incluso que los del Tyrannosaurus.", "easy", 10),
    ("Carnotaurus", "¿En qué país se halló el único esqueleto casi completo conocido?", "Argentina", "Mongolia", "Canadá", "El fósil incluso conservó impresiones de piel, algo muy poco común.", "hard", 25),

    # ---------- Brontosaurus ----------
    ("Brontosaurus", "¿Con qué otro dinosaurio se lo confundió por años?", "Apatosaurus", "Triceratops", "Stegosaurus", "Durante casi un siglo se consideró un nombre inválido.", "easy", 10),
    ("Brontosaurus", "¿Cuándo se restauró su nombre como especie válida?", "En 2015", "En 1850", "Nunca se restauró", "Un estudio detallado de huesos encontró suficientes diferencias con Apatosaurus.", "easy", 10),
    ("Brontosaurus", "¿Qué significa literalmente su nombre?", "Lagarto trueno", "Lagarto veloz", "Lagarto pequeño", "El nombre evoca el supuesto sonido de sus pasos al caminar.", "hard", 25),

    # ---------- Therizinosaurus ----------
    ("Therizinosaurus", "¿Qué tenía de extremadamente largo el Therizinosaurus?", "Sus garras", "Su cuello", "Sus dientes", "Su nombre significa justamente 'lagarto guadaña'.", "easy", 10),
    ("Therizinosaurus", "¿Qué tipo de dieta tenía, a pesar de ser un terópodo?", "Principalmente vegetal", "Exclusivamente carnívora", "Solo insectos", "Es un raro ejemplo de terópodo que evolucionó hacia el herbivorismo.", "easy", 10),
    ("Therizinosaurus", "¿Para qué se cree que usaba principalmente sus enormes garras?", "Alcanzar y cortar vegetación, y defenderse", "Cavar túneles subterráneos", "Nadar más rápido", "También pudieron servir como exhibición o defensa ante depredadores.", "hard", 25),

    # ---------- Oviraptor ----------
    ("Oviraptor", "¿De qué fue injustamente acusado durante años?", "De robar huevos ajenos", "De ser venenoso", "De no poder caminar", "Su nombre significa literalmente 'ladrón de huevos'.", "easy", 10),
    ("Oviraptor", "¿De quién eran realmente los huevos que incubaba?", "Eran los suyos propios", "Eran de otra especie", "No incubaba huevos", "Se halló un fósil sentado sobre un nido en posición de incubación, como un ave.", "easy", 10),
    ("Oviraptor", "¿Qué tenía en lugar de dientes?", "Un pico óseo robusto", "Colmillos largos", "Ningún tipo de boca", "Ese pico le habría permitido romper cáscaras de huevo o conchas duras.", "hard", 25),

    # ---------- Deinonychus ----------
    ("Deinonychus", "¿Qué tenía en cada pie?", "Una garra curva para atacar", "Una pezuña como un caballo", "Membranas para nadar", "Esa garra podía mantenerse levantada del suelo al caminar para no desgastarse.", "easy", 10),
    ("Deinonychus", "¿Qué cambió su descubrimiento en la ciencia?", "La imagen de los dinosaurios como animales lentos", "Nada relevante", "Se descartó como dinosaurio", "Impulsó la teoría de que algunos dinosaurios eran activos y de sangre caliente.", "easy", 10),
    ("Deinonychus", "¿Qué significa su nombre científico?", "Garra terrible", "Diente afilado", "Cola larga", "Hace referencia directa a su garra característica en el segundo dedo del pie.", "hard", 25),

    # ---------- Microraptor ----------
    ("Microraptor", "¿Cuántas alas emplumadas tenía?", "Cuatro", "Dos", "Ninguna", "Tenía plumas largas tanto en las patas delanteras como en las traseras.", "easy", 10),
    ("Microraptor", "¿Cómo era el brillo de sus plumas?", "Iridiscente, como un cuervo", "Totalmente blanco", "Transparente", "Esto se determinó estudiando la estructura microscópica de sus melanosomas fosilizados.", "easy", 10),
    ("Microraptor", "¿Cómo se desplazaba probablemente entre árboles?", "Planeando", "Con vuelo batido sostenido", "Nunca dejaba el suelo", "Sus cuatro alas habrían actuado como un biplano natural.", "hard", 25),

    # ---------- Edmontosaurus ----------
    ("Edmontosaurus", "¿Cómo era su pico?", "De pato", "Curvo como de loro", "No tenía pico", "Por eso se lo agrupa entre los hadrosaurios o 'dinosaurios pico de pato'.", "easy", 10),
    ("Edmontosaurus", "¿Qué tenía en la boca?", "Cientos de dientes de repuesto", "Ningún diente", "Solo cuatro dientes", "Esos dientes formaban baterías dentales que se desgastaban y renovaban constantemente.", "easy", 10),
    ("Edmontosaurus", "¿En qué región de Norteamérica se hallaron la mayoría de sus fósiles?", "Canadá y el oeste de EE.UU.", "Sudamérica", "Europa central", "Le da nombre la ciudad canadiense de Edmonton.", "hard", 25),

    # ---------- Camarasaurus ----------
    ("Camarasaurus", "¿Cómo era su cuello comparado con otros saurópodos?", "Relativamente corto", "El más largo conocido", "No tenía cuello", "Aun así, seguía siendo mucho más largo que el de cualquier animal actual.", "easy", 10),
    ("Camarasaurus", "¿Qué tenían de especial sus vértebras?", "Grandes cavidades huecas", "Eran macizas y pesadas", "Eran de cartílago", "Esas cavidades reducían el peso total del esqueleto sin perder resistencia.", "easy", 10),
    ("Camarasaurus", "¿Qué significa su nombre científico?", "Lagarto con cámaras (por sus vértebras huecas)", "Lagarto sin cuello", "Lagarto venenoso", "Hace referencia directa a esas cavidades internas descubiertas en sus huesos.", "hard", 25),

    # ---------- Kentrosaurus ----------
    ("Kentrosaurus", "¿De qué dinosaurio es pariente africano?", "Stegosaurus", "Triceratops", "Velociraptor", "Pertenece a la misma familia de dinosaurios con placas y espinas.", "easy", 10),
    ("Kentrosaurus", "¿Dónde tenía espinas defensivas además de la cola?", "Sobre los hombros", "En las patas delanteras", "En la cabeza", "Esas espinas adicionales lo distinguen claramente del Stegosaurus.", "easy", 10),
    ("Kentrosaurus", "¿En qué país africano se hallaron sus fósiles originales?", "Tanzania", "Egipto", "Sudáfrica", "Provienen de la famosa formación Tendaguru, también rica en saurópodos.", "hard", 25),

    # ---------- Plateosaurus ----------
    ("Plateosaurus", "¿En qué período vivió?", "Triásico", "Cretácico", "Jurásico tardío", "Es uno de los primeros grandes dinosaurios herbívoros conocidos.", "easy", 10),
    ("Plateosaurus", "¿Qué sugiere el hallazgo de varios esqueletos juntos?", "Que viajaban en grupo", "Que vivían solos", "Que eran acuáticos", "Se han hallado decenas de individuos en un mismo yacimiento en Alemania.", "easy", 10),
    ("Plateosaurus", "¿A qué grupo de dinosaurios pertenece, antecesor de los grandes saurópodos?", "Prosaurópodos / sauropodomorfos basales", "Terópodos", "Anquilosaurios", "Este grupo allanó el camino evolutivo hacia gigantes como el Brachiosaurus.", "hard", 25),

    # ---------- Coelophysis ----------
    ("Coelophysis", "¿Qué tenían de especial sus huesos?", "Eran huecos", "Eran macizos", "Eran de cartílago", "Esa característica también se observa en las aves modernas.", "easy", 10),
    ("Coelophysis", "¿Cómo cazaba según la evidencia fósil?", "En grandes grupos", "Siempre en solitario", "Solo de noche", "Se hallaron cientos de individuos juntos en Ghost Ranch, Nuevo México.", "easy", 10),
    ("Coelophysis", "¿De qué período es uno de los dinosaurios mejor documentados?", "Triásico tardío", "Cretácico temprano", "Jurásico medio", "Esto lo convierte en una referencia clave para entender a los primeros dinosaurios.", "hard", 25),

    # ---------- Dilophosaurus ----------
    ("Dilophosaurus", "¿Qué tenía sobre la cabeza?", "Dos crestas óseas paralelas", "Un cuerno único", "Una placa transparente", "Esas crestas eran probablemente demasiado frágiles para el combate.", "easy", 10),
    ("Dilophosaurus", "¿Qué mostró el cine que no era real?", "Que escupía veneno", "Que tenía crestas", "Que era carnívoro", "Tampoco era tan pequeño como se lo representó en esa película.", "easy", 10),
    ("Dilophosaurus", "¿Qué significa su nombre científico?", "Lagarto de dos crestas", "Lagarto sin cresta", "Lagarto venenoso", "Hace referencia directa al par de crestas sobre su cráneo.", "hard", 25),

    # ---------- Megalosaurus ----------
    ("Megalosaurus", "¿Qué logro histórico tiene el Megalosaurus?", "Fue el primer dinosaurio descrito científicamente", "Fue el último en descubrirse", "Nunca tuvo nombre científico", "Fue descrito en 1824 por William Buckland.", "easy", 10),
    ("Megalosaurus", "¿Qué significa su nombre?", "Lagarto grande", "Pequeño cazador", "Rey de las plumas", "En ese momento ni siquiera existía todavía la palabra 'dinosaurio'.", "easy", 10),
    ("Megalosaurus", "¿En qué año se acuñó la palabra 'dinosaurio', usando entre otros al Megalosaurus como referencia?", "1842", "1900", "1750", "El término fue propuesto por el científico Richard Owen.", "hard", 25),

    # ---------- Styracosaurus ----------
    ("Styracosaurus", "¿Qué tenía coronando su escudo craneal?", "Largas espinas", "Plumas coloridas", "Una vela ósea", "Esas espinas podían ser tan largas como las de un Triceratops, pero más numerosas.", "easy", 10),
    ("Styracosaurus", "¿Cuántas espinas largas podía tener en el escudo?", "Hasta seis", "Solo una", "Ninguna", "Su nombre significa justamente 'lagarto con púas'.", "easy", 10),
    ("Styracosaurus", "¿A qué familia de dinosaurios con cuernos pertenece, junto al Triceratops?", "Ceratopsios", "Hadrosaurios", "Anquilosaurios", "Esta familia se caracteriza por sus escudos óseos y cuernos faciales.", "hard", 25),
]


def get_dino_map():
    with urllib.request.urlopen(f"{API_BASE}/dinos/") as r:
        dinos = json.loads(r.read())
    return {d["name"]: d["id"] for d in dinos}


def main():
    dino_map = get_dino_map()
    created, skipped = 0, 0

    for name, question, correct, wrong1, wrong2, fact, difficulty, points in QUESTIONS:
        dino_id = dino_map.get(name)
        if not dino_id:
            print(f"⚠️  Saltando '{question[:40]}...' — no encontré el dinosaurio '{name}'")
            skipped += 1
            continue

        payload = json.dumps({
            "dinosaur_id": dino_id,
            "question": question,
            "correct_answer": correct,
            "wrong_answer_1": wrong1,
            "wrong_answer_2": wrong2,
            "points": points,
            "fact": fact,
            "difficulty": difficulty,
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{API_BASE}/quiz/",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req) as r:
                r.read()
            created += 1
        except urllib.error.HTTPError as e:
            print(f"❌ Error creando pregunta para '{name}': {e.code} {e.read().decode()}")
            skipped += 1

    print(f"\nListo: {created} preguntas creadas, {skipped} saltadas.")


if __name__ == "__main__":
    main()
