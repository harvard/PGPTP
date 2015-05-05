import collections

class Student(object):
  _by_id = {}
  _by_concentration = collections.defaultdict(list)
  _by_year_term = collections.defaultdict(lambda: collections.defaultdict(set))

  @classmethod
  def get_concentrations(cls):
    return cls._by_concentration.keys()

  @classmethod
  def by_id(cls, id):
    return cls._by_id.get(id)

  @classmethod
  def by_year_term(cls, year, term):
    return cls._by_year_term.get(year, {}).get(term, [])

  @classmethod
  def print_all(cls):
    '''
      for debugging
    '''
    print '\nPrinting all students...\n'
    for student in cls._by_id.values():
      print student
      print ''
    print 'Those are all the students!\n'

  def add_year_term(year, term):
    self.year_terms.add((year, term))
    self._by_year_term[year][term].add(self)

  def __str__(self):
    return '[Student '+ str(self.id) + ']:\n' \
           + 'Concentrations: ' + str(self.concentrations) + '\n' \
           + 'Secondary: ' + self.secondary + '\n' \
           + 'Terms: ' + str([str(year) + '-' + str(term) for (year, term) in self.year_terms]) + '\n' \
           + 'Courses: ' + str([meeting.course.number for meeting in self.meetings])

  def __init__(self, student_id, ugrad, concentrations, secondary, adv_standing, year_terms=[]):
    self.id = student_id
    self.ugrad = ugrad
    self.concentrations = concentrations
    self.secondary = secondary
    self.adv_standing = adv_standing
    self.year_terms = year_terms
    self.meetings = []
    
    self._by_id[student_id] = self
    for concentration in self.concentrations:
      self._by_concentration[concentration].append(self)

    # will we actually use by_year_term?
    #for ((year, term) in year_terms):
    # self._by_year_term[year][term].add(self)
