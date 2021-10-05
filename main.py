import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
import json

budgetMin = 300
budgetMax = 7000
assortmentMin = 5
assortmentMax = 30
crowdednessMin = 0
crowdednessMax = 30
barNames = ["Дом Ани", "Пьяная Свинья", "Бюро Дезинформации", "KillFish", "Цех этого города", "Видеосалон Закрыт", "Руки Вверх", "Harat's Pub", "Rock Bar", "Urban Pub", "Sgt.Pepper's Bar", "Большая Рыба", "Раковая №1", "Архитектор Бар", "McKey", "La Villa", "Томми Ли", "Funky Food", "Holly Place", "Apollo Bar"]


budget_universe = np.arange(budgetMin, budgetMax + 1, 1)
assortment_universe = np.arange(assortmentMin, assortmentMax + 1, 1)
crowdedness_universe = np.arange(crowdednessMin, crowdednessMax + 1, 1)
target_universe = np.arange(1, len(barNames) + 1, 1)

with open("dataset.json", "r") as read_file:
    data = json.load(read_file)

budgetMean = np.mean(data['budget'])
budgetStd = np.std(data['budget'])
assortmentMean = np.mean(data['assortment'])
assortmentStd = np.std(data['assortment'])
crowdednessMean = np.mean(data['crowdedness'])
crowdednessStd = np.std(data['crowdedness'])


budget = ctrl.Antecedent(budget_universe, 'budget')
assortment = ctrl.Antecedent(assortment_universe, 'assortment')
crowdedness = ctrl.Antecedent(crowdedness_universe, 'crowdedness')
target = ctrl.Consequent(target_universe, 'target')

budget['low'] = fuzz.trapmf(budget_universe, [budgetMin, budgetMin, round(budgetMean - 1.5 * budgetStd), round(budgetMean - 0.5 * budgetStd)])
budget['medium'] = fuzz.trapmf(budget_universe, [round(budgetMean - 1.5 * budgetStd), round(budgetMean - 0.5 * budgetStd), round(budgetMean + 0.5 * budgetStd), round(budgetMean + 1.5 * budgetStd)])
budget['high'] = fuzz.trapmf(budget_universe, [round(budgetMean + 0.5 * budgetStd), round(budgetMean + 1.5 * budgetStd), budgetMax, budgetMax])

assortment['small'] = fuzz.trapmf(assortment_universe, [assortmentMin, assortmentMin, round(assortmentMean - 1.5 * assortmentStd), round(assortmentMean - 0.5 * assortmentStd)])
assortment['medium'] = fuzz.trapmf(assortment_universe, [round(assortmentMean - 1.5 * assortmentStd), round(assortmentMean - 0.5 * assortmentStd), round(assortmentMean + 0.5 * assortmentStd), round(assortmentMean + 1.5 * assortmentStd)])
assortment['wide'] = fuzz.trapmf(assortment_universe, [round(assortmentMean + 0.5 * assortmentStd), round(assortmentMean + 1.5 * assortmentStd), assortmentMax, assortmentMax])

crowdedness['low'] = fuzz.trapmf(crowdedness_universe, [crowdednessMin, crowdednessMin, round(crowdednessMean - 1.5 * crowdednessStd), round(crowdednessMean - 0.5 * crowdednessStd)])
crowdedness['medium'] = fuzz.trapmf(crowdedness_universe, [round(crowdednessMean - 1.5 * crowdednessStd), round(crowdednessMean - 0.5 * crowdednessStd), round(crowdednessMean + 0.5 * crowdednessStd), round(crowdednessMean + 1.5 * crowdednessStd)])
crowdedness['high'] = fuzz.trapmf(crowdedness_universe, [round(crowdednessMean + 0.5 * crowdednessStd), round(crowdednessMean + 1.5 * crowdednessStd), crowdednessMax, crowdednessMax])

target.automf(len(barNames), names=barNames)

print("Введите ваш бюджет:")
x = input()
print("Введите желаемое количество напитков:")
y = input()
print("Введите желаемое количество людей в баре:")
z = input()

