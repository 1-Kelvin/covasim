import covasim as cv
import math

if __name__ == '__main__':

    msim1 = cv.MultiSim.load('pop1.msim')
    msim2 = cv.MultiSim.load('pop2.msim')
    msim3 = cv.MultiSim.load('pop3.msim')

    data1 = msim1.compare(output=True)
    data1 = data1.transpose()
    mue_in = sum(data1['cum_infections'])/11
    mue_se = sum(data1['cum_severe'])/11
    mue_cr = sum(data1['cum_critical'])/11
    mue_d = sum(data1['cum_deaths'])/11
    var_in = 0
    var_se = 0
    var_cr = 0
    var_d = 0
    for i in range(11):
        var_in = var_in + (data1['cum_infections'][i]   - mue_in)**2
        var_se = var_se + (data1['cum_severe'][i]       - mue_se)**2
        var_cr = var_cr + (data1['cum_critical'][i]     - mue_cr)**2
        var_d  = var_d  + (data1['cum_deaths'][i]       - mue_d )**2

    var_in = var_in/11
    var_se = var_se/11
    var_cr = var_cr/11
    var_d  = var_d /11

    print('\nSeed 1')
    print('cum_infections-----------------------------')
    print(f"min:{ min(data1['cum_infections']) }")
    print(f"av: {mue_in}")
    print(f"max: {max(data1['cum_infections'])}")
    print(f"var: {var_in}")
    print(f"sigma: {math.sqrt(var_in)}")

    print('cum_severe-----------------------------')
    print(f"min:{ min(data1['cum_severe']) }")
    print(f"av: {mue_se}")
    print(f"max: {max(data1['cum_severe'])}")
    print(f"var: {var_se}")
    print(f"sigma: {math.sqrt(var_se)}")

    print('cum_critical-----------------------------')
    print(f"min:{ min(data1['cum_critical']) }")
    print(f"av: {mue_cr}")
    print(f"max: {max(data1['cum_critical'])}")
    print(f"var: {var_cr}")
    print(f"sigma: {math.sqrt(var_cr)}")

    print('cum_deaths-----------------------------')
    print(f"min:{ min(data1['cum_deaths']) }")
    print(f"av: {mue_d}")
    print(f"max: {max(data1['cum_deaths'])}")
    print(f"var: {var_d}")
    print(f"sigma: {math.sqrt(var_d)}")

    data2 = msim2.compare(output=True)
    data2 = data2.transpose()
    mue_in = sum(data2['cum_infections']) / 11
    mue_se = sum(data2['cum_severe']) / 11
    mue_cr = sum(data2['cum_critical']) / 11
    mue_d = sum(data2['cum_deaths']) / 11
    var_in = 0
    var_se = 0
    var_cr = 0
    var_d = 0
    for i in range(11):
        var_in = var_in + (data2['cum_infections'][i] - mue_in) ** 2
        var_se = var_se + (data2['cum_severe'][i] - mue_se) ** 2
        var_cr = var_cr + (data2['cum_critical'][i] - mue_cr) ** 2
        var_d = var_d + (data2['cum_deaths'][i] - mue_d) ** 2

    var_in = var_in/11
    var_se = var_se/11
    var_cr = var_cr/11
    var_d  = var_d /11


    print('\nSeed 2')
    print('cum_infections-----------------------------')
    print(f"min:{min(data2['cum_infections'])}")
    print(f"av: {mue_in}")
    print(f"max: {max(data2['cum_infections'])}")
    print(f"var: {var_in}")
    print(f"sigma: {math.sqrt(var_in)}")

    print('cum_severe-----------------------------')
    print(f"min:{min(data2['cum_severe'])}")
    print(f"av: {mue_se}")
    print(f"max: {max(data2['cum_severe'])}")
    print(f"var: {var_se}")
    print(f"sigma: {math.sqrt(var_se)}")

    print('cum_critical-----------------------------')
    print(f"min:{min(data2['cum_critical'])}")
    print(f"av: {mue_cr}")
    print(f"max: {max(data2['cum_critical'])}")
    print(f"var: {var_cr}")
    print(f"sigma: {math.sqrt(var_cr)}")

    print('cum_deaths-----------------------------')
    print(f"min:{min(data2['cum_deaths'])}")
    print(f"av: {mue_d}")
    print(f"max: {max(data2['cum_deaths'])}")
    print(f"var: {var_d}")
    print(f"sigma: {math.sqrt(var_d)}")

    data3 = msim3.compare(output=True)
    data3 = data3.transpose()
    mue_in = sum(data3['cum_infections']) / 11
    mue_se = sum(data3['cum_severe']) / 11
    mue_cr = sum(data3['cum_critical']) / 11
    mue_d = sum(data3['cum_deaths']) / 11
    var_in = 0
    var_se = 0
    var_cr = 0
    var_d = 0
    for i in range(11):
        var_in = var_in + (data3['cum_infections'][i] - mue_in) ** 2
        var_se = var_se + (data3['cum_severe'][i] - mue_se) ** 2
        var_cr = var_cr + (data3['cum_critical'][i] - mue_cr) ** 2
        var_d = var_d + (data3['cum_deaths'][i] - mue_d) ** 2

    var_in = var_in / 11
    var_se = var_se / 11
    var_cr = var_cr / 11
    var_d = var_d / 11

    print('\nSeed 3')
    print('cum_infections-----------------------------')
    print(f"min:{min(data3['cum_infections'])}")
    print(f"av: {mue_in}")
    print(f"max: {max(data3['cum_infections'])}")
    print(f"var: {var_in}")
    print(f"sigma: {math.sqrt(var_in)}")

    print('cum_severe-----------------------------')
    print(f"min:{min(data3['cum_severe'])}")
    print(f"av: {mue_se}")
    print(f"max: {max(data3['cum_severe'])}")
    print(f"var: {var_se}")
    print(f"sigma: {math.sqrt(var_se)}")

    print('cum_critical-----------------------------')
    print(f"min:{min(data3['cum_critical'])}")
    print(f"av: {mue_cr}")
    print(f"max: {max(data3['cum_critical'])}")
    print(f"var: {var_cr}")
    print(f"sigma: {math.sqrt(var_cr)}")

    print('cum_deaths-----------------------------')
    print(f"min:{min(data3['cum_deaths'])}")
    print(f"av: {mue_d}")
    print(f"max: {max(data3['cum_deaths'])}")
    print(f"var: {var_d}")
    print(f"sigma: {math.sqrt(var_d)}")