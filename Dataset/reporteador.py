"""
Generación automática de reportes de tracción y compresión.
Proyecto: "PFA of AM composites" Por: Juan Sebastian León Becerra y Diego
Alexander Leon Becerra
Versión: 5.0 Actualizado 2 de Septiembre
"""
import pandas as pd
from pathlib import Path
import os
import numpy as np
from scipy.stats import linregress
print("""Generación automática de reportes de tracción y compresión.
Proyecto: "PFA of AM composites" Por:
Juan Sebastian León Becerra y Diego Alexander Leon Becerra
Versión: 5.0 Actualizado 2 de Septiembre
""")

def txt_to_dict(filename): #procesamiento datos
    file=open(filename)
    count=0
    headers=[]
    body={}
    body["Axial Force"]=[]
    body["Axial Displacement"]=[]
    body["Time"]=[]
    #body["Axial Force Abs. Error"]=[]
    body["Axial Displacement Error"]=[]
    body["Axial 634.12F "]=[]

    for line in file:
        words=line.split()
        if count < 28:
            headers.append(words)
            count=count+1
        else:
            body["Axial Force"].append(float(words[0]))
            body["Axial Displacement"].append(float(words[1]))
            body["Time"].append(float(words[2]))
            #body["Axial Force Abs. Error"].append(float(words[3]))
            body["Axial Displacement Error"].append(float(words[4]))
            body["Axial 634.12F "].append(float(words[5]))
    return body,headers

def dict_to_dataframe(body): #Creacion del DataFrame
    area=30 #Area transversal 13x3.2 mm
    long=61 #Longitud en mm, verificar este valor
    df = pd.DataFrame({key: pd.Series(value) for key, value in body.items()})
    df['Strain [mm/mm]']=df['Axial Displacement']/long
    df['Stress[MPa]']=df['Axial Force']/area
    df['StrainExt[mm/mm]']=df['Axial 634.12F ']/25
    return df

def generate_excel(df,headers,writer):
    sheet_name_title=headers[2][-1]
    df.to_excel(writer,sheet_name=sheet_name_title)
    worksheet = writer.sheets[sheet_name_title]
    #Calculo Valores REsultados
    MaxForce=df['Axial Force'].max()
    MaxStrain=df['Strain [mm/mm]'].max()
    MaxStrainExt=df['StrainExt[mm/mm]'].max()
    #CALCULO PENDIENTE
    MaxPosition=df[(df['Stress[MPa]']==df['Stress[MPa]'].max())].index[0]+1
    df_2=df.iloc[:MaxPosition-1,]
    x = np.array(df_2['Strain [mm/mm]'])
    y = np.array(df_2['Stress[MPa]'])
    x2=np.array(df_2['StrainExt[mm/mm]'])
    pendiente=linregress(x,y)
    pendientext=linregress(x2,y)
    #Cálculo Resiliencia
    resiliencia=0
    for i in range(len(x)):
        if i==0:continue
        delta_x=x[i]-x[i-1]
        resiliencia+=delta_x*y[i]
    #CALCULO tenacidad
    tenacidad=0
    xt=np.array(df['Strain [mm/mm]'])
    yt = np.array(df['Stress[MPa]'])
    for i in range(len(xt)):
        if i==0:continue
        delta_xt=xt[i]-xt[i-1]
        tenacidad+=delta_xt*yt[i]
    #Writing the Results
    resultados={'Max Force':MaxForce,'MaxStrain':MaxStrain,
    'MaxStrainExt':MaxStrainExt,'Modulo Young':pendiente[0],
    'Modulo Young Extensometro':pendientext[0],
    'Resiliencia':resiliencia,'Tenacidad':tenacidad}
    resultados_df=pd.DataFrame({value: pd.Series(key) for key, value in resultados.items()}).T
    worksheet.write(1,10,"Resultados")
    resultados_df.to_excel(writer,sheet_name=sheet_name_title,header=None,startcol=10,startrow=2)

    #Gráficas
    # Create a new Chart object.
    chart = workbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
    # Configure the first series.
    valueschartlist=list()
    Catchartlist=list()
    Catchart="="+str(sheet_name_title)+"!$G$2:$G${}".format(len(list(df.index))+1)
    valueschart="="+str(sheet_name_title)+"!$H$2:$H${}".format(len(list(df.index))+1)
    valueschartlist.append(valueschart)
    Catchartlist.append(Catchart)
    chart.add_series({
        'name':       'Stress strain curve',
        'categories': Catchart,
        'values':     valueschart,
    })
    # Add a chart title and some axis labels.
    chart.set_title ({'name': 'Stress strain curve'})
    chart.set_x_axis({'name': 'Strain (mm/mm)'})
    chart.set_y_axis({'name': 'Stress (MPa)'})
    chart.set_legend({'none': True})
    # Configure the series of the chart from the dataframe data.
    # Insert the chart into the worksheet.
    worksheet.insert_chart('K15', chart)
    #Generate the second graph which represents the elastic part of the test
    # Create a new Chart object.

    chart2 = workbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
    # Configure the second series.
    Catchart2="="+str(sheet_name_title)+"!$G$2:$G${}".format(MaxPosition)
    valueschart2="="+str(sheet_name_title)+"!$H$2:$H${}".format(MaxPosition)
    chart2.add_series({
        'name':       'Elastic curve ',
        'categories': Catchart2,
        'values':     valueschart2,
        'trendline': {
            'type': 'linear',
            'display_equation': True,
            'line': {
                'color': 'red',
                'width': 1,},
            'display_r_squared': True
            },
    })
    # Add a chart title and some axis labels.
    chart2.set_title ({'name': 'Stress strain curve'})
    chart2.set_x_axis({'name': 'Strain (mm/mm)'})
    chart2.set_y_axis({'name': 'Stress (MPa)'})
    chart2.set_legend({'none': True})
    # Configure the series of the chart from the dataframe data.
    # Insert the chart into the worksheet.
    worksheet.insert_chart('K30', chart2)

    # Create a new Chart object.
    chart3 = workbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
    # Configure the first series.
    Catchart3="="+str(sheet_name_title)+"!$I$2:$I${}".format(MaxPosition)
    valueschart3="="+str(sheet_name_title)+"!$H$2:$H${}".format(MaxPosition)
    chart3.add_series({
        'name':       'Stress strain curve',
        'categories': Catchart3,
        'values':     valueschart3,
        'trendline': {
            'type': 'linear',
            'display_equation': True,
            'line': {
                'color': 'red',
                'width': 1,},
            'display_r_squared': True
            },
    })
    # Add a chart title and some axis labels.
    chart3.set_title ({'name': 'Estensometer S-S curve'})
    chart3.set_x_axis({'name': 'Extensometer Strain (mm/mm)'})
    chart3.set_y_axis({'name': 'Stress (MPa)'})
    chart3.set_legend({'none': True})
    # Configure the series of the chart from the dataframe data.
    # Insert the chart into the worksheet.
    worksheet.insert_chart('K45', chart3)
    # Close the Pandas Excel writer and output the Excel file.
    #generate_excel(df,[col1,col2],xlsxwriter)
    return resultados,valueschartlist,Catchartlist

