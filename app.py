import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="LIM - Del reparto al algoritmo", layout="wide")

if "pasos" not in st.session_state:
    st.session_state.pasos = []
if "dividendo" not in st.session_state:
    st.session_state.dividendo = 3478
if "divisor" not in st.session_state:
    st.session_state.divisor = 24

st.markdown("""
<style>
.block-container{max-width:1180px;padding-top:1.2rem;padding-bottom:2rem}
[data-testid="stAppViewContainer"]{background:radial-gradient(circle at top left,#3a2412 0%,#111827 42%,#070b12 100%);color:#f8fafc}
[data-testid="stHeader"]{background:rgba(0,0,0,0)}
h1,h2,h3,p,li,span,div{color:#f8fafc}
.top{display:flex;align-items:center;border-bottom:1px solid rgba(148,163,184,.45);padding-bottom:14px;margin-bottom:24px}
.code{color:#f97316;font-weight:850;font-size:22px}.title{font-size:22px;margin-left:12px}
.step{font-size:30px;font-weight:850;margin-top:24px;margin-bottom:18px}
.info{border:1px solid rgba(249,115,22,.55);background:rgba(154,52,18,.28);border-radius:10px;padding:18px 22px;font-size:19px;margin:18px 0}
.ok{border:1px solid rgba(134,239,172,.55);background:rgba(22,101,52,.25);border-radius:10px;padding:16px 20px;font-size:18px;margin:16px 0}
.warn{border:1px solid rgba(252,165,165,.65);background:rgba(127,29,29,.35);border-radius:10px;padding:16px 20px;font-size:18px;margin:16px 0}
.num,.orange{color:#fb923c;font-weight:900}.green{color:#86efac;font-weight:900}.red{color:#fca5a5;font-weight:900}.blue{color:#93c5fd;font-weight:900}.yellow{color:#facc15;font-weight:900}
.panel{border:1px solid rgba(148,163,184,.35);background:rgba(15,23,42,.55);border-radius:12px;padding:20px;margin-top:18px}
.card{border:1px solid rgba(148,163,184,.38);background:rgba(2,6,23,.42);border-radius:10px;padding:14px;margin-bottom:12px}
.expr{font-size:23px;font-weight:800;line-height:1.5}.note{color:#cbd5e1;font-size:16px;font-style:italic;margin-top:8px}
.summary{display:grid;grid-template-columns:1fr .15fr 1fr .15fr 1fr;gap:14px;align-items:center;border:1px solid rgba(148,163,184,.35);background:rgba(15,23,42,.58);border-radius:12px;padding:18px;margin:18px 0}
.box{border-radius:10px;padding:12px;text-align:center;background:rgba(2,6,23,.36)}.b1{border:1px solid #fb923c}.b2{border:1px solid #86efac}.b3{border:1px solid #fca5a5}
.label{font-size:18px}.n{font-size:32px;font-weight:900}.op{font-size:30px;font-weight:900;text-align:center}
.alg{border:1px solid rgba(148,163,184,.4);background:rgba(2,6,23,.42);border-radius:12px;padding:22px;overflow-x:auto}
.alg-wrap{display:flex;gap:26px;align-items:flex-start;flex-wrap:wrap}
.alg-table{border-collapse:collapse;font-family:"Courier New",monospace;font-size:24px;color:#f8fafc}
.alg-table td{padding:4px 12px;text-align:right;white-space:nowrap}
.divisor{border-left:4px solid #f8fafc;border-bottom:4px solid #f8fafc;color:#93c5fd;font-weight:900;text-align:center!important}
.quot{color:#86efac;font-weight:900;text-align:center!important}.sub{color:#86efac;font-weight:900}.rem{color:#fca5a5;font-weight:900}
.alg-note{font-size:16px;color:#cbd5e1;line-height:1.5;max-width:430px}
</style>
""", unsafe_allow_html=True)

def step(n, txt):
    st.markdown(f"<div class='step'>{n}. {txt}</div>", unsafe_allow_html=True)

def leer_entero(texto, nombre, minimo=1):
    try:
        v = int(texto)
    except ValueError:
        st.error(f"{nombre} debe ser un número entero.")
        return None
    if v < minimo:
        st.error(f"{nombre} debe ser mayor o igual que {minimo}.")
        return None
    return v

