from sympy import Symbol, Add, Eq, pprint, init_printing, expand

ditc1 = {"P01":{"F1":0.4,"P02":0.6}, "P02":{"F2":0.3, "P03":0.7}, "P03":{"F3":0.2, "P02":0.8}}

expressions = []
for p, equation_components in ditc1.items():
    p = Symbol(p)
    expression = []
    for name, multiplier in equation_components.items():
        expression.append(Symbol(name) * multiplier)
    expressions.append(Eq(p, Add(*expression)))

for expr in expressions:
    pprint(expr)

n = 2
init_printing()
a = Symbol('a')
b = Symbol('b')
e = (a+b)**n
print(expand(e))




# A1
# A1toT = 0 * taxaTrancar
# #A1toT = 0.15 * taxaTrancar
# A1toA1R = 0.3 * taxaRetencao
# A1toE = 0.1 * taxaEvasao
# A1toA2 = 1 - A1toA1R - A1toE - A1toT
# TtoA1 = 0.1 * taxaVoltar
#
# # A1R
# A1RtoT = A1toT * taxaTrancarR * taxaProporcaoTrancar
# A1RtoE = A1toE * taxaEvasaoR * taxaProporcaoEvasao
# A1RtoA2R = 1 - A1RtoE - A1RtoT
# TtoA1R = 0.1 * taxaVoltar

ditc = {"PA1":{"F1":0.4,"P02":0.6}}

expressions = []
for p, equation_components in ditc.items():
    p = Symbol(p)
    expression = []
    for name, multiplier in equation_components.items():
        expression.append(Symbol(name) * multiplier)
    expressions.append(Eq(p, Add(*expression)))

for expr in expressions:
    pprint(expr)