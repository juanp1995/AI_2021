import itertools, re
import numpy as np
# import pylab as plt
# import time

# X = []
# Y = []

# plt.ion()
# # graph, = plt.plot([], [])
# figure, ax = plt.subplots()
# lines, = ax.plot([],[], 'o')
# ax.set_autoscale_on(True)

# x = 0
# y = 0
# for x in range(30):
#     X.append(x)
#     Y.append(y)
#     x+=1
#     y+=1
#     lines.set_xdata(X)
#     lines.set_ydata(Y)
#     ax.relim()
#     ax.autoscale_view()
#     # graph.xlim([min(X), max(X)])
#     # graph.ylim([min(Y), max(Y)])
#     figure.canvas.draw()
#     figure.canvas.flush_events()
#     # plt.draw()
#     # plt.pause(0.5)
#     time.sleep(0.1)

# plt.ioff()
# plot = plt.plot(X,Y)
# plt.show()

l = np.zeros((1, 100), dtype=int)

l[0][0] = 5
l[0][1] = 10

print(l)