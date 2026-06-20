""" Pizza con biga """

import sys
import math
try:
    sys.stdout.reconfigure(encoding="utf-8")  # per il simbolo ° su console Windows
except AttributeError:
    pass

# =============================================================================
# 1) CONFIG INGREDIENTI  (tutte le percentuali sono sulla farina = baker's %)
#    Esempio: 0.70 = 70%, 0.025 = 2.5%
# =============================================================================
# pizza 09/05/2026 [0.70, 0.025, 0.0053, 0.0, 0.0, 250, 7] [0.40, 0.44, 0.01]
INGREDIENTS_LIST = [0.70, 0.025, 0.0053, 0.0, 0.0, 250, 7]
BIGA_LIST        = [0.40, 0.44, 0.01]

WATER_PERCENTAGE      = INGREDIENTS_LIST[0]  # %  acqua totale sulla farina      (0.70 = 70%)
SALT_PERCENTAGE       = INGREDIENTS_LIST[1]  # %  sale sulla farina              (0.025 = 2.5%)
YEAST_PERCENTAGE      = INGREDIENTS_LIST[2]  # %  lievito totale (biga+rinfresco)
OIL_PERCENTAGE        = INGREDIENTS_LIST[3]  # %  olio sulla farina
MALT_PERCENTAGE       = INGREDIENTS_LIST[4]  # %  malto sulla farina

BIGA_PERCENTAGE       = BIGA_LIST[0]         # %  quota di farina che va in biga  (0.40 = 40%)
BIGA_WATER_PERCENTAGE = BIGA_LIST[1]         # %  idratazione della biga          (classica ~44%)
BIGA_YEAST_PERCENTAGE = BIGA_LIST[2]         # %  lievito sulla farina di biga    (classica ~1%)

PANETTO_WEIGHT = INGREDIENTS_LIST[5]         # g  peso obiettivo di un panetto
PIZZA_NUMBER   = INGREDIENTS_LIST[6]         #    numero di panetti

# =============================================================================
# 2) CONFIG FERMENTAZIONE
# =============================================================================
TEMP_AMB   = 22.0  # °C  temperatura ambiente di casa  <-- il parametro principale da cambiare
TEMP_FRIGO =  4.0  # °C  temperatura del frigo
FLOUR_W    =  330  #     forza della farina (W): debole <240, media 240-320, forte >320

# BIGA_ORA e IMPASTO_ORA sono INPUT dell'utente, non calcolati:
# tu scegli a che ora vuoi iniziare la biga e a che ora vuoi fare l'impasto.
# Lo script usa questi due orari per calcolare il split tamb/frigo della biga
# (quanto tenerla fuori e quanto in frigo) in modo che sia pronta esattamente
# all'ora dell'impasto. Se gli orari sono impossibili per la temperatura data,
# lo script segnala l'errore e suggerisce quanto modificare il lievito.
BIGA_ORA    = 20  # h  ora del Giorno 1 in cui parti con la biga    [ORA_MIN..ORA_MAX]
IMPASTO_ORA = 10  # h  ora del Giorno 2 in cui fai l'impasto        [ORA_MIN..ORA_MAX]
STESURA_ORA = 19  # h  ora del Giorno 3 in cui stendi (di solito fisso)
ORA_MIN     =  8  # h  |-- finestra oraria ammessa per BIGA_ORA
ORA_MAX     = 22  # h  |   e IMPASTO_ORA; fuori range = errore

# --- Parametri fisici del modello Q10 (NON toccarli, sono valori di letteratura) ---
# Ogni fase (T °C, durata h) equivale a: ore * Q10^((T - REF_TEMP) / 10) "ore-equivalenti"
# a REF_TEMP. Lievitazione e maturazione hanno Q10 diversi: il frigo rallenta molto
# più la lievitazione che la maturazione, ed è per questo che matura senza esplodere.
# Q10_LIEV e Q10_MATUR sono valori misurati in letteratura su lievito ed enzimi in
# laboratorio: non dipendono dalla tua cucina o farina, non richiedono calibrazione.
REF_TEMP  = 20.0  # °C  temperatura di riferimento per le ore-equivalenti
Q10_LIEV  =  2.2  #     accelerazione LIEVITAZIONE ogni +10 °C  (letteratura: 2.0-2.5)
Q10_MATUR =  1.5  #     accelerazione MATURAZIONE ogni +10 °C   (letteratura: 1.3-1.7)

# --- Obiettivi biologici (ore-equivalenti a REF_TEMP) ---
# Anche questi NON richiedono calibrazione personale: vengono dalle buone pratiche
# standard della panificazione. Al limite, se noti che la tua biga è sempre troppo
# pronta o non abbastanza, puoi aggiustare BIGA_TARGET di qualche unità.
BIGA_TARGET     = 15.0  # h-eq  prontezza target della biga. Viene dalla ricetta classica:
                        #       1% lievito × 18h a 18°C = ~15 h-eq. È una convenzione
                        #       del mondo della panificazione, non una misura personale.
