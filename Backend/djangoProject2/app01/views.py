import webbrowser
import pywebio
from pywebio.input import *
import loica as lc
from pywebio.output import put_html, use_scope, put_file, put_image, put_text, put_table, span, popup, put_buttons, \
    put_tabs
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flapjack import *
import time
import json

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from util.imageutil import drawImage
def task_func():
    osc = lc.GeneticNetwork()
    RegulatorNum = input("Please enter the number of Regulators", type=NUMBER)
    actsmap = {}
    j = []
    k = []
    regulartorInfo = []

    def check_from(data):
        if len(data['name']) > 6:
            return ('name', 'Name to long!')
        if data['rate'] < 0:
            return ('rate', 'The value cannot be negative！')
        if data['iC'] < 0:
            return ('iC', 'The value can be zero but not negative！')

    def check_from1(data):
        if len(data['name']) > 6:
            return ('name', 'Name to long!')


    for i in range(RegulatorNum):
        RegulatorInfo = input_group("Regulator Information", [
            input('Regulator name', name='name'),
            input('Degradation rate ', name='rate', type=FLOAT, value=1),
            input('initial concentration', name='iC', type=FLOAT, value=0),
        ], validate=check_from)

        acts = lc.Regulator(name=RegulatorInfo['name'],
                            color='cyan',
                            degradation_rate=float(RegulatorInfo['rate']),
                            init_concentration=float(RegulatorInfo['iC'])
                            )

        actsmap[RegulatorInfo['name']] = acts
        j.append(actsmap[RegulatorInfo['name']])
        regulartorInfo.append(RegulatorInfo['name'])
        osc.add_regulator(j)

    reportersInfo = []

    ReporterNum = input("Enter the number of reporters", type=NUMBER)

    for i in range(ReporterNum):
        ReporterInfo = input_group("Reporter Information", [
            input('Reporter name', name='name'),
            input('Degradation rate ', name='rate', type=FLOAT, value=1),
            input('initial concentration', name='iC', value=0, type=FLOAT)
        ], validate=check_from)
        act = lc.Reporter(name=ReporterInfo['name'],
                          color='yellow',
                          degradation_rate=float(ReporterInfo['rate']),
                          init_concentration=float(ReporterInfo['iC']))

        actsmap[ReporterInfo['name']] = act
        k.append(actsmap[ReporterInfo['name']])
        reportersInfo.append(ReporterInfo['name'])
        osc.add_reporter(k)

    with use_scope('table'):

        put_table([
            ['Regulators', regulartorInfo],
            ['Reporters', reportersInfo],
        ], header=['type', 'name'])

    print(actsmap)

    Hill1Num = input("Enter the number of Hill1", type=NUMBER)
    arr = []
    arr1 = []
    arr2 = []
    arr3 = []

    def put_text1(i):

        arr.append(i)
        print(arr)
        with use_scope('h1i'):
            put_text(f'Add {i} to input{arr}')

    def put_text2(i):

        arr1.append(i)
        print(arr1)
        with use_scope('h1o'):
            put_text(f'Add {i} to output{arr1}')

    def put_text3(i):

        arr2.append(i)
        print(arr2)
        with use_scope('h2o'):
            put_text(f'Add {i} to input{arr2}')

    def put_text4(i):

        arr3.append(i)
        print(arr3)
        with use_scope('h2o'):
            put_text(f'Add {i}  to output{arr3}')

    def dele_data1():
        if arr:
            arr.pop()
            print(arr)
            with use_scope('dh1i'):
                put_text(f'Delete current data,input{arr}')
        else:
            popup('Error', 'input is 0')

    def dele_data2():
        if arr1:
            arr1.pop()
            print(arr1)
            with use_scope('dh1o'):
                put_text(f'Delete current data，output{arr1}')
        else:
            popup('Error', 'output is 0')

    def dele_data3():
        if arr2:
            arr2.pop()
            print(arr2)
            with use_scope('dh2i'):
                put_text(f'Delete current data，input{arr2}')
        else:
            popup('Error', 'input is 0')

    def dele_data4():
        if arr3:
            arr3.pop()
            print(arr3)
            with use_scope('dh2o'):
                put_text(f'Delete current data，output{arr3}')
        else:
            popup('Error', 'output is 0')

    for i in range(Hill1Num):
        with use_scope('bu1'):
            put_table([
                ['input', put_buttons([
                    dict(label=i, value=i, color='primary')
                    for i in actsmap
                ], onclick=put_text1, )],
                ['output', put_buttons([
                    dict(label=i, value=i, color='primary')
                    for i in actsmap
                ], onclick=put_text2, )],
                ['Delete', put_buttons(['input', 'output'], onclick=[dele_data1, dele_data2])]],
            )



        Hill1Info = input_group("Hill1 Information", [
            input("name", name="name"),
            input("alpha", name="alpha")
        ], validate=check_from1)
        pywebio.output.remove('bu1')

        listOut = arr1
        print(listOut)
        if len(listOut) == 2:

            a = actsmap[listOut[0]]
            b = actsmap[listOut[1]]
            c = [a, b]
        else:
            a = actsmap[listOut[0]]

            c = [a]

        hill1 = lc.Hill1(input=actsmap[arr[0]],
                         output=c,
                         alpha=list(map(int,
                                        Hill1Info['alpha'].split(','))),
                         K=10,
                         n=2,
                         name=Hill1Info['name'])
        osc.add_operator([hill1])

        arr.clear()
        arr1.clear()
        pywebio.output.remove('bu1')
        pywebio.output.remove('h1i')
        pywebio.output.remove('h1o')
        pywebio.output.remove('dh1i')
        pywebio.output.remove('dh1o')


    if Hill1Num != 3:
        Hill2Num = input("Enter the number of Hill2", type=NUMBER)

        for i in range(Hill2Num):
            with use_scope('bu3'):
                put_table([
                    ['input', put_buttons([
                        dict(label=i, value=i, color='danger')
                        for i in actsmap
                    ], onclick=put_text3, )],
                    ['output', put_buttons([
                        dict(label=i, value=i, color='danger')
                        for i in actsmap
                    ], onclick=put_text4, )],
                    ['Delete', put_buttons(['input', 'output'], onclick=[dele_data3, dele_data4])]
                ])



            Hill2Info = input_group("Hill2 information", [
                input("name", name="name"),

                input("alpha", name="alpha"),
            ])
            pywebio.output.remove('bu3')
            list2input = arr2
            c = actsmap[list2input[0]]
            d = actsmap[list2input[1]]

            list2output = arr3
            e = actsmap[list2output[0]]
            f = actsmap[list2output[1]]
            k = actsmap[list2output[2]]

            hill2 = lc.Hill2(input=[c, d],
                             output=[e, f, k],
                             alpha=list(map(int,
                                            Hill2Info['alpha'].split(','))),
                             K=[10, 10],
                             n=[2, 2],
                             name=Hill2Info['name'])
            osc.add_operator([hill2])
            arr2.clear()
            arr3.clear()
            pywebio.output.remove('bu2')
            pywebio.output.remove('table')
            pywebio.output.remove('h2i')
            pywebio.output.remove('h2o')
            pywebio.output.remove('dh2i')
            pywebio.output.remove('dh2o')



    def changeFig():
        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)
        figdata_png = base64.b64encode(figfile.getvalue())
        figdata_str = str(figdata_png, "utf-8")
        html = '<img src=\"data:image/png;base64,{}\"/>'.format(figdata_str)
        filename = 'png.html'
        with open(filename, 'w') as f:
            f.write(html)

    osc.draw(alpha=1)
    changeFig()
    plt.title('diagrammatic figure')
    plt.savefig('Loica_picture.png')

    img = open('./Loica_picture.png', 'rb').read()
    put_image(img)


    test = input_group('Please enter assay information', [
        input("Number of measurements to take", name='meaN', type=NUMBER),
        input("Time in hours between each measurements", name='mT', type=FLOAT),
        input('name', name='name'),
        input("description", name='des')
    ])
    put_tabs([
        {'title': 'Assay Name', 'content': test['name']},
        {'title': 'Description', 'content': test['des']},
        {'title': 'Component', 'content': [
            put_table([
                ['Regulators', regulartorInfo],
                ['Reporters', reportersInfo],
            ], header=['type', 'name'])

        ]}

    ])

    def growth_rate(t):
        return gompertz_growth_rate(t, 0.01, 1, 1, 0.5)

    def biomass(t):
        return gompertz(t, 0.01, 1, 1, 0.5)

    metab = lc.SimulatedMetabolism('Loica', biomass, growth_rate)

    sample = lc.Sample(genetic_network=osc,
                       metabolism=metab)

    assay = lc.Assay([sample],
                     n_measurements=test['meaN'],
                     interval=test['mT'],
                     name=test['name'],
                     description=test['des']
                     )
    assay.run()

    m = assay.measurements

    f = pd.DataFrame(m)
    writer = pd.ExcelWriter('app01/templates/Assay.xlsx')
    f.to_excel(writer, float_format='%.5f')
    writer.save()
    file_path='app01/templates/Assay.xlsx'
    writer = pd.ExcelWriter(file_path)
    f.to_excel(writer)
    writer.save()



    content = open('app01/templates/Assay.xlsx', 'rb').read()


    def showResult():

        '''
        state of process
        '''
        pywebio.output.put_processbar('bar', auto_close=True);
        for i in range(1, 11):
            pywebio.output.set_processbar('bar', i / 10)
            time.sleep(0.1)

        put_file('simulation result.xlsx', content, 'download measurements')


    def Redesign():
        webbrowser.open('http://127.0.0.1:8000/tool/')

    def backH():
        webbrowser.open('https://github.com/RudgeLab/LOICA')



    put_buttons(['Show Result','Redesign','Learn more'],onclick=[showResult,Redesign,backH])

