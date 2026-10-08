import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO

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


# =========================================================
# CUENTA DE DIVIDIR
# =========================================================

def dibujar_cuenta(
    dividendo: int,
    divisor: int,
    cociente: int,
    producto: int,
    resto: int
) -> BytesIO:

    fig, ax = plt.subplots(figsize=(8, 4.6), dpi=150)

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")

    negro = "#111111"
    azul = "#0057D9"
    verde = "#137A2A"
    naranja = "#C45100"
    rojo = "#C00000"
    gris = "#DDDDDD"

    ax.add_patch(
        plt.Rectangle(
            (0.2, 0.2),
            9.6,
            6.6,
            linewidth=2,
            edgecolor=gris,
            facecolor="white"
        )
    )

    x_izq = 3.4
    x_der = 6.3

    ax.text(
        x_izq, 5.2,
        str(dividendo),
        fontsize=40,
        fontweight="bold",
        ha="center",
        va="center",
        color=naranja
    )

    ax.text(
        x_der, 5.2,
        str(divisor),
        fontsize=40,
        fontweight="bold",
        ha="center",
        va="center",
        color=azul
    )

    ax.plot(
        [4.8, 4.8],
        [2.0, 6.1],
        color=negro,
        linewidth=4
    )

    ax.plot(
        [4.8, 7.55],
        [4.4, 4.4],
        color=negro,
        linewidth=4
    )

    ax.text(
        x_der, 3.4,
        str(cociente),
        fontsize=40,
        fontweight="bold",
        ha="center",
        va="center",
        color=verde
    )

    ax.text(
        x_izq, 3.4,
        f"−{producto}",
        fontsize=34,
        fontweight="bold",
        ha="center",
        va="center",
        color=verde
    )

    ax.plot(
        [2.35, 4.35],
        [2.65, 2.65],
        color=negro,
        linewidth=3
    )

    ax.text(
        x_izq, 1.7,
        str(resto),
        fontsize=40,
        fontweight="bold",
        ha="center",
        va="center",
        color=rojo
    )

    ax.annotate(
        "Dividendo",
        xy=(x_izq - 0.45, 5.2),
        xytext=(0.85, 5.2),
        fontsize=16,
        fontweight="bold",
        color=naranja,
        arrowprops=dict(
            arrowstyle="->",
            lw=2.5,
            color=naranja
        ),
        ha="left",
        va="center"
    )

    ax.annotate(
        "Divisor",
        xy=(x_der + 0.25, 5.2),
        xytext=(7.85, 5.2),
        fontsize=16,
        fontweight="bold",
        color=azul,
        arrowprops=dict(
            arrowstyle="->",
            lw=2.5,
            color=azul
        ),
        ha="left",
        va="center"
    )

    ax.annotate(
        "Cociente",
        xy=(x_der + 0.25, 3.4),
        xytext=(7.85, 3.4),
        fontsize=16,
        fontweight="bold",
        color=verde,
        arrowprops=dict(
            arrowstyle="->",
            lw=2.5,
            color=verde
        ),
        ha="left",
        va="center"
    )

    ax.annotate(
        "Resto",
        xy=(x_izq + 0.20, 1.7),
        xytext=(4.75, 1.15),
        fontsize=16,
        fontweight="bold",
        color=rojo,
        arrowprops=dict(
            arrowstyle="->",
            lw=2.5,
            color=rojo
        ),
        ha="left",
        va="center"
    )

    ax.text(
        5,
        0.55,
        (
            f"Al repartir {dividendo} objetos en "
            f"{divisor} grupos iguales, quedan "
            f"{cociente} objetos en cada grupo y "
            f"quedan {resto} objetos sin repartir."
        ),
        fontsize=12,
        ha="center",
        va="center",
        color=negro
    )

    buffer = BytesIO()

    fig.savefig(
        buffer,
        format="png",
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close(fig)

    buffer.seek(0)

    return buffer


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
    f"<div class='main-expression'>{dividendo} ÷ {divisor}</div>",
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

            estado, producto_propuesto, nuevo_restante = analyze_partial(
                propuesta,
                divisor,
                restante
            )

            st.markdown(
                f"<div class='metric'>"
                f"{divisor} × {propuesta} = {producto_propuesto}"
                f"</div>",
                unsafe_allow_html=True
            )

            if estado == "possible":

                mensaje = (
                    "<div class='possible'>"
                    "<span class='green'>"
                    "La propuesta es posible."
                    "</span><br><br>"
                    f"Si incorporás <b>{propuesta}</b> "
                    f"al cociente parcial, se restarían "
                    f"<b>{producto_propuesto}</b> y quedarían "
                    f"<b>{nuevo_restante}</b>.<br><br>"
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
                    "</span><br><br>"
                    f"Quedan <b>{restante}</b> y el producto "
                    f"sería <b>{producto_propuesto}</b>.<br><br>"
                    f"Supera lo disponible en <b>{exceso}</b>."
                    "</div>"
                )

                st.markdown(
                    mensaje,
                    unsafe_allow_html=True
                )


# ---------------------------------------------------------
# 3. ESTRATEGIA REGISTRADA
# ---------------------------------------------------------

with p3:

    with st.container(border=True):

        st.markdown("### 3. Lo registrado")

        st.markdown(
            f"<div class='metric'>"
            f"<span class='orange'>{restante}</span>"
            f"</div>"
            f"<div style='text-align:center;color:#f8fafc'>"
            f"quedan por aproximar"
            f"</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            (
                "<div style='margin-top:18px;color:#f8fafc'>"
                "Cociente parcial acumulado: "
                f"<span class='green'>{cociente_acumulado}</span>"
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

        st.session_state.aproximaciones.append(propuesta)
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
            f"<b>Paso {i}</b><br><br>"
            "Cociente parcial: "
            f"<span class='orange'>{aproximacion}</span><br>"
            "Producto: "
            f"<span class='green'>"
            f"{divisor} × {aproximacion} = {producto_paso}"
            "</span><br>"
            "Quedan: "
            f"<span class='red'>{nuevo}</span>"
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
        "La cuenta de dividir organiza de otra manera "
        "las mismas cantidades y relaciones."
    )

    mostrar_cuenta = st.checkbox(
        "Mostrar la cuenta de dividir"
    )

    if mostrar_cuenta:

        # Resultado completo de la división
        cociente_final = dividendo // divisor
        resto_final = dividendo % divisor
        producto_final = divisor * cociente_final

        st.image(
            dibujar_cuenta(
                dividendo,
                divisor,
                cociente_final,
                producto_final,
                resto_final
            ),
            use_container_width=True
        )

        st.markdown(
            f"""
- **{dividendo}** es el **dividendo**.
- **{divisor}** es el **divisor**.
- **{cociente_final}** es el **cociente**.
- **{resto_final}** es el **resto**.
- **{producto_final}** es la cantidad representada por **{divisor} × {cociente_final}**.
"""
        )

        if st.session_state.aproximaciones:

            st.markdown("#### Compará las dos escrituras")

            st.markdown(
                f"""
Tu estrategia construyó hasta ahora:

**{expresion_cociente} = {cociente_acumulado}**

La cuenta de dividir muestra como cociente:

**{cociente_final}**

**¿Dónde pueden reconocerse en la cuenta las aproximaciones que fuiste realizando?**
"""
            )


# =========================================================
# PARA OBSERVAR
# =========================================================

st.markdown("### Para observar en esta versión")

st.markdown(
    """
- ¿Qué aproximaciones resultan útiles para avanzar?
- ¿Cómo se construye el cociente a partir de los cocientes parciales?
- ¿Qué cambia cuando se elige una aproximación mayor o menor?
- ¿Qué relación puede establecerse entre la estrategia construida y la cuenta de dividir?
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

st.caption("Versión 1.0")
