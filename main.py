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

assortment['low'] = fuzz.trimf(assortment_universe, [5, 10, 15])
assortment['medium'] = fuzz.trapmf(assortment_universe, [10, 15, 20, 25])
assortment['high'] = fuzz.trimf(assortment_universe, [20, 25, 30])

crowdedness['low'] = fuzz.trimf(crowdedness_universe, [0, 5, 8])
crowdedness['medium'] = fuzz.gauss2mf(crowdedness_universe, 10, 0.5, 13, 0.5)
crowdedness['high'] = fuzz.trimf(crowdedness_universe, [20, 25, 30])

barNames = ["а", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t"]
target.automf(20, names=barNames)

budget.view()
assortment.view()
crowdedness.view()
target.view()
plt.show()