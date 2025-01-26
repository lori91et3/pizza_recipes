
WATER_RATIO = 0.60 # 60%
SALT_RATIO = 0.025 # 2.5%
YEAST_RATIO = 0.0023 # 0.15%
OIL_RATIO = 0.0 # 2.5%

PANETTO_WEIGHT = 220 # g
PIZZA_NUMBER = 3

DOUGHT_WEIGHT = PANETTO_WEIGHT * PIZZA_NUMBER

#flour + water + salt + oil + yeast = dought_weight
#flour + flour*WATER_RATIO + flour*SALT_RATIO + flouf*OIL_RATIO + flour*YEAST_RATIO = dought_weight
FLOUR = DOUGHT_WEIGHT/(1+WATER_RATIO+SALT_RATIO+OIL_RATIO+YEAST_RATIO)
WATER = FLOUR*WATER_RATIO
SALT = FLOUR*SALT_RATIO
OIL = FLOUR*OIL_RATIO
YEAST = FLOUR*YEAST_RATIO
print(f"Dought weight = {DOUGHT_WEIGHT}")
print(f"flour = {FLOUR}")
print(f"water = {WATER}")
print(f"salt = {SALT}")
print(f"oil = {OIL}")
print(f"yeast = {YEAST}")

print("Dopo aver impastato (mettere il sale alla fine), lasciare riposare per 2 ore. Staglio. \
Far fermentare 1-2 ore a temperatura ambiente. Mettere in frigo per 24-48 ore. \
Prima dell'utilizzo riportare l'impasto a temperatura ambiente e lasciarlo fermentare 4-5 ore.")


