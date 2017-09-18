# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import StringIO
import qrcode
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.http import HttpResponse

from account.models import Profile


class SendProduct(models.Model):
    PAYMENT_CHOICE = (
        ('A', 'Advanced'),
        ('C', 'COD'),
    )
    item_name = models.CharField(max_length=200)
    item_details = models.TextField()
    delivery_address = models.TextField()
    payment_type = models.CharField(max_length=1, choices=PAYMENT_CHOICE)
    payable_amount = models.IntegerField(default=0)
    delivery_charge = models.IntegerField(default=0)
    qr_code = models.ImageField(upload_to='qrcode', blank=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    @property
    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )
        qr.add_data(self.item_name)
        qr.make(fit=True)

        img = qr.make_image()
        buffer = StringIO.StringIO()
        img.save(buffer)
        filename = 'qrcode-%s.png' % (self.item_name)
        filebuffer = InMemoryUploadedFile(
            buffer, None, filename, 'image/png', buffer.len, None)
        self.qr_code.save(filename, filebuffer)
        return self.qr_code.url

    def __str__(self):
        return self.item_name



