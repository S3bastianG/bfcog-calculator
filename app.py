import math
import streamlit as st
from engine.calculator import calculate_cs_trade, calculate_minimum_back_stake
from engine.betfair_ladder import BETFAIR_LADDER, next_tick, previous_tick

st.set_page_config(page_title="BFCOG → Calculator", page_icon="⚽", layout="centered")

APP_VERSION = "1.0.1"

st.markdown("""
<style>
.block-container {
    width: 100%;
    max-width: 1450px;
    margin: 0 auto;
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}
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
.custom-input-label {
    font-size: 1rem;
    font-weight: 700;
    line-height: 1.2;
    margin-top: 0.1rem;
    margin-bottom: 0.55rem;
    color: var(--text-color) !important;
}
[data-testid="stTextInput"] label {
    display: none !important;
}
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
[data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}
.st-key-stake-controls,
.st-key-quote-controls-back_odds,
.st-key-quote-controls-odds_02,
.st-key-quote-controls-odds_12 {
    width: 100% !important;
    margin-top: 0.15rem;
    margin-bottom: 0.7rem;
}
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
.st-key-stake-controls [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child,
.st-key-quote-controls-back_odds [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child,
.st-key-quote-controls-odds_02 [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child,
.st-key-quote-controls-odds_12 [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child {
    flex: 0 0 2.3rem !important;
    width: 2.3rem !important;
    min-width: 2.3rem !important;
    max-width: 2.3rem !important;
}
.st-key-stake-controls [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2),
.st-key-quote-controls-back_odds [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2),
.st-key-quote-controls-odds_02 [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2),
.st-key-quote-controls-odds_12 [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) {
    flex: 1 1 0 !important;
    width: auto !important;
    min-width: 0 !important;
    max-width: none !important;
}
.st-key-stake-controls [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child,
.st-key-quote-controls-back_odds [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child,
.st-key-quote-controls-odds_02 [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child,
.st-key-quote-controls-odds_12 [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {
    flex: 0 0 2.3rem !important;
    width: 2.3rem !important;
    min-width: 2.3rem !important;
    max-width: 2.3rem !important;
}
.st-key-stake-controls [data-testid="stColumn"],
.st-key-quote-controls-back_odds [data-testid="stColumn"],
.st-key-quote-controls-odds_02 [data-testid="stColumn"],
.st-key-quote-controls-odds_12 [data-testid="stColumn"] {
    min-width: 0 !important;
}
.st-key-stake-controls [data-testid="stTextInput"],
.st-key-quote-controls-back_odds [data-testid="stTextInput"],
.st-key-quote-controls-odds_02 [data-testid="stTextInput"],
.st-key-quote-controls-odds_12 [data-testid="stTextInput"] {
    width: 100% !important;
}
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
.st-key-favorite-away-box,
.st-key-sharp-exchange-box,
.st-key-solo-x-box {
    margin-top: 0.1rem;
    margin-bottom: 0.75rem;
    padding: 0.75rem 0.9rem;
    border-radius: 0.6rem;
    border: 1px solid rgba(255, 255, 255, 0.14);
    background: rgba(255, 255, 255, 0.035);
}
.st-key-favorite-away-box [data-testid="stToggle"],
.st-key-sharp-exchange-box [data-testid="stToggle"],
.st-key-solo-x-box [data-testid="stToggle"] {
    margin: 0 !important;
    padding: 0 !important;
}
.st-key-favorite-away-box [data-testid="stToggle"] label,
.st-key-favorite-away-box [data-testid="stToggle"] p,
.st-key-sharp-exchange-box [data-testid="stToggle"] label,
.st-key-sharp-exchange-box [data-testid="stToggle"] p,
.st-key-solo-x-box [data-testid="stToggle"] label,
.st-key-solo-x-box [data-testid="stToggle"] p {
    font-size: 1.05rem !important;
    font-weight: 700 !important;
}
button[kind="primary"] {
    min-height: 2.8rem;
    height: 2.8rem;
    margin-top: 0.15rem;
    font-size: 1rem;
    font-weight: 700;
}
[data-testid="stMetric"] {
    padding: 0 !important;
    margin: 0 !important;
}
.result-label,
[data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    line-height: 1.2 !important;
    color: var(--text-color) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    text-decoration: none !important;
    margin: 0 0 0.15rem 0 !important;
    padding: 0 !important;
}
[data-testid="stMetricLabel"] > div,
[data-testid="stMetricLabel"] p {
    font-size: inherit !important;
    font-weight: inherit !important;
    line-height: inherit !important;
    color: inherit !important;
    text-transform: inherit !important;
    letter-spacing: inherit !important;
    text-decoration: none !important;
    margin: 0 !important;
    padding: 0 !important;
}
[data-testid="stMetricValue"] {
    font-size: clamp(1.45rem, 2vw, 2rem) !important;
    font-weight: 400 !important;
    line-height: 1.15 !important;
    margin: 0 !important;
    padding: 0 !important;
}
[data-testid="stMetricDelta"] {
    font-size: 0.78rem;
}
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
[data-testid="stExpander"] {
    margin-top: 0.35rem;
    margin-bottom: 0.35rem;
}
[data-testid="stExpander"] details summary {
    padding-top: 0.65rem;
    padding-bottom: 0.65rem;
}
[data-testid="stAlert"] {
    padding-top: 0.65rem;
    padding-bottom: 0.65rem;
}
.empty-container {
    display: none !important;
}
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
    .st-key-favorite-away-box [data-testid="stToggle"] label,
    .st-key-favorite-away-box [data-testid="stToggle"] p,
    .st-key-sharp-exchange-box [data-testid="stToggle"] label,
    .st-key-sharp-exchange-box [data-testid="stToggle"] p,
    .st-key-solo-x-box [data-testid="stToggle"] label,
    .st-key-solo-x-box [data-testid="stToggle"] p {
        font-size: 1.1rem !important;
    }
}

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
    .st-key-favorite-away-box,
    .st-key-solo-x-box {
        padding: 0.8rem 0.85rem;
        margin-top: 0.1rem;
        margin-bottom: 0.75rem;
    }
    .st-key-favorite-away-box [data-testid="stToggle"] label,
    .st-key-favorite-away-box [data-testid="stToggle"] p,
    .st-key-solo-x-box [data-testid="stToggle"] label,
    .st-key-solo-x-box [data-testid="stToggle"] p {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }
    .st-key-sharp-exchange-box {
        padding: 0.8rem 0.85rem;
        margin-top: 0.1rem;
        margin-bottom: 0.75rem;
    }
    .st-key-sharp-exchange-box [data-testid="stToggle"] label,
    .st-key-sharp-exchange-box [data-testid="stToggle"] p {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }
    .st-key-stake-controls,
    .st-key-quote-controls-back_odds,
    .st-key-quote-controls-odds_02,
    .st-key-quote-controls-odds_12 {
        width: 100% !important;
        margin-top: 0.1rem;
        margin-bottom: 0.7rem;
    }
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
    .st-key-stake-controls [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child,
    .st-key-quote-controls-back_odds [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child,
    .st-key-quote-controls-odds_02 [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child,
    .st-key-quote-controls-odds_12 [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child {
        flex: 0 0 2.2rem !important;
        width: 2.2rem !important;
        min-width: 2.2rem !important;
        max-width: 2.2rem !important;
    }
    .st-key-stake-controls [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2),
    .st-key-quote-controls-back_odds [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2),
    .st-key-quote-controls-odds_02 [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2),
    .st-key-quote-controls-odds_12 [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) {
        flex: 1 1 0 !important;
        width: auto !important;
        min-width: 0 !important;
        max-width: none !important;
    }
    .st-key-stake-controls [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child,
    .st-key-quote-controls-back_odds [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child,
    .st-key-quote-controls-odds_02 [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child,
    .st-key-quote-controls-odds_12 [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {
        flex: 0 0 2.2rem !important;
        width: 2.2rem !important;
        min-width: 2.2rem !important;
        max-width: 2.2rem !important;
    }
    .st-key-stake-controls [data-testid="stColumn"],
    .st-key-quote-controls-back_odds [data-testid="stColumn"],
    .st-key-quote-controls-odds_02 [data-testid="stColumn"],
    .st-key-quote-controls-odds_12 [data-testid="stColumn"] {
        min-width: 0 !important;
    }
    .st-key-stake-controls [data-testid="stTextInput"],
    .st-key-quote-controls-back_odds [data-testid="stTextInput"],
    .st-key-quote-controls-odds_02 [data-testid="stTextInput"],
    .st-key-quote-controls-odds_12 [data-testid="stTextInput"] {
        width: 100% !important;
        min-width: 0 !important;
    }
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
    .st-key-stake-results [data-testid="stHorizontalBlock"],
    .st-key-cs-results [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: flex-start !important;
        width: 100% !important;
        min-width: 0 !important;
        gap: 0.5rem !important;
    }
    .st-key-stake-results [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
    .st-key-cs-results [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        flex: 1 1 0% !important;
        width: 50% !important;
        min-width: 0 !important;
        max-width: 50% !important;
    }
    .st-key-stake-results [data-testid="stMetric"],
    .st-key-cs-results [data-testid="stMetric"] {
        width: 100% !important;
        min-width: 0 !important;
    }
    .st-key-stake-results [data-testid="stMetricLabel"],
    .st-key-cs-results [data-testid="stMetricLabel"] {
        white-space: normal !important;
    }
    .st-key-stake-results [data-testid="stMetricValue"],
    .st-key-cs-results [data-testid="stMetricValue"] {
        white-space: nowrap !important;
    }
}
.st-key-favorite-away-box,
.st-key-sharp-exchange-box,
.st-key-solo-x-box {
    background: color-mix(in srgb, var(--text-color) 4%, transparent) !important;
    border-color: color-mix(in srgb, var(--text-color) 18%, transparent) !important;
}
.st-key-favorite-away-box:hover,
.st-key-sharp-exchange-box:hover,
.st-key-solo-x-box:hover {
    background: color-mix(in srgb, var(--text-color) 7%, transparent) !important;
    border-color: color-mix(in srgb, var(--text-color) 30%, transparent) !important;
}
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
.info-popover {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    margin: 0 !important;
    padding: 0 !important;
}
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
""", unsafe_allow_html=True)

