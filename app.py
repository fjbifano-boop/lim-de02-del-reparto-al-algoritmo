import streamlit as st

st.set_page_config(
    page_title="LIM - Aproximaciones en la división",
    layout="wide"
)

# =========================================================
# ESTADO INICIAL
# =========================================================

if "dividendo" not in st.session_state:
    st.session_state.dividendo = 25683

if "divisor" not in st.session_state:
    st.session_state.divisor = 23

if "aproximaciones" not in st.session_state:
    st.session_state.aproximaciones = []


# =========================================================
# ESTILO
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1150px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(
                circle at top left,
                #3a2412 0%,
                #111827 42%,
                #070b12 100%
            );
        color: #f8fafc;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    h1, h2, h3, p, li {
        color: #f8fafc;
    }

    .topbar {
        display: flex;
        align-items: center;
        border-bottom: 1px solid rgba(148,163,184,.45);
        padding-bottom: 14px;
        margin-bottom: 24px;
    }

    .code {
        color: #f97316;
        font-weight: 850;
        font-size: 22px;
    }

    .title {
        color: #f8fafc;
        font-size: 22px;
        margin-left: 12px;
    }

    .main-expression {
        color: #f8fafc;
        font-size: 34px;
        font-weight: 900;
        text-align: center;
        margin: 12px 0 22px 0;
    }

    .metric {
        color: #f8fafc;
        font-size: 30px;
        font-weight: 900;
        text-align: center;
        margin-bottom: 18px;
    }

    .possible {
        border: 1px solid rgba(134,239,172,.55);
        background: rgba(22,101,52,.25);
        border-radius: 10px;
        padding: 16px 20px;
        font-size: 18px;
        color: #f8fafc;
    }

    .excess {
        border: 1px solid rgba(252,165,165,.65);
        background: rgba(127,29,29,.35);
        border-radius: 10px;
        padding: 16px 20px;
        font-size: 18px;
        color: #f8fafc;
    }

    .info {
        border: 1px solid rgba(249,115,22,.55);
        background: rgba(154,52,18,.28);
        border-radius: 10px;
        padding: 16px 20px;
        font-size: 18px;
        margin: 14px 0;
        color: #f8fafc;
    }

    .orange {
        color: #fb923c;
        font-weight: 900;
    }

    .green {
        color: #86efac;
        font-weight: 900;
    }

    .yellow {
        color: #facc15;
        font-weight: 900;
    }

    .red {
        color: #fca5a5;
        font-weight: 900;
    }

    .small {
        color: #cbd5e1;
        font-size: 15px;
    }

    .history-card {
        border: 1px solid rgba(148,163,184,.35);
        background: rgba(2,6,23,.40);
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 10px;
        color: #f8fafc;
    }

    /* Botones activos */
    div.stButton > button {
        color: #111827 !important;
        font-weight: 700 !important;
    }

    /* Botones deshabilitados */
    div.stButton > button:disabled {
        color: #64748b !important;
        opacity: 0.70;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FUNCIONES
# =========================================================

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


def analyze_partial(partial, divisor, remaining):
    """
    Analiza la aproximación sin valorar si es 'buena' o 'mala'.

    Devuelve:
    - possible: el producto no supera lo que queda.
    - excess: el producto supera lo que queda.
    """

    product = partial * divisor

    if product > remaining:
        return "excess", product, remaining - product

    new_remaining = remaining - product

    return "possible", product, new_remaining


# =========================================================
# ENCABEZADO
# =========================================================

st.markdown(
    """
    <div class="topbar">
        <span class="code">DE-02</span>
        <span style="color:#94a3b8;margin-left:12px">|</span>
        <span class="title">
            Aproximaciones sucesivas en la división
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("Del reparto al algoritmo")

st.subheader(
    "Probamos cocientes parciales para acercarnos al resultado"
)

st.write(
    "Esta versión permite construir una estrategia mediante "
    "aproximaciones sucesivas: elegir un cociente parcial, "
    "anticipar qué producto genera y decidir si conviene registrarlo."
)


# =========================================================
# DIVISIÓN A EXPLORAR
# =========================================================

with st.container(border=True):

    st.markdown("### División a explorar")

    c1, c2, c3 = st.columns([1.2, 1.2, .8])

    with c1:
        dividendo_txt = st.text_input(
            "Dividendo",
            value=str(st.session_state.dividendo)
        )

    with c2:
        divisor_txt = st.text_input(
            "Divisor",
            value=str(st.session_state.divisor)
        )

    with c3:
        st.write("")
        st.write("")

        if st.button(
            "Aplicar",
            use_container_width=True
        ):

            dividendo = read_int(
                dividendo_txt,
                "El dividendo"
            )

            divisor = read_int(
                divisor_txt,
                "El divisor"
            )

            if dividendo is not None and divisor is not None:

                st.session_state.dividendo = dividendo
                st.session_state.divisor = divisor

                reset_strategy()

                st.rerun()


# =========================================================
# ESTADO ACTUAL
# =========================================================

dividendo = st.session_state.dividendo
divisor = st.session_state.divisor

cociente_acumulado, usado, restante = current_state()

st.markdown(
    f"""
    <div class='main-expression'>
        {dividendo} ÷ {divisor}
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TRES MOMENTOS DE LA ESTRATEGIA
# =========================================================

p1, p2, p3 = st.columns(3)


# ---------------------------------------------------------
# 1. PROBAR
# ---------------------------------------------------------

with p1:

    with st.container(border=True):

        st.markdown("### 1. Probar una aproximación")

        propuesta_txt = st.text_input(
            "¿Qué cociente parcial querés probar?",
            value="1000",
            key="propuesta"
        )

        propuesta = read_int(
            propuesta_txt,
            "El cociente parcial"
        )

        st.caption(
            "Todavía no se registra. "
            "Primero miramos qué produce."
        )


# ---------------------------------------------------------
# 2. ANALIZAR
# ---------------------------------------------------------

with p2:

    with st.container(border=True):

        st.markdown("### 2. Analizar la aproximación")

        estado = None
        producto = None
        nuevo_restante = None

        if propuesta is not None:

            estado, producto, nuevo_restante = analyze_partial(
                propuesta,
                divisor,
                restante
            )

            st.markdown(
                f"""
                <div class='metric'>
                    {divisor} × {propuesta} = {producto}
                </div>
                """,
                unsafe_allow_html=True
            )

            if estado == "possible":

                st.markdown(
                    f"""
                    <div class='possible'>
                        <span class='green'>
                            Esta aproximación es posible.
                        </span>
                        <br><br>
                        Si la registrás, quedarían
                        <b>{nuevo_restante}</b>.
                        <br><br>
                        ¿Querés registrarla o probar otra?
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                exceso = producto - restante

                st.markdown(
                    f"""
                    <div class='excess'>
                        <span class='red'>
                            Esta aproximación supera
                            lo que queda.
                        </span>
                        <br><br>
                        Quedan <b>{restante}</b>
                        y el producto sería
                        <b>{producto}</b>.
                        <br><br>
                        El producto supera lo disponible
                        en <b>{exceso}</b>.
                        <br><br>
                        Probá con un cociente parcial menor.
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ---------------------------------------------------------
# 3. ESTADO DE LA ESTRATEGIA
# ---------------------------------------------------------

with p3:

    with st.container(border=True):

        st.markdown("### 3. Estado de la estrategia")

        st.markdown(
            f"""
            <div class='metric'>
                <span class='orange'>
                    {restante}
                </span>
            </div>

            <div style='text-align:center;color:#f8fafc'>
                quedan por aproximar
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style='margin-top:18px;color:#f8fafc'>
                Cociente parcial acumulado:
                <span class='green'>
                    {cociente_acumulado}
                </span>
                <br><br>
                Cantidad de aproximaciones:
                <span class='yellow'>
                    {len(st.session_state.aproximaciones)}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# ACCIONES
# =========================================================

c_accept, c_undo, c_reset = st.columns(3)

with c_accept:

    can_register = (
        propuesta is not None
        and estado == "possible"
        and restante >= divisor
    )

    if st.button(
        "Registrar esta aproximación",
        use_container_width=True,
        disabled=not can_register
    ):

        st.session_state.aproximaciones.append(
            propuesta
        )

        st.rerun()


with c_undo:

    if st.button(
        "Deshacer última aproximación",
        use_container_width=True,
        disabled=not st.session_state.aproximaciones
    ):

        st.session_state.aproximaciones.pop()

        st.rerun()


with c_reset:

    if st.button(
        "Reiniciar estrategia",
        use_container_width=True,
        disabled=not st.session_state.aproximaciones
    ):

        reset_strategy()

        st.rerun()


# =========================================================
# HISTORIAL
# =========================================================

st.markdown("### Estrategia registrada")

if not st.session_state.aproximaciones:

    st.info("Todavía no registraste aproximaciones.")

else:

    parcial = dividendo
    acumulado = 0

    for i, aproximacion in enumerate(
        st.session_state.aproximaciones,
        start=1
    ):

        producto = divisor * aproximacion
        nuevo = parcial - producto
        acumulado += aproximacion

        historial_html = (
            f"<div class='history-card'>"
            f"<b>Paso {i}</b><br><br>"
            f"Cociente parcial: "
            f"<span class='orange'>{aproximacion}</span><br>"
            f"Producto: "
            f"<span class='green'>{divisor} × {aproximacion} = {producto}</span><br>"
            f"Quedan: "
            f"<span class='red'>{nuevo}</span>"
            f"</div>"
        )

        st.markdown(
            historial_html,
            unsafe_allow_html=True
        )

        parcial = nuevo

    expresion_cociente = " + ".join(
        str(x)
        for x in st.session_state.aproximaciones
    )

    resumen_html = (
        f"<div class='info'>"
        f"Cociente construido hasta ahora: "
        f"<span class='orange'>"
        f"{expresion_cociente} = {acumulado}"
        f"</span>"
        f"</div>"
    )

    st.markdown(
        resumen_html,
        unsafe_allow_html=True
    )

# =========================================================
# CIERRE DE LA DIVISIÓN
# =========================================================

if restante < divisor:

    st.success(
        f"La división terminó: "
        f"cociente {cociente_acumulado} "
        f"y resto {restante}."
    )


# =========================================================
# PREGUNTAS PARA ANALIZAR EL PROTOTIPO
# =========================================================

st.markdown("### Para observar en esta versión")

st.markdown(
    """
    - ¿Resulta natural proponer un cociente parcial?
    - ¿La anticipación del producto ayuda a decidir antes de registrar?
    - ¿Conviene que el entorno valore la aproximación o solamente informe qué produce?
    - ¿El historial permite seguir cómo se va construyendo el cociente?
    """
)


# =========================================================
# CONTACTO
# =========================================================

st.divider()

st.markdown(
    """
    ### ¿Usaste este laboratorio?

    Si sos docente y estás pensando utilizar este laboratorio,
    o ya lo probaste con estudiantes, nos interesa conocer tu experiencia.

    📩 **Contacto:**  
    [fjbifano@ccpems.exactas.uba.ar](mailto:fjbifano@ccpems.exactas.uba.ar)
    """
)

st.caption(
    "Laboratorio de Ideas Matemáticas (LIM) · "
    "Instituto CeFIEC – FCEN – UBA"
)

st.caption("Versión 0.9")
