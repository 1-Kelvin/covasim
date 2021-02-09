import covasim as cv
import sciris as sc
import numpy as np
import matplotlib.pyplot as pl
#from experiments import experiment 


if __name__ == "__main__":
    scenarios = {}
    vaccProbs = [0.2]
    for vaccination_prob in vaccProbs:
        
        scen_name = '% vaccinated: ' + str(vaccination_prob)
        scenarios[scen_name]={
                
                'name':scen_name,
                'pars': {
                    'interventions': [
                        cv.interventions.vaccine(days=1,prob=vaccination_prob)
                    ]
                }
                
        }
    
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

    vlbgSimulation = cv.sim.Sim(pars=pars, popfile='pop1.pop')    
    scens = cv.Scenarios(sim=vlbgSimulation, metapars=metapars, scenarios=scenarios)

    scens.run(verbose=1)
    
    img=vlbgSimulation.people.plot()
    img.show()
    img.savefig('popStatistics2.png')

   
    
  