if "back_odds" not in st.session_state: st.session_state.back_odds = "4.50"
if "odds_02" not in st.session_state: st.session_state.odds_02 = "20.00"
if "odds_12" not in st.session_state: st.session_state.odds_12 = "10.00"
if "stake_x" not in st.session_state: st.session_state.stake_x = "125"
if "favorita_trasferta" not in st.session_state: st.session_state.favorita_trasferta = False
if "sharp_exchange" not in st.session_state: st.session_state.sharp_exchange = True
if "solo_x" not in st.session_state: st.session_state.solo_x = False
if "solo_x_previous" not in st.session_state: st.session_state.solo_x_previous = False
if "minimum_back_stake" not in st.session_state: st.session_state.minimum_back_stake = None
if "calculated" not in st.session_state: st.session_state.calculated = False
if "cs_independent" not in st.session_state: st.session_state.cs_independent = False
if "cs_freebet" not in st.session_state: st.session_state.cs_freebet = "100"

def get_quote_from_state(key: str, default: float) -> float:
    value = st.session_state.get(key, default)
    try:
        return float(str(value).replace(",", "."))
    except (ValueError, TypeError):
        return default

def stake_step(value: float) -> float:
    if value <= 20: return 1
    if value <= 50: return 10
    if value <= 100: return 10.0
    if value <= 1000: return 100.0
    return 1000.0

