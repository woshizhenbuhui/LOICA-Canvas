import datetime

import pandas as pd
from flapjack import *
import loica as lc
import matplotlib.pyplot as plt
from django.conf import settings
import os

def growth_rate(t):
    return gompertz_growth_rate(t, 0.01, 1, 1, 0.5)

def biomass(t):
    return gompertz(t, 0.01, 1, 1, 0.5)


def drawImage(regularProp, reporterProp, hill1Prop, hill2Prop, globalname, globaldesc, globalgap, globalnum):
    osc = lc.GeneticNetwork()
    allMap = {};
    acts = []
    for regular in regularProp:
        act = lc.Regulator(name=f'{regular["name"]}', init_concentration=regular["moer"], degradation_rate=regular["ratio"]);
        acts.append(act)
        allMap.setdefault(regular["name"], act)

    osc.add_regulator(acts)
    reporters = []
    for reporter in reporterProp:
        rep = lc.Reporter(name=f'{reporter["name"]}', init_concentration=reporter["moer"], color='blue',degradation_rate=reporter["ratio"])
        reporters.append(rep)
        allMap.setdefault(reporter["name"], rep)
    osc.add_reporter(reporters)
    ops = []
    for hill2op in hill2Prop:
        inputs = [allMap.get(item) for item in hill2op["input"]]
        outputs = [allMap.get(item) for item in hill2op["output"]]
        ops.append( lc.Hill2(inputs, outputs, hill2op["alpha"], K=[10, 10], n=[2, 2], name=hill2op["name"]) )
    for hill1op in hill1Prop:
        inputs = [allMap.get(item) for item in hill1op["input"]]
        outputs = [allMap.get(item) for item in hill1op["output"]]
        ops.append(lc.Hill1(inputs[0], outputs, hill1op["alpha"], K=10, n=2, name=hill1op["name"]))


    # op2 = lc.Hill1(acts[1], [acts[2], reporters[1]], alpha=[1, 100], K=10, n=2)
    # op3 = lc.Hill1(acts[2], [rep, reporters[2]], alpha=[1, 100], K=10, n=2)
    osc.add_operator(ops)

    plt.figure(figsize=(3, 3), dpi=300)
    t = osc.draw(contracted=False, arrowsize=7, node_size=500, linewidths=0, alpha=1)
    # t = osc.draw(contracted=False, arrowsize=7, node_size=500, linewidths=0, alpha=1)
    # plt.show()

    metab = lc.SimulatedMetabolism('test', biomass, growth_rate)
    sample = lc.Sample(genetic_network=osc,
                       metabolism=metab)
    assay = lc.Assay([sample],
                     n_measurements=globalnum,
                     interval=globalgap,
                     name=f'{globalname}',
                     description=f'{globaldesc}'
                     )
    assay.run(stochastic=False)
    m = assay.measurements

    gg=pd.DataFrame(m)

    wr=pd.ExcelWriter('app01/templates/Assay2.xlsx')
    gg.to_excel(wr,float_format='%.5f')
    wr.save()
    file_path = 'app01/templates/Assay2.xlsx'
    writer = pd.ExcelWriter(file_path)
    gg.to_excel(writer)
    writer.save()

    content = open('app01/templates/Assay2.xlsx', 'rb').read()



    print(m)
    fig, ax = plt.subplots(1, 1)  # fig is to create a canvas, ax is to draw a subgraph of the object
    '''
    Show line graph
    '''
    for reporter in reporterProp:
        m[m.Signal == f'{reporter["name"]}'].plot(x='Time', y='Measurement', style='-', ax=ax)
    plt.legend([f'{reporter["name"]}' for reporter in reporterProp])
    if os.path.exists(settings.BASE_DIR / 'static/media/line.png'):
        os.remove(settings.BASE_DIR / 'static/media/line.png')
    plt.title('Line Chart')
    plt.savefig(settings.BASE_DIR / 'static/media/line.png')
    plt.show()

    '''
    Display and heat map correlation
    '''

    col = lc.Colony(osc, 1, 1)
    kymo = col.kymograph(nx=500, t0=0, tmax=48)  # nx=500, t0=0, tmax=48

    '''
    Show heat map
    '''
    plt.figure(figsize=(3, 2.5), dpi=300)
    plt.imshow(col.map_kymo(col.norm_kymo(kymo)), aspect='auto')
    if os.path.exists(settings.BASE_DIR / 'static/media/hot.png'):
        os.remove(settings.BASE_DIR / 'static/media/hot.png')
    plt.title('Heat Map')
    plt.savefig(settings.BASE_DIR / 'static/media/hot.png')
    plt.show()





