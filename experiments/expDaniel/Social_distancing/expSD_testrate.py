import covasim as cv
import sciris as sc

#from experiments import experiment 

pars = sc.objdict(
    pop_size        = 40e3,
    pop_infected    = 30,
    start_day       = '2020-03-01',
    location        = 'Vorarlberg',
    n_days          = 180,
    verbose         = 1,
    pop_scale       = 10,
    n_beds_hosp     = 700 ,  #source: http://www.kaz.bmg.gv.at/fileadmin/user_upload/Betten/1_T_Betten_SBETT.pdf (2019)
    n_beds_icu      = 30,      # source: https://vbgv1.orf.at/stories/493214 (2011 no recent data found)
)

if __name__ == "__main__":
    scenarios = {}
    start_social_distancing = 15
    for i in range(0,4):
        daily_tests = 250
        test_delay = 2

        contact_tracing_prob = 0.25
        contact_tracing_time = 2

        social_distancing_work_layer = 1-i*0.25
        social_distancing_school_layer = 1-i*0.25
        social_distancing_community_layer = 1-i*0.25
        hygiene_measures = 0.8
        
        scenario_name = 'social distancing '+str(i*25)+'%'
        scenarios[scenario_name] = {
                
                'name':scenario_name,
                'pars': {
                    'interventions': [
                            #Basistestrate
                            cv.test_num(daily_tests=daily_tests,symp_test=100,quar_test=0.9,quar_policy='start',test_delay=test_delay),
                            cv.contact_tracing(trace_probs=0.25,trace_time=contact_tracing_time),
                            ##Lockdown 16.03
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing_work_layer,layers='w'),
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing_school_layer,layers='s'),
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing_community_layer,layers='c'),
                            cv.change_beta(days=start_social_distancing,changes=0.8),]
                    }
                }
    
    scens = cv.experiment.run_experiment(expName = 'SDEqualReduction',scenarios = scenarios, pars=pars)
    
  