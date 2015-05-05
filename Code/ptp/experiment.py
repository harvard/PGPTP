from course import Meeting
import errors
import predictors
import csv, os

def write_predictions(predictions, root, filename):
  print('\nwriting predictions to ' + root + '/' + filename)

  if not os.path.exists(root):
    os.makedirs(root)
  outfile = open(root + '/' + filename, 'w')
  writer = csv.writer(outfile)
  writer.writerow(['ccn', 'number', 'year', 'term', 'actual enrollment', 'predicted enrollment', 'ptp', 'new course'])
  for meeting, prediction in predictions.iteritems():
    writer.writerow([meeting.course.id, meeting.course.department + ' ' +
                     str(meeting.course.number), meeting.year, meeting.term,
                     len(meeting.students), prediction, meeting.ptp, meeting.is_new])
  outfile.close()

def predict_semesters(semesters, predictor=predictors.predictor_weatherman, filt=None):
  predictions = {}
  for semester in semesters:
    current = filter(filt, Meeting.by_year_term(*semester))
    earlier = filter(filt, Meeting.before_semester(*semester))
    if earlier:
      predictions.update(predictor(earlier, current))

  return predictions

def predict_all_semesters(predictor=predictors.predictor_weatherman, filt=None):
  return predict_semesters(Meeting.get_semesters(), predictor, filt)

def score_all_predictions(predictions, comp=errors.abs_TF_diff):
  actuals = [len(meeting.students) for meeting in predictions.keys()]
  predictions = predictions.values()
  return comp(predictions, actuals)

def score_by_semester(predictions, comp=errors.abs_TF_diff):
  semesters = Meeting.get_semesters()
  scores = {}
  for semester in semesters:
    meetings = Meeting.by_year_term(*semester)
    actuals = []
    predicts = []
    for meeting in meetings:
      if meeting in predictions:
        actuals.append(len(meeting.students))
        predicts.append(predictions[meeting])
    if predicts:
      scores[semester] = comp(predicts, actuals)
    else:
      scores[semester] = -1
  return scores

      