def round_minimum_stake(value: float) -> float:
    if value <= 0: return 0.0
    step = 1 if value <= 10 else 2 if value <= 50 else 5 if value <= 250 else 25 if value <= 1000 else 100
    return math.ceil(value / step) * step


def move_stake_down():
    try:
        value = float(st.session_state["stake_x"].replace(",", "."))
        step = stake_step(value)
        new_value = max(2.0, value - step)
        st.session_state["stake_x"] = str(int(new_value))
    except (ValueError, KeyError, AttributeError):
        pass

def move_stake_up():
    try:
        value = float(st.session_state["stake_x"].replace(",", "."))
        step = stake_step(value)
        new_value = value + step
        st.session_state["stake_x"] = str(int(new_value))
    except (ValueError, KeyError, AttributeError):
        pass

def move_quote_down(key: str):
    try:
        value = float(st.session_state[key].replace(",", "."))
        new_value = previous_tick(value)
        st.session_state[key] = f"{new_value:.2f}"
    except (ValueError, KeyError, AttributeError):
        pass

def move_quote_up(key: str):
    try:
        value = float(st.session_state[key].replace(",", "."))
        new_value = next_tick(value)
        st.session_state[key] = f"{new_value:.2f}"
    except (ValueError, KeyError, AttributeError):
        pass

