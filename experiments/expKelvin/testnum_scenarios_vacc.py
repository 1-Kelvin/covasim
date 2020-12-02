import covasim as cv
import sciris as sc

def createTestnumScenario(val=[1.5,1.8]):
    # Run options
    do_plot = 1
    do_show = 1
    verbose = 1
    start_day = '2020-03-01'

    # scenario variables
    # 0, 45, 90, 135
    test_delay = 2
    quar_test = 1
    sensitivity = 0.98
    target_age = 65 # retirement age
    vac_day = 135

    pars = pars = sc.objdict(
        pop_size        = 40000,
        pop_infected    = 10,
        pop_type        = 'synthpops',
        location        = 'Vorarlberg',
        n_days          = 180,
        verbose         = 1,
        pop_scale       = 10,
        n_beds_hosp     = 700 ,  #source: http://www.kaz.bmg.gv.at/fileadmin/user_upload/Betten/1_T_Betten_SBETT.pdf (2019)
        n_beds_icu      = 30,      # source: https://vbgv1.orf.at/stories/493214
        iso_factor      = dict(h=0.3, s=0.1, w=0.1, c=0.1), 
        quar_factor     = dict(h=0.8, s=0.0, w=0.0, c=0.1),
        start_day       = start_day
    )

    sim = cv.Sim(pars)
    sim.init_people(load_pop=True, popfile='vlbgPop40000.pop')


    sequence0 = [
        cv.test_num(200, symp_test=60, sensitivity=sensitivity, quar_test=quar_test, test_delay=test_delay), 
        cv.test_num(900, symp_test=70, sensitivity=sensitivity, quar_test=quar_test, test_delay=test_delay), 
        cv.test_num(1600, symp_test=80, sensitivity=sensitivity, quar_test=quar_test, test_delay=test_delay),
        cv.test_num(2500, symp_test=90, sensitivity=sensitivity, quar_test=quar_test, test_delay=test_delay),
    ]

    # no clip edges, subtarget
    sequence1 = [
        cv.test_num(100, symp_test=60, sensitivity=sensitivity, quar_test=quar_test, test_delay=test_delay),
        cv.test_num(100, symp_test=60, sensitivity=sensitivity, quar_test=quar_test, test_delay=test_delay, subtarget={'inds': sim.people.age>=target_age, 'vals': val[0]}),
        cv.test_num(450, symp_test=70, sensitivity=sensitivity, quar_test=quar_test, test_delay=test_delay),
        cv.test_num(450, symp_test=70, sensitivity=sensitivity, quar_test=quar_test, test_delay=test_delay, subtarget={'inds': sim.people.age>=target_age, 'vals': val[0]}),
        cv.test_num(800, symp_test=80, sensitivity=sensitivity, quar_test=quar_test, test_delay=test_delay),
        cv.test_num(800, symp_test=80, sensitivity=sensitivity, quar_test=quar_test, test_delay=test_delay, subtarget={'inds': sim.people.age>=target_age, 'vals': val[1]}), 
        cv.test_num(1250, symp_test=90, sensitivity=sensitivity, quar_test=quar_test, test_delay=test_delay),
        cv.test_num(1250, symp_test=90, sensitivity=sensitivity, quar_test=quar_test, test_delay=test_delay, subtarget={'inds': sim.people.age>=target_age, 'vals': val[1]}),
    ]

    # /w clip edges(40%), subtarget
    sequence2 = [
        cv.test_num(100, symp_test=60, sensitivity=sensitivity, quar_test=1, test_delay=test_delay),
        cv.test_num(100, symp_test=60, sensitivity=sensitivity, quar_test=1, test_delay=test_delay, subtarget={'inds': sim.people.age>=target_age, 'vals': val[0]}),
        cv.test_num(450, symp_test=70, sensitivity=sensitivity, quar_test=1, test_delay=test_delay),
        cv.test_num(450, symp_test=70, sensitivity=sensitivity, quar_test=1, test_delay=test_delay, subtarget={'inds': sim.people.age>=target_age, 'vals': val[0]}),
        cv.test_num(800, symp_test=80, sensitivity=sensitivity, quar_test=1, test_delay=test_delay),
        cv.test_num(800, symp_test=80, sensitivity=sensitivity, quar_test=1, test_delay=test_delay, subtarget={'inds': sim.people.age>=target_age, 'vals': val[1]}), 
        cv.test_num(1250, symp_test=90, sensitivity=sensitivity, quar_test=1, test_delay=test_delay),
        cv.test_num(1250, symp_test=90, sensitivity=sensitivity, quar_test=1, test_delay=test_delay, subtarget={'inds': sim.people.age>=target_age, 'vals': val[1]}),
    ]

    scenarios = { '32500/day': {
                'name':'32500/day',
                'pars': {
                    'interventions': [
                        cv.test_num(32500, symp_test=100, sensitivity=0.98, test_delay=2, start_day=start_day)
                    ]
                    }
                },
                'sequence0': {
                'name':'regular testing',
                'pars': {
                    'interventions': [
                            cv.sequence(days=[0, 45, 90, 135], interventions=sequence0),
                            cv.vaccine(days=vac_day, prob=0.3, rel_sus=0.5, rel_symp=0.1)
                        ]
                    }
                },
                'sequence1-65': {
                'name':'sequence-65',
                'pars': {
                    'interventions': [
                            cv.sequence(days=[0, 0, 45, 45, 90, 90, 135, 135], interventions=sequence1),
                            cv.vaccine(days=vac_day, prob=0.3, rel_sus=0.5, rel_symp=0.1)
                        ]
                    }
                },
                'sequence2-65/clip-edges': {
                'name':'sequence-65/clip-edges',
                'pars': {
                    'interventions': [
                            cv.sequence(days=[0, 0, 45, 45, 90, 90, 135, 135], interventions=sequence2),
                            cv.clip_edges(45, 0.7),
                            cv.vaccine(days=vac_day, prob=0.3, rel_sus=0.5, rel_symp=0.1),
                            cv.vaccine(days=vac_day, prob=0.8, rel_sus=0.5, rel_symp=0.1, subtarget={'inds': sim.people.age>=target_age, 'vals': 1.9})
                        ]
                    }
                },
            }

    return scenarios