#Se abre carpeta por carpeta y se pre procesa la información
print('\nProcesando Informacion...')
currentpath=Path.cwd()
dflist=[]
headerslist=[]
for folderName, subfolders, filenames in os.walk(currentpath):
    for filename in filenames:
        if filename.endswith('2.txt'): continue
        if filename[-3:]=='txt':
            file=str(folderName+"\\"+filename)
            #print(file)
            body,headers=txt_to_dict(file)
            df=dict_to_dataframe(body)
            dflist.append(df)
            headerslist.append(headers)

#Se crea el archivo excel y se pasa la inormación procesada hacia la funcion generate_excel
writer = pd.ExcelWriter('Datos_consolidados.xlsx', engine = 'xlsxwriter')
workbook  = writer.book
resultados=list()
valuescharts=list()
catchartsy=list()
for i in range(len(headerslist)):
    headers=headerslist[i]
    df=dflist[i]
    resultado,ejey,ejex=generate_excel(df, headers, writer)
    resultados.append(resultado)
    valuescharts.append(ejey)
    catchartsy.append(ejex)
print('Generando reporte en excel...')
#Generacion Hoja Resumen donde se encuentran los resultados de cada prueba, así com una gráfica superpuesta de cada prueba
nombres=list()
chartresumen=dict()
tempnombre=list()
contador=0
i=0
for nombre in headerslist:
    sheet_name_title=nombre[2][-1]
    nombres.append(sheet_name_title)
    tipoarreglo=sheet_name_title[:2]
    if tipoarreglo in tempnombre:
        grafica=chartresumen[i]
        grafica.add_series({
            'name':'{}'.format(sheet_name_title),
            'categories': catchartsy[contador][0],
            'values':     valuescharts[contador][0],
        })
    else:
        i += 1
        chartresumen[i]= chartresumen.get(i,workbook.add_chart({'type': 'scatter','subtype': 'smooth'}))
        chartresumen[i].add_series({
            'name':'{}'.format(sheet_name_title),
            'categories': catchartsy[contador][0],
            'values':     valuescharts[contador][0],
        })
        chartresumen[i].set_title ({'name': 'Stress strain curve{}'.format(sheet_name_title[:-1])})
        chartresumen[i].set_x_axis({'name': 'Strain (mm/mm)'})
        chartresumen[i].set_y_axis({'name': 'Stress (MPa)'})
        tempnombre.append(tipoarreglo)
    contador += 1

resultados_df=pd.DataFrame(resultados)
resultados_df['Nombre']=nombres
resultados_df=resultados_df.set_index('Nombre')
resultados_df.to_excel(writer,'Resumen')

worksheet = writer.sheets['Resumen']
inicio=2
for plotresume in chartresumen.values():
    worksheet.insert_chart('J{}'.format(inicio), plotresume)
    inicio += 16
writer.save()
#writer.close()

print('Información procesada\nReporte Generado y guardado en Datos_consolidados.xlsx')
