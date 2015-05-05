import ptp
import pdb
import numpy as np
from sklearn import linear_model

np.set_printoptions(threshold='nan')


# Helpers 

def features(meetings):
  feats = []
  for meeting in meetings:
    feat = []

    # past enrollments
    if not meeting.is_new:
      earlier = ptp.Meeting.before_semester_by_course(meeting.year, meeting.term, meeting.course)
      most_recent = max(earlier, key=lambda m: (m.year, m.term))
      feat.append(len(most_recent.students))
    else:
      feat.append(0)
 
    # including the features below just makes the basic regression worse.

    # class type (is lecture?)
    #feat.append(1 if 'Lecture' in meeting.type else 0)

    #for i in range(4):
    #  feat.append(1 if meeting.course.get_level() == i else 0)

    # department
    #for dept in ptp.Course.all_departments():
    #  feat.append(1 if meeting.course.department == dept else 0)
    
    feats.append(feat)

  return np.array(feats)

def enrollments(meetings):
  return np.array([[len(meeting.students)] for meeting in meetings])

def new_course_default(meeting):
  if ('Lecture' in meeting.type):
    return 30
  else:
    return 10


# Predictors

def predictor_ptp(meetings, meetings_to_predict):
  predictions = {}
  for meeting_to_predict in meetings_to_predict:
    predictions[meeting_to_predict] = meeting_to_predict.ptp
  return predictions 

def predictor_weatherman(meetings, meetings_to_predict):
  predictions = {}
  for meeting_to_predict in meetings_to_predict:
    matches = [meeting for meeting in meetings if meeting.course == meeting_to_predict.course]
    if (matches):
      most_recent = max(matches, key=lambda m: (m.year, m.term))
      predictions[meeting_to_predict] = len(most_recent.students)
    else:
      predictions[meeting_to_predict] = new_course_default(meeting_to_predict)
  return predictions

def predictor_lin_regr(meetings, meetings_to_predict):
  regr = linear_model.LinearRegression()
  regr.fit(features(meetings), enrollments(meetings))

  feats = features(meetings_to_predict)

  predictions = regr.predict(feats).flatten().astype(int)

  # predict
  return dict(zip(meetings_to_predict, predictions))
