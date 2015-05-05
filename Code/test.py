import ptp, datautils

l = datautils.Loader('data/full/out')

start_year = 2010
end_year = 2014

l.load(start_year, end_year)

#ptp.Course.print_all()
#ptp.Meeting.print_all()
#ptp.Student.print_all()


# THIS WRITES OUT SPECIFIC PREDICTIONS 

semesters = [(2014, 1), (2014,0), (2013, 1), (2013, 0)]
predictions = ptp.experiment.predict_semesters(semesters, predictor=ptp.predictors.predictor_weatherman)

ptp.experiment.write_predictions(predictions, 'predictions', 'weatherman_2014_1.csv')



# THIS DOES THE TIME SERIES STUFF

#predictions = ptp.experiment.predict_all_semesters(predictor=ptp.predictors.predictor_lin_regr)
#scores_by_semester = ptp.experiment.score_by_semester(predictions)

#scores = [str(scores_by_semester[semester]) for semester in ptp.Meeting.get_semesters()]
#rint '\t'.join(scores[::-1])
	