#!/usr/bin/env python
'''
Created on Oct 13, 2014

@author: waldo, mdeng
'''

import sys, os, csv, time
import params

def make_outfile(root, fname, outdict, year, sem, header):
    '''
        Creates the directory root/year/sem if it doesn't exist, and [over]writes a 
        new file named fname in it.
    '''
    if not os.path.exists(root + '/out/' + year + '/' + sem + '/'):
        os.makedirs(root + '/out/' + year + '/' + sem + '/')

    outfile = csv.writer(open(root + '/out/' + year + '/' + sem + '/' + fname, 'w'))
    outdict[year + sem] = outfile
    outfile.writerow(header)

def process_qdata(root, fname):
    '''
        Cleans the Q Guide data.
    '''         
    infile = csv.reader(open(root + '/' + fname, 'rU'))
    header = infile.next()
    header[0] = 'year'
    header[3] = 'semester'
    header = [h.strip().lower().replace(' ', '_') for h in header]
    outdict = {}
    for l in infile:
        year = l[0].split('-')[0] # ACADEMIC_YEAR: yyya-yyyb --> yyya
        sem = str(int(l[3])-1)
        if (year + sem) not in outdict:
            make_outfile(root, fname, outdict, year, sem, header)
        l[0] = year
        l[3] = sem
        l = [ll.strip() for ll in l]
        outdict[year + sem].writerow(l)

def process_enrollment(root, fname):
    '''
        Cleans the enrollment data.
    ''' 
    infile = csv.reader(open(root + '/' + fname, 'rU'))
    header = infile.next()
    header[0] = 'year'
    header[1] = 'semester'
    header = [h.strip().lower().replace(' ', '_') for h in header]
    outdict = {}
    for l in infile:
        raw_term = l[1].strip()
        # TERM is previously encoded as YYYYX, where X is 1 or 2 for spring or fall, respectively, 
        # and YYYY is the calendar year in the fall of that academic year
        year = raw_term[:-1]
        sem = str(int(raw_term[-1]) - 1)
        if (year + sem) not in outdict:
            make_outfile(root, fname, outdict, year, sem, header)
        l[0] = year
        l[1] = sem
        l = [ll.strip() for ll in l]
        outdict[year + sem].writerow(l)

# does it make sense to do this for students?
def process_students(root, fname):
    '''
        Cleans the student information data.
    ''' 
    infile = csv.reader(open(root + '/' + fname, 'rU'))
    header = infile.next()
    header[1] = 'year'
    header.append('semester')
    header[3] = 'primary_concentration'
    header = [h.strip().lower().replace(' ', '_') for h in header]
    outdict = {}
    for l in infile:
        raw_term = l[1].strip()
        # TERM is previously encoded as YYYYX, where X is 1 or 2 for spring or fall, respectively, 
        # and YYYY is the calendar year in the fall of that academic year
        year = raw_term[:-1]
        sem = str(int(raw_term[-1]) - 1)
        if (year + sem) not in outdict:
            make_outfile(root, fname, outdict, year, sem, header)
        l[1] = year
        l.append(sem)
        l = [ll.strip() for ll in l]
        outdict[year + sem].writerow(l)

def process_ptp(root, fname):
    '''
        Cleans the PTP numbers data.
    ''' 
    infile = csv.reader(open(root + '/' + fname, 'rU'))
    header = infile.next()
    header[2] = 'year'
    header.append('semester')
    header = [h.strip().lower().replace(' ', '_') for h in header]
    outdict = {}
    for l in infile:
        raw_term = l[2].strip()
        # TERM is previously encoded as YYYYX, where X is 1 or 2 for spring or fall, respectively, 
        # and YYYY is the calendar year in the fall of that academic year
        year = raw_term[:-1]
        sem = str(int(raw_term[-1]) - 1)
        if (year + sem) not in outdict:
            make_outfile(root, fname, outdict, year, sem, header)
        l[2] = year
        l.append(sem)
        l = [ll.strip() for ll in l]
        outdict[year + sem].writerow(l)

