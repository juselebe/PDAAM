"""
Volume average stiffness method
 Juan Sebastian Leon Becerra  UIS
Juselebe@gmail.com
"""
import numpy as np
import math as mt
import micromechanics as mic
import patrones
#data definition of geometrical and process parameters
#Height H, width W, thickness T and number of layers N

VAScalc(240.9,12.7,2,0.2,12.5,0.1,1,1,10,0,8)

def VAScalc(H,W,T,W_shell=0,W_fiber,T_layer,N_floor,N_ceiling,N_solid,N_infill,N_fiber):
    """
    Función calculo total usando el metodo de VAS|
    """
    V_ten=H*W*T
    V_floor=(W-W_shell*2)*H*T_layer*N_floor
    V_ceiling=(W-W_shell*2)*H*T_layer*N_ceiling
    V_solid=(W-W_shell*2)*H*T_layer*N_solid
    V_infill=(W-W_shell*2)*H*T_layer*N_infill
    V_infillfiber=(W-W_shell*2)*H*T_layer*N_fiber
    V_fiber=W_fiber*H*T_layer*N_fiber
    V_shell=H*W_shell*2*T
    #Volumetric fractions
    Vf_floor=V_floor/V_ten
    Vf_ceiling=V_ceiling/V_ten
    Vf_solid=V_solid/V_ten
    Vf_infill=V_infill/V_ten
    Vf_fiber=V_fiber/V_ten
    Vf_shell=V_shell/V_ten
    #resultados=[H,W]
    #print("tolis")
    return
#Definition of the volume in function of geometrical and process parameters

#Volume averaging

#Definition of material properties
E=940 #Matrix young modulus MPA
nu=0.39 #Matrix Poisson ratio
G=E/(2*(1+nu))
p_1=.1 #Porosity value
# Capas sólidas
Engsolid=patrones.solid(E,G,nu,p_1)
#Capas infill
Enginfill=patrones.solid(E,G,nu,.05)
##Capas de refuerzo
Engfiber=mic.mechcar(19890,940,0.33,0.1,0.39)#Ef,Em,V_f,nu_f,nu_m
#Creation of the stiffness matrices
def stiff(a):
    S=np.array([[1/a[0],-a[8]/a[1],-a[10]/a[2],0,0,0],[-a[6]/a[0],1/a[1],-a[11]/a[2],0,0,0], \
                [-a[9]/a[0],-a[9]/a[1],1/a[2],0,0,0],[0,0,0,1/a[5],0,0],[0,0,0,0,1/a[4],0],[0,0,0,0,0,1/a[3]]])
    return S

S_solid=stiff(Engsolid)
S_shell=S_solid
S_ceiling=S_solid
S_floor=S_solid
S_fiber=stiff(Engfiber)
S_infill=stiff(Enginfill)
#S=np.array([[1/E_1,-nu_21/E_2,-nu_31/E_3,0,0,0],[-nu_12/E_1,1/E_2,-nu_32/E_3,0,0,0], \
   #             [-nu_13/E_1,-nu_23/E_2,1/E_3,0,0,0],[0,0,0,1/G_23,0,0],[0,0,0,0,1/G_13,0],[0,0,0,0,0,1/G_12]])
#Rotation of the stiffness Matrix and findind compliance
def rotmat(S,theta):
    theta=theta*mt.pi/180 #angulo en radianes
    c=mt.cos(theta)
    s=mt.sin(theta)
    Tm=np.array([[c**2,s**2,0,0,0,2*c*s],[s**2,c**2,0,0,0,-2*c*s], \
                [0,0,1,0,0,0],[0,0,0,c,s,0],[0,0,0,-s,c,0],[-c*s,c*s,0,0,0,c**2-s**2]])
    S_XY=Tm.transpose()*S*Tm
    C_xy=np.linalg.inv(S_XY)
    return C_xy
C_xysolid=rotmat(S_solid,0)
C_xyfloor=rotmat(S_floor,0)
C_xyceiling=rotmat(S_ceiling,0)
C_xyfiber=rotmat(S_fiber,0)
C_xyshell=rotmat(S_shell,0)
C_xyinfill=rotmat(S_infill,0)
#Summing all the compliances matrices, finding equivalent stiffness and eng constants

C_g=Vf_infill*C_xyinfill+Vf_floor*C_xyfloor+Vf_fiber*C_xyfiber+\
    Vf_shell*C_xyshell++Vf_solid*C_xysolid

S_g=np.linalg.inv(C_g)
E_x=1/S_g[0,0]
E_y=1/S_g[1,1]
E_z=1/S_g[2,2]
G_xy=1/S_g[5,5]
G_yz=1/S_g[3,3]
G_xz=1/S_g[4,4]
nu_xy=-S_g[0,1]/S_g[0,0]
nu_zx=-S_g[0,2]/S_g[2,2]
nu_yz=-S_g[1,2]/S_g[1,1]
#print (V_ten,V_floor,V_ceiling)
#print ("Matriz rotada S",C_g)
print ("Ex",E_x)
#print(Engfiber)
