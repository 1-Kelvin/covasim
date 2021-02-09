import covasim as cv
import sciris as sc

#from experiments import experiment 

pars = sc.objdict(
    pop_size        = 40e3,
    pop_infected    = 15,
    start_day       = '2020-03-01',
    n_days          = 90,
    verbose         = 1,
    pop_scale       = 10,
    n_beds_hosp     = 200 ,  #source: http://www.kaz.bmg.gv.at/fileadmin/user_upload/Betten/1_T_Betten_SBETT.pdf (2019)
    n_beds_icu      = 20,      # source: https://vbgv1.orf.at/stories/493214 (2011 no recent data found)
    rel_crit_prob = 2.5,
)

if __name__ == "__main__":
    
    lockdown1_date = '2020-03-18'
    lockdown1_store_opening_date = '2020-04-14'
    lockdown1_school_opening_date = '2020-05-01'
    lockdown1_restaurant_opening_date = '2020-05-15'
    reduced_masks_date = '2020-06-15'
    
    scenarios = {
            'timeline': {
              'name':'Intervention Timeline in Austria',
              'pars': {
                  'interventions': [
                        #Basistestrate
                        cv.test_num(start_day=lockdown1_date,daily_tests=250,symp_test=100,quar_test=0.9,test_delay=2),
                        cv.contact_tracing(start_day=lockdown1_date,trace_probs=0.5,trace_time=2),
                        ##Lockdown 16.03
                        cv.clip_edges(days=lockdown1_date,changes=0.6,layers='w'),
                        cv.clip_edges(days=lockdown1_date,changes=0.15,layers='s'),
                        cv.clip_edges(days=lockdown1_date,changes=0.25,layers='c'),
                        cv.change_beta(days=lockdown1_date,changes=0.8),

                        ## Eröffnung Geschaefte
                        cv.clip_edges(days=lockdown1_store_opening_date,changes=0.4,layers='c'),

                        ##Eroeffnung Schulen
                        cv.clip_edges(days=lockdown1_school_opening_date,changes=0.8,layers='s'),
                        cv.clip_edges(days=lockdown1_school_opening_date,changes=0.75,layers='w'),
                        ##Eroeffnung Gastronomie
                        cv.clip_edges(days=lockdown1_restaurant_opening_date,changes=0.7,layers='c'),
                        cv.clip_edges(days=lockdown1_restaurant_opening_date,changes=0.85,layers='w'),
                        ]
                  }
              },
            }
    scens = cv.experiment.run_experiment(expName = 'verTimeline',scenarios = scenarios, pars=pars, do_plot=False)
    cv.experiment.plot_res_diagnoses(scens,expName = 'verTimeline')