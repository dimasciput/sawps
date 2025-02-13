from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import status

from django.test import TestCase
from django.http import JsonResponse
from frontend.views.totp_device import (
    generate_qr_code,
    generate_qrcode,
    return_json
)
from django_otp.plugins.otp_totp.models import TOTPDevice


class UtilityFunctionsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.device = TOTPDevice.objects.create(
            user=self.user, name='Test Device')

    def test_return_json(self):
        data = {'id': 1, 'name': 'Test Device',
                'user': 'testuser', 'qrcode': 'base64encodedimage'}
        response = return_json(data)
        self.assertIsInstance(response, JsonResponse)

    def test_generate_qr_code(self):
        otpauth_url = "otpauth://totp/username?secret=FL3DAN6DO4GVMHVCANNJBGJ2CICM3ETP&algorithm=SHA1&digits=6&period=30"
        qr_code_base64 = generate_qr_code(otpauth_url)
        self.assertIsInstance(qr_code_base64, str)

    def test_generate_qrcode(self):
        device_data = generate_qrcode(self.device)
        self.assertIsInstance(device_data, list)
        self.assertEqual(len(device_data), 1)


class TOTPDeviceViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.device = TOTPDevice.objects.create(
            user=self.user,
            name='Test Device'
        )

    def test_view_totp_devices(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Send a GET request to the view
        response = self.client.post(reverse('view_totp_devices'))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_totp_device(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Send a POST request to the view with device_name in the data
        data = {'device_name': 'New Device'}
        response = self.client.post(reverse('add_totp_devices'), data=data)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that a new device is created
        self.assertEqual(TOTPDevice.objects.count(), 2)

    def test_delete_totp_device(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Send a POST request to the view to delete the device
        response = self.client.post(
            reverse('delete_totp_device', args=[self.device.id]))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the device is deleted
        self.assertEqual(TOTPDevice.objects.count(), 0)
