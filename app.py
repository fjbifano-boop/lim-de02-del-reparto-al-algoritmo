import streamlit as st

st.set_page_config(page_title="LIM - Del reparto al algoritmo", layout="wide")

if "pasos" not in st.session_state:
    st.session_state.pasos = []
if "dividendo_anterior" not in st.session_state:
    st.session_state.dividendo_anterior = 3478
if "divisor_anterior" not in st.session_state:
    st.session_state.divisor_anterior = 24

st.markdown('''
<style>
.block-container{max-width:1200px;padding-top:1.2rem;padding-bottom:2rem}
[data-testid="stAppViewContainer"]{background:radial-gradient(circle at top left,#3a2412 0%,#111827 42%,#070b12 100%);color:#f8fafc}
[data-testid="stHeader"]{background:rgba(0,0,0,0)}
h1,h2,h3,p,li,span,div{color:#f8fafc}
.top{display:flex;align-items:center;border-bottom:1px solid rgba(148,163,184,.45);padding-bottom:14px;margin-bottom:24px}
.code{color:#f97316;font-weight:850;font-size:22px}.title{font-size:22px;margin-left:12px}
.step{font-size:32px;font-weight:850;margin-top:24px;margin-bottom:18px}
.info{border:1px solid rgba(249,115,22,.55);background:rgba(154,52,18,.28);border-radius:10px;padding:18px 22px;font-size:19px;margin:18px 0}
.info .num{color:#fb923c;font-weight:900}
.panel{border:1px solid rgba(148,163,184,.35);background:rgba(15,23,42,.55);border-radius:12px;padding:20px;margin-top:18px}
.card{border:1px solid rgba(148,163,184,.38);background:rgba(2,6,23,.42);border-radius:10px;padding:14px;margin-bottom:12px}
.expr{font-size:24px;font-weight:800;line-height:1.5}.note{color:#cbd5e1;font-size:16px;font-style:italic;margin-top:8px}
.green{color:#86efac;font-weight:900}.orange{color:#fb923c;font-weight:900}.red{color:#fca5a5;font-weight:900}
.summary{display:grid;grid-template-columns:1fr .15fr 1fr .15fr 1fr;gap:14px;align-items:center;border:1px solid rgba(148,163,184,.35);background:rgba(15,23,42,.58);border-radius:12px;padding:18px;margin:18px 0}
.box{border-radius:10px;padding:12px;text-align:center;background:rgba(2,6,23,.36)}
.b1{border:1px solid #fb923c}.b2{border:1px solid #86efac}.b3{border:1px solid #fca5a5}
.label{font-size:18px}.n{font-size:34px;font-weight:900}.op{font-size:30px;font-weight:900;text-align:center}
</style>
''', unsafe_allow_html=True)

def reiniciar():
    st.session_state.pasos = []

def step(n, txt):
    st.markdown(f"<div class='step'>{n}. {txt}</div>", unsafe_allow_html=True)

def estado(dividendo, divisor):
    cociente = sum(st.session_state.pasos)
    repartido = divisor * cociente
    restante = dividendo - repartido
    return cociente, repartido, restante

def registrar(cantidad, divisor, restante):
    if cantidad <= 0:
        st.warning("La cantidad debe ser mayor que 0.")
        return
    producto = cantidad * divisor
    if producto > restante:
        st.warning(f"No alcanza para dar {cantidad} más a cada grupo: eso requeriría {producto} objetos y quedan {restante}.")
        return
    st.session_state.pasos.append(cantidad)

def deshacer():
    if st.session_state.pasos:
        st.session_state.pasos.pop()

def resumen(dividendo, divisor, cociente, restante):
    st.markdown(f'''
    <div class="summary">
      <div class="box b1"><div class="label">Objetos iniciales</div><div class="n orange">{dividendo}</div></div>
      <div class="op">=</div>
      <div class="box b2"><div class="label">{divisor} × cociente parcial</div><div class="n green">{divisor} × {cociente}</div></div>
      <div class="op">+</div>
      <div class="box b3"><div class="label">Quedan sin repartir</div><div class="n red">{restante}</div></div>
    </div>
    ''', unsafe_allow_html=True)

