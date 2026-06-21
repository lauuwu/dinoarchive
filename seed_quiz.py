"""
Carga preguntas de quiz para los dinosaurios ya existentes en la API.
Busca cada dinosaurio por nombre (no asume IDs fijos) y le asigna 2 preguntas.

Uso:
    python3 seed_quiz.py

Si tu túnel apunta a otro lado, cambiá la variable API_BASE de abajo.
"""
import json
import urllib.request
import urllib.error

API_BASE = "http://dinoarchive.local:8080"

QUESTIONS = [
    # (nombre_dino, pregunta, correcta, incorrecta_1, incorrecta_2)
    ("Tyrannosaurus Rex", "¿En qué período vivió el Tyrannosaurus Rex?", "Cretácico", "Jurásico", "Triásico"),
    ("Tyrannosaurus Rex", "¿Qué característica de su mordida lo hacía único?", "Podía triturar huesos", "No tenía dientes", "Mordía muy débil"),
    ("Velociraptor", "¿Qué tenía el Velociraptor que casi nunca se muestra en el cine?", "Plumas", "Branquias", "Caparazón"),
    ("Velociraptor", "¿Cómo solía cazar el Velociraptor?", "En grupos", "Siempre solo", "Bajo el agua"),
    ("Stegosaurus", "¿Qué tenía el Stegosaurus en la espalda?", "Placas óseas", "Branquias", "Aletas"),
    ("Stegosaurus", "¿Cómo era el cerebro del Stegosaurus en relación a su tamaño corporal?", "Muy pequeño, como una nuez", "Enorme", "Inexistente"),
    ("Triceratops", "¿Cuántos cuernos faciales tenía el Triceratops?", "Tres", "Uno", "Cinco"),
    ("Triceratops", "¿Para qué se usaba probablemente su escudo óseo?", "Defensa y exhibición", "Para volar", "Para nadar"),
    ("Diplodocus", "¿Qué lo hacía uno de los dinosaurios más largos?", "Su cuello y cola extremadamente largos", "Su altura", "Su peso extremo"),
    ("Diplodocus", "¿Cómo podía usar su cola para defenderse?", "Como un látigo", "Como una maza", "Como una lanza"),
    ("Allosaurus", "¿En qué período dominó el Allosaurus?", "Jurásico", "Cretácico", "Triásico"),
    ("Allosaurus", "¿Cómo cazaba presas más grandes que él?", "En grupos", "Siempre solo", "Con veneno"),
    ("Ankylosaurus", "¿Qué tenía el Ankylosaurus en la punta de la cola?", "Una maza ósea", "Espinas venenosas", "Garras"),
    ("Ankylosaurus", "¿Cómo estaba protegido su cuerpo?", "Con placas óseas", "No tenía protección", "Con escamas blandas"),
    ("Pteranodon", "¿El Pteranodon era técnicamente un dinosaurio?", "No, era un reptil volador", "Sí, un dinosaurio típico", "Era un ave moderna"),
    ("Pteranodon", "¿Cómo se alimentaba?", "Como un pelícano, sin dientes", "Masticando con muelas", "Filtrando plancton"),
    ("Compsognathus", "¿Qué tamaño tenía aproximadamente?", "El de un pollo", "El de un elefante", "El de una ballena"),
    ("Compsognathus", "¿Qué solía cazar?", "Insectos y pequeños lagartos", "Grandes saurópodos", "Peces de mar abierto"),
    ("Parasaurolophus", "¿Qué tenía en la cabeza?", "Una cresta tubular", "Cuernos retorcidos", "Una placa frontal"),
    ("Parasaurolophus", "¿Para qué se cree que usaba su cresta?", "Para emitir sonidos", "Para volar", "Para nadar mejor"),

    ("Yutyrannus huali", "¿Qué tenía de especial el Yutyrannus?", "Estaba cubierto de plumas", "Tenía branquias", "Era acuático"),
    ("Yutyrannus huali", "¿Qué relación tenía con el Tyrannosaurus?", "Era un pariente mucho más antiguo", "Era su presa habitual", "No tenía relación"),
    ("Spinosaurus", "¿Qué tenía en el lomo el Spinosaurus?", "Una vela ósea", "Placas acorazadas", "Una joroba de grasa"),
    ("Spinosaurus", "¿Dónde pasaba probablemente buena parte del tiempo?", "Nadando en busca de peces", "Bajo tierra", "En la copa de los árboles"),
    ("Giganotosaurus", "¿Cómo se compara su tamaño con el T-Rex?", "Era ligeramente más largo", "Era mucho más pequeño", "Eran idénticos"),
    ("Giganotosaurus", "¿Cómo cazaba presas grandes?", "En grupo", "Siempre en solitario", "Con trampas"),
    ("Brachiosaurus", "¿Qué característica tenían sus patas?", "Las delanteras eran más largas", "Las traseras eran más largas", "Todas iguales"),
    ("Brachiosaurus", "¿Qué altura podía alcanzar su cabeza?", "Más de 12 metros", "Apenas 2 metros", "Nunca se levantaba del suelo"),
    ("Iguanodon", "¿Qué tenía de particular su pulgar?", "Tenía forma de pico, usado como arma", "Era igual al resto de los dedos", "No tenía pulgar"),
    ("Iguanodon", "¿Qué importancia histórica tiene el Iguanodon?", "Fue de los primeros descritos científicamente", "Fue descubierto este siglo", "Nunca se halló un fósil completo"),
    ("Pachycephalosaurus", "¿Qué tenía de especial su cráneo?", "Era abovedado y muy grueso", "Era plano y frágil", "No tenía cráneo óseo"),
    ("Pachycephalosaurus", "¿Para qué se cree que usaba su cabeza?", "Para embestir como un carnero", "Para excavar túneles", "Para filtrar agua"),
    ("Carnotaurus", "¿Qué tenía sobre los ojos?", "Pequeños cuernos", "Una cresta de plumas", "Una placa transparente"),
    ("Carnotaurus", "¿Cómo eran sus brazos?", "Diminutos", "Extremadamente largos", "Con seis dedos"),
    ("Brontosaurus", "¿Con qué otro dinosaurio se lo confundió por años?", "Apatosaurus", "Triceratops", "Stegosaurus"),
    ("Brontosaurus", "¿Cuándo se restauró su nombre como especie válida?", "En 2015", "En 1850", "Nunca se restauró"),
    ("Therizinosaurus", "¿Qué tenía de extremadamente largo el Therizinosaurus?", "Sus garras", "Su cuello", "Sus dientes"),
    ("Therizinosaurus", "¿Qué tipo de dieta tenía, a pesar de ser un terópodo?", "Principalmente vegetal", "Exclusivamente carnívora", "Solo insectos"),
    ("Oviraptor", "¿De qué fue injustamente acusado durante años?", "De robar huevos ajenos", "De ser venenoso", "De no poder caminar"),
    ("Oviraptor", "¿De quién eran realmente los huevos que incubaba?", "Eran los suyos propios", "Eran de otra especie", "No incubaba huevos"),
    ("Deinonychus", "¿Qué tenía en cada pie?", "Una garra curva para atacar", "Una pezuña como un caballo", "Membranas para nadar"),
    ("Deinonychus", "¿Qué cambió su descubrimiento en la ciencia?", "La imagen de los dinosaurios como animales lentos", "Nada relevante", "Se descartó como dinosaurio"),
    ("Microraptor", "¿Cuántas alas emplumadas tenía?", "Cuatro", "Dos", "Ninguna"),
    ("Microraptor", "¿Cómo era el brillo de sus plumas?", "Iridiscente, como un cuervo", "Totalmente blanco", "Transparente"),
    ("Edmontosaurus", "¿Cómo era su pico?", "De pato", "Curvo como de loro", "No tenía pico"),
    ("Edmontosaurus", "¿Qué tenía en la boca?", "Cientos de dientes de repuesto", "Ningún diente", "Solo cuatro dientes"),
    ("Camarasaurus", "¿Cómo era su cuello comparado con otros saurópodos?", "Relativamente corto", "El más largo conocido", "No tenía cuello"),
    ("Camarasaurus", "¿Qué tenían de especial sus vértebras?", "Grandes cavidades huecas", "Eran macizas y pesadas", "Eran de cartílago"),
    ("Kentrosaurus", "¿De qué dinosaurio es pariente africano?", "Stegosaurus", "Triceratops", "Velociraptor"),
    ("Kentrosaurus", "¿Dónde tenía espinas defensivas además de la cola?", "Sobre los hombros", "En las patas delanteras", "En la cabeza"),
    ("Plateosaurus", "¿En qué período vivió?", "Triásico", "Cretácico", "Jurásico tardío"),
    ("Plateosaurus", "¿Qué sugiere el hallazgo de varios esqueletos juntos?", "Que viajaban en grupo", "Que vivían solos", "Que eran acuáticos"),
    ("Coelophysis", "¿Qué tenían de especial sus huesos?", "Eran huecos", "Eran macizos", "Eran de cartílago"),
    ("Coelophysis", "¿Cómo cazaba según la evidencia fósil?", "En grandes grupos", "Siempre en solitario", "Solo de noche"),
    ("Dilophosaurus", "¿Qué tenía sobre la cabeza?", "Dos crestas óseas paralelas", "Un cuerno único", "Una placa transparente"),
    ("Dilophosaurus", "¿Qué mostró el cine que no era real?", "Que escupía veneno", "Que tenía crestas", "Que era carnívoro"),
    ("Megalosaurus", "¿Qué logro histórico tiene el Megalosaurus?", "Fue el primer dinosaurio descrito científicamente", "Fue el último en descubrirse", "Nunca tuvo nombre científico"),
    ("Megalosaurus", "¿Qué significa su nombre?", "Lagarto grande", "Pequeño cazador", "Rey de las plumas"),
    ("Styracosaurus", "¿Qué tenía coronando su escudo craneal?", "Largas espinas", "Plumas coloridas", "Una vela ósea"),
    ("Styracosaurus", "¿Cuántas espinas largas podía tener en el escudo?", "Hasta seis", "Solo una", "Ninguna"),
]


def get_dino_map():
    with urllib.request.urlopen(f"{API_BASE}/dinos/") as r:
        dinos = json.loads(r.read())
    return {d["name"]: d["id"] for d in dinos}


def main():
    dino_map = get_dino_map()
    created, skipped = 0, 0

    for name, question, correct, wrong1, wrong2 in QUESTIONS:
        dino_id = dino_map.get(name)
        if not dino_id:
            print(f"⚠️  Saltando '{question[:40]}...' — no encontré el dinosaurio '{name}' (¿corriste el seed de dinos primero?)")
            skipped += 1
            continue

        payload = json.dumps({
            "dinosaur_id": dino_id,
            "question": question,
            "correct_answer": correct,
            "wrong_answer_1": wrong1,
            "wrong_answer_2": wrong2,
            "points": 10,
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
