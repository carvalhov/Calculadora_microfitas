import math
import numpy as np

print("_______Projeto de Microfitas_______\n")
#impedância característica (100 ohms)
Z0 = float(input("Informe a Impedãncia característica (ohm): "))
#Espessura do diélétrico 'h', também chamado de 'd' (0,158 cm)
h = float(input("Informe a Espessura do dielétrico (cm): "))
#εr: constante dielétrica (2,20)
er = float(input("Informe a Constante dielétrica: "))
#tangente de perdas, baixa tgperdas é um bom dielético, adimensional. 
tgperd = float(input("Informe a tangente de perdas: "))

pi = math.pi
w = float()

"""
  _____Encontrar espessura (W):____
Passo 1: Encotrar parametros A e B, com as informações possuidas
Passo 2: Encontrar o valor da relação entre W/h, pelos parâmetros A e B
Passo 3: Isolar W, como já se sabe h e encontrou a relação W/h, isola W

"""

A = (Z0/60)*(math.sqrt((er+1)/2)) + ((er-1)/(er+1))*(0.23+0.11/er)
print(f'\nParâmetro A = {A:.3f}')

B = (377*pi)/(2*Z0*math.sqrt(er))
print(f'Parâmetro B = {B:.3f}')

if A > 1.52: 
  #w/h < 2
  relation1 = ((8*pow(math.e, A))/(pow(math.e, 2*A) - 2))
  print(f'\nRelação de w/h <= 2, igual a {relation1:.3f}')
  w = relation1*h
  print(f'Espessura da microfita (W): {w:.3f} cm')
else: 
  #w/h >= 2
  relation2 = (2/pi)*(B - 1 - np.log(2*B - 1) + (er-1)/(2*er))*((np.log(B-1)) + 0.39 - 0.61/er)
  print(f'\nRelação de w/h > 2, igual a {relation2:.3f}')
  w = relation2*h
  print(f'Espessura da microfita (W): {w:.3f} cm')

#Encontrar o comprimendo de onda guiado:


x = w/h
y = h/w

if x < 1: 
  print("W/h < 1")
  eeff = ((er+1)/2) + ((er-1)/2)*(math.pow(1+12*(y), -0.5) + 0.04*math.pow(1-(x), 2))
  Z0 = (60/math.sqrt(eeff))*np.log(8*(y)+ 0.25*(x))
else: 
  print("W/h >= 1")
  eeff = ((er+1)/2) + ((er-1)/2)*(math.pow(1+12*(y), -0.5))
  Z0 = (120*pi/math.sqrt(eeff))/(x + 1.393 + 0.667*(np.log(x + 1.444)))


print(f'\nConstante dielétrica efetiva (eeff) = {eeff:,.3f}')
print(f'\nImpedância característica (Z0 - teste) = {Z0:.3f} Ohms')

"""
Encontrar o comprimento de onda guiado(Lambdag):
Passo 1) Encontrar a freqência ou lambda no vácuo

λm = vp/f <=> c/(f*math.sqrt(eeff)) <=> λ0/math.sqrt(eeff)
λm = λ0/math.sqrt(eeff)

constante de fases:
beta = K0*math.sqrt(eeff)
1.00 Np = 8.686 Db

K0 = w/c <=> (2*pi*f)/c <=> 2*pi/λ

f = K0/(2*pi)

λg = 2pi/beta
λg = 2pi/k0*math.sqrt(eeff)
λg = 2pi/(2pif/c)*math.sqrt(eeff)
λg = c/f(Hz)*math.sqrt(eeff)
λg = 300/(f(GHz)*math.sqrt(eeff))

//
c = 29.979 cm/nanosecond
C = λ x f
Speed = Wavelength x Wave Frequency
//

f0 = 0.3*math.pow(Z0/(h*math.sqrt(er-1)), 0.5)
print(f'frequência = {f0:,.2f} GHz')
"""

#Velocidade da Luz no vácuo em m/s
c = 3*10**8
#velocidade de fase
vp = c/(math.sqrt(eeff))
print(f'\nVelocidade de fase: {vp:,.3f} m/s')

#Como a velocidade da luz está no numerador, eu vou dividir por GHz, assim, dá para anular os expoentes 10^(8-9) 
λg = c/(10**9*math.sqrt(eeff))
print(f'\nComprimento de onda guiado: {λg:.4f}/f(GHz)')


"""
Encontre a atenuação devido ao dielétrico
fator de atenunação (α) = αd (perda dielétrica) + αc (perda por condução)
Passo 1) Definir a atenuação do dielétrico

αd = (K0*er*(eeff-1)*tgperd)/(2*math.sqrt(eeff)*(er-1))
K0 = 2pi/λ0

#Encontrar Atenuação devido ao dielétrico:
#unidade diferente
aten_d = 27.3*(er/math.sqrt(eeff))*((eeff -1)/(er-1))*(tgperd/Lambda_guiado) 

αd = 0.9106*math.sqrt(er)*tgperd*f(GHz)
αd = 0.00135 x f(GHz) Db/cm (Da questão exemplo)
"""
#Como divide pela velocidade da luz, eu vou multiplicar por GHz, assim, dá para anular os expoentes 10^(9-8) 
αd = 2*pi*10**9*(er*(eeff-1)*tgperd)/(c*2*math.sqrt(eeff)*(er-1))
print(f'\nAtenuação do dielétrico: {αd:.4f}xf(GHz) Np/m')

f = float(input("Informe a frequência (GHz): "))

λg = λg/f
print(f'\nComprimento de onda guiado: {λg:.4f}')
αd = αd*f
print(f'\nAtenuação do dielétrico: {αd:.4f} Np/m')

