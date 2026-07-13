import streamlit as st

st.set_page_config(page_title="LIM - Aproximaciones en la división", layout="wide")

if "dividendo" not in st.session_state:
    st.session_state.dividendo = 25683
if "divisor" not in st.session_state:
    st.session_state.divisor = 23
if "aproximaciones" not in st.session_state:
    st.session_state.aproximaciones = []

st.markdown("""
<style>
.block-container{max-width:1150px;padding-top:1.2rem;padding-bottom:2rem}
[data-testid="stAppViewContainer"]{background:radial-gradient(circle at top left,#3a2412 0%,#111827 42%,#070b12 100%);color:#f8fafc}
[data-testid="stHeader"]{background:rgba(0,0,0,0)}
h1,h2,h3,p,li,span,div{color:#f8fafc}
.topbar{display:flex;align-items:center;border-bottom:1px solid rgba(148,163,184,.45);padding-bottom:14px;margin-bottom:24px}
.code{color:#f97316;font-weight:850;font-size:22px}.title{font-size:22px;margin-left:12px}
.panel{border:1px solid rgba(148,163,184,.35);background:rgba(15,23,42,.55);border-radius:12px;padding:20px;min-height:235px}
.panel-title{font-size:23px;font-weight:850;margin-bottom:16px}
.main-expression{font-size:34px;font-weight:900;text-align:center;margin:12px 0 22px 0}
.info{border:1px solid rgba(249,115,22,.55);background:rgba(154,52,18,.28);border-radius:10px;padding:16px 20px;font-size:18px;margin:14px 0}
.good{border:1px solid rgba(134,239,172,.55);background:rgba(22,101,52,.25);border-radius:10px;padding:16px 20px;font-size:18px}
.possible{border:1px solid rgba(250,204,21,.55);background:rgba(113,63,18,.28);border-radius:10px;padding:16px 20px;font-size:18px}
.excess{border:1px solid rgba(252,165,165,.65);background:rgba(127,29,29,.35);border-radius:10px;padding:16px 20px;font-size:18px}
.orange{color:#fb923c;font-weight:900}.green{color:#86efac;font-weight:900}.yellow{color:#facc15;font-weight:900}.red{color:#fca5a5;font-weight:900}
.metric{font-size:30px;font-weight:900;text-align:center}.small{color:#cbd5e1;font-size:15px}
.history-card{border:1px solid rgba(148,163,184,.35);background:rgba(2,6,23,.40);border-radius:10px;padding:14px;margin-bottom:10px}
</style>
""", unsafe_allow_html=True)

def reset_strategy():
    st.session_state.aproximaciones = []

def read_int(text, label):
    try:
        value = int(text)
    except ValueError:
        st.error(f"{label} debe ser un número entero.")
        return None
    if value <= 0:
        st.error(f"{label} debe ser mayor que 0.")
        return None
    return value

def current_state():
    quotient = sum(st.session_state.aproximaciones)
    used = st.session_state.divisor * quotient
    remaining = st.session_state.dividendo - used
    return quotient, used, remaining