def reiniciar():
    st.session_state.pasos = []

def deshacer():
    if st.session_state.pasos:
        st.session_state.pasos.pop()

def estado(dividendo, divisor):
    q = sum(st.session_state.pasos)
    repartido = divisor * q
    resto = dividendo - repartido
    return q, repartido, resto

def sugerencia(resto, divisor):
    if resto >= divisor * 1000: return 1000
    if resto >= divisor * 100: return 100
    if resto >= divisor * 10: return 10
    return 1

def registrar(decision, dividendo, divisor):
    q, rep, resto = estado(dividendo, divisor)
    prod = decision * divisor
    if prod > resto:
        st.warning(f"Con esa decisión no alcanza: necesitarías {prod} objetos y quedan {resto} por repartir.")
        return
    st.session_state.pasos.append(decision)

def resumen(dividendo, divisor, q, resto):
    st.markdown(f"""
    <div class="summary">
      <div class="box b1"><div class="label">Cantidad inicial</div><div class="n orange">{dividendo}</div></div>
      <div class="op">=</div>
      <div class="box b2"><div class="label">{divisor} × cociente parcial</div><div class="n green">{divisor} × {q}</div></div>
      <div class="op">+</div>
      <div class="box b3"><div class="label">Quedan por repartir</div><div class="n red">{resto}</div></div>
    </div>""", unsafe_allow_html=True)

def preview(decision, divisor, resto):
    if decision is None:
        return False

    # Si queda menos que la cantidad de grupos, el reparto entero ya terminó.
    # No corresponde decir "te pasás": eso que queda es el resto.
    if resto < divisor:
        st.markdown(f"""<div class="ok">
        Ya no alcanza para dar 1 objeto más a cada grupo.
        Quedan <span class="red"><b>{resto}</b></span> objetos: esa cantidad es el resto.
        </div>""", unsafe_allow_html=True)
        return False

    prod = decision * divisor

    if prod <= resto:
        nuevo = resto - prod
        st.markdown(f"""<div class="ok">
        Si das <span class="orange"><b>{decision}</b></span> más a cada grupo, usás
        <span class="green"><b>{divisor} × {decision} = {prod}</b></span> objetos.
        Después quedarían <span class="red"><b>{nuevo}</b></span> objetos por repartir.
        </div>""", unsafe_allow_html=True)
        return True

    exceso = prod - resto
    maximo = resto // divisor

    st.markdown(f"""<div class="warn">
    Con esa decisión no alcanza: <span class="red"><b>{divisor} × {decision} = {prod}</b></span>,
    pero quedan <span class="orange"><b>{resto}</b></span> objetos por repartir.
    Harían falta <span class="red"><b>{exceso}</b></span> objetos más.
    <br><br>
    Con lo que queda, como máximo podrías dar <span class="orange"><b>{maximo}</b></span> más a cada grupo.
    </div>""", unsafe_allow_html=True)
    return False

def historia(divisor):
    if not st.session_state.pasos:
        st.caption("Todavía no registraste decisiones de reparto.")
        return
    acum = 0
    for i, p in enumerate(st.session_state.pasos, start=1):
        acum += p
        st.markdown(f"""<div class="card">
        <div class="expr">Paso {i}: dar <span class="orange">{p}</span> más a cada grupo</div>
        <div>Se usan <span class="green">{divisor} × {p} = {divisor*p}</span> objetos.</div>
        <div class="note">Cociente parcial hasta acá: {acum}</div>
        </div>""", unsafe_allow_html=True)

def descomposicion(dividendo, divisor, resto):
    if not st.session_state.pasos: return
    productos = " + ".join(f"{divisor}×{p}" for p in st.session_state.pasos)
    suma = " + ".join(str(p) for p in st.session_state.pasos)
    q = sum(st.session_state.pasos)
    st.markdown("### Lo que fuimos construyendo")
    st.markdown(f"""<div class="panel">
    <div class="expr">{dividendo} = {productos} + {resto}</div>
    <div class="expr">{dividendo} = {divisor} × ({suma}) + {resto}</div>
    <div class="expr">{dividendo} = {divisor} × {q} + {resto}</div>
    </div>""", unsafe_allow_html=True)

