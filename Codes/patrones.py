"""
Module  for calculate the material properties based on the book "Solid cell structures"
stiffness and strenght characterization of 3D printed lattice structures
Three structures are presented: Triangular, rectangular and Honeycomb.
Analytical Equations are based on the book Cellular solids and structures
Of Gibson and Ashby
Last version: 16/09/2020
"""
import math as mt
def honeycomb(Es,t,l,h,theta=60):
	"""
    stiffness characterization of honeycomb or hexagonal-shaped infill pattern
    Parameters
        ----------
        Es : float
            Young´s modulus of the solid
        t : float
            Thickness of the strut, for complete
		l : float
	        Lenght of the side for complete
		h : float
	        Thickness of the strut, for complete
        theta : int, optional
            The smallest (check) angle in degrees of the hexagonal
			 (default is 60 degrees)
	Returns
    -------
    	list
        	a list of strings used that are the header columns
    """
	if theta==60:
		E1=2.3*Es*(t/l)**3
		E2=E1
		G12=0.57*(t/l)**3
		nu12=0.39

	else:
		E1=Es*((t/l)**3)*(mt.cos(theta)/(mt.sin(theta)**2*((h/l)+mt.sin(theta))))
		E2=Es*((t/l)**3)*(((h/l)+mt.sin(theta))/mt.cos(theta))
		nu12=(((h/l)+mt.sin(theta))*mt.sin(theta))/(mt.cos(theta)**2)
		G12=((h/l)+mt.sin(theta))/((h/l)**2*(1+2*h/l)*mt.sin(theta))

	return [E1,E2,nu12,G12]

def rect(Es,t,l):
	"""
    stiffness characterization of honeycomb or hexagonal-shaped infill pattern
    Parameters
        ----------
        Es : float
            Young´s modulus of the solid
        t : float
            Thickness of the strut, for complete
		l : float
	        Lenght of the side
	Returns
    -------
    	list
        	a list of strings used that are the header columns
    """
	E1=Es*t/l
	E2=E1
	return [E1,E2]

def triangle(Es,t,l):
	"""
    stiffness characterization of honeycomb or hexagonal-shaped infill pattern
    Parameters
        ----------
        Es : float
            Young´s modulus of the solid
        t : float
            Thickness of the strut, for complete
		l : float
	        Lenght of the side
	Returns
    -------
    	list
        	a list of strings used that are the header columns
    """
	E1=1.15*Es*t/l
	E2=E1
	return [E1,E2]

def solid(Es,G,nu,p=0.1):
	"""
    stiffness characterization of the solid region used in 100% infill as well as
	for solid or shell regions.
    Parameters
        ----------
        Es : float
            Young´s modulus of the solid
        G : float
            Shear modulus of the Solid
		nu : float
	        Poisson's ratio of the solid
		p_1 : float, optional
	        Porosity value (default is 0.1)
	Returns
    -------
    	list
        	a list of strings used that are the header columns
    """
	E_1=(1-p)*Es
	E_2=(1-mt.sqrt(p))*Es
	E_3=E_2
	G_12=G*((1-p)*(1-mt.sqrt(p)))/((1-p)+(1-mt.sqrt(p)))
	G_13=G_12
	G_23=(1-mt.sqrt(p))*G
	nu_12=(1-p)*nu
	nu_13=nu_12
	nu_21=(1-mt.sqrt(p))*nu
	nu_23=nu_21
	nu_31=nu_21
	nu_32=nu_21
	return [E_1,E_2,E_3,G_12,G_13,G_23,nu_12,nu_13,nu_21,nu_23,nu_31,nu_32]