def classify(partial, divisor, remaining):
    product = partial * divisor
    if product > remaining:
        return "excess", product, remaining - product
    new_remaining = remaining - product
    maximum = remaining // divisor
    if maximum > 0 and partial >= max(1, maximum // 2):
        return "good", product, new_remaining
    return "possible", product, new_remaining

st.markdown('<div class="topbar"><span class="code">DE-02</span><span style="color:#94a3b8;margin-left:12px">|</span><span class="title">Aproximaciones sucesivas en la división</span></div>', unsafe_allow_html=True)
st.title("Del reparto al algoritmo")
st.subheader("Probamos cocientes parciales para acercarnos al resultado")
st.write("Esta versión mínima permite probar una estrategia: elegir un cociente parcial, anticipar qué producto genera y decidir si conviene registrarlo.")

with st.container(border=True):
    st.markdown("### División a explorar")
    c1, c2, c3 = st.columns([1.2,1.2,.8])
    with c1:
        dividendo_txt = st.text_input("Dividendo", value=str(st.session_state.dividendo))
    with c2:
        divisor_txt = st.text_input("Divisor", value=str(st.session_state.divisor))
    with c3:
        st.write("")
        st.write("")
        if st.button("Aplicar", use_container_width=True):
            dividendo = read_int(dividendo_txt, "El dividendo")
            divisor = read_int(divisor_txt, "El divisor")
            if dividendo is not None and divisor is not None:
                st.session_state.dividendo = dividendo
                st.session_state.divisor = divisor
                reset_strategy()
                st.rerun()

dividendo = st.session_state.dividendo
divisor = st.session_state.divisor
cociente_acumulado, usado, restante = current_state()

st.markdown(f"<div class='main-expression'>{dividendo} ÷ {divisor}</div>", unsafe_allow_html=True)

p1, p2, p3 = st.columns(3)

with p1:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-title'>1. Probar una aproximación</div>", unsafe_allow_html=True)
    propuesta_txt = st.text_input("¿Qué cociente parcial querés probar?", value="1000", key="propuesta")
    propuesta = read_int(propuesta_txt, "El cociente parcial")
    st.markdown("<div class='small'>Todavía no se registra. Primero miramos qué produce.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with p2:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-title'>2. Analizar la aproximación</div>", unsafe_allow_html=True)
    estado = None
    producto = None
    nuevo_restante = None
    if propuesta is not None:
        estado, producto, nuevo_restante = classify(propuesta, divisor, restante)
        st.markdown(f"<div class='metric'>{divisor} × {propuesta} = {producto}</div>", unsafe_allow_html=True)
        if estado == "good":
            st.markdown(f"<div class='good'><span class='green'>Buena aproximación.</span><br>Quedarían <b>{nuevo_restante}</b>.</div>", unsafe_allow_html=True)
        elif estado == "possible":
            st.markdown(f"<div class='possible'><span class='yellow'>Es posible.</span><br>Quedarían <b>{nuevo_restante}</b>.<br><br>¿Podrías avanzar más con un cociente parcial mayor?</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='excess'><span class='red'>Ese producto supera lo que queda.</span><br>Quedan {restante} y el producto es {producto}.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with p3:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-title'>3. Estado de la estrategia</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric'><span class='orange'>{restante}</span></div><div style='text-align:center'>quedan por aproximar</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-top:18px'>Cociente parcial acumulado: <span class='green'>{cociente_acumulado}</span><br>Cantidad de aproximaciones: <span class='yellow'>{len(st.session_state.aproximaciones)}</span></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

c_accept, c_undo, c_reset = st.columns(3)
with c_accept:
    can_register = propuesta is not None and estado in {"good","possible"} and restante >= divisor
    if st.button("Registrar esta aproximación", use_container_width=True, disabled=not can_register):
        st.session_state.aproximaciones.append(propuesta)
        st.rerun()
with c_undo:
    if st.button("Deshacer última aproximación", use_container_width=True, disabled=not st.session_state.aproximaciones):
        st.session_state.aproximaciones.pop()
        st.rerun()
with c_reset:
    if st.button("Reiniciar estrategia", use_container_width=True, disabled=not st.session_state.aproximaciones):
        reset_strategy()
        st.rerun()

st.markdown("### Estrategia registrada")
if not st.session_state.aproximaciones:
    st.info("Todavía no registraste aproximaciones.")
else:
    parcial = dividendo
    acumulado = 0
    for i, aproximacion in enumerate(st.session_state.aproximaciones, start=1):
        producto = divisor * aproximacion
        nuevo = parcial - producto
        acumulado += aproximacion
        st.markdown(f"<div class='history-card'><b>Paso {i}</b><br>Cociente parcial: <span class='orange'>{aproximacion}</span><br>Producto: <span class='green'>{divisor} × {aproximacion} = {producto}</span><br>Quedan: <span class='red'>{nuevo}</span></div>", unsafe_allow_html=True)
        parcial = nuevo
    st.markdown(f"<div class='info'>Cociente construido hasta ahora: <span class='num'>{' + '.join(str(x) for x in st.session_state.aproximaciones)} = {acumulado}</span></div>", unsafe_allow_html=True)

if restante < divisor:
    st.success(f"La división terminó: cociente {cociente_acumulado} y resto {restante}.")

st.markdown("### Para observar en esta versión")
st.markdown("""
- ¿Resulta natural escribir un cociente parcial?
- ¿La anticipación ayuda a decidir antes de registrar?
- ¿La distinción entre aproximación posible, buena y excesiva aporta algo?
- ¿El historial permite seguir cómo se construye el cociente?
""")

st.divider()
st.markdown("**Versión:** 0.8-MVP")
