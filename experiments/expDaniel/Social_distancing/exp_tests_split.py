import covasim as cv
import sciris as sc
import os
#from experiments import experiment 

pars = sc.objdict(
    pop_size        = 40e3,
    pop_infected    = 30,
    start_day       = '2020-03-01',
    location        = 'Vorarlberg',
    n_days          = 360,
    verbose         = 1,
    pop_scale       = 10,
    n_beds_hosp     = 700 ,  #source: http://www.kaz.bmg.gv.at/fileadmin/user_upload/Betten/1_T_Betten_SBETT.pdf (2019)
    n_beds_icu      = 30,      # source: https://vbgv1.orf.at/stories/493214 (2011 no recent data found)
)
def plot_res(scenarios,expName = 'TestsNew'):
    notCreated = True
    targetDirectory = os.path.join('Results',expName)
    cnt = 0
    while(notCreated):
        try:
            os.mkdir(targetDirectory+str(cnt))
        except OSError:
            print("Creation Failed")
            cnt+=1
        else:
            notCreated = False
    filePath = os.path.join(targetDirectory+str(cnt),expName+'Results.xlsx')
    scenarios.to_excel(filePath)
    #summaryPath = os.path.join(targetDirectory+str(cnt),expName+'Summary.txt')
    #summarize_results(scenarios,summaryPath)
    figPath = os.path.join(targetDirectory+str(cnt),expName+'Results.png')
    scenarios.plot(do_show=True,do_save=True,fig_path=figPath, to_plot=sc.odict(

        {
            'cumulativ infections':['cum_infections'],
            'new infections': ['new_infections'],
            'deaths': ['cum_deaths']
        }
    
    ))


def run_experiment(expName = 'stand_name', scenarios = None, pars = None, metapars = None, do_plot = True):

    if metapars == None:
        metapars = dict(
            n_runs    = 11,
            rand_seed = 1,
        )
    if scenarios == None:
        scenarios = {
            'timeline': {
              'name':'Intervention Timeline in Austria',
              'pars': {
                  'interventions': [
                        #Basistestrate
                        cv.test_num(daily_tests=250,symp_test=100,quar_test=0.9,quar_policy='start',test_delay=2),
                        cv.contact_tracing(trace_probs=0.5,trace_time=2),]
                  }
              },
            }
    vlbgSimulation = cv.sim.Sim(pars=pars, load_pop=True, popfile='pop40k.pop')
   
    scens = cv.Scenarios(sim=vlbgSimulation, metapars=metapars, scenarios=scenarios)

    scens.run(verbose=1)
    if(do_plot==True):
        plot_res(scens,expName=expName)
    return scens 
if __name__ == "__main__":
    scenarios = {}
    metapars = dict(
            n_runs    = 11,
            rand_seed = 1,
            quantiles = {'low':0.1, 'high':0.9},
        )
    start_social_distancing = 15
    testratelist = [250,500,1000]
    testspeedlist = [3,2,1]
    for daily_tests in testratelist:
        for test_delay in [2]:

            contact_tracing_prob = 0.25
            contact_tracing_time = 2

            social_distancing_work_layer = 0.7
            social_distancing_school_layer = 0.7
            social_distancing_community_layer = 0.3
            hygiene_measures = 0.8
            
            scenario_name = 'tests:'+str(daily_tests) +'n,' + str(test_delay)+'d'
            scenarios[scenario_name] = {
                'name':scenario_name,
                'pars': {
                    'interventions': [
                            cv.test_num(daily_tests=daily_tests,symp_test=100,quar_test=0.9,quar_policy='start',test_delay=test_delay),
                            cv.contact_tracing(trace_probs=0.25,trace_time=contact_tracing_time),
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing_work_layer,layers='w'),
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing_school_layer,layers='s'),
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing_community_layer,layers='c'),
                            cv.change_beta(days=start_social_distancing,changes=0.8),]
                    }
                }
    
    #cv.experiment.run_experiment(expName = 'test_var_num',scenarios = scenarios, pars=pars,metapars=metapars)
    scenarios = {}
    for daily_tests in [500]:
        for test_delay in testspeedlist:

            contact_tracing_prob = 0.25
            contact_tracing_time = 2

            social_distancing_work_layer = 0.7
            social_distancing_school_layer = 0.7
            social_distancing_community_layer = 0.3
            hygiene_measures = 0.8
            
            scenario_name = 'tests:'+str(daily_tests) +'n,' + str(test_delay)+'d'
            scenarios[scenario_name] = {
                'name':scenario_name,
                'pars': {
                    'interventions': [
                            cv.test_num(daily_tests=daily_tests,symp_test=100,quar_test=0.9,quar_policy='start',test_delay=test_delay),
                            cv.contact_tracing(trace_probs=0.25,trace_time=contact_tracing_time),
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing_work_layer,layers='w'),
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing_school_layer,layers='s'),
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing_community_layer,layers='c'),
                            cv.change_beta(days=start_social_distancing,changes=0.8),]
                    }
                }

    #cv.experiment.run_experiment(expName = 'test_var_speed',scenarios = scenarios, pars=pars,metapars=metapars)
    
    scenarios = {}
    daily_tests=250
    test_delay = 2
    scenario_name = 'tests:'+str(daily_tests) +'n,' + str(test_delay)+'d'
    scenarios[scenario_name] = {
                'name':scenario_name,
                'pars': {
                    'interventions': [
                            cv.test_num(daily_tests=daily_tests,symp_test=100,quar_test=0.9,quar_policy='start',test_delay=test_delay),
                            cv.contact_tracing(trace_probs=0.25,trace_time=contact_tracing_time),
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing_work_layer,layers='w'),
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing_school_layer,layers='s'),
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing_community_layer,layers='c'),
                            cv.change_beta(days=start_social_distancing,changes=0.8),]
                    }
                }
    for daily_tests in [250,500,1000]:
        for test_delay in [2,3]:

            contact_tracing_prob = 0.25
            contact_tracing_time = 2

            social_distancing_work_layer = 0.7
            social_distancing_school_layer = 0.7
            social_distancing_community_layer = 0.3
            hygiene_measures = 0.8
            
            scenario_name = 'tests:'+str(daily_tests) +'n,' + str(test_delay)+'d'
            scenarios[scenario_name] = {
                'name':scenario_name,
                'pars': {
                    'interventions': [
                            cv.test_num(daily_tests=daily_tests,symp_test=100,quar_test=0.9,quar_policy='start',
                            test_delay=test_delay),
                            cv.contact_tracing(trace_probs=0.25,trace_time=contact_tracing_time),
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing_work_layer,layers='w'),
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing_school_layer,layers='s'),
                            cv.clip_edges(days=start_social_distancing,changes=social_distancing_community_layer,layers='c'),
                            cv.change_beta(days=start_social_distancing,changes=0.8),]
                    }
                }

    #cv.experiment.run_experiment(expName = 'test_compare',scenarios = scenarios, pars=pars,metapars=metapars)
    metapars = dict(
            n_runs    = 11,
            rand_seed = 1,
            quantiles = {'low':0.5, 'high':0.5},
        )
    cv.experiment.run_experiment(expName = 'test_compare_noConf',scenarios = scenarios, pars=pars,metapars=metapars)