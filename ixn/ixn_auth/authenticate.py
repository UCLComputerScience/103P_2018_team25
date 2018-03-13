from requests import get
from matchingsystem.models import Student

class AuthenticateBackend:
    def authenticate(self, request, code=None):
        state = request.GET.get('state')
        if(code):
            student_code = self.get_student_code(request, code, state)
            try:
                student = Student.objects.get(pk=student_code) # Get student
                print(student.__str__())
                return student
            except KeyError:
                return None
            except Student.DoesNotExist:
                return None

        return None

    def get_student_code(self, request, code, state):
        token_params = {
            'client_id': '3191669878317281.9925116223526035', 
            'code': code,
            'client_secret': '3089442b13bfd0f2ebe924c77d348da644d62a8a56c11aedf3560fee46fda04b'
        }
        token_url = 'https://uclapi.com/oauth/token'
        r_token = get(token_url, params=token_params).json()
        if(state != request.session.get('state')):
            raise Exception('Invalid OAuth state')

        user_params = {
            'token': r_token['token'],
            'client_secret': '3089442b13bfd0f2ebe924c77d348da644d62a8a56c11aedf3560fee46fda04b'

        }
        user_data_url = 'https://uclapi.com/oauth/user/studentnumber'
        r_user_data = get(user_data_url, params = user_params)

        if(state != request.session.get('state')):
            raise Exception('Invalid OAuth state')

        r_user_data = r_user_data.json()
        student_code = r_user_data['student_number']

        return student_code[1:] # Student code should be 8 digits

    def get_user(self, student_code):
        try:
            return Student.objects.get(pk=student_code)
        except Student.DoesNotExist:
            return None
