""" Pizza con biga """

# pizza 09/05/2026 [0.70, 0.025, 0.0053, 0.0, 0.0, 250, 4] [0.40, 0.44, 0.01]
INGREDIENTS_LIST = [0.70, 0.025, 0.0053, 0.0, 0.0, 250, 4]
BIGA_LIST = [0.40, 0.44, 0.01]

WATER_PERCENTAGE = INGREDIENTS_LIST[0] # 56%
SALT_PERCENTAGE = INGREDIENTS_LIST[1] # 2.5%
YEAST_PERCENTAGE = INGREDIENTS_LIST[2] # 0.3%
OIL_PERCENTAGE = INGREDIENTS_LIST[3] # 0.0%
MALT_PERCENTAGE = INGREDIENTS_LIST[4] # 0.3%

BIGA_PERCENTAGE = BIGA_LIST[0]
BIGA_WATER_PERCENTAGE = BIGA_LIST[1]
BIGA_YEAST_PERCENTAGE = BIGA_LIST[2]

PANETTO_WEIGHT = INGREDIENTS_LIST[5] # g
PIZZA_NUMBER = INGREDIENTS_LIST[6]

DOUGHT_WEIGHT = PANETTO_WEIGHT * PIZZA_NUMBER

# flour + water + salt + oil + yeast + malt = dought_weight
# flour + flour*WATER_PERCENTAGE + flour*SALT_PERCENTAGE + flouf*OIL_PERCENTAGE + flour*YEAST_PERCENTAGE + flour*MALT_PERCENTAGE = dought_weight
FLOUR = DOUGHT_WEIGHT/(1+WATER_PERCENTAGE+SALT_PERCENTAGE+OIL_PERCENTAGE+YEAST_PERCENTAGE+MALT_PERCENTAGE)
WATER = FLOUR*WATER_PERCENTAGE
YEAST = FLOUR*YEAST_PERCENTAGE
print(f"Dought weight = {DOUGHT_WEIGHT}")
print(f"Flour weight = {FLOUR}")
print(f"Water weight = {WATER}")
print(f"Yeast weight = {YEAST}\n")

BIGA_FLOUR = FLOUR*BIGA_PERCENTAGE
BIGA_WATER = BIGA_FLOUR*BIGA_WATER_PERCENTAGE
BIGA_YEAST = BIGA_FLOUR*BIGA_YEAST_PERCENTAGE
BIGA_WEIGHT = BIGA_FLOUR + BIGA_WATER + BIGA_YEAST
print(f"Biga weight = {BIGA_WEIGHT}")
print(f"Biga flour = {BIGA_FLOUR}")
print(f"Biga water = {BIGA_WATER}")
print(f"Biga yeast = {BIGA_YEAST}\n")

RINFRESCO_WEIGHT = DOUGHT_WEIGHT-BIGA_WEIGHT
RINFRESCO_FLOUR = FLOUR - BIGA_FLOUR
RINFRESCO_WATER = WATER-BIGA_WATER
RINFRESCO_YEAST = YEAST - BIGA_YEAST
SALT = FLOUR*SALT_PERCENTAGE
OIL = FLOUR*OIL_PERCENTAGE
MALT = FLOUR*MALT_PERCENTAGE
print(f"Rinfresco weight = {RINFRESCO_WEIGHT}")
print(f"Rinfresco flour = {RINFRESCO_FLOUR}")
print(f"Rinfresco water = {RINFRESCO_WATER}")
print(f"Rinfresco yeast = {RINFRESCO_YEAST}")
print(f"salt = {SALT}")
print(f"oil = {OIL}")
print(f"malt = {MALT}")


print("Preparare la biga e farla fermentare per 18/20 ore a 18 gradi \
Eseguire il rinfresco eseguendo gli ingredienti, dopo due minuti aggiungere la biga spezzettandola in piccole parti \
Lasciare riposare 15 minuti, poi staglio. Mettere in frigo per 24-48 ore ricordando di invertirle dopo le prime ore. \
Prima di utilizzare l'impasto riportarlo a temperatura ambiente lasciando fermentare per 3-4ore."
      )
