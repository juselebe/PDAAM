# PDAAM
Progressive damage analysis of additive manufacturing composites

This repository includes the raw data, processed data, python scripts, FEA Codes used to develop my PhD. Thesis entitled "Progressive damaga analysis of additive manufacturing composites". The repository is divided into sections corresponding with the chapter numbers, and the script are placed in the code section.

Modules description (in codes folder): 

* Module micromechanics.py --> Library of functions for appliying micromechanical equations such as ROM, iROM, PMM, SSP, HALPIN-TSAI, ETC to calculate elastic modulus.
* Module microstrength.py --> Library of functions for calculating the strength of a composite lamina from micromechanical formulations
* Module patrones.py --> Library of functions for calculating the relative density and mechanical behavior of lattice structures based on the material properties and geometric configuration. 
* Script principal.py & principal2.py--> Module that implements the calculation of the Volumetric average stiffness method, it calls the other modules of micromechanics and lattice structures. 
* Script Parajor.py ---> Module implementing a semi-rheological model developped with Jorge Diaz for characterizing AM composites. 
* Mecprop.xls---> Excel file containing the implementation of VAS technique into an excel spreedsheet. 






Date 28/02/2021
