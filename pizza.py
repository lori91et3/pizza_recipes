" Pizza maturazione in frigo "
# spianata 0.70, 0.025, 0.0023 0.08
# pizza 21/02/2025 0.62 0.025 0.0023 0.0
# pizza 15/03/2025 0.65 0.025 0.0023 0.0 3x260(3x220 + Titti) difficile da gestire, calare lievito
# pizza 30/03/2025 0.65 0.025 0.0021 0.0 3x260(3x220 + Titti)
# spianata 10/04/2025 0.70 0.025 0.03 0.08 920 1 comunque poco alveolata, aumentare hydro a 80 e farina
# pizza 12/04/2025 0.68 0.025 0.0021 0.0 3x260(3x220 + Titti)
# pizza 06/09/2025 0.68 0.025 0.0021 0.0 3x260(3x220 + Titti) temperatura 26.4°C, tutto ok
# spianata 06/09/2025 0.80 0.025 0.03 0.08 1200 1; buona ma aumentare farina, la teglia è grande
# spianata 15/11/2025 0.80 0.025 0.03 0.08 1500 1; teglia riempita meglio
# pizza 11/04/2026 0.70 0.025 0.0021 0.0 4x250; provato con Molina Vigevano Vesuvio; panetti un po' giù, aggiungere sale
# pizza 09/05/2026 [0.70, 0.035, 0.0021, 0.0, 250, 4] buona, ma panetti un po' giù e non molto digeribile, provare più maturazione e fare lo staglio dopo
# spianata 09/05/2026 [0.80, 0.025, 0.03, 0.08, 1500, 1] buona
# pizza 26/05/2026 [0.70, 0.035, 0.0021, 0.0, 250, 4] fatto lo staglio 2 ore prima di toglierle da frigo dopo il frigo, pare venuta bene; panetti leggermente giù ma non troppo
import sys
import math
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

# =============================================================================
# 1) CONFIG INGREDIENTI  (tutte le percentuali sono sulla farina = baker's %)
#    Esempio: 0.70 = 70%, 0.025 = 2.5%
# =============================================================================
INGREDIENTS_LIST = [0.70, 0.035, 0.0021, 0.0, 240, 2]

WATER_PERCENTAGE = INGREDIENTS_LIST[0]  # %  acqua sulla farina      (0.70 = 70%)
SALT_PERCENTAGE  = INGREDIENTS_LIST[1]  # %  sale sulla farina       (0.025 = 2.5%)
YEAST_PERCENTAGE = INGREDIENTS_LIST[2]  # %  lievito sulla farina
OIL_PERCENTAGE   = INGREDIENTS_LIST[3]  # %  olio sulla farina       (0 per pizza)

PANETTO_WEIGHT = INGREDIENTS_LIST[4]    # g  peso obiettivo di un panetto
PIZZA_NUMBER   = INGREDIENTS_LIST[5]    #    numero di panetti

# =============================================================================
# 2) CONFIG FERMENTAZIONE
# =============================================================================
TEMP_AMB   = 22.0  # °C  temperatura ambiente di casa  <-- parametro principale da cambiare
TEMP_FRIGO =  4.0  # °C  temperatura del frigo
FLOUR_W    =  300  #     forza della farina (W): debole <240, media 240-320, forte >320

# IMPASTO_ORA è un INPUT dell'utente: tu scegli a che ora vuoi fare l'impasto il G1.
# Lo script calcola puntata e appretto dalla temperatura, e il frigo riempie il resto.
IMPASTO_ORA = 20   # h  ora del Giorno 1 in cui fai l'impasto  [ORA_MIN..ORA_MAX]
STESURA_ORA = 19   # h  ora del Giorno 3 in cui stendi (di solito fisso)
ORA_MIN     =  8   # h  |-- finestra oraria ammessa per IMPASTO_ORA
ORA_MAX     = 22   # h  |   fuori range = errore

