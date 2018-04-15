from matchingsystem.models import Student, Project, Tag, Project_assignment, members, leaders
from itertools import chain
from django.contrib.messages import constants as messages

#matching results are on Project_assignment in the order of Project (leader|member|member|..)

def size_checker(module, team_size):
	selected_projects = Project.objects.filter(project_module = module)
	selected_student = Student.objects.filter(student_modules = module)

	number_of_students = selected_student.count()
	number_of_groups = number_of_students // team_size
	number_of_projects = selected_projects.count()

	if number_of_groups > number_of_projects:
		return 1

	elif number_of_projects > number_of_groups:
		return 2

	return 3


def module_matching(module, team_size):
	selected_projects = Project.objects.filter(project_module = module)
	selected_student = Student.objects.filter(student_modules= module)

	number_of_students = selected_student.count()
	number_of_groups = number_of_students // 3
	number_of_projects = selected_projects.count()
	unmatched_student = 0

		#add a view that suggests there are too many projects
	if number_of_students % number_of_groups != 0:
		unmatched_student = number_of_students % number_of_groups
		#need cases for splitting students
	if team_size == 1:
		matchpool(selected_student, selected_projects, 1, 0, module)
	else:
		leader_vacancy = number_of_projects
		female_leader_vacancy = leader_vacancy // 3

		students_by_grade = Student.objects.order_by('-exam_results')
		female_list = Student.objects.filter(gender = "F")
		female_leader_grade = female_list[female_leader_vacancy-1].exam_results
		female_leader_list = female_list.filter(exam_results__gte = female_leader_grade)
		leader_vacancy -= female_leader_vacancy
		student_list_updated = selected_student.exclude(student_code = female_leader_list).order_by('-exam_results')
		remaining_leader_grade = student_list_updated[leader_vacancy-1].exam_results
		remaining_leader_list = student_list_updated.filter(exam_results__gte = remaining_leader_grade)
		
		#need to combine female_leader_list and remaining_leaders
		final_leader_list = female_leader_list | remaining_leader_list

		member_list = list(set(students_by_grade).difference(set(final_leader_list)))
		member_student_code_list = []
		for x in range(len(member_list)):
			member_student_code_list.append(member_list[x].student_code)

		final_member_list = selected_student.filter(student_code__in = member_student_code_list)
		#here we have final_leader_list and final_member_list by grades
		matchpool(final_leader_list, selected_projects, 1, 1, module)
		matchpool(final_member_list, selected_projects, team_size-1, 0, module)

		if unmatched_student > 0:
			matched_student_code_list = []
			matched_student_in_module = Project_assignment.objects.filter(module = module)
			for item in matched_student_in_module.iterator():
				matched_student_code_list.append(item.student.student_code)
			unmatched_student = selected_student.exclude(student_code__in = matched_student_code_list )
			unmatched_student_code_list = []

			for x in range(len(unmatched_student)):
				unmatched_student_code_list.append(unmatched_student[x].student_code)
			unmatched_student_query = selected_student.filter(student_code__in = unmatched_student_code_list)
			remaining_students(unmatched_student_query, selected_projects, module)