def set_minimum_stake():
    minimum = st.session_state.get("minimum_back_stake")
    if minimum is not None:
        st.session_state["stake_x"] = str(int(minimum))
        st.session_state["calculated"] = True

def stake_input() -> float:
    st.markdown('<div class="custom-input-label">Stake X</div>', unsafe_allow_html=True)
    with st.container(key="stake-controls"):
        col_down, col_input, col_up = st.columns([0.65, 4.7, 0.65], gap="small", vertical_alignment="center")
        with col_down:
            st.button("▼", key="stake_x_down", use_container_width=True, on_click=move_stake_down)
        with col_input:
            st.text_input("stake_x_input", key="stake_x", label_visibility="collapsed", placeholder="300")
        with col_up:
            st.button("▲", key="stake_x_up", use_container_width=True, on_click=move_stake_up)
    try:
        return float(st.session_state["stake_x"].replace(",", "."))
    except (ValueError, AttributeError):
        return 0.0

def quote_input(label: str, key: str) -> float:
    st.markdown(f'<div class="custom-input-label">{label}</div>', unsafe_allow_html=True)
    with st.container(key=f"quote-controls-{key}"):
        col_down, col_input, col_up = st.columns([0.65, 4.7, 0.65], gap="small", vertical_alignment="center")
        with col_down:
            st.button("▼", key=f"{key}_down", use_container_width=True, on_click=move_quote_down, args=(key,))
        with col_input:
            st.text_input(f"{key}_input", key=key, label_visibility="collapsed", placeholder="3.80")
        with col_up:
            st.button("▲", key=f"{key}_up", use_container_width=True, on_click=move_quote_up, args=(key,))
    try:
        return float(st.session_state[key].replace(",", "."))
    except (ValueError, AttributeError):
        return 0.0

st.markdown(f"""
<div style="
    display: flex;
    align-items: baseline;
    gap: 0.6rem;
    margin-bottom: 0.35rem;
    margin-top: 1rem;
">
    <span style="
        font-size: clamp(2rem, 2.5vw, 3rem);
        font-weight: 700;
        line-height: 1.1;
    ">
        BFCOG → Calculator (Cover)
    </span>
    <span style="
        font-size: 0.7rem;
        font-weight: 500;
    ">
        v{APP_VERSION}
    </span>
</div>
""", unsafe_allow_html=True)


