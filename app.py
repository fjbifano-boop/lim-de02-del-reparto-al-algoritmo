import html
import streamlit as st

st.set_page_config(page_title="LIM · ¿Cómo economizar una cuenta de dividir?", layout="wide")

# ---------------------------------------------------------
# Estado: los campos comienzan vacíos; no hay cuenta activa.
# ---------------------------------------------------------
for key, default in {
    "dividendo": None,
    "divisor": None,
    "aproximaciones": [],
    "entrada_dividendo": "",
    "entrada_divisor": "",
    "propuesta": "",
    "mostrar_cuenta": True,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.markdown("""
<style>
.block-container {max-width: 1160px; padding-top: 1.3rem; padding-bottom: 2.5rem;}
[data-testid="stAppViewContainer"] {background: radial-gradient(circle at top left,#352213 0%,#111827 43%,#070b12 100%);color:#f8fafc;}
[data-testid="stHeader"] {background:transparent;}
h1,h2,h3,p,li {color:#f8fafc;}
.topbar {border-bottom:1px solid #526074;padding-bottom:12px;margin-bottom:20px;color:#f8fafc;font-size:19px;}
.topbar b {color:#fb923c;}
.division-entry {max-width:690px;margin:8px auto 12px;}
.division-entry-labels {display:grid;grid-template-columns:55% 45%;color:#cbd5e1;text-align:center;font-weight:700;}
.st-key-division_editor [data-testid="stColumn"]:first-child {border-right:4px solid #f8fafc;padding-right:12px;}
.st-key-division_editor [data-testid="stColumn"]:nth-child(2) {padding-left:12px;}
.st-key-division_editor [data-testid="stColumn"]:nth-child(2) [data-testid="stTextInput"] {border-bottom:3px solid #f8fafc;padding-bottom:10px;}
/* En la entrada, los dos controles están en la disposición de la cuenta. */
[data-testid="stHorizontalBlock"] [data-testid="stTextInput"] input {font-size:21px; font-weight:750;}
div.stButton > button {background:#f97316 !important;color:#fff !important;border:2px solid #fdba74 !important;border-radius:10px !important;font-weight:800 !important;min-height:49px !important;box-shadow:0 4px 10px #0007 !important;cursor:pointer !important;}
div.stButton > button:hover {background:#c2410c !important;border-color:#ffedd5 !important;box-shadow:0 6px 15px #0009 !important;}
div.stButton > button:focus-visible {outline:3px solid #fef08a !important;outline-offset:3px;}
div.stButton > button:disabled {background:#334155 !important;color:#cbd5e1 !important;border:2px solid #64748b !important;box-shadow:none !important;cursor:not-allowed !important;opacity:.75 !important;}
div.stButton > button[kind="secondary"] {background:#f8fafc !important;color:#111827 !important;border-color:#cbd5e1 !important;}
div.stButton > button[kind="secondary"]:hover {background:#fed7aa !important;color:#111827 !important;}
div.stButton > button[kind="secondary"]:disabled {background:#334155 !important;color:#cbd5e1 !important;border-color:#64748b !important;}
.notice {border:1px solid #64748b;border-radius:10px;padding:15px;margin-top:12px;color:#f8fafc;background:#172033;}
.notice.good {border-color:#4ade80;background:#123529;}
.notice.bad {border-color:#fca5a5;background:#491d23;}
.metric {font-size:30px;font-weight:900;color:#fb923c;}
.history {padding:13px 16px;border:1px solid #64748b;border-radius:9px;margin:9px 0;color:#f8fafc;background:#131d30;}
.history strong {color:#86efac;}
.division-card {background:#fff;color:#111827;border:2px solid #cbd5e1;border-radius:12px;padding:26px 20px;max-width:790px;margin:16px auto;overflow-x:auto;}
.division-layout {display:grid;grid-template-columns:minmax(190px,1fr) minmax(200px,1fr);max-width:680px;margin:auto;align-items:start;}
.division-left {border-right:4px solid #111827;padding:10px 24px 8px 12px;text-align:right;min-width:0;}
.division-right {min-width:0;}
.division-divisor {border-bottom:4px solid #111827;padding:10px 16px 12px;color:#0057d9;font-size:32px;font-weight:900;}
.division-quotient {padding:13px 16px;color:#137a2a;font-size:22px;font-weight:800;overflow-wrap:anywhere;}
.division-dividend {color:#c45100;font-size:32px;font-weight:900;margin-bottom:16px;}
.calc-step {margin:0 0 16px auto;max-width:320px;text-align:right;border-bottom:1px solid #e2e8f0;padding-bottom:11px;}
.calc-step .step-label {font-size:12px;color:#64748b;text-align:left;font-weight:650;}
.calc-step .minus {font-size:23px;color:#137a2a;font-weight:850;}
.calc-step .remainder {border-top:2px solid #111827;padding-top:4px;font-size:24px;color:#c00000;font-weight:900;}
.calc-start {font-size:16px;color:#475569;text-align:center;padding:16px 4px;}
.calc-status {text-align:center;background:#fff7ed;color:#9a3412;padding:13px;border-radius:9px;margin:16px auto 0;max-width:680px;font-weight:700;}
.calc-status.done {background:#ecfdf5;color:#166534;}
</style>
""", unsafe_allow_html=True)


def current_state():
    total = sum(st.session_state.aproximaciones)
    return total, st.session_state.dividendo - st.session_state.divisor * total


def progressive_account(dividendo, divisor, approximations):
    remaining = dividendo
    quotient = 0
    steps = []
    for i, part in enumerate(approximations, 1):
        product = divisor * part
        next_remaining = remaining - product
        steps.append(
            '<div class="calc-step">'
            f'<div class="step-label">Paso {i} · cociente parcial {part}</div>'
            f'<div style="font-size:23px;font-weight:800">{remaining}</div>'
            f'<div class="minus">− {product}</div>'
            f'<div class="remainder">{next_remaining}</div>'
            '</div>'
        )
        remaining = next_remaining
        quotient += part
    quotient_text = ' + '.join(map(str, approximations))
    if len(approximations) > 1:
        quotient_text += f' = {quotient}'
    if not approximations:
        steps_html = '<div class="calc-start">La cuenta todavía no tiene aproximaciones registradas.</div>'
    else:
        steps_html = ''.join(steps)
    done = remaining < divisor
    status = (f'Cociente: {quotient} · Resto: {remaining}' if done else
              f'Quedan {remaining}. Podés seguir aproximando.')
    return (
        '<div class="division-card">'
        '<div class="division-layout">'
        '<div class="division-left">'
        f'<div class="division-dividend">{dividendo}</div>{steps_html}'
        '</div>'
        '<div class="division-right">'
        f'<div class="division-divisor">{divisor}</div>'
        f'<div class="division-quotient">{html.escape(quotient_text) if quotient_text else "Cociente por construir"}</div>'
        '</div></div>'
        f'<div class="calc-status {"done" if done else ""}">{status}</div>'
        '</div>'
    )


st.markdown('<div class="topbar"><b>DE-02</b> &nbsp;|&nbsp; Aproximaciones sucesivas en la división</div>', unsafe_allow_html=True)
st.title('¿Cómo economizar una cuenta de dividir?')
st.write('Explorá diferentes maneras de construir el cociente mediante aproximaciones sucesivas. ¿Cómo podrías resolver una misma división con menos pasos?')

# ---------------------------------------------------------
# Entrada de datos: representación de cuenta escolar.
# ---------------------------------------------------------
st.subheader('1. Elegí la división')
with st.container(border=True):
    st.caption('Escribí el dividendo y el divisor directamente en los dos espacios de la cuenta. Después pulsá «Iniciar nueva división».')
    left_margin, main, right_margin = st.columns([1, 4, 1])
    with main:
      with st.container(key="division_editor"):
        a, b = st.columns([1.05, 1], gap='small')
        with a:
            st.text_input('Dividendo', key='entrada_dividendo', placeholder='Escribí el dividendo')
        with b:
            st.text_input('Divisor', key='entrada_divisor', placeholder='Escribí el divisor')
            st.caption('──────────────  Cociente por construir')
        if st.button('Iniciar nueva división', type='primary', use_container_width=True):
            raw_a = st.session_state.entrada_dividendo.strip()
            raw_b = st.session_state.entrada_divisor.strip()
            if not raw_a.isdecimal() or not raw_b.isdecimal():
                st.error('Ingresá números enteros no negativos en ambos espacios.')
            elif int(raw_b) == 0:
                st.error('El divisor debe ser mayor que cero.')
            else:
                st.session_state.dividendo = int(raw_a)
                st.session_state.divisor = int(raw_b)
                st.session_state.aproximaciones = []
                st.session_state.propuesta = ''
                st.rerun()

if st.session_state.dividendo is None:
    st.info('Para comenzar, escribí una división y pulsá «Iniciar nueva división».')
    st.stop()

dividendo = st.session_state.dividendo
divisor = st.session_state.divisor
quotient, remaining = current_state()
finished = remaining < divisor
st.markdown(f'### División en curso: {dividendo} ÷ {divisor}')

# ---------------------------------------------------------
# Proponer, anticipar y registrar son momentos diferentes.
# ---------------------------------------------------------
st.subheader('2. Construí una estrategia')
p1, p2, p3 = st.columns(3)
with p1:
    with st.container(border=True):
        st.markdown('#### Proponer')
        st.text_input('¿Qué cociente parcial querés probar?', key='propuesta', placeholder='Por ejemplo, 100')
        st.caption('Es una propuesta: todavía no modifica la cuenta.')

raw_proposal = st.session_state.propuesta.strip()
proposal = int(raw_proposal) if raw_proposal.isdecimal() else None
if proposal is not None and proposal <= 0:
    proposal = None
product = divisor * proposal if proposal is not None else None
possible = proposal is not None and product <= remaining

with p2:
    with st.container(border=True):
        st.markdown('#### Anticipar')
        if finished:
            st.success('La división ya está terminada.')
        elif not raw_proposal:
            st.write('Ingresá un cociente parcial para observar qué produciría.')
        elif proposal is None:
            st.warning('La aproximación debe ser un entero mayor que cero.')
        elif possible:
            st.markdown(f'<div class="notice good"><b>{divisor} × {proposal} = {product}</b><br>Si la registrás, quedarán <b>{remaining - product}</b>. Podés registrarla o probar otra.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="notice bad"><b>{divisor} × {proposal} = {product}</b><br>Supera lo que queda ({remaining}) en <b>{product - remaining}</b>.</div>', unsafe_allow_html=True)

with p3:
    with st.container(border=True):
        st.markdown('#### Lo registrado')
        st.markdown(f'<div class="metric">{remaining}</div>', unsafe_allow_html=True)
        st.caption('Cantidad que queda por dividir')
        st.write(f'Cociente parcial acumulado: **{quotient}**')
        st.write(f'Aproximaciones registradas: **{len(st.session_state.aproximaciones)}**')

c1, c2, c3 = st.columns(3)
with c1:
    if st.button('Registrar esta aproximación', type='primary', use_container_width=True,
                 disabled=finished or not possible):
        st.session_state.aproximaciones.append(proposal)
        st.session_state.propuesta = ''
        st.rerun()
with c2:
    if st.button('Deshacer última aproximación', type='secondary', use_container_width=True,
                 disabled=not st.session_state.aproximaciones):
        st.session_state.aproximaciones.pop()
        st.rerun()
with c3:
    if st.button('Reiniciar estrategia', type='secondary', use_container_width=True,
                 disabled=not st.session_state.aproximaciones):
        st.session_state.aproximaciones = []
        st.session_state.propuesta = ''
        st.rerun()

# ---------------------------------------------------------
# La misma cuenta elegida al inicio se construye por pasos.
# ---------------------------------------------------------
st.subheader('3. La cuenta que vas construyendo')
with st.container(border=True):
    st.checkbox('Mostrar la cuenta de dividir', key='mostrar_cuenta')
    if st.session_state.mostrar_cuenta:
        st.markdown(progressive_account(dividendo, divisor, st.session_state.aproximaciones),
                    unsafe_allow_html=True)

st.subheader('4. Estrategia construida')
if not st.session_state.aproximaciones:
    st.info('Todavía no registraste aproximaciones.')
else:
    pending = dividendo
    for i, part in enumerate(st.session_state.aproximaciones, 1):
        prod = divisor * part
        pending -= prod
        st.markdown(f'<div class="history"><b>Paso {i}</b> · Cociente parcial: <strong>{part}</strong> · Producto: {divisor} × {part} = {prod} · Quedan: <strong>{pending}</strong></div>', unsafe_allow_html=True)
    expression = ' + '.join(map(str, st.session_state.aproximaciones))
    st.markdown(f'<div class="notice">Cociente construido: <b>{expression} = {quotient}</b></div>', unsafe_allow_html=True)

if finished:
    st.success(f'La estrategia llegó al final: cociente {quotient} y resto {remaining}.')

st.subheader('Para seguir explorando')
st.markdown('''
- ¿Podrías llegar al mismo cociente con otras aproximaciones?
- ¿Qué hace que una estrategia necesite más o menos pasos?
- ¿Cómo podrías modificar tu estrategia para economizar la cuenta?
- ¿Qué relaciones entre los números permiten elegir aproximaciones mayores sin pasarse?
- ¿Qué se mantiene y qué cambia entre distintas estrategias para una misma división?
''')

st.divider()
st.markdown('**¿Usaste este laboratorio?** Si sos docente y estás pensando utilizarlo o ya lo probaste con estudiantes, nos interesa conocer tu experiencia. [Contacto: fjbifano@ccpems.exactas.uba.ar](mailto:fjbifano@ccpems.exactas.uba.ar)')
st.caption('Laboratorio de Ideas Matemáticas (LIM) · Instituto CeFIEC – FCEN – UBA · Versión 1.4')
