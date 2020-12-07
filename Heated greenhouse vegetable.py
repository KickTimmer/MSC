# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 17:03:46 2020

@author: kick_
"""

#!pip install sparql-client
#!pip install SPARQLWrapper

import rdflib
import matplotlib.pyplot as plt
import urllib.request
import json
from omlib.constants import SI
from omlib.omconstants import OM
from omlib.measure import om, Point, Measure
from prettytable import PrettyTable

# Your Bing Maps Key 
bingMapsKey = "ArrnkeiRDpMYcdQqlz4HkOxNyxVflvKFberjZ_1VLoMHFfek-laRRGPkMtzDxzjo"

#Collect the ontologies and parse them into a collective dataset called 'dataset'
product = rdflib.Graph()
product.parse("Ontologies MSC\product_specifications.ttl", format="n3")

cultivation = rdflib.Graph()
cultivation.parse("Ontologies MSC\Cultivation.ttl", format="n3")

transport = rdflib.Graph()
transport.parse("Ontologies MSC\Transport.ttl", format="n3")

packaging = rdflib.Graph()
packaging.parse("Ontologies MSC\packeging.ttl", format="n3")

dataset = product + cultivation + transport + packaging

#----------------------------USER INPUT--------------------------------------- 

#SELECT PRODUCT 

ProductSelect = " 'Belichte Nederlandse Komkommer 3' " 
#Choose from: Onbelichte Nederlandse Komkommer 1, Belichte Nederlandse Komkommer 1 , Spaanse Komkommer 1, Klassiek Nederlandse Tomatensoep 1 

#---------------------------DEFAULTS------------------------------------------
prefix = ("PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> ")
              
#DEFAULT CO2 Values. (kg CO2 per kg product)
CapitalGoodsDEFAULT = 0.06
EnergyDEFAULT = 1.4
CarbondioxideDEFAULT = 0.065
CultivationDEFAULT = 0.04
PackagingDEFAULT = 0.12
TransportDEFAULT = 0.01



#UNITS and CONSTANTS Co2 per Unit CULTIVATION
YieldUnit = OM.kilogramPerSquareMetre
PostharvestlossUnit = OM.percent
Yield_Default = om(100, OM.kilogramPerSquareMetre)
Post_harvest_Default = om(10, OM.percent)

Nitrogen_fertiliserCo2Constant = 4.5
Nitrogen_fertiliserClass = "<http://www.semanticweb.org/kick_/ontologies/2020/4/Cultivation#Nitrogen_Fertiliser>"
Nitrogen_fertiliserUnit = OM.kilogramPerSquareMetre

Greenhouse_glassCo2Constant = 5
Greenhouse_glassClass = "<http://www.semanticweb.org/kick_/ontologies/2020/4/Cultivation#Greenhouse_glass>"
Greenhouse_glassUnit = OM.squareMetrePerSquareMetre

Greenhouse_plasticCo2Constant = 2.8
Greenhouse_plasticClass = "<http://www.semanticweb.org/kick_/ontologies/2020/4/Cultivation#Greenhouse_plastic>"
Greenhouse_plasticUnit = OM.squareMetrePerSquareMetre

CHP_heatCo2Constant = 0.078
CHP_heatClass = "<http://www.semanticweb.org/kick_/ontologies/2020/4/Cultivation#CHP_Heat>"
CHP_heatUnit = OM.megajoulePerSquareMetre

Geothermal_heatCo2Constant = 0.017
Geothermal_heatClass = "<http://www.semanticweb.org/kick_/ontologies/2020/4/Cultivation#Geothermal_Heat>"
Geothermal_heatUnit = OM.megajoulePerSquareMetre

CHP_electricityCo2Constant = 0.280
CHP_electricityClass = "<http://www.semanticweb.org/kick_/ontologies/2020/4/Cultivation#CHP_Electricity>"
CHP_electricityUnit = OM.kilowattHour

Grid_electricityCo2Constant = 0.635
Grid_electricityClass = "<http://www.semanticweb.org/kick_/ontologies/2020/4/Cultivation#Grid_Electricity>"
Grid_electricityUnit = OM.kilowattHour

CO2_purifiedCo2Constant = 0.28
CO2_purifiedClass = "<http://www.semanticweb.org/kick_/ontologies/2020/4/Cultivation#Purified_CO2_Enrichment>"
CO2_purifiedUnit = OM.kilogramPerSquareMetre

CO2_externalCo2Constant = 0.37
CO2_externalClass = "<http://www.semanticweb.org/kick_/ontologies/2020/4/Cultivation#External_CO2_Enrichment>"
CO2_externalUnit = OM.kilogramPerSquareMetre

BiowasteCo2Constant = 0.15
BiowasteClass = "<http://www.semanticweb.org/kick_/ontologies/2020/4/Cultivation#Biowaste>"
BiowasteUnit = OM.kilogramPerSquareMetre

Other_inputCo2Constant = 1
Other_inputClass = "<http://www.semanticweb.org/kick_/ontologies/2020/4/Cultivation#Other_Input_CO2>"
Other_inputUnit = OM.kilogramPerSquareMetre

N2O_cultivationCo2Constant = 298
N2O_cultivationClass = "<http://www.semanticweb.org/kick_/ontologies/2020/4/Cultivation#N2O_Cultivation>"
N2O_cultivationUnit = OM.kilogramPerSquareMetre
######################################################################################################################################

#DEFAULTS Co2 per Unit PACKAGING
PolyethyleneClass = "packaging:Polyethylene"
PolyetheleneCo2 = 0.004
PolyetheleneCo2_UNIT = OM.gramPerKilogram

BoardboxClass = "packaging:Board_box"
BoardboxCo2 = 0.0008
BoardboxCo2_UNIT = OM.gramPerKilogram

PalletClass = "packaging:Pallet"
PalletCo2 = 2.26
PalletCo2_UNIT = OM.one

CoolingenergyClass = "<http://www.semanticweb.org/kick_/ontologies/2020/4/packaging#Cooling_Energy>"
CoolingenergyCo2 = 0.00052
CoolingenergyCo2_UNIT = OM.wattHour
######################################################################################################################################

#DEFAULTS Co2 per Unit TRANSPORT
DistanceClass = "<http://www.semanticweb.org/kick_/ontologies/2020/5/Transport#Distance>"
DistanceUnit = OM.kilometre
KgCO2EQperTonKmConstant = 0.17
######################################################################################################################################


#---------------------------PRODUCT CHECK/ GENERAL------------------------------------------
def ProductCHECK(Product):
    query2 = ( prefix + """
    SELECT ?product
    WHERE {
    ?product rdfs:label """ + Product + """ . 
    }
    LIMIT 1
    """)
    results2 = dataset.query(query2)
    if len(results2) == 0: 
        return False
    else:
        return True
    
def ProductGTIN(Product):
    query2 = ( prefix + """
    SELECT ?GTIN
    WHERE {
    ?product rdfs:label """ + Product + """ . 
    ?product product:has_GTIN ?GTIN . 
    }
    LIMIT 1
    """)
    results2 = dataset.query(query2)
    if len(results2) == 0: 
        return ("-")
    else:
        for x in results2:
            GTIN = str(x[0])
        return (GTIN)

def ProductGLN(Product):
    query2 = ( prefix + """
    SELECT ?GLN
    WHERE {
    ?product rdfs:label """ + Product + """ . 
    ?product product:has_GLN ?GLN . 
    }
    LIMIT 1
    """)
    results2 = dataset.query(query2)
    if len(results2) == 0: 
        return ("-")
    else:
        for x in results2:
            GLN = str(x[0])
        return (GLN)

def CountryOfOrigin(Product):
    query2 = ( prefix + """
    SELECT ?country
    WHERE {
    ?product rdfs:label """ + Product + """ . 
    ?product product:Country_of_Origin ?country . 
    }
    LIMIT 1
    """)
    results2 = dataset.query(query2)
    if len(results2) == 0: 
        return ("-")
    else:
        for x in results2:
            country = str(x[0])
        return (country)

#---------------------------CULTIVATION------------------------------------------

#Returns a tuple, containing the Yield and Post harvest losses of a production system
def CutltivationYieldandLoss(Product):
    query2 = ( prefix + """
    SELECT ?YieldUnit ?YieldNumvalue ?postUnit ?postNumvalue
    WHERE {
    ?product rdfs:label """ + Product + """ . 
    ?product product:has_Production_System ?system .
    
    ?yield om:hasPhenomenon ?system . 
    ?yield rdf:type cultivation:Yield . 
    ?yield om:hasValue ?Yieldvalue . 
    ?Yieldvalue om:hasUnit ?YieldUnit . 
    ?Yieldvalue cultivation:hasNumericalValue ?YieldNumvalue . 
    
    ?postloss om:hasPhenomenon ?system . 
    ?postloss rdf:type cultivation:Post_Harvest_Loss . 
    ?postloss om:hasValue ?postvalue . 
    ?postvalue om:hasUnit ?postUnit . 
    ?postvalue cultivation:hasNumericalValue ?postNumvalue .
    
    } 
    LIMIT 1
    """)
    results2 = dataset.query(query2)
    if len(results2) == 0: 
        print ("Yield and post harvest losses: DEFAULT")
        return (Yield_Default, Post_harvest_Default)
    for x in results2:
        Yieldunit = str(x[0].replace('http://www.ontology-of-units-of-measure.org/resource/om-2/', ''))
        YieldNum = float(x[1])
        PostlossUnit = str(x[2].replace('http://www.ontology-of-units-of-measure.org/resource/om-2/', ''))
        PostlossNum = float(x[3])
    
    Yield = om(YieldNum, getattr(OM, Yieldunit))
    Yield.convert(YieldUnit)
    
    PostharvestLoss = om(PostlossNum, getattr(OM, PostlossUnit))
    PostharvestLoss.convert(PostharvestlossUnit)
    
    return (Yield, PostharvestLoss)

CutltivationYieldandLoss



#Returns a list containing: Property label, measure before convertion, measure after convertion, calculated kg co2 per kg product 
def CultivationProductCo2 (Product, Cultivationproperty, Propertyconstant, Propertyunit):  
    YieldandLoss = CutltivationYieldandLoss(Product)
    Yield = YieldandLoss[0]
    PostharvestLoss = YieldandLoss[1]

    query1 =     ( prefix + """
    SELECT ?Numvalue ?Unit ?label
    WHERE {
    ?product rdfs:label """ + Product + """ . 
    
    ?product product:has_Production_System ?system .
    ?Property om:hasPhenomenon ?system .
    ?Property rdf:type """ + Cultivationproperty + """ .  
    """ + Cultivationproperty + """ rdfs:label ?label .
    
    ?Property om:hasValue ?Value .
    OPTIONAL{?Value om:hasUnit ?Unit .} 
    ?Value cultivation:hasNumericalValue ?Numvalue . 

    } 
    LIMIT 1
    """)
    results1 = dataset.query(query1)
    if len(results1) == 0: 
        return
    for item in results1:
        Numvalue = float(item[0])
        Unit = str(item[1].replace('http://www.ontology-of-units-of-measure.org/resource/om-2/', ''))
        Label = str(item[2])     
    Unit = Unit.replace("-", "")
    
    measure = om(Numvalue, getattr(OM, Unit))
    measure2 = Measure.create_by_converting(measure, Propertyunit)
    
    CO2_contribution = (measure2.numericalValue * Propertyconstant) * (Yield.numericalValue / ( 100 - PostharvestLoss.numericalValue)) / 100
    return [Label, format(measure), format(measure2), round(CO2_contribution, 4)]

#returns only the Kg co2 per kg product value
def CultivationProductNumValue(Product, Cultivationproperty, Propertyconstant, Propertyunit):
    YieldandLoss = CutltivationYieldandLoss(Product)
    Yield = YieldandLoss[0]
    PostharvestLoss = YieldandLoss[1]

    query1 =     ( prefix + """
    SELECT ?Numvalue ?Unit
    WHERE {
    ?product rdfs:label """ + Product + """ . 
    
    ?product product:has_Production_System ?system .
    ?Property om:hasPhenomenon ?system .
    ?Property rdf:type """ + Cultivationproperty + """ . 
    ?Property rdfs:label ?label . 
    
    ?Property om:hasValue ?Value .
    OPTIONAL{?Value om:hasUnit ?Unit .} 
    ?Value cultivation:hasNumericalValue ?Numvalue . 
    
    ?yield om:hasPhenomenon ?system . 
    ?yield rdf:type cultivation:Yield . 
    ?yield om:hasValue ?Yieldvalue . 
    ?Yieldvalue om:hasUnit ?YieldUnit . 
    ?Yieldvalue cultivation:hasNumericalValue ?YieldNumvalue . 
    
    } 
    LIMIT 1
    """)
    results1 = dataset.query(query1)
    if len(results1) == 0: 
        return float(0)
    for item in results1:
        Numvalue = float(item[0])
        Unit = str(item[1].replace('http://www.ontology-of-units-of-measure.org/resource/om-2/', ''))
    
    Unit = Unit.replace("-", "")
    measure = om(Numvalue, getattr(OM, Unit))
    measure2 = Measure.create_by_converting(measure, Propertyunit)
    
    CO2_contribution = (measure2.numericalValue * Propertyconstant) * (Yield.numericalValue / ( 100 - PostharvestLoss.numericalValue)) / 100
    
    return CO2_contribution

#---------------------------------Calculation schemes-----------------------------------------------------

#returns a signle number with the total CO2 from all energy usage
def TotalEnergyCultivationCO2():
    CHP_heat = CultivationProductNumValue(ProductSelect, CHP_heatClass, CHP_heatCo2Constant, CHP_heatUnit)
    Geothermal_heat = CultivationProductNumValue(ProductSelect, Geothermal_heatClass, Geothermal_heatCo2Constant, Geothermal_heatUnit)
    CHP_electricity = CultivationProductNumValue(ProductSelect, CHP_electricityClass, CHP_electricityCo2Constant, CHP_electricityUnit)
    Grid_Electricity = CultivationProductNumValue(ProductSelect, Grid_electricityClass, Grid_electricityCo2Constant, Grid_electricityUnit)
    Total = CHP_heat + Geothermal_heat + CHP_electricity + Grid_Electricity 
    if Total == 0: 
        Total = EnergyDEFAULT
    return Total

#returns a signle number with the total CO2 from all carbon dioxide
def TotalCarbondioxideCultivationCO2():
    CO2_external = CultivationProductNumValue(ProductSelect, CO2_externalClass, CO2_externalCo2Constant, CO2_externalUnit)
    CO2_purified = CultivationProductNumValue(ProductSelect, CO2_purifiedClass, CO2_purifiedCo2Constant, CO2_purifiedUnit)
    Total = CO2_purified + CO2_external
    if Total == 0: 
        Total = CarbondioxideDEFAULT
    return Total

#returns a signle number with the total CO2 from capital goods (Glass plastic)
def TotalCapitalgoodsCultivationCO2():
    GreenhouseGlass = CultivationProductNumValue(ProductSelect, Greenhouse_glassClass, Greenhouse_glassCo2Constant, Greenhouse_glassUnit)
    GreenhousePlastic = CultivationProductNumValue(ProductSelect, Greenhouse_plasticClass, Greenhouse_plasticCo2Constant, Greenhouse_plasticUnit)
    Total = GreenhouseGlass + GreenhousePlastic
    if Total == 0: 
        Total = CapitalGoodsDEFAULT
    return Total

#returns a signle number with the total CO2 from all cultivation specific properties
def TotalCultivationCultivationCO2():
    Nitrogen = CultivationProductNumValue(ProductSelect, Nitrogen_fertiliserClass, Nitrogen_fertiliserCo2Constant, Nitrogen_fertiliserUnit)
    Biowaste = CultivationProductNumValue(ProductSelect, BiowasteClass, BiowasteCo2Constant, BiowasteUnit)
    N2O = CultivationProductNumValue(ProductSelect, N2O_cultivationClass, N2O_cultivationCo2Constant, N2O_cultivationUnit)
    Other_input = CultivationProductNumValue(ProductSelect, Other_inputClass, Other_inputCo2Constant, Other_inputUnit)
    Total = Nitrogen + Biowaste + N2O + Other_input
    if Total == 0: 
        Total = CultivationDEFAULT
    return Total

#returns a table containing all properties and values with regards to energy usage 
def CO2detailsEnergy():
    Result = []
    Result.append(CultivationProductCo2(ProductSelect, CHP_heatClass, CHP_heatCo2Constant, CHP_heatUnit))
    Result.append(CultivationProductCo2(ProductSelect, Geothermal_heatClass, Geothermal_heatCo2Constant, Geothermal_heatUnit))
    Result.append(CultivationProductCo2(ProductSelect, CHP_electricityClass, CHP_electricityCo2Constant, CHP_electricityUnit))
    Result.append(CultivationProductCo2(ProductSelect, Grid_electricityClass, Grid_electricityCo2Constant, Grid_electricityUnit))
    Res = list(filter(None, Result))
    
    t = PrettyTable()
    t.field_names = ["Property", "Retrieved value", "Converted Value", "KG CO2 per KG product"]
    if len(Res) != 0:
        for x in Res:
            t.add_row(x)
    else:
        t.add_row(["Default", "-", "-", EnergyDEFAULT])
    return t

#returns a table containing all properties and values with regards to carbon dioxide
def CO2detailsCarbondioxide():
    Result = []
    Result.append(CultivationProductCo2(ProductSelect, CO2_externalClass, CO2_externalCo2Constant, CO2_externalUnit))
    Result.append(CultivationProductCo2(ProductSelect, CO2_purifiedClass, CO2_purifiedCo2Constant, CO2_purifiedUnit))
    Res = list(filter(None, Result))
   
    t = PrettyTable()
    t.field_names = ["Property", "Retrieved value", "Converted Value", "KG CO2 per KG product"]
    if len(Res) != 0:
        for x in Res:
            t.add_row(x)
    else:
        t.add_row(["Default", "-", "-", CarbondioxideDEFAULT])
    return t

#returns a table containing all properties and values with regards to capital goods
def CO2detailsCapitalgoods():
    Result = []
    Result.append(CultivationProductCo2(ProductSelect, Greenhouse_glassClass, Greenhouse_glassCo2Constant, Greenhouse_glassUnit))
    Result.append(CultivationProductCo2(ProductSelect, Greenhouse_plasticClass, Greenhouse_plasticCo2Constant, Greenhouse_plasticUnit))
    Res = list(filter(None, Result))
    
    t = PrettyTable()
    t.field_names = ["Property", "Retrieved value", "Converted Value", "KG CO2 per KG product"]
    if len(Res) != 0:
        for x in Res:
            t.add_row(x)
    else:
        t.add_row(["Default", "-", "-", CapitalGoodsDEFAULT])
    return t

#returns a table containing all properties and values with regards to cultivation
def CO2detailsCultivationCultivation():
    Result = []
    Result.append(CultivationProductCo2(ProductSelect, Nitrogen_fertiliserClass, Nitrogen_fertiliserCo2Constant, Nitrogen_fertiliserUnit))
    Result.append(CultivationProductCo2(ProductSelect, BiowasteClass, BiowasteCo2Constant, BiowasteUnit))
    Result.append(CultivationProductCo2(ProductSelect, N2O_cultivationClass, N2O_cultivationCo2Constant, N2O_cultivationUnit))
    Result.append(CultivationProductCo2(ProductSelect, Other_inputClass, Other_inputCo2Constant, Other_inputUnit))
    Res = list(filter(None, Result))
    
    t = PrettyTable()
    t.field_names = ["Property", "Retrieved value", "Converted Value", "KG CO2 per KG product"]
    if len(Res) != 0:
        for x in Res:
            t.add_row(x)
    else:
        t.add_row(["Default", "-", "-", CultivationDEFAULT])
    return t
##################################################################################



#---------------------------PACKAGING-------------------------------------
#Returns a list containing: Property label, measure before convertion, measure after convertion, calculated kg co2 per kg product 
def PackagingProductCo2(Product, Packagingproperty, Propertyconstant, Propertyunit):
    query1 =     ( prefix + """
    SELECT ?Numvalue ?Unit ?label
    WHERE {
    ?product rdfs:label """ + Product + """ . 
    
    ?product product:has_Packaging ?packaging .
    ?Property om:hasPhenomenon ?packaging .
    ?Property rdf:type """ + Packagingproperty + """ . 
    """ + Packagingproperty + """ rdfs:label ?label . 
    
    ?Property om:hasValue ?Value .
    OPTIONAL{?Value om:hasUnit ?Unit .} 
    ?Value packaging:hasNumericalValue ?Numvalue . 
    
    } 
    LIMIT 1
    """)
    results1 = dataset.query(query1)
    if len(results1) == 0: 
        print ("Ingredient has no linked property from the class: %s" % Packagingproperty)
        return 
    for item in results1:
        Numvalue = float(item[0])
        Unit = str(item[1].replace('http://www.ontology-of-units-of-measure.org/resource/om-2/', ''))
        Label = str(item[2])
    Unit = Unit.replace("-", "")
    
    measure = om(Numvalue, getattr(OM, Unit))
    measure2 = Measure.create_by_converting(measure, Propertyunit)
    CO2_contribution = measure2.numericalValue * Propertyconstant
    return [Label, format(measure), format(measure2), round(CO2_contribution, 4)]

#returns only the Kg co2 per kg product value  
def PackagingProductCo2NumValue(Product, Packagingproperty, Propertyconstant, Propertyunit):
    query1 =     ( prefix + """
    SELECT ?Numvalue ?Unit 
    WHERE {
    ?product rdfs:label """ + Product + """ . 
    
    ?product product:has_Packaging ?packaging .
    ?Property om:hasPhenomenon ?packaging .
    ?Property rdf:type """ + Packagingproperty + """ . 
    
    ?Property om:hasValue ?Value .
    OPTIONAL{?Value om:hasUnit ?Unit .} 
    ?Value packaging:hasNumericalValue ?Numvalue . 
    
    } 
    LIMIT 1
    """)
    results1 = dataset.query(query1)
    if len(results1) == 0: 
        return float(0)
    for item in results1:
        Numvalue = float(item[0])
        Unit = str(item[1].replace('http://www.ontology-of-units-of-measure.org/resource/om-2/', ''))
    Unit = Unit.replace("-", "")
    
    measure = om(Numvalue, getattr(OM, Unit))
    measure2 = Measure.create_by_converting(measure, Propertyunit)
    CO2_contribution = measure2.numericalValue * Propertyconstant
    
    return CO2_contribution

#returns a signle number with the total CO2 from packaging
def TotalPackagingCO2():
    polythelene = PackagingProductCo2NumValue(ProductSelect, PolyethyleneClass, PolyetheleneCo2, PolyetheleneCo2_UNIT) 
    boardbox = PackagingProductCo2NumValue(ProductSelect, BoardboxClass, BoardboxCo2, BoardboxCo2_UNIT)
    pallet = PackagingProductCo2NumValue(ProductSelect, PalletClass, PalletCo2, PalletCo2_UNIT)
    coolingenergy = PackagingProductCo2NumValue(ProductSelect, CoolingenergyClass, CoolingenergyCo2, CoolingenergyCo2_UNIT)
    total = polythelene + boardbox + pallet + coolingenergy
    if total == 0: 
        total = PackagingDEFAULT
    return total

#returns a table containing all properties and values with regards to packaging
def CO2detailsPackaging():    
    Result = []
    Result.append(PackagingProductCo2(ProductSelect, PolyethyleneClass, PolyetheleneCo2, PolyetheleneCo2_UNIT))
    Result.append(PackagingProductCo2(ProductSelect, BoardboxClass, BoardboxCo2, BoardboxCo2_UNIT))
    Result.append(PackagingProductCo2(ProductSelect, PalletClass, PalletCo2, PalletCo2_UNIT))
    Result.append(PackagingProductCo2(ProductSelect, CoolingenergyClass, CoolingenergyCo2, CoolingenergyCo2_UNIT))
    Res = list(filter(None, Result))
    
    t = PrettyTable()
    t.field_names = ["Property", "Retrieved value", "Converted Value", "KG CO2 per KG product"]
    if len(Res) != 0:
        for x in Res:
            t.add_row(x)
    else:
        t.add_row(["Default", "-", "-", PackagingDEFAULT])
    return t

#---------------------------TRANSPORT-----------------------------------------

    

def TransportcoordinatesCHECK(Product):
    query2 =     (prefix + """
    SELECT ?startlat ?startlon ?Deslat ?Deslong
    WHERE {
    ?product rdfs:label """ + Product + """ . 
    ?product product:has_Transportation ?transportation . 
    ?transportation rdfs:label ?Transportrecord . 
    ?transportation transport:hasStartLocation ?Startloc . ?Startloc geo:lat ?startlat . ?Startloc geo:long ?startlon . 
    ?transportation transport:hasDestination ?Destination . ?Destination geo:lat ?Deslat . ?Destination geo:long ?Deslong . 
    } """)
    
    results = dataset.query(query2)
    if len(results) == 0:
        return False
    else:
        return True

#Returns a table with information about coordinates, distance and predicted time duration. 
def Transportdetails_coordinates(Product, CO2constant):
    query2 =     (prefix + """
    SELECT ?startlat ?startlon ?Deslat ?Deslong
    WHERE {
    ?product rdfs:label """ + Product + """ . 
    ?product product:has_Transportation ?transportation . 
    ?transportation rdfs:label ?Transportrecord . 
    ?transportation transport:hasStartLocation ?Startloc . ?Startloc geo:lat ?startlat . ?Startloc geo:long ?startlon . 
    ?transportation transport:hasDestination ?Destination . ?Destination geo:lat ?Deslat . ?Destination geo:long ?Deslong . 
    } """)
    
    results = dataset.query(query2)
    
    if len(results) == 0:
        return ("There are no coordinates available for this transportation")
    
    for row in results: 
        startlat = float(row[0])
        startlong = float(row[1])
        Deslat = float(row[2])
        Deslong = float(row[3])
    
    routeUrl = "http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=" + str(startlat) + "," + str(startlong) + "&wp.1=" + str(Deslat) + "," + str(Deslong) + "&key=" + bingMapsKey

    request = urllib.request.Request(routeUrl)
    response = urllib.request.urlopen(request)
    
    r = response.read().decode(encoding="utf-8")
    result = json.loads(r)
    
    Distance = result["resourceSets"][0]["resources"][0]["travelDistance"]
    Duration = result["resourceSets"][0]["resources"][0]["travelDuration"]
    
    DistanceOM = om(Distance, OM.kilometre)
    DurationOM = om(Duration, SI.SECOND)
    DurationOMminute = DurationOM.create_by_converting(DurationOM, OM.minuteTime)
    DurationOMhour = DurationOM.create_by_converting(DurationOM, OM.hour)
    
    CO2_contribution = DistanceOM.numericalValue * CO2constant / 1000
    
    Results = [round(DistanceOM.numericalValue, 2), round(DurationOMminute.numericalValue, 2), round(DurationOMhour.numericalValue, 2), round(CO2_contribution, 4)]
    t = PrettyTable()
    t.field_names = ["Calculated Distance", "estimated duration (min)", "Estimated duration (hour)", "KG CO2"]
    t.add_row(Results)
    return t
        

#Returns a list containing: Property label, measure before convertion, measure after convertion, calculated kg co2 per kg product 
def TransportProductCo2(Product, TransportProperty, Propertyconstant, Propertyunit):
    query1 =     ( prefix + """
    SELECT ?Numvalue ?Unit ?label
    WHERE {
    ?product rdfs:label """ + Product + """ . 
    
    ?product product:has_Transportation ?transport .
    ?Property om:hasPhenomenon ?transport .
    ?Property rdf:type """ + TransportProperty + """ . 
    """ + TransportProperty + """ rdfs:label ?label . 
    
    ?Property om:hasValue ?Value .
    OPTIONAL{?Value om:hasUnit ?Unit .} 
    ?Value transport:hasNumericalValue ?Numvalue . 
    
    } 
    LIMIT 1
    """)
    results1 = dataset.query(query1)
    if len(results1) == 0: 
        print ("Ingredient has no linked property from the class: %s" % TransportProperty)
        return 
    for item in results1:
        Numvalue = float(item[0])
        Unit = str(item[1].replace('http://www.ontology-of-units-of-measure.org/resource/om-2/', ''))
        Label = str(item[2])
    Unit = Unit.replace("-", "")
    
    measure = om(Numvalue, getattr(OM, Unit))
    measure2 = Measure.create_by_converting(measure, Propertyunit)
    CO2_contribution = measure2.numericalValue * Propertyconstant / 1000
    return [Label, format(measure), format(measure2), round(CO2_contribution, 4)]

#returns only the Kg co2 per kg product value
def TransportProductCo2NumValue(Product, TransportProperty, Propertyconstant, Propertyunit):
    query1 =     ( prefix + """
    SELECT ?Numvalue ?Unit 
    WHERE {
    ?product rdfs:label """ + Product + """ . 
    
    ?product product:has_Transportation ?transport .
    ?Property om:hasPhenomenon ?transport .
    ?Property rdf:type """ + TransportProperty + """ . 
    
    ?Property om:hasValue ?Value .
    OPTIONAL{?Value om:hasUnit ?Unit .} 
    ?Value transport:hasNumericalValue ?Numvalue . 
    
    } 
    LIMIT 1
    """)
    results1 = dataset.query(query1)
    if len(results1) == 0 and TransportcoordinatesCHECK(ProductSelect) == False: 
        return float(0)
    
    if len(results1) != 0:
        for item in results1:
            Numvalue = float(item[0])
            Unit = str(item[1].replace('http://www.ontology-of-units-of-measure.org/resource/om-2/', ''))
        Unit = Unit.replace("-", "")
        
        measure = om(Numvalue, getattr(OM, Unit))
        measure2 = Measure.create_by_converting(measure, Propertyunit)
        CO2_contribution = measure2.numericalValue * Propertyconstant / 1000
        
        return CO2_contribution

    if TransportcoordinatesCHECK(ProductSelect) == True: 
        query2 =     (prefix + """
        SELECT ?startlat ?startlon ?Deslat ?Deslong
        WHERE {
        ?product rdfs:label """ + Product + """ . 
        ?product product:has_Transportation ?transportation . 
        ?transportation rdfs:label ?Transportrecord . 
        ?transportation transport:hasStartLocation ?Startloc . ?Startloc geo:lat ?startlat . ?Startloc geo:long ?startlon . 
        ?transportation transport:hasDestination ?Destination . ?Destination geo:lat ?Deslat . ?Destination geo:long ?Deslong . 
        } """)
        results = dataset.query(query2)
        if len(results) != 0: 
            for row in results: 
                startlat = float(row[0])
                startlong = float(row[1])
                Deslat = float(row[2])
                Deslong = float(row[3])
            
            routeUrl = "http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=" + str(startlat) + "," + str(startlong) + "&wp.1=" + str(Deslat) + "," + str(Deslong) + "&key=" + bingMapsKey
    
            request = urllib.request.Request(routeUrl)
            response = urllib.request.urlopen(request)
            
            r = response.read().decode(encoding="utf-8")
            result = json.loads(r)
            
            Distance = result["resourceSets"][0]["resources"][0]["travelDistance"]
            
            CO2_contribution_coordinates = Distance * Propertyconstant / 1000
            
            return CO2_contribution_coordinates
    else:
        return float(0)

#returns a signle number with the total CO2 from transport
def TransportTotalCO2():
    transport = TransportProductCo2NumValue(ProductSelect, DistanceClass, KgCO2EQperTonKmConstant, DistanceUnit)
    total = transport 
    if total == 0: 
        total = TransportDEFAULT
    return total

#returns a table containing all properties and values with regards to transport
def CO2detailsTransport():
    Result = []
    Result.append(TransportProductCo2(ProductSelect, DistanceClass, KgCO2EQperTonKmConstant, DistanceUnit))
    Res = list(filter(None, Result))
    t = PrettyTable()
    t.field_names = ["Property", "Retrieved value", "Converted Value", "KG CO2 per KG product"]
    if len(Res) != 0:
        for x in Res:
            t.add_row(x)
    elif len(Res) == 0 and TransportcoordinatesCHECK(ProductSelect) == True:
        t.add_row(["-", "-", "-", "-"])
    else:
            t.add_row(["Default", "-", "-", TransportDEFAULT])
    return t
#---------------------------TOTALS+FIGURRES-----------------------------------

#TOTALS
def totalCO2():
    energy = TotalEnergyCultivationCO2()
    carbondioxide = TotalCarbondioxideCultivationCO2()
    capitalgoods = TotalCapitalgoodsCultivationCO2()
    cult =  TotalCultivationCultivationCO2() 
    packaging = TotalPackagingCO2() 
    transport = TransportTotalCO2()
    total = energy + carbondioxide + capitalgoods + cult + packaging + transport
    return total
    
#print ("The total Co2 contribution from packaging estimates: %s " % round(TotalPackagingCO2(), 2))
#print ("The total Co2 contribution from Energy estimates: %s " % round(TotalEnergyCultivationCO2(), 2))
#print ("The total Co2 contribution from carbion dioxide estimates: %s " % round(TotalCarbondioxideCultivationCO2(), 2))
#print ("The total Co2 contribution from capital goods estimates: %s " % round(TotalCapitalgoodsCultivationCO2(), 2))
#print ("The total Co2 contribution from cultivation estimates: %s " % round(TotalCultivationCultivationCO2(), 2))
# ("The total Co2 contribution from transport estimates: %s " % round(TransportTotalCO2(), 2))

#TABLES WITH DETAILS
    
#print ("Energy details for: %s \n" % (ProductSelect), CO2detailsEnergy())
#print ("Capital goods details for: %s \n" % (ProductSelect), CO2detailsCapitalgoods())
#print ("Carbon dioxide details for: %s \n" % (ProductSelect), CO2detailsCarbondioxide())     
#print ("Cultivation details for: %s \n" % (ProductSelect), CO2detailsCultivationCultivation())
#print ("Packaging details for: %s \n" % (ProductSelect), CO2detailsPackaging())
#print ("Transport details for: %s \n" % (ProductSelect), CO2detailsTransport())
#print ("Transport details derived from coordinates, for: %s \n" % (ProductSelect), Transportdetails_coordinates(ProductSelect, KgCO2EQperTonKmConstant))
    
#PLOTS
def PlotCO2total():
    if ProductCHECK(ProductSelect) == False:
        print ("No product found.")
        return
    labels = 'Energy', 'Carbon dioxide', 'Capital goods', 'Cultivation', 'Transport', 'Packaging'
    sizes = [round(TotalEnergyCultivationCO2(), 2), round(TotalCarbondioxideCultivationCO2(), 2), round(TotalCapitalgoodsCultivationCO2(), 2), round(TotalCultivationCultivationCO2(), 2), round(TransportTotalCO2(), 2), round(TotalPackagingCO2(), 2)]
    explode = (0, 0.15, 0.15, 0.15, 0.15, 0.15)  # only "explode" the 2nd slice (i.e. 'Hogs')
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'red', 'slateblue']
    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', pctdistance=0.8, labeldistance=1.1, radius=1, shadow=True, rotatelabels=False, startangle=30)

    plt.axis('equal')
    plt.tight_layout()
    title = ("Distribution of CO2 emission for: %s " % ProductSelect)
    plt.title(title)
    plt.show()

PlotCO2total()

def CreateReport():
    if ProductCHECK(ProductSelect) == False:
        print ("No product found.")
        return
    Energy = CO2detailsEnergy().get_string()
    Capitalgoods = CO2detailsCapitalgoods().get_string()
    carbondioxide = CO2detailsCarbondioxide().get_string()
    Cultivation = CO2detailsCultivationCultivation().get_string()
    Packaging = CO2detailsPackaging().get_string()
    Transport = CO2detailsTransport().get_string()
    if type(Transportdetails_coordinates(ProductSelect, KgCO2EQperTonKmConstant)) == str:
        Transport_coordinates = Transportdetails_coordinates(ProductSelect, KgCO2EQperTonKmConstant)
    else:
        Transport_coordinates = Transportdetails_coordinates(ProductSelect, KgCO2EQperTonKmConstant).get_string()
    
    with open('output.txt','w') as file:
        file.write("CO2 emission report for : %s" % ProductSelect)
        file.write("\nCountry of origin: %s" % CountryOfOrigin(ProductSelect))
        file.write("\nGTIN: %s" % ProductGTIN(ProductSelect))
        file.write("\nGLN: %s" % ProductGLN(ProductSelect))
        file.write("\n\nTotal emission KG CO2 per kilo product : %s " % round(totalCO2(), 2))
        file.write("\n\nEnergy Usage:\n")
        file.write(Energy)
        file.write("\n\nCaptial goods:\n")
        file.write(Capitalgoods)
        file.write("\n\nCarbon dioxide:\n")
        file.write(carbondioxide)
        file.write("\n\nCultivation:\n")
        file.write(Cultivation)
        file.write("\n\nPackaging:\n")
        file.write(Packaging)
        file.write("\n\nTransport:\n")
        file.write(Transport)
        file.write("\n\nTransport based on coordinates:\n")
        file.write(Transport_coordinates)




CreateReport()