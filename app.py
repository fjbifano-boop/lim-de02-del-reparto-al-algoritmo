import streamlit as st

st.set_page_config(
    page_title="LIM - Del reparto al algoritmo",
    layout="wide"
)

# ============================================================
# DE-02 · Del reparto al algoritmo
# Primer prototipo reconstruido
# ============================================================

# -----------------------------
# Estado
# -----------------------------
if "pasos" not in st.session_state:
    st.session_state.pasos = []

if "dividendo" not in st.session_state:
    st.session_state.dividendo = 3478

if "divisor" not in st.session_state:
    st.session_state.divisor = 24


# -----------------------------
# Estilo
# -----------------------------
st.markdown("""
<style>
.block-container {
    max-width: 1180px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top left, #3a2412 0%, #111827 42%, #070b12 100%);
    color: #f8fafc;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

h1, h2, h3, p, li, span, div {
    color: #f8fafc;
}

.topbar {
    display:flex;
    align-items:center;
    border-bottom:1px solid rgba(148,163,184,.45);
    padding-bottom:14px;
    margin-bottom:24px;
}

.code {
    color:#f97316;
    font-weight:850;
    font-size:22px;
}

.title {
    font-size:22px;
    margin-left:12px;
}

.step {
    font-size:30px;
    font-weight:850;
    margin-top:24px;
    margin-bottom:18px;
}

.info {
    border:1px solid rgba(249,115,22,.55);
    background:rgba(154,52,18,.28);
    border-radius:10px;
    padding:18px 22px;
    font-size:19px;
    margin:18px 0;
}

.info .num {
    color:#fb923c;
    font-weight:900;
}

.panel {
    border:1px solid rgba(148,163,184,.35);
    background:rgba(15,23,42,.55);
    border-radius:12px;
    padding:20px;
    margin-top:18px;
}

.card {
    border:1px solid rgba(148,163,184,.38);
    background:rgba(2,6,23,.42);
    border-radius:10px;
    padding:14px;
    margin-bottom:12px;
}

.expr {
    font-size:23px;
    font-weight:800;
    line-height:1.5;
}

.note {
    color:#cbd5e1;
    font-size:16px;
    font-style:italic;
    margin-top:8px;
}

.orange { color:#fb923c; font-weight:900; }
.green { color:#86efac; font-weight:900; }
.red { color:#fca5a5; font-weight:900; }
.blue { color:#93c5fd; font-weight:900; }

.summary {
    display:grid;
    grid-template-columns:1fr .15fr 1fr .15fr 1fr;
    gap:14px;
    align-items:center;
    border:1px solid rgba(148,163,184,.35);
    background:rgba(15,23,42,.58);
    border-radius:12px;
    padding:18px;
    margin:18px 0;
}

.box {
    border-radius:10px;
    padding:12px;
    text-align:center;
    background:rgba(2,6,23,.36);
}

.b1 { border:1px solid #fb923c; }
.b2 { border:1px solid #86efac; }
.b3 { border:1px solid #fca5a5; }

.label { font-size:18px; }
.n { font-size:32px; font-weight:900; }
.op { font-size:30px; font-weight:900; text-align:center; }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Funciones
# -----------------------------
def reiniciar():
    st.session_state.pasos = []


def deshacer():
    if st.session_state.pasos:
        st.session_state.pasos.pop()


def step(numero: int, titulo: str):
    st.markdown(f"<div class='step'>{numero}. {titulo}</div>", unsafe_allow_html=True)


def estado_reparto(dividendo: int, divisor: int):
    cociente_parcial = sum(st.session_state.pasos)
    repartido = divisor * cociente_parcial
    restante = dividendo - repartido
    return cociente_parcial, repartido, restante



def leer_entero(texto: str, nombre: str, minimo: int = 1):
    try:
        valor = int(texto)
    except ValueError:
        st.error(f"{nombre} debe ser un número entero.")
        return None

    if valor < minimo:
        st.error(f"{nombre} debe ser mayor o igual que {minimo}.")
        return None

    return valor


def registrar_decision(cantidad: int, dividendo: int, divisor: int):
    cociente_parcial, repartido, restante = estado_reparto(dividendo, divisor)

    if cantidad <= 0:
        st.warning("La cantidad debe ser mayor que 0.")
        return

    producto = cantidad * divisor

    if producto > restante:
        st.warning(
            f"No alcanza para dar {cantidad} más a cada grupo: "
            f"eso requeriría {producto} objetos y quedan {restante}."
        )
        return

    st.session_state.pasos.append(cantidad)


def sugerencia(restante: int, divisor: int):
    if restante >= divisor * 1000:
        return 1000
    if restante >= divisor * 100:
        return 100
    if restante >= divisor * 10:
        return 10
    return 1


def render_resumen(dividendo: int, divisor: int, cociente: int, restante: int):
    st.markdown(f"""
    <div class="summary">
        <div class="box b1">
            <div class="label">Cantidad inicial</div>
            <div class="n orange">{dividendo}</div>
        </div>
        <div class="op">=</div>
        <div class="box b2">
            <div class="label">{divisor} × cociente parcial</div>
            <div class="n green">{divisor} × {cociente}</div>
        </div>
        <div class="op">+</div>
        <div class="box b3">
            <div class="label">Quedan sin repartir</div>
            <div class="n red">{restante}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_historia(divisor: int):
    if not st.session_state.pasos:
        st.caption("Todavía no registraste decisiones de reparto.")
        return

    acumulado = 0
    for i, paso in enumerate(st.session_state.pasos, start=1):
        acumulado += paso
        st.markdown(f"""
        <div class="card">
            <div class="expr">
                Paso {i}: dar <span class="orange">{paso}</span> más a cada grupo
            </div>
            <div>
                Se usan <span class="green">{divisor} × {paso} = {divisor * paso}</span> objetos.
            </div>
            <div class="note">
                Cociente parcial hasta acá: {acumulado}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_descomposicion(dividendo: int, divisor: int, restante: int):
    if not st.session_state.pasos:
        return

    productos = " + ".join([f"{divisor}×{p}" for p in st.session_state.pasos])
    suma_pasos = " + ".join([str(p) for p in st.session_state.pasos])
    cociente = sum(st.session_state.pasos)

    st.markdown("### Lo que fuimos construyendo")

    st.markdown(f"""
    <div class="panel">
        <div class="expr">{dividendo} = {productos} + {restante}</div>
        <div class="expr">{dividendo} = {divisor} × ({suma_pasos}) + {restante}</div>
        <div class="expr">{dividendo} = {divisor} × {cociente} + {restante}</div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------
# Interfaz
# -----------------------------
st.markdown(
    '<div class="topbar"><span class="code">DE-02</span><span style="color:#94a3b8;margin-left:12px">|</span><span class="title">Del reparto al algoritmo</span></div>',
    unsafe_allow_html=True
)

st.title("Del reparto al algoritmo")
st.subheader("Hacer cada vez más económico un reparto")

st.write(
    "Exploramos cómo una división puede resolverse mediante decisiones sucesivas de reparto "
    "y cómo esas decisiones pueden escribirse de forma cada vez más económica."
)

st.info(
    "La idea no es empezar por el algoritmo convencional, sino construir una estrategia: "
    "decidir cuánto dar a cada grupo, mirar cuánto se repartió y cuánto queda."
)

st.divider()

# Paso 1
step(1, "Escribí una división para explorar")

col_a, col_b, col_c = st.columns([1.2, 1.2, 0.8])

with col_a:
    dividendo_txt = st.text_input("Cantidad total de objetos", value=str(st.session_state.dividendo))

with col_b:
    divisor_txt = st.text_input("Cantidad de grupos", value=str(st.session_state.divisor))

with col_c:
    st.write("")
    st.write("")
    if st.button("Aplicar división", use_container_width=True):
        nuevo_dividendo = leer_entero(dividendo_txt, "La cantidad total de objetos", minimo=1)
        nuevo_divisor = leer_entero(divisor_txt, "La cantidad de grupos", minimo=1)
        if nuevo_dividendo is not None and nuevo_divisor is not None:
            st.session_state.dividendo = nuevo_dividendo
            st.session_state.divisor = nuevo_divisor
            reiniciar()
            st.rerun()

dividendo = st.session_state.dividendo
divisor = st.session_state.divisor

cociente, repartido, restante = estado_reparto(dividendo, divisor)

st.markdown(f"""
<div class="info">
    Queremos repartir <span class="num">{dividendo}</span> objetos en
    <span class="num">{divisor}</span> grupos.
</div>
""", unsafe_allow_html=True)

# Paso 2
step(2, "Tomá una decisión de reparto")

st.write("Elegí cuántos objetos más querés dar a cada grupo en este paso.")

sugerido = sugerencia(restante, divisor)

col_decision, col_registro = st.columns([2, 1])

with col_decision:
    decision_txt = st.text_input(
        "Dar esta cantidad más a cada grupo",
        value=str(sugerido)
    )

with col_registro:
    st.write("")
    st.write("")
    if st.button("Registrar esta decisión", use_container_width=True):
        decision = leer_entero(decision_txt, "La decisión de reparto", minimo=1)
        if decision is not None:
            registrar_decision(decision, dividendo, divisor)
            st.rerun()

col_undo, col_reset = st.columns(2)

with col_undo:
    if st.button("Deshacer último paso", use_container_width=True):
        deshacer()
        st.rerun()

with col_reset:
    if st.button("Reiniciar estrategia", use_container_width=True):
        reiniciar()
        st.rerun()

# Actualizar estado luego de posibles cambios
cociente, repartido, restante = estado_reparto(dividendo, divisor)

# Paso 3
step(3, "Miramos el estado del reparto")

render_resumen(dividendo, divisor, cociente, restante)

if restante >= divisor:
    st.markdown(f"""
    <div class="info">
        Todavía quedan <span class="num">{restante}</span> objetos.
        Como hay <span class="num">{divisor}</span> grupos, todavía podrías seguir repartiendo.
    </div>
    """, unsafe_allow_html=True)
else:
    st.success(
        f"Ya no alcanza para dar 1 objeto más a cada grupo. "
        f"El cociente es {cociente} y el resto es {restante}."
    )

# Paso 4
step(4, "Tu historia de reparto")

with st.container(border=True):
    render_historia(divisor)

render_descomposicion(dividendo, divisor, restante)

# Paso 5
step(5, "Para pensar la economía del procedimiento")

with st.container(border=True):
    st.markdown("""
1. ¿Cuántos pasos usaste para llegar al resultado?
2. ¿Qué pasaría si en lugar de varios pasos pequeños usaras uno más grande?
3. ¿Podrías juntar algunos pasos sin cambiar el resultado?
4. ¿Cómo se fue formando el cociente?
5. ¿Qué relación hay entre esta estrategia y la cuenta convencional de dividir?
""")

if st.checkbox("Mostrar una ayuda"):
    st.info(
        "El cociente se va construyendo como suma de decisiones. "
        "Por ejemplo, si diste 100, luego 40 y luego 4 a cada grupo, "
        "el cociente parcial es 100 + 40 + 4 = 144. "
        "El algoritmo convencional puede pensarse como una forma más económica de registrar estas decisiones."
    )

st.divider()

st.markdown("### Sobre este laboratorio")
st.markdown(
    "**Del reparto al algoritmo** forma parte de **LIM (Laboratorio de Ideas Matemáticas)**."
)
st.markdown("**Versión:** 0.3 (prototipo)")
