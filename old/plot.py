# def barplot(title, height, bars):
#     # Make a dataset:
#     y_pos = np.arange(len(bars))
#
#     # Create bars
#     plt.bar(y_pos, height)
#     plt.title(title)
#
#     # Create names on the x-axis
#     plt.xticks(y_pos, bars)
#
#     # Show graphic
#     plt.show()



# # Gráfico Retenção
# barplot("Probabilidade de Retenção", ret, statenames[:5])
# plt.show()
#
# print("\n Probabilidade de Retenção: ")
# print(ret)
#
# # Gráfico Progressão
# dfGE = pd.DataFrame({'Não Retidos': progres[:5],
#                      'Retidos': progres[-5:]}, index=statenames[:5])
# dfGE.plot.bar(rot=0, color={"Não Retidos": "green", "Retidos": "red"}, title="Probabilidade de Progressão")
# plt.show()
#
# print("\n Probabilidade de Progressão: ")
# print(np.round(progres, 4))
#
# # Gráficos Graduação e Evasão individuais
# # barplot("G", probGE.T[0], statenames[:len(statenames)-2])
# # barplot("E", probGE.T[1], statenames[:len(statenames)-2])
#
# # Gráfico Graduação e Evasão Agrupado
# e = probGE.T[1]
# g = probGE.T[0]
#
# dfGE = pd.DataFrame({'Não Retidos': e[:5],
#                      'Retidos': e[-5:]}, index=statenames[:5])
# dfGE.plot.bar(rot=0, color={"Não Retidos": "green", "Retidos": "red"}, title="Probabilidade de Evasão")
# plt.show()
#
# dfGE = pd.DataFrame({'Não Retidos': g[:5],
#                      'Retidos': g[-5:]}, index=statenames[:5])
# dfGE.plot.bar(rot=0, color={"Não Retidos": "green", "Retidos": "red"}, title="Probabilidade de Graduação")
# plt.show()

# Quantidade de anos para simulação
# passosSimu = 10  # Sem trancar
# passosSimu = 18 # Com trancar

# Gráfico do histórico de distribuição
# for x in range(passosSimu):
#     # probalidade dos estado
#     # print(np.round(state, 3))
#     state = np.dot(state, p)
#     stateHist = np.append(stateHist, state, axis=0)
#     dfDistrHist = pd.DataFrame(stateHist, columns=statenames)
#
# dfDistrHist.plot()
# plt.show()
# print(dfDistrHist)

# Outros
# print(mc.expected_transitions(1))
# print(mc.recurrent_states)
# print(mc.transient_states)
# print(mc.steady_states)
# print(mc.topological_entropy)
# plot_walk(mc, 10, 'A1')