def restas(dividendo, divisor):
    if not st.session_state.pasos: return
    st.markdown("### Las restas sucesivas que hicimos")
    st.write("Cada decisión de reparto puede verse como una resta. Al usar cantidades grandes, hacemos menos restas que si restáramos el divisor una y otra vez.")
    parcial = dividendo
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    for i, p in enumerate(st.session_state.pasos, start=1):
        prod = divisor * p
        nuevo = parcial - prod
        st.markdown(f"""<div class="card"><div class="expr">{parcial} − ({divisor} × {p}) = {nuevo}</div>
        <div class="note">En el paso {i}, en lugar de restar {divisor} muchas veces, restamos {prod} de una sola vez.</div></div>""", unsafe_allow_html=True)
        parcial = nuevo
    st.markdown('</div>', unsafe_allow_html=True)

def cuenta_escolar(dividendo, divisor, resto):
    if not st.session_state.pasos:
        return

    q = sum(st.session_state.pasos)
    suma = " + ".join(str(p) for p in st.session_state.pasos)
    parcial = dividendo

    rows = f"""
    <tr>
        <td class="num-left">{dividendo}</td>
        <td class="divisor-cell">{divisor}</td>
    </tr>
    <tr>
        <td></td>
        <td class="quotient-cell">{q}</td>
    </tr>
    """

    for p in st.session_state.pasos:
        prod = divisor * p
        nuevo = parcial - prod
        rows += f"""
        <tr>
            <td class="sub-cell">− {prod}</td>
            <td></td>
        </tr>
        <tr>
            <td class="result-cell">{nuevo}</td>
            <td></td>
        </tr>
        """
        parcial = nuevo

    altura = max(360, 170 + len(st.session_state.pasos) * 64)

    html = f"""
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            background: #020617;
            color: #f8fafc;
            font-family: Arial, sans-serif;
        }}
        .alg {{
            border: 1px solid rgba(148,163,184,.40);
            background: rgba(2,6,23,.42);
            border-radius: 12px;
            padding: 22px;
            overflow-x: auto;
        }}
        .wrap {{
            display: flex;
            gap: 34px;
            align-items: flex-start;
            flex-wrap: wrap;
        }}
        table {{
            border-collapse: collapse;
            font-family: "Courier New", monospace;
            font-size: 24px;
            color: #f8fafc;
        }}
        td {{
            padding: 4px 14px;
            text-align: right;
            white-space: nowrap;
        }}
        .num-left {{
            color: #fb923c;
            font-weight: 900;
        }}
        .divisor-cell {{
            border-left: 4px solid #f8fafc;
            border-bottom: 4px solid #f8fafc;
            color: #93c5fd;
            font-weight: 900;
            text-align: center;
        }}
        .quotient-cell {{
            color: #86efac;
            font-weight: 900;
            text-align: center;
        }}
        .sub-cell {{
            color: #86efac;
            font-weight: 900;
        }}
        .result-cell {{
            border-top: 2px solid #f8fafc;
            color: #f8fafc;
        }}
        .note {{
            font-size: 16px;
            color: #cbd5e1;
            line-height: 1.5;
            max-width: 430px;
        }}
        .yellow {{
            color: #facc15;
            font-weight: 900;
        }}
    </style>
    </head>
    <body>
        <div class="alg">
            <div class="wrap">
                <div>
                    <table>
                        {rows}
                    </table>
                </div>
                <div class="note">
                    <p><span class="yellow">Cociente construido:</span> {suma} = <b>{q}</b></p>
                    <p><span class="yellow">Resto:</span> {resto}</p>
                    <p>
                        Esta cuenta organiza de manera más económica las restas que ya hicimos durante el reparto.
                    </p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    st.markdown("### La misma estrategia en una cuenta de dividir")
    st.write(
        "La cuenta escolar puede verse como una forma de ubicar verticalmente las restas parciales. "
        "El cociente aparece como la suma de las decisiones tomadas."
    )
    components.html(html, height=altura, scrolling=True)


def economia(divisor):
    if not st.session_state.pasos: return
    q = sum(st.session_state.pasos)
    suma = " + ".join(str(p) for p in st.session_state.pasos)
    st.markdown("### Cómo se economiza la escritura")
    st.markdown(f"""<div class="panel">
    <div class="expr">Cociente construido: {suma} = <span class="orange">{q}</span></div>
    <div class="expr">En lugar de registrar varios repartos parciales, podemos reunirlos en uno solo:</div>
    <div class="expr"><span class="green">{divisor} × ({suma})</span> = <span class="green">{divisor} × {q}</span></div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="top"><span class="code">DE-02</span><span style="color:#94a3b8;margin-left:12px">|</span><span class="title">Del reparto al algoritmo</span></div>', unsafe_allow_html=True)