# Create your views here.



@csrf_exempt
def index(request):
    if request.method == 'POST':
        regularProp = []
        reporterProp = []
        hill1Prop = []
        hill2Prop = []
        origindata = json.loads(request.body)
        jsondata = origindata.get('jsonarr')
        globalname = origindata.get('globalname')
        globaldesc = origindata.get('globaldesc')
        globalnum = origindata.get('globalnum')
        globalgap = origindata.get('globalgap')
        for item in jsondata:
            if item.get('type') == 'rect':
                repoter = {"ratio": int(item.get('ratio')), "name": item.get('name'), "moer": int(item.get('moer'))}
                reporterProp.append(repoter)
            if item.get('type') == 'circle':
                regularProp.append({'ratio': int(item.get('ratio')), 'name': item.get('name'), 'moer':  int(item.get('moer'))})
            if item.get('type') == 'hill1':
                inputarr = item.get('input').split(",")
                outputarr = item.get('output').split(",")
                alphaInt = [int(alpha) for alpha in item.get('alpha').split(",")]
                hill1Prop.append({'input': inputarr, 'output': outputarr, 'alpha': alphaInt, 'name': item.get('name')})
            if item.get('type') == 'hill2':
                inputarr = item.get('input').split(",")
                outputarr = item.get('output').split(",")
                alphaInt = [int(alpha) for alpha in item.get('alpha').split(",")]
                hill2Prop.append({'input': inputarr, 'output': outputarr, 'alpha': alphaInt, 'name': item.get('name')})
        drawImage(regularProp, reporterProp, hill1Prop, hill2Prop, globalname, globaldesc, float(globalgap), int(globalnum))
        jsonresp = {
            'code': 200,
            'data': ["http://localhost:8000/media/line.png", "http://localhost:8000/media/hot.png"]
        }
    return HttpResponse(json.dumps(jsonresp))

def task_func2():
    content2 = open('app01/templates/Assay2.xlsx', 'rb').read()
    put_file('simulation result.xlsx', content2, 'download measurements')






























