"""
Module for the calculation of composite properties base on
Micromechanical formulations from the Barbero Book.
By: Juan Sebastian Leon Becerra. Last version: 16/09/2020
"""
import numpy as np
###Calculation of other isotropic constants
#G_f=E_f/(2*(1+nu_f))#Calculation of fiber´s shear modulus.
#G_m=E_m/(2*(1+nu_m))#Calculation of matrix´s shear modulus.
#mu_m=G_m # Mu are the lames constants
#mu_f=G_f
#G_12=((V_f/G_f)+(V_m/G_m))**(-1) # Calculo rigidez transversal
#nu_12=V_f*nu_f+V_m*nu_m # Calculo poisoon ratio
#########FUNCIONES#####
def ROM(f,m,V_f):
    """
    Rule of mixture
    Parameters
        ----------
        f : float
            The propertie value for the fiber phase
        m : float
            The propertie value for the matrix phase
        V_f : float
            The fiber volumetric fiber fraction
    Returns
    -------
    list
        a list of strings in which the first value is the property and the second
        value is the matrix volumetric fraction.
        Test:
    >>>ROM(0.5,0.5,0.5)
    0.25
    """
    Vm=1-V_f
    P=V_f*f+Vm*m
    return P , Vm
def iROM(f,m,V_f):
    """
    Inverse rule of mixture
    Parameters
        ----------
        f : float
            The propertie value for the fiber phase
        m : float
            The propertie value for the matrix phase
        V_f : float
            The fiber volumetric fiber fraction
            Returns
    -------
    Float
        The value of the whole composite property
    """
    Vm=1-V_f
    q=Vm/m+V_f/f
    P=1/q
    return P
def HPTS(f,m,V_f,eta=0.2):
    """
    Halpin-Tsai method
    Parameters
        ----------
        f : float
            The propertie value for the fiber phase
        m : float
            The propertie value for the matrix phase
        V_f : float
            The fiber volumetric fiber fraction
        eta : float, optional
            eta parameter (the default is 0.2)
    Returns
    -------
    Float
        The value of the whole composite property
    """
    nu=((f/m)-1)/((f/m)+eta)
    P=m*((1+eta*nu*V_f)/(1-nu*V_f))
    return P
def SPP(f,m,V_f):
    """
    Stress partitioning-parameter method
    Parameters
        ----------
        f : float
            The propertie value for the fiber phase
        m : float
            The propertie value for the matrix phase
        V_f : float
            The fiber volumetric fiber fraction
            Returns
    -------
    Float
        The value of the whole composite property
    """
    eta_2=0.5*(1+m/f)
    P=m*((V_f+eta_2*(1-V_f))/(eta_2*(1-V_f)+V_f*m/f))
    return P
def SEMSPP(Gf,Gm,nu_f,nu_m,V_f):
    """
    Semi-empirical stress partitioning-parameter method
    Parameters
        ----------
        Gf : float
            The shear modulus value for the fiber phase
        Gm : float
            The shear modulus value for the matrix phase
        nu_f : float
            The Poisson ratio of the fiber.
        nu_m : float
            The Poisson ratio of the matrix.
        V_f : float
            The fiber volumetric fiber fraction
    Returns
    -------
        Float
            The value of the whole composite property
    """
    eta_4=(3-4*nu_m+Gf/Gm)/(4*(1-nu_m))
    P=Gm*((V_f+eta_4*(1-V_f))/(eta_4*(1-V_f)+V_f*Gm/Gf))
    return P
def CAM(f,m,V_f):
    """
    Cylindrical Assemblage method
    Parameters
        ----------
        f : float
            The propertie value for the fiber phase
        m : float
            The propertie value for the matrix phase
        V_f : float
            The fiber volumetric fiber fraction
    Returns
    -------
    Float
        The value of the whole composite property
    """
    G12=m*(((1+V_f)+(1-V_f)*m/f)/((1-V_f)+(1+V_f)*m/f))
    return G12
def moist_exp(f,m,V_f,E_1=1):
    """
    Equation for finding the moisture expansion of a composite from individual
    moisture expansion properties
    Parameters
        ----------
        f : float
            The propertie value for the fiber phase
        m : float
            The propertie value for the matrix phase
        V_f : float
            The fiber volumetric fiber fraction
        E_1 : float, optional
                 parameter (the default is 1)
    Returns
    -------
    Float
        The value of the whole composite moisture expansion property
    """
    beta_1=m*(1-V_f)*m/E_1
    return beta_1
