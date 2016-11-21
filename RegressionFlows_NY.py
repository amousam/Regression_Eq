# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 10:15:02 2016

This module contains functions for calculating regression flows
for each of the 6 hydrologic Regions of NY as developed by USGS:
http://pubs.usgs.gov/sir/2006/5112/SIR2006-5112.pdf

Complete as of 11-18-2016

slawler@dewberry.com, amousam@dewberry.com
"""

#coefficent Definitions 
	#A, drainage area, in square miles; 
	#ST, basin storage, in percent; 
	#P, mean annual precipitation, in inches;
	#LAG, basin lag factor; 
	#FOR, basin forested area, in percent; 
	#RUNF, mean annual runoff, in inches;
	#MXSNO, seasonal maximum snow depth, 50th percentile, in inches; 
	#SR, slope ratio; 
	#SL, main channel slope, in feet per mile; 
	#EL12, percent of basin above 1,200 feet; 
	#Q, flow. subscript is recurrence interval; thus, Q2refers to discharge with 2-year recurrence interval

#---Recurrence Intervals & Hydrologic Regions
recurrence   = ['Q1_25','Q1_5','Q2','Q5','Q10','Q25',
                'Q50','Q100','Q200','Q500']
region       = ['R1','R2','R3','R4','R5','R6']

#---Coefficient Dictionaries by Hydrologic Regions
c1 = {"Q1_25":69.0,"Q1_5":144.0, "Q2":299.0,"Q5":1180.0,"Q10":2310.0,
      "Q25":4580.0,"Q50":7030.0,"Q100":10300.0,"Q200":14500.0,
      "Q500":22000.0}
c2 = {"Q1_25":32.2,"Q1_5":32.5, "Q2":33.3,"Q5":37.6,"Q10":41.6,
      "Q25":46.5,"Q50":49.7,"Q100":52.3,"Q200":54.3, 
      "Q500":55.9}
c3 = {"Q1_25":0.038,"Q1_5":0.052, "Q2":0.051,"Q5":0.083,"Q10":0.103,
      "Q25":0.117,"Q50":0.119,"Q100":0.115,"Q200":0.111, 
      "Q500":0.105}
c4 = {"Q1_25":0.037,"Q1_5":0.064, "Q2":0.115,"Q5":0.424,"Q10":0.829,
      "Q25":1.585,"Q50":2.330,"Q100":3.243,"Q200":4.350, 
      "Q500":6.163}      
c5 = {"Q1_25":0.020,"Q1_5":0.040, "Q2":0.083,"Q5":0.322,"Q10":0.597,
      "Q25":1.05,"Q50":1.46,"Q100":1.91,"Q200":2.43, 
      "Q500":3.22}
c6 = {"Q1_25":4.50,"Q1_5":6.36, "Q2":8.98,"Q5":17.1,"Q10":23.4,
      "Q25":32.1,"Q50":39.0,"Q100":46.0,"Q200":53.2, 
      "Q500":62.7}

#---Exponent Dictionaries by Hydrologic Regions
R1Q1_25 = {'A': 0.972,'ST':-0.160, 'P':1.859,'LAG':-0.355,'FOR':-1.514}
R1Q1_5  = {'A': 0.973,'ST':-0.164, 'P':1.718,'LAG':-0.383,'FOR':-1.519}
R1Q2    = {'A': 0.972,'ST':-0.169, 'P':1.576,'LAG':-0.411,'FOR':-1.518}
R1Q5    = {'A': 0.970,'ST':-0.178, 'P':1.335,'LAG':-0.460,'FOR':-1.530}
R1Q10   = {'A': 0.968,'ST':-0.184, 'P':1.241,'LAG':-0.482,'FOR':-1.549}
R1Q25   = {'A': 0.965,'ST':-0.192, 'P':1.167,'LAG':-0.500,'FOR':-1.582}
R1Q50   = {'A': 0.963,'ST':-0.197, 'P':1.131,'LAG':-0.511,'FOR':-1.610}
R1Q100  = {'A': 0.962,'ST':-0.202, 'P':1.106,'LAG':-0.520,'FOR':-1.638}
R1Q200  = {'A': 0.960,'ST':-0.206, 'P':1.086,'LAG':-0.528,'FOR':-1.667}
R1Q500  = {'A': 0.959,'ST':-0.210, 'P':1.067,'LAG':-0.539,'FOR':-1.704}

R2Q1_25 = {'A':0.943,'ST':-0.943,'LAG':-0.294,'RUNF':0.588} 
R2Q1_5  = {'A':0.936,'ST':-0.962,'LAG':-0.306,'RUNF':0.672} 
R2Q2    = {'A':0.928,'ST':-0.976,'LAG':-0.318,'RUNF':0.759}
R2Q5    = {'A':0.914,'ST':-0.985,'LAG':-0.356,'RUNF':0.905}
R2Q10   = {'A':0.909,'ST':-0.977,'LAG':-0.385,'RUNF':0.968}
R2Q25   = {'A':0.905,'ST':-0.958,'LAG':-0.418,'RUNF':1.029}
R2Q50   = {'A':0.902,'ST':-0.939,'LAG':-0.441,'RUNF':1.068}
R2Q100  = {'A':0.900,'ST':-0.918,'LAG':-0.416,'RUNF':1.104}
R2Q200  = {'A':0.898,'ST':-0.894,'LAG':-0.479,'RUNF':1.138}
R2Q500  = {'A':0.895,'ST':-0.860,'LAG':-0.500,'RUNF':1.183}

R3Q1_25 = {'A':0.959,'LAG':-0.141,'RUNF':1.234,'MXSNO':1.037}
R3Q1_5  = {'A':0.961,'LAG':-0.161,'RUNF':1.142,'MXSNO':1.110}
R3Q2    = {'A':0.962,'LAG':-0.179,'RUNF':1.009,'MXSNO':1.360}
R3Q5    = {'A':0.965,'LAG':-0.215,'RUNF':0.776,'MXSNO':1.632}
R3Q10   = {'A':0.963,'LAG':-0.228,'RUNF':0.658,'MXSNO':1.794}
R3Q25   = {'A':0.957,'LAG':-0.239,'RUNF':0.524,'MXSNO':2.016}
R3Q50   = {'A':0.953,'LAG':-0.244,'RUNF':0.430,'MXSNO':2.195}
R3Q100  = {'A':0.951,'LAG':-0.249,'RUNF':0.341,'MXSNO':2.375}
R3Q200  = {'A':0.949,'LAG':-0.253,'RUNF':0.255,'MXSNO':2.547}
R3Q500  = {'A':0.948,'LAG':-0.258,'RUNF':0.147,'MXSNO':2.759}

R4Q1_25 = {'A':1.029,'ST':-0.104,'RUNF':2.308,'SR':0.317}
R4Q1_5  = {'A':1.022,'ST':-0.120,'RUNF':2.205,'SR':0.320}
R4Q2    = {'A':1.012,'ST':-0.139,'RUNF':2.092,'SR':0.319}
R4Q5    = {'A':0.992,'ST':-0.189,'RUNF':1.822,'SR':0.316}
R4Q10   = {'A':0.981,'ST':-0.219,'RUNF':1.685,'SR':0.314}
R4Q25   = {'A':0.970,'ST':-0.250,'RUNF':1.559,'SR':0.312}
R4Q50   = {'A':0.963,'ST':-0.269,'RUNF':1.489,'SR':0.312}
R4Q100  = {'A':0.957,'ST':-0.285,'RUNF':1.431,'SR':0.312}
R4Q200  = {'A':0.952,'ST':-0.300,'RUNF':1.380,'SR':0.313}
R4Q500  = {'A':0.946,'ST':-0.317,'RUNF':1.320,'SR':0.315}

R5Q1_25 = {'A':0.971,'SL':0.377,'P':1.625}
R5Q1_5  = {'A':0.968,'SL':0.402,'P':1.468}
R5Q2    = {'A':0.965,'SL':0.431,'P':1.305}
R5Q5    = {'A':0.965,'SL':0.498,'P':0.995}
R5Q10   = {'A':0.967,'SL':0.538,'P':0.853}
R5Q25   = {'A':0.972,'SL':0.581,'P':0.724}
R5Q50   = {'A':0.976,'SL':0.610,'P':0.651}
R5Q100  = {'A':0.980,'SL':0.636,'P':0.590} 
R5Q200  = {'A':0.984,'SL':0.659,'P':0.536}
R5Q500  = {'A':0.989,'SL':0.688,'P':0.473}

R6Q1_25 = {'A':0.811,'ST':-0.270,'RUNF':0.840,'EL12':0.066,'SR':0.168}
R6Q1_5  = {'A':0.809,'ST':-0.265,'RUNF':0.790,'EL12':0.079,'SR':0.190} 
R6Q2    = {'A':0.807,'ST':-0.258,'RUNF':0.740,'EL12':0.093,'SR':0.209}
R6Q5    = {'A':0.807,'ST':-0.234,'RUNF':0.646,'EL12':0.120,'SR':0.248}
R6Q10   = {'A':0.810,'ST':-0.218,'RUNF':0.600,'EL12':0.133,'SR':0.268}
R6Q25   = {'A':0.815,'ST':-0.200,'RUNF':0.555,'EL12':0.148,'SR':0.290}
R6Q50   = {'A':0.819,'ST':-0.188,'RUNF':0.528,'EL12':0.157,'SR':0.305}
R6Q100  = {'A':0.823,'ST':-0.177,'RUNF':0.505,'EL12':0.166,'SR':0.318}
R6Q200  = {'A':0.828,'ST':-0.167,'RUNF':0.487,'EL12':0.173,'SR':0.330}
R6Q500  = {'A':0.834,'ST':-0.155,'RUNF':0.466,'EL12':0.183,'SR':0.345}

#----List of Exponent Dictionaries by Hydrologic Regions
e1 = [R1Q1_25,R1Q1_5,R1Q2,R1Q5,R1Q10,R1Q25,R1Q50,R1Q100,R1Q200,R1Q500]
e2 = [R2Q1_25,R2Q1_5,R2Q2,R2Q5,R2Q10,R2Q25,R2Q50,R2Q100,R2Q200,R2Q500]
e3 = [R3Q1_25,R3Q1_5,R3Q2,R3Q5,R3Q10,R3Q25,R3Q50,R3Q100,R3Q200,R3Q500]
e4 = [R4Q1_25,R4Q1_5,R4Q2,R4Q5,R4Q10,R4Q25,R4Q50,R4Q100,R4Q200,R4Q500]
e5 = [R5Q1_25,R5Q1_5,R5Q2,R5Q5,R5Q10,R5Q25,R5Q50,R5Q100,R5Q200,R5Q500]
e6 = [R6Q1_25,R6Q1_5,R6Q2,R6Q5,R6Q10,R6Q25,R6Q50,R6Q100,R6Q200,R6Q500]

#---Complete List of Paramters by Hydrologic Regions (Coefficients & Exponents)
p1= {'c':c1,'e':e1}
p2= {'c':c2,'e':e2}
p3= {'c':c3,'e':e3}
p4= {'c':c4,'e':e4}
p5= {'c':c5,'e':e5}
p6= {'c':c6,'e':e6}


#============================================================================#
#============--------------------FUNCTIONS--------------------===============#
#============================================================================#

#---REGION 1 EQUATION
def r1_qs(A,ST,P,LAG,FOR, params =p1):
    p=params; OUTPUT = dict()
    for r in range(len(recurrence)):
        recur      = recurrence[r]
        coeff      = p['c'][recur]
        e1 = p['e'][r]['A']     
        e2 = p['e'][r]['ST'] 
        e3 = p['e'][r]['P'] 
        e4 = p['e'][r]['LAG']  
        e5 = p['e'][r]['FOR']  
        Q = coeff*(A)**e1*(ST+1)**e2*(P)**e3*(LAG+1)**e4*(FOR+80)**e5
        OUTPUT[recur] = round(Q,0)
    return OUTPUT    


#---REGION 2 EQUATION
def r2_qs(A,ST,LAG,RUNF, params =p2):
    p=params; OUTPUT = dict()
    for r in range(len(recurrence)):
        recur      = recurrence[r]
        coeff      = p['c'][recur]
        e1 = p['e'][r]['A']     
        e2 = p['e'][r]['ST'] 
        e3 = p['e'][r]['LAG'] 
        e4 = p['e'][r]['RUNF']  
        Q = coeff*(A)**e1*(ST+5)**e2*(LAG+1)**e3*(RUNF)**e4
        OUTPUT[recur] = round(Q,0)
    return OUTPUT            


#---REGION 3 EQUATION
def r3_qs(A,LAG,RUNF,MXSNO, params =p3):
    p=params; OUTPUT = dict()
    for r in range(len(recurrence)):
        recur      = recurrence[r]
        coeff      = p['c'][recur]
        e1 = p['e'][r]['A']     
        e2 = p['e'][r]['LAG'] 
        e3 = p['e'][r]['RUNF'] 
        e4 = p['e'][r]['MXSNO']  
        Q = coeff*(A)**e1*(LAG+1)**e2*(RUNF)**e3*(MXSNO)**e4
        OUTPUT[recur] = round(Q,0)
    return OUTPUT    


#---REGION 4 EQUATION
def r4_qs(A,ST,RUNF,SR, params =p4):
    p=params; OUTPUT = dict()
    for r in range(len(recurrence)):
        recur      = recurrence[r]
        coeff      = p['c'][recur]
        e1 = p['e'][r]['A']     
        e2 = p['e'][r]['ST'] 
        e3 = p['e'][r]['RUNF'] 
        e4 = p['e'][r]['SR']  
        Q = coeff*(A)**e1*(ST+0.5)**e2*(RUNF)**e3*(SR)**e4
        OUTPUT[recur] = round(Q,0)
    return OUTPUT    


#---REGION 5 EQUATION
def r5_qs(A,SL,P, params =p5):
    p=params; OUTPUT = dict()
    for r in range(len(recurrence)):
        recur      = recurrence[r]
        coeff      = p['c'][recur]
        e1 = p['e'][r]['A']     
        e2 = p['e'][r]['SL'] 
        e3 = p['e'][r]['P'] 
        Q = coeff*(A)**e1*(SL)**e2*(P)**e3
        OUTPUT[recur] = round(Q,0)
    return OUTPUT    


#---REGION 6 EQUATION
def r6_qs(A,ST,RUNF,EL12,SR, params = p6):
    p=params; OUTPUT = dict()
    for r in range(len(recurrence)):
        recur      = recurrence[r]
        coeff      = p['c'][recur]
        e1 = p['e'][r]['A']     
        e2 = p['e'][r]['ST'] 
        e3 = p['e'][r]['RUNF'] 
        e4 = p['e'][r]['EL12']  
        e5 = p['e'][r]['SR']  
        Q = coeff*(A)**e1*(ST+0.5)**e2*(RUNF)**e3*(EL12+1)**e4*(SR)**e5
        OUTPUT[recur] = round(Q,0)
    return OUTPUT 