BIGA_YEAST_REF  =  0.01 # %    NON TOCCARE. Costante di calibrazione: dice che BIGA_TARGET
                        #       è stato misurato con l'1% di lievito. Se cambi il lievito
                        #       (BIGA_YEAST_PERCENTAGE in BIGA_LIST), lo script scala
                        #       automaticamente le ore reali. Es: 2% → metà ore reali.
# PUNTATA_TARGET e APPRETTO_TARGET sono input (quanto "lavoro biologico" vuoi in quella
# fase), non ore reali. Le ore reali vengono calcolate e stampate nel report: a 20°C
# coincidono coi valori qui sotto, a temperature più alte durano meno (es. a 29°C:
# puntata ~1h reale, appretto ~2h reali). Valori dalle buone pratiche standard.
PUNTATA_TARGET  =  2.0  # h-eq  lavoro biologico target per la puntata
APPRETTO_TARGET =  4.0  # h-eq  lavoro biologico target per l'appretto

# =============================================================================
# 3) CALCOLO INGREDIENTI
# =============================================================================
DOUGH_WEIGHT = PANETTO_WEIGHT * PIZZA_NUMBER

# farina * (1 + acqua% + sale% + olio% + lievito% + malto%) = peso impasto
FLOUR = DOUGH_WEIGHT / (1 + WATER_PERCENTAGE + SALT_PERCENTAGE
                        + OIL_PERCENTAGE + YEAST_PERCENTAGE + MALT_PERCENTAGE)
WATER = FLOUR * WATER_PERCENTAGE
YEAST = FLOUR * YEAST_PERCENTAGE
print(f"Dough weight = {DOUGH_WEIGHT:.0f} g")
print(f"Flour weight = {FLOUR:.0f} g")
print(f"Water weight = {WATER:.0f} g")
print(f"Yeast weight = {YEAST:.2f} g\n")

BIGA_FLOUR = FLOUR * BIGA_PERCENTAGE
BIGA_WATER = BIGA_FLOUR * BIGA_WATER_PERCENTAGE
BIGA_YEAST = BIGA_FLOUR * BIGA_YEAST_PERCENTAGE
BIGA_WEIGHT = BIGA_FLOUR + BIGA_WATER + BIGA_YEAST
print(f"Biga weight = {BIGA_WEIGHT:.0f} g")
print(f"Biga flour = {BIGA_FLOUR:.0f} g")
print(f"Biga water = {BIGA_WATER:.0f} g")
print(f"Biga yeast = {BIGA_YEAST:.2f} g\n")

RINFRESCO_FLOUR = FLOUR - BIGA_FLOUR
RINFRESCO_WATER = WATER - BIGA_WATER
RINFRESCO_YEAST = YEAST - BIGA_YEAST
SALT  = FLOUR * SALT_PERCENTAGE
OIL   = FLOUR * OIL_PERCENTAGE
MALT  = FLOUR * MALT_PERCENTAGE
RINFRESCO_WEIGHT = DOUGH_WEIGHT - BIGA_WEIGHT

if RINFRESCO_YEAST < 0:
    print(f"!! ATTENZIONE: lievito biga ({BIGA_YEAST:.2f} g) > lievito totale "
          f"({YEAST:.2f} g): nessun lievito nel rinfresco.\n")
    RINFRESCO_YEAST = 0.0

print(f"Rinfresco weight = {RINFRESCO_WEIGHT:.0f} g")
print(f"Rinfresco flour  = {RINFRESCO_FLOUR:.0f} g")
print(f"Rinfresco water  = {RINFRESCO_WATER:.0f} g")
print(f"Rinfresco yeast  = {RINFRESCO_YEAST:.2f} g")
print(f"salt = {SALT:.1f} g")
print(f"oil  = {OIL:.1f} g")
print(f"malt = {MALT:.1f} g\n")

# =============================================================================
# 4) MODELLO Q10: funzioni di base
# =============================================================================
def f_liev(temp):
    return Q10_LIEV ** ((temp - REF_TEMP) / 10.0)

def f_matur(temp):
    return Q10_MATUR ** ((temp - REF_TEMP) / 10.0)

def ore_reali(target_heq, temp):
    """Ore reali necessarie a 'temp' per accumulare 'target_heq' ore-equivalenti."""
    return target_heq / f_liev(temp)

def ore_maturazione_range(w):
    """Range consigliato di ore-equivalenti di maturazione per W della farina."""
    if w < 240:  return (6, 12)
    if w < 280:  return (12, 24)
    if w < 320:  return (24, 48)
    if w < 360:  return (48, 72)
    return (72, 96)