def PMM(mu_f,mu_m,nu_f,nu_m,la_m,V_f):
    """
    Periodic microestructural model
    Parameters
        ----------
        mu_f : float
            The propertie value for the fiber phase
        mu_m : float
            The propertie value for the matrix phase
        nu_f : float
            The propertie value for the fiber phase
        mu_m : float
            The propertie value for the matrix phase
        la_m : float
            The propertie value for the matrix phase
        V_f : float
            The fiber volumetric fiber fraction
            Returns
    -------
    list
        a list of strings used that are the header columns
    """
    a=mu_f-mu_m-2*mu_f*nu_m+2*mu_m*nu_f
    b=-mu_m*nu_m+mu_f*nu_f+2*mu_m*nu_m*nu_f-2*mu_f*nu_f*nu_m
    c=(mu_m-mu_f)*(mu_f-mu_m+mu_f*nu_f-mu_m*nu_m+2*mu_m*nu_f-2*mu_f*nu_m+2*mu_m*nu_m*nu_f-2*mu_f*nu_m*nu_f)
    g=(2-2*nu_m)
    S_3=0.49247-0.47603*V_f-0.02748*V_f**2
    S_6=0.36844-0.14944*V_f-0.27152*V_f**2
    S_7=0.12346-0.32035*V_f+0.23517*V_f**2
    D=(a*S_3**2/(2*c*mu_m**2))-(a*S_6*S_3/(g*c*mu_m**2))+(a*((S_6**2)-S_7**2))/(2*(g**2)*c*
    mu_m**2)-(S_3*(b**2-a**2))/(2*(c**2)*mu_m)+(S_6*(a**2-b**2)+S_7*(a*b+b**2))/(2*g*c**2
    *mu_m)+(a**3-2*b**3-3*a*b**2)/(8*c**3)
    C_11=la_m+2*mu_m-(V_f/D)*((S_3**2/mu_m**2)-(2*S_6*S_3/(g*mu_m**2))-a*S_3/(mu_m*c)+
    (S_6**2-S_7**2)/(mu_m**2*g**2)+(a*S_6+b*S_7)/(mu_m*g*c)+(a**2-b**2)/(4*c**2))
    C_12=la_m+(V_f/D)*b*((S_3/(2*c*mu_m))-(S_6-S_7)/(2*mu_m*c*g)-(a+b)/(4*c**2))
    C_23=la_m+(V_f/D)*((a*S_7/(2*mu_m*g*c))-(b*a+b**2)/(4*a*c**2))
    C_22=la_m+2*mu_m-(V_f/D)*(-(a*S_3/(2*c*mu_m))+(a*S_6)/(2*mu_m*c*g)-(a**2-b**2)/(4*c**2))
    C_44=mu_m-V_f*(-(2*S_3/mu_m)+(mu_m-mu_f)**(-1)+(4*S_7/(mu_m*(2-2*nu_m))))**(-1)
    C_66=mu_m-V_f*(-(S_3/mu_m)+(mu_m-mu_f)**(-1))**(-1)
    return C_11,C_12,C_23,C_22,C_44,C_66

def mechcar(Ef,Em,V_f,nu_f,nu_m):
    """
    Mechanical characterization of the complete composite based on the best
    micromechanical models for each of the cgaracteristic seeked
    Parameters
        ----------
        Ef : float
            Young's Moduls value for the fiber phase
        Em : float
            Young's Moduls value for the matrix phase
        V_f : float
            The fiber volumetric fiber fraction.
        nu_f : float
            The Poisson ratio of the fiber.
        nu_m : float
            The Poisson ratio of the matrix.
    Returns
    -------
    list
        a list of mechanical properties of the whole composite in the following
        order: E1,E2,E3,G12,G13,G23,nu_12,nu_13,nu_21,nu_23,nu_31,nu_32
    """
    E1=ROM(Ef,Em,V_f)[0]
    E2=iROM(Ef,Em,V_f)
    E3=E2
    Gf=Ef/(2*(1+nu_f))
    Gm=Em/(2*(1+nu_m))
    G12=CAM(Gf,Gm,V_f)
    G23=SEMSPP(Gf,Gm,nu_f,nu_m,V_f)
    G13=G12
    nu_12=ROM(nu_f,nu_m,V_f)[0]
    nu_23=nu_12-0.1 #Verify this
    nu_13=nu_12-0.1 #Verify this
    nu_21=E2*nu_12/E1
    nu_31=E3*nu_13/E1
    nu_32=E3*nu_23/E2

    return [E1,E2,E3,G12,G13,G23,nu_12,nu_13,nu_21,nu_23,nu_31,nu_32]

print("Micromechanics module loaded")