budget.view()
assortment.view()
crowdedness.view()
target.view()
plt.show()

rule0 = ctrl.Rule(antecedent=((budget['low'] & assortment['small'] & crowdedness['low']) |
                              (budget['low'] & assortment['small'] & crowdedness['medium'])),
                  consequent=target['Дом Ани'])
rule1 = ctrl.Rule(antecedent=((budget['low'] & assortment['medium'] & crowdedness['low']) |
                              (budget['low'] & assortment['medium'] & crowdedness['medium'])),
                  consequent=target['Бюро Дезинформации'])

rule2 = ctrl.Rule(antecedent=((budget['low'] & assortment['wide'] & crowdedness['low']) |
                              (budget['low'] & assortment['wide'] & crowdedness['medium']) |
                              (budget['low'] & assortment['wide'] & crowdedness['high'])
                              ),
                  consequent=target['Цех этого города'])

rule3 = ctrl.Rule(antecedent=((budget['medium'] & assortment['small'] & crowdedness['low']) |
                              (budget['medium'] & assortment['small'] & crowdedness['medium'])),
                  consequent=target['Видеосалон Закрыт'])

rule4 = ctrl.Rule(budget['medium'] & assortment['medium'] & crowdedness['medium'], target['Rock Bar'])

rule5 = ctrl.Rule(budget['medium'] & assortment['wide'] & crowdedness['low'], target['Urban Pub'])

rule6 = ctrl.Rule(antecedent=((budget['high'] & assortment['small'] & crowdedness['medium']) |
                              (budget['high'] & assortment['small'] & crowdedness['high'])),
                  consequent=target['Раковая №1'])

rule7 = ctrl.Rule(antecedent=((budget['high'] & assortment['wide'] & crowdedness['low']) |
                              (budget['high'] & assortment['wide'] & crowdedness['medium'])),
                  consequent=target['Томми Ли'])

rule8 = ctrl.Rule(budget['low'] & assortment['small'] & crowdedness['high'], target['Пьяная Свинья'])
rule9 = ctrl.Rule(budget['low'] & assortment['medium'] & crowdedness['high'], target['KillFish'])
rule10 = ctrl.Rule(budget['medium'] & assortment['small'] & crowdedness['high'], target['Руки Вверх'])
rule11 = ctrl.Rule(budget['medium'] & assortment['medium'] & crowdedness['low'], target["Harat's Pub"])
rule12 = ctrl.Rule(budget['medium'] & assortment['medium'] & crowdedness['high'], target['Apollo Bar'])
rule13 = ctrl.Rule(budget['medium'] & assortment['wide'] & crowdedness['medium'], target['Funky Food'])
rule14 = ctrl.Rule(budget['medium'] & assortment['wide'] & crowdedness['high'], target["Sgt.Pepper's Bar"])
rule15 = ctrl.Rule(budget['high'] & assortment['small'] & crowdedness['low'], target['Большая Рыба'])
rule16 = ctrl.Rule(budget['high'] & assortment['medium'] & crowdedness['low'], target['Архитектор Бар'])
rule17 = ctrl.Rule(budget['high'] & assortment['medium'] & crowdedness['medium'], target['McKey'])
rule18 = ctrl.Rule(budget['high'] & assortment['medium'] & crowdedness['high'], target['La Villa'])
rule19 = ctrl.Rule(budget['high'] & assortment['wide'] & crowdedness['high'], target['Holly Place'])

rule5.view()
plt.show()
bar_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11,
                               rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19])
bar_choice = ctrl.ControlSystemSimulation(bar_ctrl)

bar_choice.input['budget'] = int(x)
bar_choice.input['assortment'] = int(y)
bar_choice.input['crowdedness'] = int(z)


bar_choice.compute()
print(bar_choice.output['target'])
print(barNames[int(round(bar_choice.output['target'])) - 1])
target.view(sim=bar_choice)
data["budget"].append(int(x))
data["assortment"].append(int(y))
data["crowdedness"].append(int(z))
with open("dataset.json", "w") as write_file:
    json.dump(data, write_file)
plt.show()










