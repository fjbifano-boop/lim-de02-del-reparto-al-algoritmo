import streamlit as st

st.title("¿Cómo economizar una cuenta de dividir?")

st.subheader(
    "Exploramos distintas maneras de construir el cociente "
    "mediante aproximaciones sucesivas"
)

st.write(
    "Elegí cocientes parciales, observá qué producen y compará "
    "distintas estrategias. ¿Cómo podrías llegar al resultado "
    "utilizando menos pasos?"
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

    .history-card {
        border: 1px solid rgba(148,163,184,.35);
        background: rgba(2,6,23,.40);
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 10px;
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

    div.stButton > button {
        color: #111827 !important;
        font-weight: 700 !important;
    }

    div.stButton > button:disabled {
        color: #64748b !important;
        opacity: 0.70;
    }

    /* =====================================================
       CUENTA PROGRESIVA
       ===================================================== */

    .division-wrapper {
        display: flex;
        justify-content: center;
        margin: 25px 0;
    }

    .division-card {
        background: white;
        color: #111111;
        border: 2px solid #dddddd;
        border-radius: 12px;
        padding: 30px 38px;
        width: 100%;
        max-width: 780px;
    }

    .progressive-header {
        display: flex;
        justify-content: center;
        align-items: flex-start;
        margin: 5px auto 30px auto;
        font-size: 34px;
        font-weight: 900;
    }

    .progressive-dividend {
        color: #C45100;
        padding: 12px 28px;
        border-right: 4px solid #111111;
    }

    .progressive-right {
        min-width: 330px;
    }

    .progressive-divisor {
        color: #0057D9;
        padding: 12px 25px;
        border-bottom: 4px solid #111111;
    }

    .progressive-quotient {
        color: #137A2A;
        padding: 12px 25px;
        font-size: 25px;
    }

    .algorithm-body {
        max-width: 480px;
        margin: 0 auto;
    }

    .algorithm-step {
        margin-bottom: 22px;
        padding-bottom: 10px;
        border-bottom: 1px solid #e2e8f0;
    }

    .algorithm-step-title {
        color: #64748b;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .algorithm-operation {
        display: grid;
        grid-template-columns: 1fr;
        width: 220px;
        margin-left: 40px;
        text-align: right;
        font-size: 25px;
        font-weight: 800;
        color: #111827;
    }

    .algorithm-current {
        color: #111827;
    }

    .algorithm-minus {
        color: #137A2A;
    }

    .algorithm-line {
        display: block;
        border-top: 2px solid #111111;
        margin-top: 3px;
    }

    .algorithm-result {
        color: #C00000;
        padding-top: 4px;
    }

    .algorithm-finished {
        margin-top: 25px;
        padding: 14px;
        text-align: center;
        border-radius: 8px;
        background: #ecfdf5;
        color: #166534;
        font-size: 18px;
    }

    .algorithm-open {
        margin-top: 25px;
        padding: 14px;
        text-align: center;
        border-radius: 8px;
        background: #fff7ed;
        color: #9a3412;
        font-size: 17px;
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

    product = partial * divisor

    if product > remaining:
        return "excess", product, remaining - product

    new_remaining = remaining - product

    return "possible", product, new_remaining


def dibujar_cuenta_html(dividendo, divisor, aproximaciones):
    """
    Construye la cuenta progresivamente utilizando solamente
    las aproximaciones efectivamente registradas.
    """

    if not aproximaciones:

        return (
            "<div class='division-wrapper'>"
            "<div class='division-card'>"
            "<div style='text-align:center;color:#475569;font-size:17px;'>"
            "Todavía no hay aproximaciones registradas."
            "</div>"
            "</div>"
            "</div>"
        )

    restante_actual = dividendo
    cociente_acumulado = 0
    pasos_html = ""

    for i, aproximacion in enumerate(
        aproximaciones,
        start=1
    ):

        producto = divisor * aproximacion
        nuevo_restante = restante_actual - producto

        cociente_acumulado += aproximacion

        pasos_html += (
            "<div class='algorithm-step'>"

            f"<div class='algorithm-step-title'>"
            f"Paso {i} · cociente parcial {aproximacion}"
            f"</div>"

            "<div class='algorithm-operation'>"

            f"<span class='algorithm-current'>"
            f"{restante_actual}"
            f"</span>"

            f"<span class='algorithm-minus'>"
            f"− {producto}"
            f"</span>"

            "<span class='algorithm-line'></span>"

            f"<span class='algorithm-result'>"
            f"{nuevo_restante}"
            f"</span>"

            "</div>"

            "</div>"
        )

        restante_actual = nuevo_restante

    suma = " + ".join(
        str(x)
        for x in aproximaciones
    )

    if len(aproximaciones) > 1:
        cociente_html = (
            f"{suma} = {cociente_acumulado}"
        )
    else:
        cociente_html = suma

    if restante_actual < divisor:

        estado_html = (
            "<div class='algorithm-finished'>"
            "La estrategia llegó al final.<br>"
            f"Cociente: <b>{cociente_acumulado}</b>"
            " &nbsp;·&nbsp; "
            f"Resto: <b>{restante_actual}</b>"
            "</div>"
        )

    else:

        estado_html = (
            "<div class='algorithm-open'>"
            f"Todavía quedan <b>{restante_actual}</b>. "
            "La cuenta puede seguir construyéndose."
            "</div>"
        )

    return (
        "<div class='division-wrapper'>"

        "<div class='division-card'>"

        "<div class='progressive-header'>"

        f"<div class='progressive-dividend'>"
        f"{dividendo}"
        f"</div>"

        "<div class='progressive-right'>"

        f"<div class='progressive-divisor'>"
        f"{divisor}"
        f"</div>"

        f"<div class='progressive-quotient'>"
        f"{cociente_html}"
        f"</div>"

        "</div>"

        "</div>"

        "<div class='algorithm-body'>"
        f"{pasos_html}"
        "</div>"

        f"{estado_html}"

        "</div>"

        "</div>"
    )


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
    "Construimos el cociente mediante aproximaciones sucesivas"
)

st.write(
    "Elegí un cociente parcial, anticipá qué producto genera "
    "y decidí si querés incorporarlo a tu estrategia."
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
    f"<div class='main-expression'>"
    f"{dividendo} ÷ {divisor}"
    f"</div>",
    unsafe_allow_html=True
)


# =========================================================
# TRES MOMENTOS
# =========================================================

p1, p2, p3 = st.columns(3)


# ---------------------------------------------------------
# 1. PROPONER
# ---------------------------------------------------------

with p1:

    with st.container(border=True):

        st.markdown("### 1. Proponer")

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
            "Esta propuesta todavía no forma parte de la estrategia. "
            "Primero observá qué produciría."
        )


# ---------------------------------------------------------
# 2. ANTICIPAR
# ---------------------------------------------------------

with p2:

    with st.container(border=True):

        st.markdown("### 2. Anticipar")

        estado = None
        producto_propuesto = None
        nuevo_restante = None

        if propuesta is not None:

            (
                estado,
                producto_propuesto,
                nuevo_restante
            ) = analyze_partial(
                propuesta,
                divisor,
                restante
            )

            st.markdown(
                f"<div class='metric'>"
                f"{divisor} × {propuesta} "
                f"= {producto_propuesto}"
                f"</div>",
                unsafe_allow_html=True
            )

            if estado == "possible":

                mensaje = (
                    "<div class='possible'>"

                    "<span class='green'>"
                    "La propuesta es posible."
                    "</span>"

                    "<br><br>"

                    f"Si incorporás <b>{propuesta}</b> "
                    "al cociente parcial, se restarían "
                    f"<b>{producto_propuesto}</b> "
                    f"y quedarían <b>{nuevo_restante}</b>."

                    "<br><br>"

                    "Podés registrarla o probar otra."

                    "</div>"
                )

                st.markdown(
                    mensaje,
                    unsafe_allow_html=True
                )

            else:

                exceso = producto_propuesto - restante

                mensaje = (
                    "<div class='excess'>"

                    "<span class='red'>"
                    "Esta propuesta supera lo que queda."
                    "</span>"

                    "<br><br>"

                    f"Quedan <b>{restante}</b> "
                    f"y el producto sería "
                    f"<b>{producto_propuesto}</b>."

                    "<br><br>"

                    f"Supera lo disponible en "
                    f"<b>{exceso}</b>."

                    "</div>"
                )

                st.markdown(
                    mensaje,
                    unsafe_allow_html=True
                )


# ---------------------------------------------------------
# 3. LO REGISTRADO
# ---------------------------------------------------------

with p3:

    with st.container(border=True):

        st.markdown("### 3. Lo registrado")

        st.markdown(
            (
                "<div class='metric'>"
                f"<span class='orange'>{restante}</span>"
                "</div>"

                "<div style='text-align:center;color:#f8fafc'>"
                "quedan por aproximar"
                "</div>"
            ),
            unsafe_allow_html=True
        )

        st.markdown(
            (
                "<div style='margin-top:18px;color:#f8fafc'>"

                "Cociente parcial acumulado: "
                f"<span class='green'>"
                f"{cociente_acumulado}"
                "</span>"

                "<br><br>"

                "Aproximaciones registradas: "
                f"<span class='yellow'>"
                f"{len(st.session_state.aproximaciones)}"
                "</span>"

                "</div>"
            ),
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

st.markdown("### Estrategia construida")

if not st.session_state.aproximaciones:

    st.info(
        "Todavía no registraste aproximaciones."
    )

    expresion_cociente = ""

else:

    parcial = dividendo
    acumulado = 0

    for i, aproximacion in enumerate(
        st.session_state.aproximaciones,
        start=1
    ):

        producto_paso = divisor * aproximacion
        nuevo = parcial - producto_paso
        acumulado += aproximacion

        historial_html = (
            "<div class='history-card'>"

            f"<b>Paso {i}</b>"

            "<br><br>"

            "Cociente parcial: "
            f"<span class='orange'>"
            f"{aproximacion}"
            "</span>"

            "<br>"

            "Producto: "
            f"<span class='green'>"
            f"{divisor} × {aproximacion} "
            f"= {producto_paso}"
            "</span>"

            "<br>"

            "Quedan: "
            f"<span class='red'>"
            f"{nuevo}"
            "</span>"

            "</div>"
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
        "<div class='info'>"

        "Cociente construido hasta ahora: "

        "<span class='orange'>"
        f"{expresion_cociente} = {acumulado}"
        "</span>"

        "</div>"
    )

    st.markdown(
        resumen_html,
        unsafe_allow_html=True
    )


# =========================================================
# FINALIZACIÓN
# =========================================================

if restante < divisor:

    st.success(
        f"La estrategia llegó al final: "
        f"cociente {cociente_acumulado} "
        f"y resto {restante}."
    )


# =========================================================
# DEL PROCEDIMIENTO AL ALGORITMO
# =========================================================

st.markdown("### Del procedimiento al algoritmo")

with st.container(border=True):

    st.write(
        "Podés hacer visible la cuenta para observar cómo "
        "las aproximaciones que registraste van construyendo "
        "el procedimiento."
    )

    mostrar_cuenta = st.checkbox(
        "Mostrar la cuenta de dividir"
    )

    if mostrar_cuenta:

        cuenta_html = dibujar_cuenta_html(
            dividendo,
            divisor,
            st.session_state.aproximaciones
        )

        st.markdown(
            cuenta_html,
            unsafe_allow_html=True
        )

        if st.session_state.aproximaciones:

            st.markdown("#### Mirá las dos formas de registrar la estrategia")

            st.markdown(
                f"""
En el historial, el cociente parcial se construyó como:

**{expresion_cociente} = {cociente_acumulado}**

En la cuenta, cada una de esas aproximaciones aparece asociada
al producto que se resta y a una nueva cantidad pendiente.

**¿Qué relaciones encontrás entre las dos formas de registrar el procedimiento?**
"""
            )


# =========================================================
# PREGUNTAS
# =========================================================

st.markdown("### Para observar en esta versión")

st.markdown(
    """
- ¿Qué aproximaciones permiten avanzar?
- ¿Cómo se construye el cociente a partir de los cocientes parciales?
- ¿Qué cambia cuando elegís una aproximación mayor o menor?
- ¿Qué relaciones aparecen entre las aproximaciones, los productos que se restan y las cantidades que van quedando?
- ¿Cómo se relaciona la estrategia construida con la cuenta de dividir?
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

st.caption("Versión 1.2")
