import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression

data = pd.read_excel("D:\Kuliah\Big Data\Datareg.xlsx")
data = data.drop("No.",axis = 1)

#Soal no.1
plt.scatter(data.A, data.Sales)
plt.ylabel('Sales')
plt.xlabel('A')
plt.show()

plt.scatter(data.B, data.Sales)
plt.ylabel('Sales')
plt.xlabel('B')
plt.show()

plt.scatter(data.C, data.Sales)
plt.ylabel('Sales')
plt.xlabel('C')
plt.show()

#Soal no.2
print("Persamaan regresi sederhana: y = a + bx")
print("\n")

regr1 = LinearRegression()
regr1.fit(data[['A']], data.Sales)
print("Model regresi dengan variabel bebas A dan variabel terikat Sales:")
print("Nilai Koefisien a : %s" %regr1.intercept_)
print("Nilai Koefisien b : %s" %regr1.coef_)
print("\n")

regr2 = LinearRegression()
regr2.fit(data[['B']], data.Sales)
print("Model regresi dengan variabel bebas B dan variabel terikat Sales:")
print("Nilai Koefisien a : %s" %regr2.intercept_)
print("Nilai Koefisien b : %s" %regr2.coef_)
print("\n")

regr3 = LinearRegression()
regr3.fit(data[['C']], data.Sales)
print("Model regresi dengan variabel bebas C dan variabel terikat Sales:")
print("Nilai Koefisien a : %s" %regr3.intercept_)
print("Nilai Koefisien b : %s" %regr3.coef_)
print("\n")

#Soal no.3
print("Nilai x = 200, untuk model regresi pertama : %s" %regr1.predict([[200]]))
print("Nilai x = 200, untuk model regresi kedua : %s" %regr2.predict([[200]]))
print("Nilai x = 200, untuk model regresi ketiga : %s" %regr3.predict([[200]]))
print("\n")

#Soal no.4
x = data[['A','B','C']]
y = data['Sales']

regr = LinearRegression()
regr.fit(x,y)
print("Model regresi dengan variabel bebas A, B, C dan variabel terikat Sales:")
print("Nilai Koefisien a : %s" %regr.intercept_)
print("Nilai Koefisien b : %s" %regr.coef_)