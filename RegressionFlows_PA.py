# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 10:15:02 2016

This module contains functions for calculating regression flows
for each of the 4 hydrologic Regions of PA as developed by USGS:
http://pubs.usgs.gov/sir/2008/5102/pdf/sir2008-5102.pdf

Complete as of 11-18-2016

slawler@dewberry.com, amousam@dewberry.com
"""

#---Recurrence Intervals & Hydrologic Regions
recurrence   = ['Q2','Q5','Q10','Q50','Q100','Q500']
region       = ['R1','R2','R3','R4']

#---Intercept Dictionaries by Hydrologic Regions
c1 = {"Q2":1.84257,"Q5":2.10658,"Q10":2.24305,
      "Q50":2.47845,"Q100":2.56172,"Q500":2.73185}
c2 = {"Q2":2.20340,"Q5":2.50745,"Q10":2.66804,
      "Q50":2.94676,"Q100":3.04617,"Q500":3.25362}
c3 = {"Q2":3.27469,"Q5":3.73436,"Q10":3.98972,
      "Q50":4.42545,"Q100":4.5808,"Q500":4.90955}
c4 = {"Q2":1.82330,"Q5":2.09191,"Q10":2.23878,
      "Q50":2.50038,"Q100":2.59407,"Q500":2.78822}
# Definitions 
	#A = the intercept (estimated by GLS);
	#DA = drainage area, in square miles;
	#El = mean elevation, in feet;
	#C = basin underlain by carbonate bedrock, in percent;
	#U = urban area in the basin, in percent;
	#Sto = storage in the basin, in percent; and
	#b, c, d, e, and f = basin characteristic coefficients of regression estimated by GLS.

	
#---Dictionaries by Hydrologic Regions
R1Q2    = {'DA': 0.86396,'Sto':-0.49180}
R1Q5    = {'DA': .84127,'Sto':-.49148}
R1Q10   = {'DA': .83197,'Sto':-.47595}
R1Q50   = {'DA': .81981,'Sto':-.43501}
R1Q100  = {'DA': .81626,'Sto':-.41724}
R1Q500  = {'DA': .81002,'Sto':-.37550}

R2Q2    = {'DA': .69782,'C':-0.47534, 'U':0.91196}
R2Q5    = {'DA': .66365,'C':-.65666, 'U':.56109}
R2Q10   = {'DA': .64853,'C':-.75941, 'U':.39037}
R2Q50   = {'DA': .62615,'C':-.92098, 'U':.11100}
R2Q100  = {'DA': .61864,'C':-.97299, 'U':.00947}
R2Q500  = {'DA': .60294,'C':-1.07780, 'U':-.21084}

R3Q2    = {'DA': .82143,'El':-0.4517, 'C':-1.96079, 'Sto':-.74815}
R3Q5    = {'DA': .79492,'El':-.51761, 'C':-1.78595, 'Sto':-.90039}
R3Q10   = {'DA': .78127,'El':-.55653, 'C':-1.66440, 'Sto':-.99420}
R3Q50   = {'DA': .75816,'El':-.62224, 'C':-1.45536, 'Sto':-1.15401}
R3Q100  = {'DA': .75043,'El':-.64613, 'C':-1.38215, 'Sto':-1.20941}
R3Q500  = {'DA': .73500,'El':-.69814, 'C':-1.22437, 'Sto':-1.32521}

R4Q2    = {'DA': .84471}
R4Q5    = {'DA': .81363}
R4Q10   = {'DA': .79689}
R4Q50   = {'DA': .77079}
R4Q100  = {'DA': .76279}
R4Q500  = {'DA': .74809}


#----List of Exponent Dictionaries by Hydrologic Regions
e1= [R1Q2,R1Q5,R1Q10,R1Q50,R1Q100,R1Q500]
e2= [R2Q2,R2Q5,R2Q10,R2Q50,R2Q100,R2Q500]
e3= [R3Q2,R3Q5,R3Q10,R3Q50,R3Q100,R3Q500]
e4= [R4Q2,R4Q5,R4Q10,R4Q50,R4Q100,R4Q500]

#---Complete List of Paramters by Hydrologic Regions (Coefficients & Exponents)
p1= {'c':c1,'e':e1}
p2= {'c':c2,'e':e2}
p3= {'c':c3,'e':e3}
p4= {'c':c4,'e':e4}


#============================================================================#
#============--------------------FUNCTIONS--------------------===============#
#============================================================================#

#---REGION 1 EQUATION
def r1_qs(DA,Sto, params =p1):
    p=params; OUTPUT = dict()
    for r in range(len(recurrence)):
        recur      = recurrence[r]
        coeff      = p['c'][recur]
        e1 = p['e'][r]['DA']     
        e2 = p['e'][r]['Sto']   
        Q = 10**coeff*(DA)**e1*(1+0.1*Sto)**e2
        OUTPUT[recur] = round(Q,0)
    return OUTPUT    


#---REGION 2 EQUATION
def r2_qs(DA,C,U, params =p2):
    p=params; OUTPUT = dict()
    for r in range(len(recurrence)):
        recur      = recurrence[r]
        coeff      = p['c'][recur]
        e1 = p['e'][r]['DA']     
        e2 = p['e'][r]['C']
		e3 = p['e'][r]['U'] 
        Q = 10**coeff*(DA)**e1*(1+0.1*C)**e2*(1+0.1*U)**e2
        OUTPUT[recur] = round(Q,0)
    return OUTPUT    

#---REGION 3 EQUATION
def r3_qs(DA,El,C, Sto, params =p3):
    p=params; OUTPUT = dict()
    for r in range(len(recurrence)):
        recur      = recurrence[r]
        coeff      = p['c'][recur]
        e1 = p['e'][r]['DA']     
        e2 = p['e'][r]['El']
		e3 = p['e'][r]['C'] 
		e4 = p['e'][r]['Sto'] 
        Q = 10**coeff*(DA)**e1*El**e2*(1+0.1*C)**e3*(1+0.1*Sto)**e4
        OUTPUT[recur] = round(Q,0)
    return OUTPUT  
#---REGION 4 EQUATION

def r4_qs(DA, params =p4):
    p=params; OUTPUT = dict()
    for r in range(len(recurrence)):
        recur      = recurrence[r]
        coeff      = p['c'][recur]
        e1 = p['e'][r]['DA']      
        Q = 10**coeff*(DA)**e1
        OUTPUT[recur] = round(Q,0)
    return OUTPUT  