# --- Parametri fisici del modello Q10 (NON toccarli, sono valori di letteratura) ---
# Ogni fase (T °C, durata h) equivale a: ore * Q10^((T - REF_TEMP)/10) "ore-equivalenti".
# Lievitazione e maturazione hanno Q10 diversi: il frigo rallenta molto più la
# lievitazione che la maturazione, ed è per questo che matura senza esplodere.
# Q10_LIEV e Q10_MATUR sono valori misurati su lievito ed enzimi in laboratorio:
# non dipendono dalla tua cucina o farina, non richiedono calibrazione personale.
REF_TEMP  = 20.0  # °C  temperatura di riferimento per le ore-equivalenti
Q10_LIEV  =  2.2  #     accelerazione LIEVITAZIONE ogni +10 °C  (letteratura: 2.0-2.5)
Q10_MATUR =  1.5  #     accelerazione MATURAZIONE ogni +10 °C   (letteratura: 1.3-1.7)

# --- Obiettivi biologici (ore-equivalenti a REF_TEMP) ---
# NON richiedono calibrazione personale: vengono dalle buone pratiche standard.
# Sono "lavoro biologico" target, non ore reali: le ore reali vengono calcolate
# e stampate nel report (a 20°C coincidono col valore; a 29°C sono circa la metà).
PUNTATA_TARGET  = 2.0  # h-eq  riposo + pieghe dopo l'impasto (G1)
APPRETTO_TARGET = 4.0  # h-eq  riposo palline a tamb prima della stesura (G3)

# =============================================================================
# 3) CALCOLO INGREDIENTI
# =============================================================================
DOUGH_WEIGHT = PANETTO_WEIGHT * PIZZA_NUMBER

# farina * (1 + acqua% + sale% + olio% + lievito%) = peso impasto
FLOUR = DOUGH_WEIGHT / (1 + WATER_PERCENTAGE + SALT_PERCENTAGE
                        + OIL_PERCENTAGE + YEAST_PERCENTAGE)
WATER = FLOUR * WATER_PERCENTAGE
SALT  = FLOUR * SALT_PERCENTAGE
OIL   = FLOUR * OIL_PERCENTAGE
YEAST = FLOUR * YEAST_PERCENTAGE
print(f"Dough weight = {DOUGH_WEIGHT:.0f} g")
print(f"Flour  = {FLOUR:.0f} g")
print(f"Water  = {WATER:.0f} g")
print(f"Salt   = {SALT:.1f} g")
print(f"Oil    = {OIL:.1f} g")
print(f"Yeast  = {YEAST:.2f} g\n")

# =============================================================================
# 4) MODELLO Q10: funzioni di base
# =============================================================================
def f_liev(temp):
    return Q10_LIEV ** ((temp - REF_TEMP) / 10.0)

def f_matur(temp):
    return Q10_MATUR ** ((temp - REF_TEMP) / 10.0)

def ore_reali(target_heq, temp):
    return target_heq / f_liev(temp)

def ore_maturazione_range(w):
    if w < 240:  return (6, 12)
    if w < 280:  return (12, 24)
    if w < 320:  return (24, 48)
    if w < 360:  return (48, 72)
    return (72, 96)

# =============================================================================
# 5) CALENDARIO (ore dalla mezzanotte di G1)
#    G1 = 0..24, G2 = 24..48, G3 = 48..72
# =============================================================================
ore_punt = ore_reali(PUNTATA_TARGET, TEMP_AMB)
ore_appr = ore_reali(APPRETTO_TARGET, TEMP_AMB)
if TEMP_AMB >= 35.0:
    ore_punt = 0.0   # troppo caldo: in frigo subito

t_impasto     = float(IMPASTO_ORA)
t_stesura     = 48.0 + STESURA_ORA
t_frigo_start = t_impasto + ore_punt
t_appretto    = t_stesura - ore_appr
ore_frigo     = t_appretto - t_frigo_start

