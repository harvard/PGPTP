import sys, os, csv, collections, ast
import ptp, params

class Loader(object):
    def _load_times(self, start_year, end_year):
        for year in range(start_year, end_year + 1):
            for term in range(2):
                path = '/'.join([self.root, str(year), str(term), params.fname_times])
                if not os.path.exists(path):
                    print 'unable to find ' + path
                else: 
                    infile = open(path, 'rU')
                    reader = csv.reader(infile)
                    header = reader.next()
                    ccn = -1
                    for l in reader:
                        # new course
                        if ccn != int(l[2]):
                            ccn = int(l[2])
                            if l[3]:
                                instructor = int(l[3])
                            else:
                                instructor = None
                                print 'missing instructor info for ccn ' + l[2] + ', ' + str(year) + '-' + str(term)
                            full_year = ccn in self._full_year_meetings[year]
                            meeting = ptp.Meeting(ccn, instructor, year, term, full_year)
                            if not ptp.Meeting.before_semester_by_course(meeting.year, meeting.term, meeting.course):
                                meeting.is_new = True
                            else:
                                meeting.is_new = False
                        mtg_type = l[4]
                        time = ast.literal_eval(l[5])
                        if ('Section' in mtg_type or 'Screening' in mtg_type):
                            meeting.sections.append(time)
                        elif ('Lab' in mtg_type):
                            meeting.labs.append(time)
                        else:
                            meeting.lectures.append(time)
                            meeting.type = mtg_type

    # loads courses for year = [start_year, end_year)
    def _load_catalog(self, start_year, end_year):
        for year in range(start_year, end_year + 1):
            for term in range(2):
                path = '/'.join([self.root, str(year), str(term), params.fname_catalog])
                if not os.path.exists(path):
                    print 'unable to find ' + path
                else: 
                    infile = open(path, 'rU')
                    reader = csv.reader(infile)
                    header = reader.next()
                    for l in reader:
                        ccn = int(l[2])
                        numsplit = l[3].strip().split(' ')
                        dept = numsplit[0]
                        if len(numsplit) > 1:
                            num = numsplit[1]
                        else:
                            num = ''
                        title = l[4]
                        full_year = l[7] != ''
                        core = l[8] != ''
                        gen_ed = l[9] != ''
                        ptp.Course(ccn, dept, num, title, core, gen_ed)
                        if full_year:
                            self._full_year_meetings[year].add(ccn)
                    infile.close()

    def _load_ptp(self, start_year, end_year):
        for year in range(start_year, end_year + 1):
            for term in range(2):
                path = '/'.join([self.root, str(year), str(term), params.fname_ptp])
                if not os.path.exists(path):
                    print 'unable to find ' + path
                else:
                    infile = open(path, 'rU')
                    reader = csv.reader(infile)
                    header = reader.next()
                    for l in reader:
                        ccn = int(l[0])
                        meeting = ptp.Meeting.by_year_term_id(year, term, ccn)
                        if meeting:
                            meeting.ptp = int(l[3])
                        else:
                            print 'Unable to load ptp: missing meeting for ' + l[1] + ', ' + str(year) + '-' + str(term)
    # loads courses for year = [start_year, end_year)
    def _load_students(self, start_year, end_year):
        for year in range(start_year, end_year + 1):
            for term in range(2):
                path = '/'.join([self.root, str(year), str(term), params.fname_students])
                if not os.path.exists(path):
                    print 'unable to find ' + path
                else: 
                    infile = open(path, 'rU')
                    reader = csv.reader(infile)
                    header = reader.next()
                    for l in reader:
                        huid = int(l[0])
                        if not ptp.Student.by_id(huid):
                            ugrad = l[2] == 'UGrad'
                            concentrations = [l[3]]
                            if (l[4]):
                                concentrations = [l[3], l[4]]
                            else: 
                                concentrations = [l[3]]
                            secondary = l[5].rstrip(' [Approved]').rstrip(' [Filed]')
                            adv_standing = l[6] == ''
                            ptp.Student(huid, ugrad, concentrations, secondary, adv_standing)
                    infile.close()
                # add year_term if necessary later...

    def _load_enrollments(self, start_year, end_year):
        for year in range(start_year, end_year + 1):
            for term in range(2):
                path = '/'.join([self.root, str(year), str(term), params.fname_enrollment])
                if not os.path.exists(path):
                    print 'unable to find ' + path
                else: 
                    infile = open(path, 'rU')
                    reader = csv.reader(infile)
                    header = reader.next()
                    for l in reader:
                        ccn = int(l[2])
                        meeting = ptp.Meeting.by_year_term_id(year, term, ccn)
                        if not meeting: 
                            print 'Could not find Meeting for ' + ptp.Course.by_id(ccn).get_deptnum() + ', ' + str(year) + '-' + str(term)
                        else:
                            huid = int(l[3])
                            student = ptp.Student.by_id(int(l[3]))
                            if not student:
                                print 'Could not find Student ' + str(huid)
                            else:
                                meeting.students.append(student)
                                student.meetings.append(meeting)
                    infile.close()

    def load(self, start_year, end_year):
        print 'loading catalog'
        self._load_catalog(start_year, end_year)
        print 'loading meeting times'
        self._load_times(start_year, end_year)
        print 'loading students'
        self._load_students(start_year, end_year)
        print 'loading enrollments'
        self._load_enrollments(start_year, end_year)
        print 'loading ptp'
        self._load_ptp(start_year, end_year)

    def __init__(self, root):
        self.root = root
        self._full_year_meetings = collections.defaultdict(set)

 