st.title("Del reparto al algoritmo")
st.subheader("Hacer cada vez más económico un reparto")
st.write("Exploramos cómo una división puede resolverse mediante decisiones sucesivas de reparto y cómo esas decisiones pueden escribirse de forma cada vez más económica.")
st.info("La idea no es empezar por el algoritmo convencional, sino construir una estrategia: decidir cuánto dar a cada grupo, mirar cuánto se repartió y cuánto queda por repartir.")
st.divider()

step(1, "Escribí una división para explorar")
col_a, col_b, col_c = st.columns([1.2, 1.2, .8])
with col_a:
    dividendo_txt = st.text_input("Cantidad total de objetos", value=str(st.session_state.dividendo))
with col_b:
    divisor_txt = st.text_input("Cantidad de grupos", value=str(st.session_state.divisor))
with col_c:
    st.write(""); st.write("")
    if st.button("Aplicar división", use_container_width=True):
        nd = leer_entero(dividendo_txt, "La cantidad total de objetos", 1)
        nv = leer_entero(divisor_txt, "La cantidad de grupos", 1)
        if nd is not None and nv is not None:
            st.session_state.dividendo = nd
            st.session_state.divisor = nv
            reiniciar()
            st.rerun()

dividendo = st.session_state.dividendo
divisor = st.session_state.divisor
q, repartido, resto = estado(dividendo, divisor)

st.markdown(f"""<div class="info">Queremos repartir <span class="num">{dividendo}</span> objetos en <span class="num">{divisor}</span> grupos.</div>""", unsafe_allow_html=True)

step(2, "Tomá una decisión de reparto")
st.write("Elegí cuántos objetos más querés dar a cada grupo en este paso.")
sug = sugerencia(resto, divisor)
col_d, col_r = st.columns([2,1])
with col_d:
    decision_txt = st.text_input("Dar esta cantidad más a cada grupo", value=str(sug))
decision = leer_entero(decision_txt, "La decisión de reparto", 1)
valida = preview(decision, divisor, resto)
with col_r:
    st.write(""); st.write("")
    if st.button("Registrar esta decisión", use_container_width=True, disabled=not valida):
        registrar(decision, dividendo, divisor)
        st.rerun()

c1, c2 = st.columns(2)
with c1:
    if st.button("Deshacer último paso", use_container_width=True):
        deshacer()
        st.rerun()
with c2:
    if st.button("Reiniciar estrategia", use_container_width=True):
        reiniciar()
        st.rerun()

q, repartido, resto = estado(dividendo, divisor)

step(3, "Miramos el estado del reparto")
resumen(dividendo, divisor, q, resto)
if resto >= divisor:
    st.markdown(f"""<div class="info">Todavía quedan <span class="num">{resto}</span> objetos por repartir. Como hay <span class="num">{divisor}</span> grupos, todavía podrías dar al menos 1 más a cada grupo.</div>""", unsafe_allow_html=True)
else:
    st.success(f"Ya no alcanza para dar 1 objeto más a cada grupo. El cociente es {q} y el resto es {resto}.")

step(4, "Tu historia de reparto")
with st.container(border=True):
    historia(divisor)

descomposicion(dividendo, divisor, resto)
restas(dividendo, divisor)
cuenta_escolar(dividendo, divisor, resto)
economia(divisor)

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
    st.info("El cociente se va construyendo como suma de decisiones. Por ejemplo, si diste 100, luego 40 y luego 4 a cada grupo, el cociente parcial es 100 + 40 + 4 = 144. El algoritmo convencional puede pensarse como una forma más económica de registrar estas decisiones.")

st.divider()
st.markdown("### Sobre este laboratorio")
st.markdown("**Del reparto al algoritmo** forma parte de **LIM (Laboratorio de Ideas Matemáticas)**.")
st.markdown("**Versión:** 0.7 (prototipo)")
