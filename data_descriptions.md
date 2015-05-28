# PGPTP (Pretty Good Pre-Term Planning) Data files

## Course Times File

Course times are given in the format:
    Academic Year
    Term
    Course Catalog Number
    Instructor ID
    Meeting type (lecture, seminar, ...)
    Day-Time

## Course Enrollment

Course enrollment files have the format
    Term, in the format YYYYT, where T=1 -> Fall, T=2 -> Spring
    Course Catalog Number
    Student ID
    Faculty ID
    Gen-Ed
    CORE

## Course Catalog

The course catalog has entries for years from 2004 to 2014 in the format
    Academic Year
    Course Catalog Number
    Course
    Course Title
    Department
    Dept 1
    Dept 2
    Instructor ID (Term 1)
    Instructor Name (Term 1)
    Instructor ID (Term 2)
    Instructor Name (Term 2)
    Term Pattern
    Gen-Ed
    Core

Notes: The CCN may be changed or re-used over time, so that is why the academic year is needed. Note that with
    the new SIS system, the CCNs will all change. We will need a mapping from the new CCNs to the Old.

Some courses are offered by multiple departments; when that happens the Dept 1 and Dept 2 fields are filled in.

The instructor ID and term of that ID is interpreted as follows. If the course is offered only once, the instructor
    id will be the Instructor ID for Term 1. Which term will be indicated in Term Pattern. If the course is offered
    twice, the the Instructor ID for Term 1 will be the ID for the instructor in the Fall term, and the Instructor
    ID in Term 2 will be the ID for the instructor in the Spring term.
    
## Pre-term planning (when used)

The pre-term planning data has the form
    Course Catalog Number
    Course
    Term
    PTP Count
    
## Q Scores

The Q score files have the format
    ACADEMIC_YEAR	
    COURSE_ID	
    COURSE_NUMBER	
    TERM_NUM	
    CATALOG_NUMBER	
    DEPARTMENT	
    COURSE_GROUP	
    UGRADS	
    GRADS	
    X-REG	
    EMP	
    OTHER	
    VUS	
    TOTAL_ENROLLMENT	
    Number_of_Q_Responses	
    Crs_Overall	Crs_Workload	
    Crs_Difficulty	
    Instructors_Overall	
    Multiple_Instr	
    Instr 1	
    Instr 2	
    Instr 3	
    Instr 4	
    Instr 5	
    Instr 6	
    Instr 7	
    Instr 8	
    Instr 9	
    Instr 10	
    Instr 11	
    Instr 12	
    Instr 13	
    Instr 14
    ....
