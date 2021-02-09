import covasim as cv
import sciris as sc
import os
#from experiments import experiment 

pars = sc.objdict(
    pop_size        = 40e3,
    pop_infected    = 30,
    start_day       = '2020-03-01',
    location        = 'Vorarlberg',
    n_days          = 450,
    verbose         = 1,
    pop_scale       = 10,
    n_beds_hosp     = 700 ,  #source: http://www.kaz.bmg.gv.at/fileadmin/user_upload/Betten/1_T_Betten_SBETT.pdf (2019)
    n_beds_icu      = 30,      # source: https://vbgv1.orf.at/stories/493214 (2011 no recent data found)
)


if __name__ == "__main__":
    scenarios = {}
    start_social_distancing = 15
    testratelist = [4000]
    sd_drasticity = [3,4,5]
    for daily_tests in testratelist:
        for sd in sd_drasticity:

            contact_tracing_prob = 0.33
            contact_tracing_time = 2
            test_delay = 1
            social_distancing = 1-sd*0.1

            hygiene_measures = 0.8
            
            scenario_name = 'nTests:'+str(daily_tests) +',SD:' + str(sd*10)+'%'
            scenarios[scenario_name] = {
                'name':scenario_name,
                'pars': {
                    'interventions': [
                            #Basistestrate
                            cv.test_num(daily_tests=daily_tests,symp_test=100,quar_test=0.9,quar_policy='start',test_delay=test_delay),
                            cv.contact_tracing(trace_probs=0.25,trace_time=contact_tracing_time),
                            ##Lockdown 16.03
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing,layers='w'),
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing,layers='s'),
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing,layers='c'),
                            cv.change_beta(days=start_social_distancing,changes=hygiene_measures)]
                    }
                }
    cv.experiment.run_experiment(expName = 'minSD',scenarios = scenarios, pars=pars)

    #plot_res(scens, "NewTestsImage")
    
    
