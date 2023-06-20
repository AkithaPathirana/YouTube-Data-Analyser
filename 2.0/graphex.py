from matplotlib import pyplot as plt
plt.style.use('fivethirtyeight')

x1=[1,2,3,4,5]
x2=[1,2,3,4,5,6,7,8,9,10]
y1=[23,56,78,23,56]
y2=[13,86,58,63,36,23,67,89,11,23]

plt.plot(x1,y1,label='The Five')
plt.plot(x2,y2,label='The Ten')

plt.xlabel('The X')
plt.ylabel('The Y')
plt.title('The Graph')
plt.legend()
plt.grid(True)
plt.show()