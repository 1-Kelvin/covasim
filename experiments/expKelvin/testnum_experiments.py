import covasim as cv
import sciris as sc
#import experiments.SimVorarlberg.pars as pars

# Run options
do_plot = 1
do_show = 1
verbose = 1
start_day = '2020-04-04'

pars = pars = sc.objdict(
    pop_size        = 40000,
    pop_infected    = 10,
    pop_type        = 'synthpops',
    location        = 'Vorarlberg',
    n_days          = 180,
    verbose         = 1,
    pop_scale       = 10,
    n_beds_hosp     = 700 ,  #source: http://www.kaz.bmg.gv.at/fileadmin/user_upload/Betten/1_T_Betten_SBETT.pdf (2019)
    n_beds_icu      = 30,      # source: https://vbgv1.orf.at/stories/493214 (2011 no recent data found)
    iso_factor      = dict(h=0.3, s=0.1, w=0.1, c=0.1), # change this afterwards; default: 0.3, 0.1, 0.1, 0.1
    quar_factor = dict(h=0.8, s=0.0, w=0.0, c=0.1),
    start_day       = start_day
)

sim = cv.Sim(pars)
sim.init_people(load_pop=True, popfile='baseline_exp.pop')

# Scenario metaparameters
metapars = dict(
    n_runs    = 5, # Number of parallel runs; change to 3 for quick, 11 for real
    noise     = 0.1, # Use noise, optionally
    noisepar  = 'beta',
    rand_seed = 1,
    quantiles = {'low':0.4, 'high':0.6},
)

sequence0 = [
    cv.test_num(150, symp_test=40, sensitivity=0.98, quar_test=1, test_delay=2), 
    cv.test_num(200, symp_test=50, sensitivity=0.98, quar_test=1, test_delay=2), 
    cv.test_num(500, symp_test=70, sensitivity=0.98, quar_test=1, test_delay=2),
    cv.test_num(1000, symp_test=80, sensitivity=0.98, quar_test=1, test_delay=2)
]

sequence1 = [
    cv.test_num(100, symp_test=40, sensitivity=0.98, quar_test=1, test_delay=2),
    cv.test_num(50, symp_test=40, sensitivity=0.98, quar_test=1, test_delay=2, subtarget={'inds': sim.people.age>65, 'vals': 1.7}),
    cv.test_num(120, symp_test=50, sensitivity=0.98, quar_test=1, test_delay=2),
    cv.test_num(80, symp_test=50, sensitivity=0.98, quar_test=1, test_delay=2, subtarget={'inds': sim.people.age>65, 'vals': 1.7}),
    cv.test_num(250, symp_test=70, sensitivity=0.98, quar_test=1, test_delay=2),
    cv.test_num(250, symp_test=70, sensitivity=0.98, quar_test=1, test_delay=2, subtarget={'inds': sim.people.age>65, 'vals': 1.8}), 
    cv.test_num(650, symp_test=80, sensitivity=0.98, quar_test=1, test_delay=2),
    cv.test_num(350, symp_test=80, sensitivity=0.98, quar_test=1, test_delay=2, subtarget={'inds': sim.people.age>65, 'vals': 1.8}),
]

sequence2 = [
    cv.test_num(100, symp_test=50, sensitivity=0.98, quar_test=1, test_delay=2),
    cv.test_num(100, symp_test=50, sensitivity=0.98, quar_test=1, test_delay=2, subtarget={'inds': sim.people.age>65, 'vals': 1.7}),
    cv.test_num(450, symp_test=60, sensitivity=0.98, quar_test=1, test_delay=2),
    cv.test_num(450, symp_test=60, sensitivity=0.98, quar_test=1, test_delay=2, subtarget={'inds': sim.people.age>65, 'vals': 1.7}),
    cv.test_num(800, symp_test=70, sensitivity=0.98, quar_test=1, test_delay=2),
    cv.test_num(800, symp_test=70, sensitivity=0.98, quar_test=1, test_delay=2, subtarget={'inds': sim.people.age>65, 'vals': 1.8}), 
    cv.test_num(1250, symp_test=80, sensitivity=0.98, quar_test=1, test_delay=2),
    cv.test_num(1250, symp_test=80, sensitivity=0.98, quar_test=1, test_delay=2, subtarget={'inds': sim.people.age>65, 'vals': 1.8}),
]

# sterblichkeit 
# 400 tote max!

# singled out scenario for fast testing purposes 
test_scenario = { 'sequence2-65++': {
              'name':'sequence-65+/int',
              'pars': {
                  'interventions': [
                        cv.sequence(days=[0, 0, 45, 45, 90, 90, 135, 135], interventions=sequence2),
                        cv.clip_edges(45, 0.6)
                    ]
                  }
            },
}

scenarios = { '30000/day': {
              'name':'30000/day',
              'pars': {
                  'interventions': [
                      cv.test_num(32500, symp_test=100, sensitivity=0.98, test_delay=2, start_day=start_day)
                  ]
                  }
            },
#            '40000/day': {
#              'name':'40000/day',
#              'pars': {
#                  'interventions': [
#                      cv.test_num(40000, symp_test=100, sensitivity=0.98, test_delay=2, start_day=start_day)
#                  ]
#                  }
#            },
            'sequence0': {
              'name':'sequence 0',
              'pars': {
                  'interventions': [
                        cv.sequence(days=[0, 45, 90, 135], interventions=sequence0)
                    ]
                  }
            },
            'sequence1-65+': {
              'name':'sequence-65+',
              'pars': {
                  'interventions': [
                        cv.sequence(days=[0, 0, 45, 45, 90, 90, 135, 135], interventions=sequence1)
                    ]
                  }
            },
            'sequence2-55+/int': {
              'name':'sequence-65+/int',
              'pars': {
                  'interventions': [
                        cv.sequence(days=[0, 0, 45, 45, 90, 90, 135, 135], interventions=sequence2),
                        cv.clip_edges(45, 0.6)
                    ]
                  }
            },
        }



if __name__ == '__main__':
    scens = cv.Scenarios(sim=sim, metapars=metapars, scenarios=scenarios) # test_scenario for testing single scenario
    scens.run(verbose=verbose)
    if do_plot:
        fig1 = scens.plot(do_show=do_show)