from django.core.management.base import BaseCommand
from accounts.models import OtpCode
from datetime import datetime,timedelta
import pytz

class Command(BaseCommand) :

    help = 'removes all expired otp codes'

    def handle(self, *args, **options) :
        expire_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)
        OtpCode.objects.filter(create__lt=expire_time).delete()
        self.stdout.write('All expired otp codes deleted successfully')