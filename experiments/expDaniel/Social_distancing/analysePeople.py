import covasim as cv
import sciris as sc
import numpy as np
import matplotlib.pyplot as pl
import collections

#from experiments import experiment 


if __name__ == "__main__":
    
    pars = sc.objdict(
        pop_size        = 40000,
        pop_infected    = 10,
        start_day       = '2020-02-24',
        location        = 'Vorarlberg',
        pop_type = 'synthpops',
        n_days          = 180,
        verbose         = 0,
        pop_scale       = 10,
        n_beds_hosp     = 700 ,  #source: http://www.kaz.bmg.gv.at/fileadmin/user_upload/Betten/1_T_Betten_SBETT.pdf (2019)
        n_beds_icu      = 30,      # source: https://vbgv1.orf.at/stories/493214 (2011 no recent data found)
        iso_factor      = dict(h=1, s=1, w=1, c=1)
    )

    metapars = dict(
            n_runs    = 11,
            rand_seed = 1,
            quantiles = {'low':0.1, 'high':0.9},
        )
    pars = sc.objdict(
    pop_size        = 40e3,
    pop_infected    = 30,
    start_day       = '2020-03-01',
    location        = 'Vorarlberg',
    pop_type = 'synthpops',
    n_days          = 240,
    verbose         = 0,
    pop_scale       = 10,
    n_beds_hosp     = 700 ,  #source: http://www.kaz.bmg.gv.at/fileadmin/user_upload/Betten/1_T_Betten_SBETT.pdf (2019)
    n_beds_icu      = 30,      # source: https://vbgv1.orf.at/stories/493214 (2011 no recent data found)
)

    seed = 1
    vlbgSimulation = cv.sim.Sim(pars=pars, popfile='pop40k.pop',load_pop=True)
    vlbgSimulation.set_seed(seed=seed)
    vlbgSimulation.run()
    myPeople = cv.load('pop40k.pop')
    tree = cv.analysis.TransTree(vlbgSimulation)

    targets = [len(i) for i in tree.targets]

    
    rankedSpreaders=sorted(range(len(targets)),key=targets.__getitem__)
    superSpreaders = rankedSpreaders[0:39999]
    vlbgSimulation = cv.sim.Sim(pars=pars, popfile='pop1.pop',load_pop=True)
    
    
    vlbgSimulation.set_seed(seed=seed)
    scenarios={}
    
    scenarios['vaccinateTopSpreaders 10%'] = {
                'name':'vaccinateTopSpreaders 10 %',
                'pars': {
                    'interventions': [
                            #Basistestrate
                            cv.vaccine(days=0,prob=0.0,subtarget={'inds':superSpreaders,'vals':1.0}),
                            ]
                    }
                }
    scenarios['vaccinateRandom 10%'] = {
                'name':'vaccinateRandom 10 %',
                'pars': {
                    'interventions': [
                            #Basistestrate
                            cv.vaccine(days=0,prob=0.1),
                            ]
                    }
    }
    
    scens = cv.Scenarios(vlbgSimulation,scenarios=scenarios,metapars=dict(n_runs    = 1,
            rand_seed = 1,
            quantiles = {'low':0.1, 'high':0.9},
        ))
    scens.run(reseed=False)
    cv.experiment.plot_res(scens,expName='vaccTopSpreaders10pc')

