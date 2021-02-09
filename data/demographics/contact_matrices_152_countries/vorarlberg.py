import synthpops as sp

##Parameters
populationSize = 40000


population = sp.contact_networks.generate_synthetic_population(populationSize, sp.datadir, location='Vorarlberg', state_location='Vorarlberg', country_location='Austria', sheet_name='Austria', school_enrollment_counts_available=True, with_school_types=False, school_mixing_type='random', average_class_size=20, inter_grade_mixing=0.1, average_student_teacher_ratio=16, average_teacher_teacher_degree=3, teacher_age_min=25, teacher_age_max=70, average_student_all_staff_ratio=15, average_additional_staff_degree=20, staff_age_min=20, staff_age_max=70, verbose=False, plot=False, write=True, return_popdict=True, use_default=False)