def parse_timestr(timestr):
    l = timestr.strip().split(' ')
    fmt = "%I:%M%p"
    times = []
    for i in range(0, len(l), 4):
        days = l[i].split(',')
        start = time.strftime('%H:%M', time.strptime(l[i+1], fmt))
        end = time.strftime('%H:%M', time.strptime(l[i+3], fmt))
        times.extend([(day, start, end) for day in days])
    return times

def process_course_times(root, fname):
    '''
        Cleans the course times data.
    ''' 
    infile = csv.reader(open(root + '/' + fname, 'rU'))
    header = infile.next()
    header[0] = 'year'
    header[1] = 'semester'
    header[5] = 'time'
    header = [h.strip().lower().replace(' ', '_') for h in header]
    outdict = {}
    for l in infile:
        year = l[0]
        if l[1].strip() == 'Spring':
            sem = '1'
        else:
            sem = '0'
        if (year + sem) not in outdict:
            make_outfile(root, fname, outdict, year, sem, header)
        l[0] = year
        l[1] = sem
        l = [ll.strip() for ll in l]
        l[5] = parse_timestr(l[5])
        outdict[year + sem].writerow(l)

def process_course_catalog(root, fname):
    '''
        1) Splits course catalog by year and term
        2) Creates master instructor ID and department ID spreadsheets.
    ''' 
    infile = csv.reader(open(root + '/' + fname, 'rU'))
    infile.next()

    cat_header = ['year', 'semester', 'ccn', 'number', 'title', 'department_ids', 'instructor_id', 'full_year', 'core', 'gen_ed']
    cat_outdict = {}

    if not os.path.exists(root + '/out/'):
        os.makedirs(root + '/out/')

    all_instructors = set()
    instructor_outfile = csv.writer(open(root + '/out/instructors.csv', 'w'))
    instructor_outfile.writerow(['id', 'first', 'last'])

    all_depts = set()
    depts_outfile = csv.writer(open(root + '/out/departments.csv', 'w'))
    depts_outfile.writerow(['id', 'name'])

    for l in infile:
        year = l[0]
        full_year = False

        # departments
        dept0 = l[5]
        dept1 = l[6]
        dept = dept0
        deptnames = l[4].split(' AND ')
        if (dept0 not in all_depts):
            all_depts.add(dept0)
            depts_outfile.writerow([dept0, deptnames[0]])
        if (dept1):
            dept = ','.join((dept0, dept1))
            if (dept1 not in all_depts):
                all_depts.add(dept1)
            depts_outfile.writerow([dept1, deptnames[1]])
        
        # list of instructors, corresponding to each sem in sems
        instructor0 = l[7]
        if (instructor0 and instructor0 not in all_instructors):
            all_instructors.add(instructor0)
            (last, first) = l[8].split(', ')
            instructor_outfile.writerow([instructor0, first, last])
        instructor1 = l[9]
        if (instructor1 and instructor1 not in all_instructors):
            all_instructors.add(instructor1)
            (last, first) = l[10].split(', ')
            instructor_outfile.writerow([instructor1, first, last])

        # options for term are 'full year', 'fall term', 'spring term', 
        # and 'fall term; repeated spring term'
        sems = list()
        if (l[11] == 'full year'):   # full year
            sems = ['0', '1']
            full_year = True
            instructors = {'0' : instructor0, '1': instructor1 }
        elif (len(l[11]) == 9):      # fall term
            sems = ['0']
            instructors = {'0' : instructor0}
        elif (len(l[11]) == 11):     # spring term
            sems = ['1']
            instructors = {'1' : instructor0}
        else:                        # repeated fall & spring
            sems = ['0', '1']
            instructors = {'0' : instructor0, '1': instructor1 }      

        for sem in sems: 
            if (year + sem) not in cat_outdict:
                make_outfile(root, fname, cat_outdict, year, sem, cat_header)
            cat_outdict[year + sem].writerow([year, sem, l[1], l[2], l[3], dept, instructors[sem], full_year, l[13], l[12]])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: preprocess root_name'
        sys.exit(1)

    root = sys.argv[1]
    process_course_catalog(root, params.fname_catalog)
    process_students(root, params.fname_students)
    process_enrollment(root, params.fname_enrollment)
   # process_qdata(root, params.fname_qdata)
    process_ptp(root, params.fname_ptp)
    process_course_times(root, params.fname_times)
    print 'done ^_^'
