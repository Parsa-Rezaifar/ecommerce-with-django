from kavenegar import *
from django.contrib.auth.mixins import UserPassesTestMixin


def send_opt_code(phone_number,code):
    try:
        api=KavenegarAPI('59356F6F492F6D58674D574E685261485773473169375942777978464665734844616A66743357413678413D')
        params={
            'sender': '1000689696',
            'receptor':phone_number,
            'message':f'Your verification code is {code}',
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)

class Is_User_AdminMixin(UserPassesTestMixin) :

    def test_func(self) :
        return self.request.user.is_authenticated and self.request.user.is_admin