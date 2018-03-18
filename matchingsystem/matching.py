from .models import Student, Project, Tag

def start_matching_algorithm(module, team_size):
    print('Starting matching algorithm...')
    pass # Whole structure of algorithm defined in here
# will need to validate there is enough students, projects, team leaders etc
# will need to validate that all data required has been inputted to database for the chosen module
# will need to validate that students have filled in their part
# will just redirect to a page telling the error that has occured

def setup(): # Grabs required data from database
    pass
    # going to need: students, projects, tags

def allocate_students(): # Uses greedy algorithm to place students
    pass

def allocate_team_leader(): # Select the team leaders based on grades
    pass
# this changes depending on if the teams are of size 1, if they are size 1
# then don't need to allocate leaders just do normal matching algorithm
