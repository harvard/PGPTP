import collections, string

class Meeting(object):
  _by_course_id = collections.defaultdict(list)
  _by_year_term_id = collections.defaultdict(lambda: collections.defaultdict(dict))
  _by_faculty = collections.defaultdict(list)
  _meeting_types = set()  

  @classmethod
  def get_semesters(cls):
    semesters = []
    for year, terms in cls._by_year_term_id.iteritems():
      semesters += [(year, term) for term in terms]
    return semesters

  @classmethod
  def get_years(cls):
    return cls._by_year_term_id.keys()

  @classmethod
  def get_terms_for_year(cls, year):
    return cls._by_year_term_id.get(year, {}).keys()

  @classmethod
  def by_year_term(cls, year, term):
    return cls._by_year_term_id.get(year, {}).get(term, {}).values()

  @classmethod
  def by_year_term_id(cls, year, term, course_id):
    return cls._by_year_term_id.get(year, {}).get(term, {}).get(course_id)

  @classmethod
  def by_course_id(cls, course_id):
    return cls._by_course_id.get(course_id)

  @classmethod
  def before_semester(cls, year, term):
    semesters = [semester for semester in cls.get_semesters() if semester[0] < year or \
                (semester[0] == year and semester[1] < term)]
    meetings = []
    for semester in semesters:
      meetings += cls.by_year_term(*semester)
    return meetings

  @classmethod
  def before_semester_by_course(cls, year, term, course):
    return [meeting for meeting in cls.before_semester(year, term) if meeting.course == course]

  @classmethod
  def print_all(cls):
    '''
      for debugging
    '''
    print '\nPrinting all meetings...'
    for (course_id, meetings) in cls._by_course_id.iteritems():
      print Course.by_id(course_id)
      for meeting in meetings:
        print meeting
        print ''
    print 'Those are all the meetings ^_^\n'

  def __str__(self):
    return '[Meeting] ' + self.course.number + ', ' + str(self.year) + '-' + str(self.term) + ', ' + self.type + \
           '\n' + 'Lectures: ' + str(self.lectures) + \
           '\n' + 'Sections: ' + str(self.sections) + \
           '\n' + 'Labs: ' + str(self.labs) + \
           '\n' + 'Enrollment: ' + str(len(self.students))

  def __init__(self, course_id, faculty, year, term, full_year=False):
    self.lectures = []    # (day, start_hour, end_hour)
    self.sections = []    # (day, start_hour, end_hour)
    self.labs = []        # (day, start_hour, end_hour)
    self.students = []

    self.faculty = faculty
    self.year = year
    self.term = term
    self.type = 'type not set!'
    self.full_year = full_year

    self.ptp = 0

    # todo: handle if the course doesn't exist for some reason in the catalog
    self.course = Course.by_id(course_id)
    if self.course:
      self.course.meetings.add(self)
      self._by_year_term_id[year][term][course_id] = self
      self._by_course_id[course_id].append(self)
    else: 
      print 'No course found for ccn ' + str(course_id)

    if course_id == 5083:
      print 'wat!!!!!'
      print str(self)
      exit
class Course(object):
  _by_id = {}
  _by_department = collections.defaultdict(list)

  @classmethod
  def by_id(cls, course_id):
    return cls._by_id.get(course_id)

  @classmethod
  def by_department(cls, department):
    return cls._by_department.get(department)

  @classmethod
  def all_departments(cls):
    return cls._by_department.keys()

  @classmethod
  def print_all(cls):
    '''
      for debugging
    '''
    print '\nPrinting all courses...'
    for course in cls._by_id.values():
      print course
    print 'Those are all the courses :3\n'

  def get_deptnum(self):
    return self.department + ' ' + str(self.number)

  def get_level(self):
    if self.digits < 100 or (self.digits >= 900 and self.digits < 1000):
      return 0
    elif self.digits < 200 or (self.digits >= 1000 and self.digits < 2000):
      return 1
    elif self.digits < 300 or (self.digits >= 2000 and self.digits < 3000):
      return 2
    else:
      return 3

  def __str__(self):
    return '[Course] ' + self.get_deptnum() + ': ' + str(self.title)

  def __init__(self, course_id, department, number, title, gen_ed=False, core=False, description=''):
    # could change core, gen_ed to be non-boolean (but this is all the data the spreadsheets contain right now)

    self.id = course_id
    self.title = title
    self.description = description
    self.department = department 
    self.meetings = set()
    self.gen_ed = gen_ed
    self.core = core

    # todo: fix digits for a couple of weird cases
    self.number = number
    digits = number.translate(None, string.letters + '-').split('.')
    if digits[0]:
      self.digits = int(digits[0])
    else:
      self.digits = 0

    self._by_id[course_id] = self

    self._by_department[department].append(self)