def fmt(t, upper=False):
    """Formatta ore-dalla-mezzanotte-G1 come 'Gx HH:MM' (arrotonda a 5 min)."""
    t_min = math.ceil(t * 60 / 5) * 5
    giorno_idx = int(t_min // (24 * 60))
    nome = f"G{giorno_idx + 1}"
    h = int((t_min % (24 * 60)) // 60)
    m = int(t_min % 60)
    if upper:
        return f"{nome} {h:02d}:{m:02d}"
    return f"{nome:<4} {h:02d}:{m:02d}"

# --- Maturazione: tutto parte dal mixing -------------------------------------
punt_matur  = ore_punt * f_matur(TEMP_AMB)
frigo_matur = max(ore_frigo, 0.0) * f_matur(TEMP_FRIGO)
appr_matur  = ore_appr * f_matur(TEMP_AMB)
matur_tot   = punt_matur + frigo_matur + appr_matur
mat_min, mat_max = ore_maturazione_range(FLOUR_W)

# =============================================================================
# 6) REPORT
# =============================================================================
errori = []
if not (ORA_MIN <= IMPASTO_ORA <= ORA_MAX):
    errori.append(f"IMPASTO_ORA={IMPASTO_ORA} fuori finestra {ORA_MIN}-{ORA_MAX}.")
if ore_frigo < 0:
    errori.append(f"Frigo negativo ({ore_frigo:.1f} h): puntata + appretto non stanno "
                  "nello span. Riduci PUNTATA_TARGET o APPRETTO_TARGET.")

print("=" * 60)
print(f"PIANIFICAZIONE  (T amb={TEMP_AMB:.0f}°C, frigo={TEMP_FRIGO:.0f}°C, W={FLOUR_W})")
print("=" * 60)

if errori:
    print("\n!!!!!!  ERRORE: orari non realizzabili  !!!!!!")
    for e in errori:
        print(f"  - {e}")
    print("\n(Correggi i parametri in cima e rilancia.)")
    sys.exit(1)

print(f"\nFASI A TEMPERATURA AMBIENTE:")
print(f"  Puntata + pieghe (G1): {ore_punt:4.1f} h a {TEMP_AMB:.0f}°C"
      + ("  (saltata: >35°C)" if ore_punt == 0 else ""))
print(f"  Appretto palline (G3): {ore_appr:4.1f} h a {TEMP_AMB:.0f}°C")
print(f"  Frigo che ne risulta : {ore_frigo:4.1f} h a {TEMP_FRIGO:.0f}°C")

print("\nCALENDARIO:")
print(f"  Impasto     {fmt(t_impasto)}")
print(f"  In frigo    {fmt(t_frigo_start)}")
print(f"  Fuori frigo {fmt(t_appretto)}  (palline + appretto)")
print(f"  Stesura     {fmt(t_stesura)}")

print(f"\nMATURAZIONE: {matur_tot:.1f} h-eq   (target W{FLOUR_W}: {mat_min}-{mat_max} h-eq)")
if matur_tot < mat_min:
    print("  -> poca: anticipa IMPASTO_ORA o usa farina più debole")
elif matur_tot > mat_max:
    print("  -> troppa: posticipa IMPASTO_ORA o usa farina più forte")
else:
    print("  -> maturazione nel range per questa farina")

note = []
if ore_frigo < 12:
    note.append(f"frigo solo {ore_frigo:.1f} h: anticipa IMPASTO_ORA per allungarlo")
if TEMP_AMB >= 24:
    note.append(f"fa caldo ({TEMP_AMB:.0f}°C): tieni d'occhio la puntata")
if note:
    print("\nNOTE:")
    for n in note:
        print(f"  ! {n}")

# =============================================================================
# 7) PROCEDURA
# =============================================================================
print("\n" + "=" * 60)
print("PROCEDURA")
print("=" * 60)
print(f"{fmt(t_impasto, upper=True)} — IMPASTO: sciogli lievito in acqua, aggiungi farina, "
      "impasta. Aggiungi sale a metà incordatura, olio alla fine.")
if ore_punt > 0:
    print(f"   Puntata {ore_punt:.1f} h a tamb con pieghe ogni 30 min, poi in frigo.")
else:
    print("   In frigo subito (fa troppo caldo).")
print(f"   FRIGO {ore_frigo:.0f} h.")
print(f"{fmt(t_appretto, upper=True)} — fuori dal frigo: staglio, palline, "
      f"appretto {ore_appr:.1f} h a tamb.")
print(f"{fmt(t_stesura, upper=True)} — STESURA.")