# =============================================================================
# 5) TEMPI A TEMPERATURA AMBIENTE (puntata e appretto)
# =============================================================================
ore_punt = ore_reali(PUNTATA_TARGET, TEMP_AMB)
ore_appr = ore_reali(APPRETTO_TARGET, TEMP_AMB)
if TEMP_AMB >= 35.0:
    ore_punt = 0.0   # troppo caldo: impasto in frigo subito

# =============================================================================
# 6) CALENDARIO (ore dalla mezzanotte di GIORNO_BIGA)
#    Giorno 1 = 0..24, Giorno 2 = 24..48, Giorno 3 = 48..72
# =============================================================================
t_biga    = float(BIGA_ORA)
t_impasto = 24.0 + IMPASTO_ORA
t_stesura = 48.0 + STESURA_ORA

def fmt(t, upper=False):
    """Formatta ore-dalla-mezzanotte-G1 come 'Gx HH:MM' (arrotonda a 5 min)."""
    t_min = math.ceil(t * 60 / 5) * 5
    giorno_idx = int(t_min // (24 * 60))
    nome = f"G{giorno_idx + 1}"
    h = int((t_min % (24 * 60)) // 60)
    m = int(t_min % 60)
    if upper:
        return f"{nome} {h:02d}:{m:02d}"
    return f"{nome:<9} {h:02d}:{m:02d}"

# --- Biga a due fasi (tamb + frigo) per centrare l'ora dell'impasto ---------
# Obiettivo: accumulare BIGA_TARGET h-eq tra t_biga e t_impasto.
# Il lievito effettivo scala linearmente: più lievito = più veloce.
span_biga   = t_impasto - t_biga
ym          = BIGA_YEAST_PERCENTAGE / BIGA_YEAST_REF   # fattore lievito
v_amb       = f_liev(TEMP_AMB)   * ym   # h-eq/h a tamb (con ym)
v_frigo     = f_liev(TEMP_FRIGO) * ym   # h-eq/h in frigo (con ym)
acc_max     = span_biga * v_amb          # accumulo se tutta a tamb
acc_min     = span_biga * v_frigo        # accumulo se tutta in frigo

errori = []
if not (ORA_MIN <= BIGA_ORA <= ORA_MAX):
    errori.append(f"BIGA_ORA={BIGA_ORA} fuori finestra {ORA_MIN}-{ORA_MAX}.")
if not (ORA_MIN <= IMPASTO_ORA <= ORA_MAX):
    errori.append(f"IMPASTO_ORA={IMPASTO_ORA} fuori finestra {ORA_MIN}-{ORA_MAX}.")

biga_tamb_h, biga_frigo_h = span_biga, 0.0
if not errori:
    if BIGA_TARGET > acc_max:
        y_sug = BIGA_TARGET / (span_biga * f_liev(TEMP_AMB)) * BIGA_YEAST_REF
        errori.append(
            "BIGA NON PRONTA IN TEMPO con questi orari/temperatura. Rimedi:\n"
            f"      - alza BIGA_YEAST_PERCENTAGE a ~{y_sug*100:.2f}%"
            f" (attuale {BIGA_YEAST_PERCENTAGE*100:.2f}%) → fermenta prima\n"
            f"      - oppure anticipa BIGA_ORA o posticipa IMPASTO_ORA")
    elif BIGA_TARGET < acc_min:
        y_sug = BIGA_TARGET / (span_biga * f_liev(TEMP_FRIGO)) * BIGA_YEAST_REF
        errori.append(
            "BIGA TROPPO VELOCE: strafermenta anche tutta in frigo. Rimedi:\n"
            f"      - cala BIGA_YEAST_PERCENTAGE a <= {y_sug*100:.2f}%"
            f" (attuale {BIGA_YEAST_PERCENTAGE*100:.2f}%) → rallenta\n"
            f"      - oppure posticipa BIGA_ORA o anticipa IMPASTO_ORA")
    else:
        biga_tamb_h  = (BIGA_TARGET - span_biga * v_frigo) / (v_amb - v_frigo)
        biga_frigo_h = span_biga - biga_tamb_h

t_biga_frigo = t_biga + biga_tamb_h   # ora in cui la biga entra in frigo

# --- Frigo dell'impasto (riempie lo spazio rimasto fino all'appretto) --------
t_frigo_impasto = t_impasto + ore_punt
t_appretto      = t_stesura - ore_appr
ore_frigo       = t_appretto - t_frigo_impasto

# --- Maturazione pesata -------------------------------------------------------
# La farina della biga matura da subito (biga + tutto il post-impasto).
# La farina del rinfresco matura solo dal momento dell'impasto.
biga_matur  = biga_tamb_h * f_matur(TEMP_AMB) + biga_frigo_h * f_matur(TEMP_FRIGO)
punt_matur  = ore_punt * f_matur(TEMP_AMB)
frigo_matur = max(ore_frigo, 0.0) * f_matur(TEMP_FRIGO)
appr_matur  = ore_appr * f_matur(TEMP_AMB)
post_matur  = punt_matur + frigo_matur + appr_matur
matur_tot   = (BIGA_PERCENTAGE * (biga_matur + post_matur)
               + (1 - BIGA_PERCENTAGE) * post_matur)

mat_min, mat_max = ore_maturazione_range(FLOUR_W)

# =============================================================================
# 7) REPORT
# =============================================================================
print("=" * 64)
print(f"PIANIFICAZIONE  (T amb={TEMP_AMB:.0f}°C, frigo={TEMP_FRIGO:.0f}°C, W={FLOUR_W})")
print("=" * 64)

if errori:
    print("\n!!!!!!  ERRORE: orari non realizzabili  !!!!!!")
    for e in errori:
        print(f"  - {e}")
    print("\n(Correggi i parametri in cima e rilancia.)")
    sys.exit(1)

print(f"\nBIGA (Giorno 1), split tamb/frigo per centrare l'impasto:")
print(f"  a tamb  : {biga_tamb_h:5.1f} h a {TEMP_AMB:.0f}°C")
if biga_frigo_h > 0.05:
    print(f"  in frigo: {biga_frigo_h:5.1f} h a {TEMP_FRIGO:.0f}°C  (parcheggio)")
else:
    print(f"  in frigo:   --    (non necessario)")

print(f"\nFASI POST-IMPASTO a temperatura ambiente:")
print(f"  Puntata (G2) : {ore_punt:4.1f} h a {TEMP_AMB:.0f}°C"
      + ("  (saltata: >35°C, in frigo subito)" if ore_punt == 0 else ""))
print(f"  Appretto (G3): {ore_appr:4.1f} h a {TEMP_AMB:.0f}°C")
print(f"  Frigo impasto            : {ore_frigo:4.1f} h a {TEMP_FRIGO:.0f}°C")

print("\nCALENDARIO:")
print(f"  Biga avvio    {fmt(t_biga)}")
if biga_frigo_h > 0.05:
    print(f"  Biga in frigo {fmt(t_biga_frigo)}")
print(f"  Impasto       {fmt(t_impasto)}")
print(f"  In frigo      {fmt(t_frigo_impasto)}")
print(f"  Fuori frigo   {fmt(t_appretto)}  (palline + appretto)")
print(f"  Stesura       {fmt(t_stesura)}")

print(f"\nMATURAZIONE: {matur_tot:.1f} h-eq   (target W{FLOUR_W}: {mat_min}-{mat_max} h-eq)")
if matur_tot < mat_min:
    print(f"  -> poca: anticipa IMPASTO_ORA o usa farina più debole")
elif matur_tot > mat_max:
    print(f"  -> troppa: posticipa IMPASTO_ORA o usa farina più forte")
else:
    print(f"  -> maturazione nel range per questa farina")

note = []
if ore_frigo < 8:
    note.append(f"frigo impasto solo {ore_frigo:.1f} h: anticipa IMPASTO_ORA per allungarlo")
if TEMP_AMB >= 24:
    note.append(f"fa caldo ({TEMP_AMB:.0f}°C): controlla la biga, rischia di acidificarsi")
if note:
    print("\nNOTE:")
    for n in note:
        print(f"  ! {n}")

# =============================================================================
# 8) PROCEDURA
# =============================================================================
print("\n" + "=" * 64)
print("PROCEDURA")
print("=" * 64)
print(f"{fmt(t_biga, upper=True)} — BIGA: impasta farina+acqua+lievito (NO sale), "
      "grossolana e sgranata.")
if biga_frigo_h > 0.05:
    print(f"   Lascia {biga_tamb_h:.1f} h a tamb, poi metti in frigo "
          f"({fmt(t_biga_frigo, upper=True)}) per {biga_frigo_h:.1f} h.")
else:
    print(f"   Lascia {biga_tamb_h:.1f} h a tamb fino all'impasto.")
print(f"{fmt(t_impasto, upper=True)} — IMPASTO: sciogli acqua+sale+lievito del rinfresco, "
      "dopo 2 min aggiungi la biga spezzettata, incorda.")
if ore_punt > 0:
    print(f"   Puntata {ore_punt:.1f} h a tamb, poi metti in frigo.")
else:
    print("   Metti in frigo subito.")
print(f"   FRIGO {ore_frigo:.0f} h (capovolgi/ribalta nelle prime ore).")
print(f"{fmt(t_appretto, upper=True)} — fuori dal frigo: staglio, palline, "
      f"appretto {ore_appr:.1f} h a tamb.")
print(f"{fmt(t_stesura, upper=True)} — STESURA.")
