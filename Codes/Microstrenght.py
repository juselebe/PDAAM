"""
Module for calculating analytical strenght based upon micromechanical models
and from semi-analytical expressions shown in Barberos book, page 118
By: Juan Sebastian Leon Becerra. Last version: 08/10/2020 added Fft
"""
import numpy as np
def Fft(F1t,V_f,E_m,E_f):
    """
    Back-calculated apparent fiber tensile strenght characterization of composite
    Parameters
        ----------
        F1t : float
            Fiber longitudinal tensile strenght
        V_f : float
            Fiber volumetric fraction
		E_m : float
	        Matrix Young's modulus
		E_f: float
	        Fiber Young's modulus
	Returns
    -------
    	float
        	Numerical value of F1t
    """ #If V_f is low, consider to use other formula
    F1t=Fft*((V_f)+(E_m/E_f)*(1-V_f))
    return F1t


def F1t(Fft,V_f,E_m,E_f):
    """
    Longitudinal tensile strenght characterization of composite
    Parameters
        ----------
        Fft : float
            Fiber apparent strenght
        V_f : float
            Fiber volumetric fraction
		E_m : float
	        Matrix Young's modulus
		E_f: float
	        Fiber Young's modulus
	Returns
    -------
    	float
        	Numerical value of F1t
    """ #If V_f is low, consider to use other formula
    F1t=Fft*((V_f)+(E_m/E_f)*(1-V_f))
    return F1t
def F1c(G_12,alpha_s,F_6):
    """
    Longitudinal compressive strenght characterization of composite
    Parameters
        ----------
        G_12 : float
            In-plane Shear Modulus
        alpha_s : float
            Standar deviation of fiber misaligment, back-calculated or experimen-
            tally measured
		F_6 : float
	        Shear strenght of the composite
	Returns
    -------
    	float
        	Numerical value of F1c
    """
    X=G_12*alpha_s/F_6
    F1c=G_12*(1+4.76*X)**(-0.069)
    return F1c
def F2t(E_1,E_2,nu_12,G_IC,tt):
    """
    Transverse tensile strenght characterization of composite
    Parameters
        ----------
        E_1 : float
            Longitudinal composite Modulus
        E_2 : float
            Transverse composite Modulus
		nu_12 : float
	        In-plane Poisson ratio
		G_IC: float
	        Mode 1 fracture toughness
        tt: float
            Transition thickness
    Returns
    -------
    	float
        	Numerical value of F2t
    """ # There are other formulas
    A220=2*((1/E_2)-((nu_12**2)*E_2**2)/E_1**3))
    F2t=np.sqrt(G_IC/((1.12**2)*pi*(tt/4)*A220)))
    return F2t
def GIC(A220,F2t,a_0=1):
    """
    Mode 1 fracture toughness of composite
    Parameters
        ----------
        A220 : float
            Fiber apparent strenght
        F2t : float
            Transverse tensile strenght
		a_0: float
	       Parameter
	Returns
    -------
    	float
        	Numerical value of GIC
    """
    GIC=(1.12**2)*pi*(tt/4)*a_0*(F2t**2)
    return G_IC
def F2c(Fm,Cv,Vf,Et,Em):
    """
    Transverse compressive strenght of composite
    Parameters
        ----------
        Fm : float
            Fiber apparent strenght
        Cv : float
            Fiber volumetric fraction
		Vf : float

		Et: float
	        Fiber Young's modulus
        Em: Float
            Matrix Young's modulus
	Returns
    -------
    	float
        	Numerical value of F2c
    """
    F2c=Fm*Cv*(1+(Vf-np.sqrt(Vf))*(1-(Et/Em)))
    return F2c
def F6(G2c,tt,G_12):
    """
    In-plane shear strenght of composite
    Parameters
        ----------
        G2c : float
            Fiber apparent strenght
        tt : float
            Transition thickness
		G_12 : float
	        In-plane shear modulus
	Returns
    -------
    	float
        	Numerical value of F6
    """
    A440=1/G_12
    F6=np.sqrt(G2c/(pi*tt*A440/4))
    return F6
def GIIc(F6,A440,a_0):
    """
    Mode 2 fracture toughness of composite
    Parameters
        ----------
        F6 : float
            In-plane shear strenght of composite
        A440: float
            Parameter
		a_0 : float
	        Parameter
	Returns
    -------
    	float
        	Numerical value of GIIc
    """
    GIIc=pi*a_0*A440*F6**2
    return GIIc
def honeystr():
    """
    Longitudinal tensile strenght characterization of composite
    Parameters
        ----------
        Fft : float
            Fiber apparent strenght
        V_f : float
            Fiber volumetric fraction
		E_m : float
	        Matrix Young's modulus
		E_f: float
	        Fiber Young's modulus
	Returns
    -------
    	float
        	Numerical value of F1t
    """
    Honst=1
    return Honst
def rectstr():
    """
    Longitudinal tensile strenght characterization of composite
    Parameters
        ----------
        Fft : float
            Fiber apparent strenght
        V_f : float
            Fiber volumetric fraction
		E_m : float
	        Matrix Young's modulus
		E_f: float
	        Fiber Young's modulus
	Returns
    -------
    	float
        	Numerical value of F1t
    """
    rectstr=1
    return rectstr
def triangstr():
    """
    Longitudinal tensile strenght characterization of composite
    Parameters
        ----------
        Fft : float
            Fiber apparent strenght
        V_f : float
            Fiber volumetric fraction
		E_m : float
	        Matrix Young's modulus
		E_f: float
	        Fiber Young's modulus
	Returns
    -------
    	float
        	Numerical value of F1t
    """
    triangstr=1
    return triangstr

print("Microstrength module loaded")

#USAR MACHINE LEARNING PARA DETERMINAR EL VALOR OPTIMO DE LAS CONSTANTES?