st.markdown("""
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
.info-popover {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    margin: 0 !important;
    padding: 0 !important;
}
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
    .info-caption { font-size: 0.85rem; }
    .info-popover [data-testid="stPopover"] button {
        width: 1.35rem !important;
        min-width: 1.35rem !important;
        height: 1.35rem !important;
        min-height: 1.35rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

col_caption, col_info = st.columns([1, 0.07], gap="small", vertical_alignment="center")

#with col_caption:
#    st.markdown('<div class="info-caption">Calcola rapidamente le stake CS a partire dalla freebet sulla X.</div>', unsafe_allow_html=True)


#with col_info:
#    st.markdown('<div class="info-popover">', unsafe_allow_html=True)
#    with st.popover("ⓘ", key="info-popover"):
#        st.markdown("#### Come funziona")
#        st.write("Il tool calcola la freebet ottenuta sulla X dopo il piano Lay e determina le stake da puntare sui Correct Score in modo da ottenere un profitto equivalente alla freebet.")
#    st.markdown("</div>", unsafe_allow_html=True)

with st.container(key="main-layout"):
    input_col, result_col = st.columns([0.95, 1.05], gap="large")

with input_col:
    st.header("Input")

    with st.container(key="favorite-away-box"):
        favorita_trasferta = st.toggle("Favorita in trasferta", key="favorita_trasferta")

    with st.container(key="sharp-exchange-box"):
        sharp_exchange = st.toggle("Sharp Exchange", key="sharp_exchange")

    with st.container(key="solo-x-box"):
        solo_x = st.toggle("Calcola solo su X", key="solo_x")

    if st.session_state.solo_x_previous and not solo_x:
        st.session_state.odds_02 = "20.00"
        st.session_state.odds_12 = "10.00"

    st.session_state.solo_x_previous = solo_x

    back_stake = stake_input()

    if favorita_trasferta:
        stake_cs_02_label, stake_cs_12_label = "Stake CS 2-0", "Stake CS 2-1"
        quote_cs_02_label, quote_cs_12_label = "Quota CS 2-0", "Quota CS 2-1"
        cs_02_label, cs_12_label = "CS 2-0", "CS 2-1"
    else:
        stake_cs_02_label, stake_cs_12_label = "Stake CS 0-2", "Stake CS 1-2"
        quote_cs_02_label, quote_cs_12_label = "Quota CS 0-2", "Quota CS 1-2"
        cs_02_label, cs_12_label = "CS 0-2", "CS 1-2"

    back_odds = quote_input("Quota X", "back_odds")

    if not solo_x:
        odds_02 = quote_input(quote_cs_02_label, "odds_02")
        odds_12 = quote_input(quote_cs_12_label, "odds_12")
    else:
        odds_02 = get_quote_from_state("odds_02", 20.00)
        odds_12 = get_quote_from_state("odds_12", 10.00)

with result_col:
    st.header("Risultati")

    if back_stake <= 0:
        st.error("Inserisci una stake X valida.")
        st.stop()

    if back_odds <= 1.01:
        st.error("Inserisci una quota X valida.")
        st.stop()

    if not solo_x:
        if odds_02 <= 1.01:
            st.error(f"Inserisci una quota {stake_cs_02_label} valida.")
            st.stop()
        if odds_12 <= 1.01:
            st.error(f"Inserisci una quota {stake_cs_12_label} valida.")
            st.stop()

    if round(back_odds, 2) not in BETFAIR_LADDER:
        st.error(f"Quota X {back_odds:.2f} non presente nella ladder Betfair.")
        st.stop()

    if not solo_x:
        if round(odds_02, 2) not in BETFAIR_LADDER:
            st.error(f"Quota {stake_cs_02_label} {odds_02:.2f} non presente nella ladder Betfair.")
            st.stop()
        if round(odds_12, 2) not in BETFAIR_LADDER:
            st.error(f"Quota {stake_cs_12_label} {odds_12:.2f} non presente nella ladder Betfair.")
            st.stop()

    try:
        result = calculate_cs_trade(back_stake=back_stake, back_odds=back_odds, odds_02=odds_02, odds_12=odds_12, solo_x=solo_x)
    except ValueError as error:
        st.error(str(error))
        st.stop()

    freebet = result["freebet"]
    stake_02 = result["stake_02"]
    stake_12 = result["stake_12"]
    lay_plan = result["lay_plan"]

    minimum_outcome_stake = 10.0 if sharp_exchange else 1.0

    if solo_x:
        minimum_back_stake = None
        target_freebet = None
        st.session_state["minimum_back_stake"] = None
    else:
        try:
            minimum_result = calculate_minimum_back_stake(back_odds=back_odds, odds_02=odds_02, odds_12=odds_12, min_cs_stake=minimum_outcome_stake)
            minimum_back_stake_raw = minimum_result["minimum_back_stake"]
            minimum_back_stake = round_minimum_stake(minimum_back_stake_raw)
            target_freebet = minimum_result["target_freebet"]
            st.session_state["minimum_back_stake"] = minimum_back_stake
        except ValueError as error:
            minimum_back_stake = None
            target_freebet = None
            st.warning(f"Impossibile calcolare la stake X minima: {error}")

    with st.container(key="stake-results"):
        if solo_x:
            st.metric("Stake X corrente", f"{back_stake:.2f}".rstrip("0").rstrip(".") + " €")
        else:
            stake_col, minimum_col = st.columns(2, gap="medium")
            with stake_col:
                st.metric("Stake X corrente", f"{back_stake:.2f}".rstrip("0").rstrip(".") + " €")
            with minimum_col:
                if minimum_back_stake is not None:
                    st.metric("Stake X minima", f"{minimum_back_stake:.2f}".rstrip("0").rstrip(".") + " €")
                else:
                    st.metric("Stake X minima", "—")

    if not solo_x:
        with st.container(key="cs-results"):
            cs_col_02, cs_col_12 = st.columns(2, gap="medium")
            with cs_col_02:
                st.metric(stake_cs_02_label, f"{stake_02:.2f} €", delta=f"@ {odds_02:.2f}", delta_color="off")
            with cs_col_12:
                st.metric(stake_cs_12_label, f"{stake_12:.2f} €", delta=f"@ {odds_12:.2f}", delta_color="off")

    st.metric("Freebet", f"{freebet:.2f}".rstrip("0").rstrip(".") + " €")

    if solo_x:
        executable = True
    else:
        executable = stake_02 >= minimum_outcome_stake and stake_12 >= minimum_outcome_stake

    if not executable:
        st.markdown("""
        <div class="status-box status-error">
            ❌ OPERAZIONE NON ESEGUIBILE
        </div>
        """, unsafe_allow_html=True)

        with st.container(key="minimum-section"):
            st.markdown('<div class="minimum-title">Come rendere eseguibile</div>', unsafe_allow_html=True)

            if minimum_back_stake is not None:
                min_col_1, min_col_2 = st.columns(2, gap="medium")

                with min_col_1:
                    st.metric("Stake X minima", f"{minimum_back_stake:.2f}".rstrip("0").rstrip(".") + " €")

                with min_col_2:
                    st.metric("Freebet minima", f"€{target_freebet:.2f}".rstrip("0").rstrip(".") + " €")

                st.button("IMPOSTA STAKE MINIMA", key="set_minimum_stake_button", use_container_width=True, on_click=set_minimum_stake)
            else:
                st.warning("Impossibile determinare la stake X minima.")

    if executable:
        with st.expander("Piano Lay", expanded=True):
            if not lay_plan:
                st.caption("Nessun piano Lay disponibile.")
            else:
                for i, lay in enumerate(lay_plan, start=1):
                    stake_display = f"{lay.stake:.2f}".rstrip("0").rstrip(".")
                    st.write(f"**Lay {i}** ({lay.percentage:.0f}%) — **{stake_display} €** @ **{lay.odds:.2f}**")

        with st.expander("Esiti potenziali", expanded=True):
            profit_x = freebet
            outcome_col_1, outcome_col_2 = st.columns(2, gap="medium")

            with outcome_col_1:
                st.write(f"**X → {'+ ' if profit_x >= 0 else '-'}{abs(profit_x):.2f}".rstrip("0").rstrip(".") + " €**")

                if not solo_x:
                    profit_02 = stake_02 * (odds_02 - 1) - stake_12
                    st.write(f"**{cs_02_label} → {'+ ' if profit_02 >= 0 else '-'}{abs(profit_02):.2f}".rstrip("0").rstrip(".") + " €**")

            with outcome_col_2:
                if not solo_x:
                    profit_12 = stake_12 * (odds_12 - 1) - stake_02
                    profit_other = -(stake_02 + stake_12)
                    st.write(f"**{cs_12_label} → {'+ ' if profit_12 >= 0 else '-'}{abs(profit_12):.2f}".rstrip("0").rstrip(".") + " €**")
                    st.write(f"**Altri esiti → {'+ ' if profit_other >= 0 else '-'}{abs(profit_other):.2f}".rstrip("0").rstrip(".") + " €**")
                else:
                    st.write("**Altri esiti → 0 €**")