def matchpool(student_list, project_list, match_size, group_leader, module):

	s = student_list
	p = project_list

	algorithm_order = tag_counters(student_list)
	#iterate through a list with the tag's description from the most unpopular tag to the most popular
	for tag in algorithm_order:
		sl = s
		pl = p
		project_with_tag =pl.filter(project_tags = tag)
		project_no = project_with_tag.count()

		selected_student = sl.exclude(tag_dislike_1 = tag)
		tag_1_list = selected_student.filter(tag_like_1 = tag)
		tag_2_list = selected_student.filter(tag_like_2 = tag)
		tag_3_list = selected_student.filter(tag_like_3 = tag)
		sorted_shortlist = tag_1_list | tag_2_list | tag_3_list

		match_no = match_size * project_no

		if sorted_shortlist.count() < match_no:
			matched_student = 0
			remaining_match = 0
			project_number = 0
			for p_counter in range(sorted_shortlist.count()//project_no):
				remaining_match = match_size
				for x in range(match_size):
					project = project_with_tag[p_counter]
					student = sorted_shortlist[(match_size)*p_counter+x]
					temp = Project_assignment(student = student, project = project, group_leader = group_leader)
					temp.save()
					temp.module.add(module)
					s_code = student.student_code
					s = s.exclude(student_code = s_code)
					matched_student += 1
					remaining_match -= 1
				if remaining_match == 0:
					project_number += 1
					p_id = project.id
					p = p.exclude(id = p_id)

			#assigned students who have the tag in the dislike field
			new_counter = 0
			unpooled = student_list.filter(tag_dislike_1 = tag)
			while matched_student < match_no:
				project = project_with_tag[project_number]
				student = unpooled[new_counter]
				temp = Project_assignment.objects.create(student = student, project = project, group_leader = group_leader)
				temp.save()
				temp.module.add(module)

				s_code = student.student_code
				p_id = project.id
				s = s.exclude(student_code = s_code)
				matched_student += 1
				remaining_match -= 1
				if remaining_match == 0:
					project_number += 1
					p_id = project.id
					p = p.exclude(id = p_id)

			#add function to force unfavorable match
		else:
			for p_counter in range(project_no):
				for x in range(match_size):
					project = project_with_tag[p_counter]
					student = sorted_shortlist[(match_size)*p_counter+x]
					temp = Project_assignment(student = student, project = project, group_leader = group_leader)
					temp.save()
					temp.module.add(module)

					s_code = student.student_code
					p_id = project.id

					s = s.exclude(student_code = s_code)
					p = p.exclude(id = p_id)

def remaining_students(student_list, project_list, module):
	s = student_list
	p = project_list
	student_no = s.count()
	tag_queryset = Tag.objects.all()
	tag_number = tag_queryset.count()
	tag_options = list(tag_queryset)
	for x in range(tag_number):
		tag_options.append(tag_queryset[x].tag_description)
	tag_dislike_counter = [None]*tag_number
	tag_order = []
	for x in range(tag_number):
		temp = student_list.filter(tag_like_1=tag_options[x])
		tag_dislike_counter[x] = temp.count()
	for y in range(tag_number):
		max_index = tag_dislike_counter.index(max(tag_dislike_counter))
		tag_order.append(tag_options[max_index])
		tag_dislike_counter[max_index] = -1
	
	for tag in tag_order:
		sl = s
		pl = p
		project_with_tag =pl.filter(project_tags = tag)
		project_no = project_with_tag.count()
		selected_student = sl.exclude(tag_dislike_1 = tag)
		tag_1_list = selected_student.filter(tag_like_1 = tag)
		tag_2_list = selected_student.filter(tag_like_2 = tag)
		tag_3_list = selected_student.filter(tag_like_3 = tag)
		sorted_shortlist = tag_1_list | tag_2_list | tag_3_list
		while project_no > 0 :
			for x in range(sorted_shortlist.count()):
				project = project_with_tag[project_no-1]
				student = sorted_shortlist[x]
				temp = Project_assignment(student = student, project = project, group_leader = 0)
				temp.save()
				temp.module.add(module)

				s_code = student.student_code
				p_id = project.id

				s = s.exclude(student_code = s_code)
				p = p.exclude(id = p_id)
				project_no -= 1
				student_no -= 1
				if student_no == 0:
					break
			if student_no == 0:
					break
		if student_no == 0:
					break

def tag_counters(student_list):
	#need an array with proper tags
	tag_queryset = Tag.objects.all()
	tag_number = tag_queryset.count()
	tag_options = list(tag_queryset)
	for x in range(tag_number):
		tag_options.append(tag_queryset[x].tag_description)
	tag_dislike_counter = [None]*tag_number
	tag_order = []
	for x in range(tag_number):
		temp = student_list.filter(tag_dislike_1=tag_options[x])
		tag_dislike_counter[x] = temp.count()
	for y in range(tag_number):
		max_index = tag_dislike_counter.index(max(tag_dislike_counter))
		tag_order.append(tag_options[max_index])
		tag_dislike_counter[max_index] = -1
	return tag_order

#The codes below would perform a match on project-by-project instead of module-based. It is not used, but is kept for possible use in the future
def start_matching_algorithm(generated_list, project_assigned, team_size):
	allocated_slot = 0 
	project_query = Project.objects.all()
	p = project_query [:1]
	project_tag = p[0].project_tags.all()[0]
	#leader_list = generated_list[0]
	#member_list = generated_list[1]
	leader_list = leaders
	member_list = members
	leader_query = select_student(leader_list, project_tag)
	if leader_query.count() > 0 :
		selected_leader = leader_query[0]
		Project_assignment.objects.create(student = selected_leader, project = p[0], group_leader = 1)
		selected_leader.assigned = 1
		selected_leader.save()
		allocated_slot += 1

	while allocated_slot < team_size:
		member_query = select_student(member_list, project_tag)
		if member_query.count() > 0 :
			selected_member = member_query[0]
			selected_member.assigned = 1
			selected_member.save()
			Project_assignment.objects.create(student = selected_member, project = project_assigned, group_leader = 0)
		allocated_slot += 1
#function that returns a student 

def select_student(student_list,tag):
	filtered_list1 = student_list.objects.exclude(assigned = 1)
	filtered_list2 = filtered_list1.exclude(tag_dislike_1 = tag)

	tag_1_list = filtered_list2.filter(tag_like_1 = tag)
	tag_2_list = filtered_list2.filter(tag_like_2 = tag)
	tag_3_list = filtered_list2.filter(tag_like_3 = tag)
	sorted_shortlist = tag_1_list | tag_2_list | tag_3_list
	selected_student = sorted_shortlist [:1]
	
	return selected_student

#returns [leader_list, member_list] ideally for an input module_student_list

def lists_generator(student_list): 
	t = student_list.objects.order_by('-exam_results','surname')
	list_length = student_list.objects.count()
	leader_vacancy = Project.objects.count()
	female_leader_vacancy = leader_vacancy // 3
	female_list = Student.objects.filter(gender = "F").order_by('-exam_results')
	if female_leader_vacancy != 0:
		female_leader_list = female_list [:female_leader_vacancy]
	else:
		female_leader_list = t.none()

	leader_vacancy -= female_leader_vacancy
	student_list_updated = t.exclude(student_code = female_leader_list)
	remaining_leaders = student_list_updated [:leader_vacancy]
	
	#need to combine female_leader_list and remaining_leaders
	final_leader_list = female_leader_list | remaining_leaders
	
	member_list = list(set(t).difference(set(final_leader_list)))
	member_student_code_list = []
	for x in range(len(member_list)):
		member_student_code_list.append(member_list[x].student_code)

	final_member_list = t.filter(student_code__in = member_student_code_list)


	for x in range(len(member_student_code_list)):
		y = t.filter(student_code = member_student_code_list[x])
		k = members.objects.filter(student_code = member_student_code_list[x])
		if y.count() == 1 and k == 0:
			a = y[0]
			a_dict = a.__dict__
			a_dict.pop('_state')
			members.objects.create(**a_dict)

	leader_student_code_list = []
	for x in range(final_leader_list.count()):
		leader_student_code_list.append(final_leader_list[x].student_code)

	for x in range(len(leader_student_code_list)):
		y = t.filter(student_code = leader_student_code_list[x])
		k = leaders.objects.filter(student_code = leader_student_code_list[x])
		if y.count() == 1 and k ==0:
			a = y[0]
			a_dict = a.__dict__
			a_dict.pop('_state')
			leaders.objects.create(**a_dict)

	two_lists = [None] * 2
	two_lists[0] = final_leader_list
	two_lists[1] = final_member_list
	return two_lists
    # going to need: students, projects, tags
   
# Whole structure of algorithm defined in here
# will need to validate there is enough students, projects, team leaders etc
# will need to validate that all data required has been inputted to database for the chosen module
# will need to validate that students have filled in their part
# will just redirect to a page telling the error that has occured

# this changes depending on if the teams are of size 1, if they are size 1
# then don't need to allocate leaders just do normal matching algorithm


