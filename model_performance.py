''' Render final scores of all models
'''

import json
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('ggplot')

model_performance = {}
for filename in ('model_performance_2.txt',
                 'model_performance_2a.txt',
                 'model_performance_2b.txt',
                 'model_performance_2c.txt',
#                 'model_performance_2d.txt',
             ):
    print "loading", filename
    for line in open(filename, 'r'):
        d = json.loads(line)
        model_performance[d['name']] = d['perf']

baseline_values = model_performance['LogReg_CV balanced']

print "html"
h = open('docs/model_performance_table.js', 'w')
for k, d in sorted(model_performance.items()):
    s = "<tr><th>%s</th>" % (k, )
    for k2 in ('auc', 'f1', 'prec', 'score', 'test_f1_inv', 'test_prec_inv', 'test_score',) :
        v = d[k2]
    
        if k2 in ('baseline', 'test_profit', 'elapsed', 'timestamp', 'model_group'):
            continue
        try:
            base_value = baseline_values[k2]
        except:
            continue
        if k2 != 'auc':
            base_value = round(model_performance['Always 1'][k2], 3)
            
        if k2 in ('auc', 'test_f1_inv', 'test_prec_inv', 'test_score') and round(v, 3) > base_value:
            s += "<td class='better'>%.3f</td>" % (v, )
        else:
            s += "<td>%.3f</td>" % (v, )
    s += "</tr>"
    h.write('document.write("' + s + '")\n')
h.close()

model_performance_df = pd.DataFrame(model_performance).T
for col in ('auc', 'test_score', 'test_f1_inv', 'test_prec_inv'):
    print col
    base_value = baseline_values[col]
    if col != 'auc':
        base_value = model_performance['Always 1'][col]
    plt.figure(figsize=(15, .25*len(model_performance_df)))
    plt.axvline(x=base_value, color='darkgrey')
    sorted_values = model_performance_df[col].fillna(0).sort_values()
    sorted_values.plot(kind='barh', 
                       color=[['darkblue', 'orange'][i] for i in list(sorted_values.apply(lambda x: round(x, 3)) > round(base_value, 3))],
                       width=0.85)
    plt.title(col.replace('_inv', ''))
    plt.savefig('docs/images/score_' + col.replace('_inv', '') + '.png',
                bbox_inches='tight')

    
