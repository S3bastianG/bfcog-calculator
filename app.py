import math
import streamlit as st

from engine.calculator import (
    calculate_cs_trade,
    calculate_minimum_back_stake,
)

from engine.betfair_ladder import (
    BETFAIR_LADDER,
    next_tick,
    previous_tick,
)


# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="Draw → CS Calculator",
    page_icon="⚽",
    layout="centered",
)


# ==================================================
# CSS
# ==================================================

st.markdown(
    """
    <style>

    /* ==================================================
       GLOBAL
       ================================================== */

    .block-container {
        width: 100%;
        max-width: 1450px;
        margin: 0 auto;
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }


    /* ==================================================
       TITOLI
       ================================================== */

    h1 {
        font-size: clamp(2rem, 2.5vw, 3rem) !important;
        line-height: 1.1 !important;
        margin-top: 0 !important;
        margin-bottom: 0.35rem !important;
    }

    h2 {
        font-size: clamp(1.45rem, 1.7vw, 1.8rem) !important;
        line-height: 1.2 !important;
        margin-top: 0.7rem !important;
        margin-bottom: 1rem !important;
    }

    h3 {
        font-size: 1.2rem !important;
        margin-top: 0.4rem !important;
        margin-bottom: 0.5rem !important;
    }


    /* ==================================================
       LABEL INPUT PERSONALIZZATE
       ================================================== */

    .custom-input-label {
        font-size: 1rem;
        font-weight: 700;
        line-height: 1.2;
        margin-top: 0.1rem;
        margin-bottom: 0.55rem;
        color: rgba(250, 250, 250, 0.95);
    }


    /* ==================================================
       RIMUOVE LABEL NATIVE STREAMLIT
       ================================================== */

    [data-testid="stTextInput"] label {
        display: none !important;
    }


    /* ==================================================
       RIMUOVE DECORAZIONI / LINK
       ================================================== */

    .custom-input-label a,
    .custom-input-label svg,
    .custom-input-label button {
        display: none !important;
    }

    [data-testid="stMetricLabel"] a,
    [data-testid="stMetricLabel"] svg,
    [data-testid="stMetricLabel"] button {
        display: none !important;
    }

    [data-testid="stMetricLabel"] {
        text-decoration: none !important;
    }


    /* ==================================================
       INPUT
       ================================================== */

    [data-testid="stTextInput"] {
        width: 100% !important;
        margin-bottom: 0 !important;
    }

    [data-testid="stTextInput"] input {
        width: 100% !important;
        min-height: 2.55rem;
        height: 2.55rem;
        font-size: 1rem;
        padding: 0.3rem 0.65rem;
        box-sizing: border-box;
    }


    /* ==================================================
       SPAZIATURA GENERALE
       ================================================== */

    [data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }


    /* ==================================================
       CONTROLLI STAKE + QUOTE
       
       IMPORTANTE:
       usiamo le classi .st-key-quote-controls-...
       direttamente invece di [class^="..."].
       ================================================== */

    .st-key-stake-controls,
    .st-key-quote-controls-back_odds,
    .st-key-quote-controls-odds_02,
    .st-key-quote-controls-odds_12 {
        width: 100% !important;
        margin-top: 0.15rem;
        margin-bottom: 0.7rem;
    }


    /* ==================================================
       RIGA DEI CONTROLLI
       ================================================== */

    .st-key-stake-controls [data-testid="stHorizontalBlock"],
    .st-key-quote-controls-back_odds [data-testid="stHorizontalBlock"],
    .st-key-quote-controls-odds_02 [data-testid="stHorizontalBlock"],
    .st-key-quote-controls-odds_12 [data-testid="stHorizontalBlock"] {

        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;

        width: 100% !important;
        min-width: 0 !important;

        gap: 0.4rem !important;
    }


    /* ==================================================
       COLONNA FRECCIA SINISTRA
       ================================================== */

    .st-key-stake-controls
    [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"]:first-child,

    .st-key-quote-controls-back_odds
    [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"]:first-child,

    .st-key-quote-controls-odds_02
    [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"]:first-child,

    .st-key-quote-controls-odds_12
    [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"]:first-child {

        flex: 0 0 2.3rem !important;
        width: 2.3rem !important;
        min-width: 2.3rem !important;
        max-width: 2.3rem !important;
    }


    /* ==================================================
       COLONNA INPUT CENTRALE
       ================================================== */

    .st-key-stake-controls
    [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"]:nth-child(2),

    .st-key-quote-controls-back_odds
    [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"]:nth-child(2),

    .st-key-quote-controls-odds_02
    [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"]:nth-child(2),

    .st-key-quote-controls-odds_12
    [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"]:nth-child(2) {

        flex: 1 1 0 !important;
        width: auto !important;
        min-width: 0 !important;
        max-width: none !important;
    }


    /* ==================================================
       COLONNA FRECCIA DESTRA
       ================================================== */

    .st-key-stake-controls
    [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"]:last-child,

    .st-key-quote-controls-back_odds
    [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"]:last-child,

    .st-key-quote-controls-odds_02
    [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"]:last-child,

    .st-key-quote-controls-odds_12
    [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"]:last-child {

        flex: 0 0 2.3rem !important;
        width: 2.3rem !important;
        min-width: 2.3rem !important;
        max-width: 2.3rem !important;
    }


    /* ==================================================
       CONTENUTO COLONNE
       ================================================== */

    .st-key-stake-controls
    [data-testid="stColumn"],
    .st-key-quote-controls-back_odds
    [data-testid="stColumn"],
    .st-key-quote-controls-odds_02
    [data-testid="stColumn"],
    .st-key-quote-controls-odds_12
    [data-testid="stColumn"] {

        min-width: 0 !important;
    }


    /* ==================================================
       INPUT CENTRALI
       ================================================== */

    .st-key-stake-controls
    [data-testid="stTextInput"],
    .st-key-quote-controls-back_odds
    [data-testid="stTextInput"],
    .st-key-quote-controls-odds_02
    [data-testid="stTextInput"],
    .st-key-quote-controls-odds_12
    [data-testid="stTextInput"] {

        width: 100% !important;
    }


    /* ==================================================
       PULSANTI FRECCIA
       ================================================== */

    .st-key-stake-controls [data-testid="stButton"],
    .st-key-quote-controls-back_odds [data-testid="stButton"],
    .st-key-quote-controls-odds_02 [data-testid="stButton"],
    .st-key-quote-controls-odds_12 [data-testid="stButton"] {

        width: 100% !important;
        margin: 0 !important;
    }

    .st-key-stake-controls [data-testid="stButton"] button,
    .st-key-quote-controls-back_odds [data-testid="stButton"] button,
    .st-key-quote-controls-odds_02 [data-testid="stButton"] button,
    .st-key-quote-controls-odds_12 [data-testid="stButton"] button {

        min-height: 2.55rem !important;
        height: 2.55rem !important;

        width: 100% !important;

        padding: 0 !important;
        margin: 0 !important;

        font-size: 0.72rem !important;
        line-height: 1 !important;
    }


    /* ==================================================
       FAVORITA TRASFERTA
       ================================================== */

    .st-key-favorite-away-box {
        margin-top: 0.1rem;
        margin-bottom: 0.75rem;
        padding: 0.75rem 0.9rem;
        border-radius: 0.6rem;
        border: 1px solid rgba(255, 255, 255, 0.14);
        background: rgba(255, 255, 255, 0.035);
    }

    .st-key-favorite-away-box [data-testid="stCheckbox"] {
        margin: 0 !important;
        padding: 0 !important;
    }

    .st-key-favorite-away-box [data-testid="stCheckbox"] label {
        display: flex !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }

    .st-key-favorite-away-box [data-testid="stCheckbox"] p {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }


    /* ==================================================
       CALCOLA
       ================================================== */

    button[kind="primary"] {
        min-height: 2.8rem;
        height: 2.8rem;
        margin-top: 0.15rem;
        font-size: 1rem;
        font-weight: 700;
    }


    /* ==================================================
       METRICS
       ================================================== */

    [data-testid="stMetric"] {
        padding: 0;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.8rem;
        line-height: 1.2;
        text-decoration: none !important;
    }

    [data-testid="stMetricValue"] {
        font-size: clamp(1.45rem, 2vw, 2rem);
        line-height: 1.15;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.78rem;
    }


    /* ==================================================
       FREEBET
       ================================================== */

    .result-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.62);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.05rem;
    }

    .freebet-value {
        font-size: clamp(2.1rem, 3vw, 3rem);
        font-weight: 700;
        line-height: 1.05;
        margin-bottom: 0.9rem;
    }


    /* ==================================================
       STATUS
       ================================================== */

    .status-box {
        padding: 0.72rem 0.8rem;
        border-radius: 0.55rem;
        font-size: 0.95rem;
        font-weight: 700;
        text-align: center;
        margin: 0.65rem 0 0.55rem 0;
    }

    .status-error {
        background: rgba(255, 70, 70, 0.12);
        border: 1px solid rgba(255, 70, 70, 0.35);
        color: #ff6b6b;
    }


    /* ==================================================
       COME RENDERE ESEGUIBILE
       ================================================== */

    .st-key-minimum-section {
        margin-top: 0.85rem;
        margin-bottom: 0.9rem;
        padding: 0.9rem;
        border-radius: 0.65rem;
        border: 1px solid rgba(255, 180, 0, 0.28);
        background: rgba(255, 180, 0, 0.055);
    }

    .minimum-title {
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.65rem;
    }


    /* ==================================================
       EXPANDER
       ================================================== */

    [data-testid="stExpander"] {
        margin-top: 0.35rem;
        margin-bottom: 0.35rem;
    }

    [data-testid="stExpander"] details summary {
        padding-top: 0.65rem;
        padding-bottom: 0.65rem;
    }


    /* ==================================================
       ALERT
       ================================================== */

    [data-testid="stAlert"] {
        padding-top: 0.65rem;
        padding-bottom: 0.65rem;
    }


    /* ==================================================
       GRANDI SCHERMI
       ================================================== */

    @media (min-width: 1200px) {

        .block-container {
            max-width: 1450px;
            padding-left: 4rem;
            padding-right: 4rem;
            padding-top: 2.5rem;
        }

        .custom-input-label {
            font-size: 1.05rem;
            margin-bottom: 1rem;
        }

        [data-testid="stTextInput"] input {
            min-height: 2.8rem;
            height: 2.8rem;
        }

        .st-key-stake-controls [data-testid="stButton"] button,
        .st-key-quote-controls-back_odds [data-testid="stButton"] button,
        .st-key-quote-controls-odds_02 [data-testid="stButton"] button,
        .st-key-quote-controls-odds_12 [data-testid="stButton"] button {

            min-height: 2.8rem !important;
            height: 2.8rem !important;
        }

        .st-key-favorite-away-box [data-testid="stCheckbox"] label,
        .st-key-favorite-away-box [data-testid="stCheckbox"] p {
            font-size: 1.1rem !important;
        }
    }


    /* ==================================================
       GRANDI SCHERMI 1600+
       ================================================== */

    @media (min-width: 1600px) {

        .block-container {
            max-width: 1600px;
            padding-left: 5rem;
            padding-right: 5rem;
            padding-top: 3rem;
        }

        h1 {
            font-size: 3rem !important;
        }

        h2 {
            font-size: 1.8rem !important;
        }

        .custom-input-label {
            font-size: 1.08rem;
            margin-bottom: 1rem;
        }

        [data-testid="stTextInput"] input {
            min-height: 3rem;
            height: 3rem;
            font-size: 1.05rem;
        }

        .st-key-stake-controls [data-testid="stButton"] button,
        .st-key-quote-controls-back_odds [data-testid="stButton"] button,
        .st-key-quote-controls-odds_02 [data-testid="stButton"] button,
        .st-key-quote-controls-odds_12 [data-testid="stButton"] button {

            min-height: 3rem !important;
            height: 3rem !important;
        }

        .st-key-favorite-away-box {
            padding: 0.9rem 1rem;
        }

        .st-key-favorite-away-box [data-testid="stCheckbox"] label,
        .st-key-favorite-away-box [data-testid="stCheckbox"] p {
            font-size: 1.15rem !important;
        }

        .freebet-value {
            font-size: 3.1rem;
        }

        [data-testid="stMetricValue"] {
            font-size: 2.05rem;
        }
    }


    /* ==================================================
       SCHERMI MOLTO GRANDI
       ================================================== */

    @media (min-width: 2000px) {

        .block-container {
            max-width: 1750px;
            padding-left: 6rem;
            padding-right: 6rem;
        }
    }


    /* ==================================================
       MOBILE
       ================================================== */

    @media (max-width: 768px) {

        [data-testid="stHorizontalBlock"] {
            gap: 0.5rem !important;
        }
        
        h3 {
            text-align: center !important;
        }

        .block-container {
            max-width: 100%;
            margin-top: 1rem;
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 0.85rem;
            padding-right: 0.85rem;
        }

        h1 {
            font-size: 1.9rem !important;
        }

        h2 {
            font-size: 1.3rem !important;
        }

        .custom-input-label {
            font-size: 0.98rem;
            margin-bottom: 1rem;
        }


        /* ==================================================
           INPUT MOBILE
           ================================================== */

        [data-testid="stTextInput"] {
            width: 100% !important;
            min-width: 0 !important;
        }

        [data-testid="stTextInput"] input {
            width: 100% !important;
            min-height: 2.55rem;
            height: 2.55rem;
            box-sizing: border-box;
        }


        /* ==================================================
           FAVORITA TRASFERTA MOBILE
           ================================================== */

        .st-key-favorite-away-box {
            padding: 0.8rem 0.85rem;
            margin-top: 0.1rem;
            margin-bottom: 0.75rem;
        }

        .st-key-favorite-away-box [data-testid="stCheckbox"] label,
        .st-key-favorite-away-box [data-testid="stCheckbox"] p {
            font-size: 1.05rem !important;
            font-weight: 700 !important;
        }


        /* ==================================================
           TUTTI I CONTROLLI MOBILE
           ================================================== */

        .st-key-stake-controls,
        .st-key-quote-controls-back_odds,
        .st-key-quote-controls-odds_02,
        .st-key-quote-controls-odds_12 {

            width: 100% !important;
            margin-top: 0.1rem;
            margin-bottom: 0.7rem;
        }


        /* ==================================================
           RIGA SEMPRE ORIZZONTALE
           ================================================== */

        .st-key-stake-controls [data-testid="stHorizontalBlock"],
        .st-key-quote-controls-back_odds [data-testid="stHorizontalBlock"],
        .st-key-quote-controls-odds_02 [data-testid="stHorizontalBlock"],
        .st-key-quote-controls-odds_12 [data-testid="stHorizontalBlock"] {

            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            align-items: center !important;

            width: 100% !important;
            min-width: 0 !important;

            gap: 0.3rem !important;
        }


        /* ==================================================
           COLONNA SINISTRA MOBILE
           ================================================== */

        .st-key-stake-controls
        [data-testid="stHorizontalBlock"]
        > [data-testid="stColumn"]:first-child,

        .st-key-quote-controls-back_odds
        [data-testid="stHorizontalBlock"]
        > [data-testid="stColumn"]:first-child,

        .st-key-quote-controls-odds_02
        [data-testid="stHorizontalBlock"]
        > [data-testid="stColumn"]:first-child,

        .st-key-quote-controls-odds_12
        [data-testid="stHorizontalBlock"]
        > [data-testid="stColumn"]:first-child {

            flex: 0 0 2.2rem !important;
            width: 2.2rem !important;
            min-width: 2.2rem !important;
            max-width: 2.2rem !important;
        }


        /* ==================================================
           COLONNA CENTRALE MOBILE
           ================================================== */

        .st-key-stake-controls
        [data-testid="stHorizontalBlock"]
        > [data-testid="stColumn"]:nth-child(2),

        .st-key-quote-controls-back_odds
        [data-testid="stHorizontalBlock"]
        > [data-testid="stColumn"]:nth-child(2),

        .st-key-quote-controls-odds_02
        [data-testid="stHorizontalBlock"]
        > [data-testid="stColumn"]:nth-child(2),

        .st-key-quote-controls-odds_12
        [data-testid="stHorizontalBlock"]
        > [data-testid="stColumn"]:nth-child(2) {

            flex: 1 1 0 !important;
            width: auto !important;
            min-width: 0 !important;
            max-width: none !important;
        }


        /* ==================================================
           COLONNA DESTRA MOBILE
           ================================================== */

        .st-key-stake-controls
        [data-testid="stHorizontalBlock"]
        > [data-testid="stColumn"]:last-child,

        .st-key-quote-controls-back_odds
        [data-testid="stHorizontalBlock"]
        > [data-testid="stColumn"]:last-child,

        .st-key-quote-controls-odds_02
        [data-testid="stHorizontalBlock"]
        > [data-testid="stColumn"]:last-child,

        .st-key-quote-controls-odds_12
        [data-testid="stHorizontalBlock"]
        > [data-testid="stColumn"]:last-child {

            flex: 0 0 2.2rem !important;
            width: 2.2rem !important;
            min-width: 2.2rem !important;
            max-width: 2.2rem !important;
        }


        /* ==================================================
           COLONNE MOBILE: DISABILITA MIN-WIDTH AUTOMATICA
           ================================================== */

        .st-key-stake-controls
        [data-testid="stColumn"],

        .st-key-quote-controls-back_odds
        [data-testid="stColumn"],

        .st-key-quote-controls-odds_02
        [data-testid="stColumn"],

        .st-key-quote-controls-odds_12
        [data-testid="stColumn"] {

            min-width: 0 !important;
        }


        /* ==================================================
           INPUT CENTRALE MOBILE
           ================================================== */

        .st-key-stake-controls
        [data-testid="stTextInput"],

        .st-key-quote-controls-back_odds
        [data-testid="stTextInput"],

        .st-key-quote-controls-odds_02
        [data-testid="stTextInput"],

        .st-key-quote-controls-odds_12
        [data-testid="stTextInput"] {

            width: 100% !important;
            min-width: 0 !important;
        }


        /* ==================================================
           FRECCE MOBILE
           ================================================== */

        .st-key-stake-controls [data-testid="stButton"],
        .st-key-quote-controls-back_odds [data-testid="stButton"],
        .st-key-quote-controls-odds_02 [data-testid="stButton"],
        .st-key-quote-controls-odds_12 [data-testid="stButton"] {

            width: 100% !important;
            margin: 0 !important;
        }

        .st-key-stake-controls [data-testid="stButton"] button,
        .st-key-quote-controls-back_odds [data-testid="stButton"] button,
        .st-key-quote-controls-odds_02 [data-testid="stButton"] button,
        .st-key-quote-controls-odds_12 [data-testid="stButton"] button {

            min-height: 2.55rem !important;
            height: 2.55rem !important;

            width: 100% !important;

            padding: 0 !important;
            margin: 0 !important;

            font-size: 0.72rem !important;
            line-height: 1 !important;
        }


        /* ==================================================
           CS RISULTATI SEMPRE AFFIANCATI
           ================================================== */

        .cs-results [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 0.5rem !important;
        }

        .cs-results
        [data-testid="stHorizontalBlock"]
        > [data-testid="stColumn"] {

            flex: 1 1 50% !important;
            width: 50% !important;
            min-width: 0 !important;
            max-width: 50% !important;
        }
    }


    /* ==================================================
       EVENTUALI CONTAINER VUOTI
       ================================================== */

    .empty-container {
        display: none !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# SESSION STATE
# ==================================================

if "back_odds" not in st.session_state:
    st.session_state.back_odds = "3.80"

if "odds_02" not in st.session_state:
    st.session_state.odds_02 = "20.00"

if "odds_12" not in st.session_state:
    st.session_state.odds_12 = "10.00"

if "stake_x" not in st.session_state:
    st.session_state.stake_x = "300"

if "favorita_trasferta" not in st.session_state:
    st.session_state.favorita_trasferta = False

if "minimum_back_stake" not in st.session_state:
    st.session_state.minimum_back_stake = None


# ==================================================
# STAKE STEP
# ==================================================

def stake_step(value: float) -> float:

    if value < 10:
        return 2.0

    if value < 50:
        return 5.0

    if value < 100:
        return 10.0

    if value < 500:
        return 25.0

    if value < 1000:
        return 50.0

    if value < 5000:
        return 100.0

    return 250.0


# ==================================================
# ROUND MINIMUM STAKE
# ==================================================

def round_minimum_stake(value: float) -> float:

    if value <= 0:
        return 0.0

    if value <= 10:
        step = 2.0

    elif value <= 50:
        step = 5.0

    elif value <= 100:
        step = 10.0

    elif value <= 500:
        step = 25.0

    elif value <= 1000:
        step = 50.0

    elif value <= 5000:
        step = 100.0

    else:
        step = 250.0

    return math.ceil(value / step) * step


# ==================================================
# STAKE DOWN
# ==================================================

def move_stake_down():

    try:

        value = float(
            st.session_state["stake_x"].replace(",", ".")
        )

        step = stake_step(value)

        new_value = max(
            2.0,
            value - step,
        )

        st.session_state["stake_x"] = str(
            int(new_value)
        )

    except (
        ValueError,
        KeyError,
        AttributeError,
    ):
        pass


# ==================================================
# STAKE UP
# ==================================================

def move_stake_up():

    try:

        value = float(
            st.session_state["stake_x"].replace(",", ".")
        )

        step = stake_step(value)

        new_value = value + step

        st.session_state["stake_x"] = str(
            int(new_value)
        )

    except (
        ValueError,
        KeyError,
        AttributeError,
    ):
        pass


# ==================================================
# QUOTE DOWN
# ==================================================

def move_quote_down(key: str):

    try:

        value = float(
            st.session_state[key].replace(",", ".")
        )

        new_value = previous_tick(value)

        st.session_state[key] = f"{new_value:.2f}"

    except (
        ValueError,
        KeyError,
        AttributeError,
    ):
        pass


# ==================================================
# QUOTE UP
# ==================================================

def move_quote_up(key: str):

    try:

        value = float(
            st.session_state[key].replace(",", ".")
        )

        new_value = next_tick(value)

        st.session_state[key] = f"{new_value:.2f}"

    except (
        ValueError,
        KeyError,
        AttributeError,
    ):
        pass


# ==================================================
# SET MINIMUM STAKE
# ==================================================

def set_minimum_stake():

    minimum = st.session_state.get(
        "minimum_back_stake"
    )

    if minimum is not None:

        st.session_state["stake_x"] = str(
            int(minimum)
        )


# ==================================================
# STAKE INPUT
# ==================================================

def stake_input() -> float:

    st.markdown(
        '<div class="custom-input-label">Stake X</div>',
        unsafe_allow_html=True,
    )

    with st.container(key="stake-controls"):

        col_down, col_input, col_up = st.columns(
            [0.65, 4.7, 0.65],
            gap="small",
            vertical_alignment="center",
        )

        with col_down:

            st.button(
                "▼",
                key="stake_x_down",
                use_container_width=True,
                on_click=move_stake_down,
            )

        with col_input:

            st.text_input(
                "stake_x_input",
                key="stake_x",
                label_visibility="collapsed",
                placeholder="300",
            )

        with col_up:

            st.button(
                "▲",
                key="stake_x_up",
                use_container_width=True,
                on_click=move_stake_up,
            )

    try:

        return float(
            st.session_state["stake_x"].replace(",", ".")
        )

    except (
        ValueError,
        AttributeError,
    ):

        return 0.0


# ==================================================
# QUOTE INPUT
# ==================================================

def quote_input(
    label: str,
    key: str,
) -> float:

    st.markdown(
        f'<div class="custom-input-label">{label}</div>',
        unsafe_allow_html=True,
    )

    with st.container(key=f"quote-controls-{key}"):

        col_down, col_input, col_up = st.columns(
            [0.65, 4.7, 0.65],
            gap="small",
            vertical_alignment="center",
        )

        with col_down:

            st.button(
                "▼",
                key=f"{key}_down",
                use_container_width=True,
                on_click=move_quote_down,
                args=(key,),
            )

        with col_input:

            st.text_input(
                f"{key}_input",
                key=key,
                label_visibility="collapsed",
                placeholder="3.80",
            )

        with col_up:

            st.button(
                "▲",
                key=f"{key}_up",
                use_container_width=True,
                on_click=move_quote_up,
                args=(key,),
            )

    try:

        return float(
            st.session_state[key].replace(",", ".")
        )

    except (
        ValueError,
        AttributeError,
    ):

        return 0.0


# ==================================================
# TITLE
# ==================================================

st.title("Draw → Correct Score")

st.markdown(
    """
    <style>
    .info-row {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }

    .info-caption {
        color: rgba(250, 250, 250, 0.65);
        font-size: 0.9rem;
        line-height: 1.4;
    }

    /* Contenitore del popover */
    .info-popover {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Pulsante informazioni */
    .info-popover [data-testid="stPopover"] {
        width: auto !important;
        min-width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .info-popover [data-testid="stPopover"] button {
        width: 1.35rem !important;
        min-width: 1.35rem !important;
        height: 1.35rem !important;
        min-height: 1.35rem !important;

        padding: 0 !important;
        margin: 0 !important;

        border: none !important;
        background: transparent !important;
        box-shadow: none !important;

        color: rgba(255, 255, 255, 0.55) !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;

        font-family: Arial, sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        font-style: italic !important;
        line-height: 1 !important;
    }

    .info-popover [data-testid="stPopover"] button:hover {
        color: rgba(255, 255, 255, 0.9) !important;
        background: rgba(255, 255, 255, 0.06) !important;
    }

    @media (max-width: 768px) {
        .info-caption {
            font-size: 0.85rem;
        }

        .info-popover [data-testid="stPopover"] button {
            width: 1.35rem !important;
            min-width: 1.35rem !important;
            height: 1.35rem !important;
            min-height: 1.35rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


col_caption, col_info = st.columns(
    [1, 0.07],
    gap="small",
    vertical_alignment="center",
)

with col_caption:

    st.markdown(
        '<div class="info-caption">'
        'Calcola rapidamente le stake CS a partire dalla freebet sulla X.'
        '</div>',
        unsafe_allow_html=True,
    )


with col_info:

    st.markdown(
        '<div class="info-popover">',
        unsafe_allow_html=True,
    )

    with st.popover("🛈", key="info-popover"):

        st.markdown("#### Come funziona")

        st.write(
            "Il tool calcola la freebet ottenuta sulla X dopo il piano Lay "
            "e determina le stake da puntare sui Correct Score in modo da "
            "ottenere un profitto equivalente alla freebet."
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# ==================================================
# MAIN LAYOUT
# ==================================================
with st.container(key="main-layout"):
    input_col, result_col = st.columns(
        [0.95, 1.05],
        gap="large",
    )


# ==================================================
# INPUT
# ==================================================

with input_col:

    st.subheader("Input")


    # --------------------------------------------------
    # STAKE X
    # --------------------------------------------------

    back_stake = stake_input()


    # --------------------------------------------------
    # FAVORITA TRASFERTA
    # --------------------------------------------------

    with st.container(key="favorite-away-box"):

        favorita_trasferta = st.checkbox(
            "Favorita in trasferta",
            key="favorita_trasferta",
        )


    # --------------------------------------------------
    # LABEL CORRECT SCORE
    # --------------------------------------------------

    if favorita_trasferta:

        cs_02_label = "CS 2-0"
        cs_12_label = "CS 2-1"

    else:

        cs_02_label = "CS 0-2"
        cs_12_label = "CS 1-2"


    # --------------------------------------------------
    # QUOTA X
    # --------------------------------------------------

    back_odds = quote_input(
        "Quota X",
        "back_odds",
    )


    # --------------------------------------------------
    # QUOTA CS
    # --------------------------------------------------

    odds_02 = quote_input(
        cs_02_label,
        "odds_02",
    )

    odds_12 = quote_input(
        cs_12_label,
        "odds_12",
    )


    # --------------------------------------------------
    # CALCOLA
    # --------------------------------------------------

    calculate_clicked = st.button(
        "CALCOLA",
        type="primary",
        use_container_width=True,
    )


# ==================================================
# RESULTS
# ==================================================

with result_col:

    st.subheader("Risultati")


    # ==================================================
    # PRIMA DEL CALCOLO
    # ==================================================

    if not calculate_clicked:

        st.info(
            "Inserisci i valori e premi **CALCOLA**."
        )


    # ==================================================
    # CALCOLO
    # ==================================================

    else:

        st.session_state.minimum_back_stake = None


        # ==================================================
        # VALIDAZIONE
        # ==================================================

        if back_stake <= 0:

            st.error(
                "Inserisci una stake X valida."
            )

            st.stop()


        if back_odds <= 1.01:

            st.error(
                "Inserisci una quota X valida."
            )

            st.stop()


        if odds_02 <= 1.01:

            st.error(
                f"Inserisci una quota {cs_02_label} valida."
            )

            st.stop()


        if odds_12 <= 1.01:

            st.error(
                f"Inserisci una quota {cs_12_label} valida."
            )

            st.stop()


        # ==================================================
        # VALIDAZIONE LADDER
        # ==================================================

        if round(back_odds, 2) not in BETFAIR_LADDER:

            st.error(
                f"Quota X {back_odds:.2f} "
                "non presente nella ladder Betfair."
            )

            st.stop()


        if round(odds_02, 2) not in BETFAIR_LADDER:

            st.error(
                f"Quota {cs_02_label} {odds_02:.2f} "
                "non presente nella ladder Betfair."
            )

            st.stop()


        if round(odds_12, 2) not in BETFAIR_LADDER:

            st.error(
                f"Quota {cs_12_label} {odds_12:.2f} "
                "non presente nella ladder Betfair."
            )

            st.stop()


        # ==================================================
        # CALCOLO
        # ==================================================

        try:

            result = calculate_cs_trade(
                back_stake=back_stake,
                back_odds=back_odds,
                odds_02=odds_02,
                odds_12=odds_12,
            )

        except ValueError as error:

            st.error(str(error))

            st.stop()


        # ==================================================
        # RISULTATI
        # ==================================================

        freebet = result["freebet"]
        stake_02 = result["stake_02"]
        stake_12 = result["stake_12"]
        lay_plan = result["lay_plan"]


        
        # ==================================================
        # FREEBET
        # ==================================================

        st.markdown(
            '<div class="result-label">Freebet</div>',
            unsafe_allow_html=True,
        )
        
        st.markdown(
            f'<div class="freebet-value">{freebet:.2f} €</div>',
            unsafe_allow_html=True,
        )

        # ==================================================
        # CS STAKES
        # ==================================================

        with st.container(key="cs-results"):

            cs_col_02, cs_col_12 = st.columns(
                2,
                gap="medium",
            )

            with cs_col_02:

                st.metric(
                    cs_02_label,
                    f"{stake_02:.2f} €",
                    delta=f"@ {odds_02:.2f}",
                    delta_color="off",
                )

            with cs_col_12:

                st.metric(
                    cs_12_label,
                    f"{stake_12:.2f} €",
                    delta=f"@ {odds_12:.2f}",
                    delta_color="off",
                )


        # ==================================================
        # STATO
        # ==================================================

        executable = (
            stake_02 >= 1
            and stake_12 >= 1
        )


        # ==================================================
        # SOLO NON ESEGUIBILE
        # ==================================================

        if not executable:

            st.markdown(
                """
                <div class="status-box status-error">
                    ❌ OPERAZIONE NON ESEGUIBILE
                </div>
                """,
                unsafe_allow_html=True,
            )


            # ----------------------------------------------
            # COME RENDERE ESEGUIBILE
            # ----------------------------------------------

            with st.container(key="minimum-section"):

                st.markdown(
                    '<div class="minimum-title">'
                    'Come rendere eseguibile'
                    '</div>',
                    unsafe_allow_html=True,
                )

                try:

                    minimum_result = (
                        calculate_minimum_back_stake(
                            back_odds=back_odds,
                            odds_02=odds_02,
                            odds_12=odds_12,
                        )
                    )

                    minimum_back_stake_raw = (
                        minimum_result["minimum_back_stake"]
                    )

                    target_freebet = (
                        minimum_result["target_freebet"]
                    )

                    # Arrotondamento sempre per eccesso.
                    minimum_back_stake = (
                        round_minimum_stake(
                            minimum_back_stake_raw
                        )
                    )

                    st.session_state.minimum_back_stake = (
                        minimum_back_stake
                    )

                    min_col_1, min_col_2 = st.columns(
                        2,
                        gap="medium",
                    )

                    with min_col_1:

                        st.metric(
                            "Stake X minima",
                            f"{minimum_back_stake:.0f} €",
                        )

                    with min_col_2:

                        st.metric(
                            "Freebet minima",
                            f"€{target_freebet:.2f}",
                        )


                    st.button(
                        "IMPOSTA STAKE MINIMA",
                        key="set_minimum_stake_button",
                        use_container_width=True,
                        on_click=set_minimum_stake,
                    )

                except ValueError as error:

                    st.warning(
                        "Impossibile calcolare la stake X minima: "
                        f"{error}"
                    )


        # ==================================================
        # SOLO SE ESEGUIBILE
        # ==================================================

        if executable:

            # ----------------------------------------------
            # PIANO LAY
            # ----------------------------------------------

            with st.expander(
                "Piano Lay",
                expanded=True,
            ):

                if not lay_plan:

                    st.caption(
                        "Nessun piano Lay disponibile."
                    )

                else:

                    for i, lay in enumerate(
                        lay_plan,
                        start=1,
                    ):

                        st.write(
                            f"**Lay {i}** — "
                            f"{lay.stake:.2f} € "
                            f"@ {lay.odds:.2f}"
                        )


            # ----------------------------------------------
            # ESITI POTENZIALI
            # ----------------------------------------------

            with st.expander(
                "Esiti potenziali",
                expanded=True,
            ):

                profit_x = freebet

                profit_02 = (
                    stake_02 * (odds_02 - 1)
                    - stake_12
                )

                profit_12 = (
                    stake_12 * (odds_12 - 1)
                    - stake_02
                )

                profit_other = -(
                    stake_02 + stake_12
                )


                outcome_col_1, outcome_col_2 = st.columns(
                    2,
                    gap="medium",
                )

                with outcome_col_1:

                    st.write(
                        f"**X → {'+' if profit_x >= 0 else '-'}{abs(profit_x):.2f} €**"
                    )

                    st.write(
                        f"**{cs_02_label} → "
                        f"{'+' if profit_02 >= 0 else '-'}{abs(profit_02):.2f} €**"
                    )

                with outcome_col_2:

                    st.write(
                        f"**{cs_12_label} → "
                        f"{'+' if profit_12 >= 0 else '-'}{abs(profit_12):.2f} €**"
                    )

                    st.write(
                        f"**Altri esiti → "
                        f"{'+' if profit_other >= 0 else '-'}{abs(profit_other):.2f} €**"
                    )