def historia(divisor):
    if not st.session_state.pasos:
        st.caption("Todavía no tomaste decisiones de reparto.")
        return
    acumulado = 0
    for i, p in enumerate(st.session_state.pasos, start=1):
        acumulado += p
        st.markdown(f'''
        <div class="card">
            <div class="expr">Paso {i}: dar <span class="orange">{p}</span> más a cada grupo</div>
            <div>Se usan <span class="green">{divisor} × {p} = {divisor*p}</span> objetos.</div>
            <div class="note">Cociente parcial hasta acá: {acumulado}</div>
        </div>
        ''', unsafe_allow_html=True)

def descomposicion(divisor, dividendo, restante):
    if not st.session_state.pasos:
        return
    partes = " + ".join([f"{divisor}×{p}" for p in st.session_state.pasos])
    suma = " + ".join(str(p) for p in st.session_state.pasos)
    cociente = sum(st.session_state.pasos)
    st.markdown("### Lo que fuimos construyendo")
    st.markdown(f'''
    <div class="panel">
        <div class="expr">{dividendo} = {partes} + {restante}</div>
        <div class="expr">{dividendo} = {divisor} × ({suma}) + {restante}</div>
        <div class="expr">{dividendo} = {divisor} × {cociente} + {restante}</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('<div class="top"><span class="code">DE-02</span><span style="color:#94a3b8;margin-left:12px">|</span><span class="title">Del reparto al algoritmo</span></div>', unsafe_allow_html=True)

st.title("Del reparto al algoritmo")
st.subheader("Hacer cada vez más económico un reparto")
st.write("Exploramos cómo una división puede resolverse mediante decisiones sucesivas de reparto y cómo esas decisiones pueden escribirse de forma cada vez más económica.")
st.info("La idea no es empezar por el algoritmo convencional, sino construir una estrategia: decidir cuánto dar a cada grupo, mirar cuánto se repartió y cuánto queda.")
st.divider()

step(1, "Elegí una división para explorar")
col_a, col_b = st.columns(2)
with col_a:
    dividendo = st.number_input("Cantidad total de objetos", min_value=1, max_value=99999, value=3478, step=1)
with col_b:
    divisor = st.number_input("Cantidad de grupos", min_value=1, max_value=999, value=24, step=1)

if dividendo != st.session_state.dividendo_anterior or divisor != st.session_state.divisor_anterior:
    st.session_state.dividendo_anterior = dividendo
    st.session_state.divisor_anterior = divisor
    reiniciar()

cociente, repartido, restante = estado(dividendo, divisor)

st.markdown(f'<div class="info">Queremos repartir <span class="num">{dividendo}</span> objetos en <span class="num">{divisor}</span> grupos.</div>', unsafe_allow_html=True)

step(2, "Tomá una decisión de reparto")
st.write("Elegí cuántos objetos más querés dar a cada grupo en este paso.")

col_dec, col_btn = st.columns([2, 1])
with col_dec:
    sugerido = 100 if restante >= divisor*100 else 10 if restante >= divisor*10 else 1
    decision = st.number_input("Dar esta cantidad más a cada grupo", min_value=1, max_value=9999, value=sugerido, step=1)
with col_btn:
    st.write("")
    st.write("")
    if st.button("Registrar esta decisión", use_container_width=True):
        registrar(decision, divisor, restante)
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

cociente, repartido, restante = estado(dividendo, divisor)

step(3, "Miramos el estado del reparto")
resumen(dividendo, divisor, cociente, restante)

if restante >= divisor:
    st.markdown(f'<div class="info">Todavía quedan <span class="num">{restante}</span> objetos. Como hay <span class="num">{divisor}</span> grupos, todavía podrías seguir repartiendo.</div>', unsafe_allow_html=True)
else:
    st.success(f"Ya no alcanza para dar 1 objeto más a cada grupo. El cociente es {cociente} y el resto es {restante}.")

step(4, "Tu historia de reparto")
with st.container(border=True):
    historia(divisor)

descomposicion(divisor, dividendo, restante)

step(5, "Para pensar la economía del procedimiento")
with st.container(border=True):
    st.markdown(
