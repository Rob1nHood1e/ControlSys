import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

budget_universe = np.arange(300, 7001, 1)
assortment_universe = np.arange(5, 31, 1)
crowdedness_universe = np.arange(0, 31, 1)
target_universe = np.arange(1, 21, 1)

budget = ctrl.Antecedent(np.arange(300, 7001, 1), 'budget')
assortment = ctrl.Antecedent(np.arange(5, 31, 1), 'assortment')
crowdedness = ctrl.Antecedent(np.arange(0, 31, 1), 'crowdedness')
target = ctrl.Consequent(np.arange(1, 21, 1), 'target')

budget['low'] = fuzz.trimf(budget_universe, [300, 500, 1000])
budget['medium'] = fuzz.gauss2mf(budget_universe, 1500, 0.5, 3000, 0.5)
budget['high'] = fuzz.trimf(budget_universe, [3000, 5000, 7000])

assortment['small'] = fuzz.trimf(assortment_universe, [5, 10, 15])
assortment['medium'] = fuzz.trapmf(assortment_universe, [10, 15, 20, 25])
assortment['wide'] = fuzz.trimf(assortment_universe, [20, 25, 30])

crowdedness['low'] = fuzz.trimf(crowdedness_universe, [0, 5, 8])
crowdedness['medium'] = fuzz.gauss2mf(crowdedness_universe, 10, 0.5, 13, 0.5)
crowdedness['high'] = fuzz.trimf(crowdedness_universe, [20, 25, 30])

barNames = ["Дом Ани", "Пьяная Свинья", "Бюро Дезинформации", "KillFish", "Цех этого города", "Видеосалон Закрыт", "Руки Вверх", "Harat's Pub", "Rock Bar", "Urban Pub", "Sgt.Pepper's Bar", "Большая Рыба", "Раковая №1", "Архитектор Бар", "McKey", "La Villa", "Томми Ли", "Funky Food", "Holly Place", "Apollo Bar"]
target.automf(20, names=barNames)

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

bar_choice.input['budget'] = 700
bar_choice.input['assortment'] = 15
bar_choice.input['crowdedness'] = 5


bar_choice.compute()
print(bar_choice.output['target'])
print(barNames[int(round(bar_choice.output['target'])) - 1])
target.view(sim=bar_choice)
plt.show()










