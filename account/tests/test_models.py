import datetime
import tempfile
from unittest import mock

from django.core.files import File
from django.test import TestCase, override_settings

from account.models import Account, VerificationCode


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class AccountTest(TestCase):
    """ Test module for Account model """

    def setUp(self):
        Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+15205129001',
            password='123456'
        )

        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'test.jpg'

        Account.objects.create(
            first_name='James',
            last_name='Earl Johnson',
            email='jamesjohnson@gmail.com',
            phone_number='+15204862345',
            password='11110000',
            gender='Male',
            birthday='1990-12-12',
            image=file_mock,
            bio='Short bio for testing',
            is_admin=True,
            is_superuser=True
        )

    def test_account_str(self):
        account = Account.objects.get(email='danibazi9@gmail.com')
        self.assertEqual(account.__str__(), 'Danial Bazmandeh')

    def test_account_phone_number(self):
        account = Account.objects.get(email='danibazi9@gmail.com')
        self.assertEqual(account.phone_number, '+15205129001')

    def test_account_role(self):
        account = Account.objects.get(email='danibazi9@gmail.com')
        self.assertEqual(account.role, 'normal-user')

    def test_account_is_admin(self):
        account = Account.objects.get(email='jamesjohnson@gmail.com')
        self.assertEqual(account.is_admin, True)

    def test_account_is_superuser(self):
        account = Account.objects.get(email='jamesjohnson@gmail.com')
        self.assertEqual(account.is_superuser, True)

    def test_account_not_is_admin(self):
        account = Account.objects.get(email='danibazi9@gmail.com')
        self.assertEqual(account.is_admin, False)

    def test_account_not_is_superuser(self):
        account = Account.objects.get(email='danibazi9@gmail.com')
        self.assertEqual(account.is_superuser, False)

    def test_account_gender(self):
        account = Account.objects.get(email='jamesjohnson@gmail.com')
        self.assertEqual(account.gender, 'Male')

    def test_account_birthday(self):
        account = Account.objects.get(email='jamesjohnson@gmail.com')
        self.assertEqual(account.birthday, datetime.date(1990, 12, 12))

    def test_account_image(self):
        account = Account.objects.get(email='jamesjohnson@gmail.com')
        actual_file_name = account.image.name.split('/')[-1]

        self.assertTrue(actual_file_name.startswith('test'))
        self.assertTrue(actual_file_name.endswith('.jpg'))

    def test_account_bio(self):
        account = Account.objects.get(email='jamesjohnson@gmail.com')
        self.assertEqual(account.bio, 'Short bio for testing')


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class VerificationCodeTest(TestCase):
    """ Test module for Verification Code model """

    def setUp(self):
        VerificationCode.objects.create(
            email='danibazi9@gmail.com',
            vc_code='123456',
        )

    def test_verification_code_str(self):
        vc = VerificationCode.objects.get(email='danibazi9@gmail.com')
        self.assertEqual(vc.__str__(), 'danibazi9@gmail.com, Code: 123456')

    def test_verification_code_vc_code(self):
        vc = VerificationCode.objects.get(email='danibazi9@gmail.com')
        self.assertEqual(vc.vc_code, '123456')
