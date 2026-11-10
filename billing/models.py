from django.db import models
from patients.models import Patient
from appointments.models import Appointment
from datetime import date
from decimal import Decimal
import uuid

class Invoice(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('PENDING', 'Pending Payment'),
        ('PARTIALLY_PAID', 'Partially Paid'),
        ('PAID', 'Paid in Full'),
        ('CANCELLED', 'Cancelled / Void'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('CASH', 'Cash'),
        ('CREDIT_CARD', 'Credit / Debit Card'),
        ('INSURANCE', 'Health Insurance'),
        ('BANK_TRANSFER', 'Bank Wire / Transfer'),
        ('UPI', 'UPI / Digital Wallet'),
    )

    invoice_id = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='invoices')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    issue_date = models.DateField(default=date.today)
    due_date = models.DateField(null=True, blank=True)
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='CASH')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-issue_date', '-created_at']

    def __str__(self):
        return f"Invoice {self.invoice_id} - {self.patient.full_name} (${self.total_amount})"

    @property
    def balance_due(self):
        return max(Decimal('0.00'), self.total_amount - self.paid_amount)

    def calculate_totals(self):
        calc_subtotal = sum(item.total for item in self.items.all())
        self.subtotal = calc_subtotal
        self.total_amount = max(Decimal('0.00'), (calc_subtotal - self.discount) + self.tax)
        
        if self.paid_amount >= self.total_amount and self.total_amount > 0:
            self.payment_status = 'PAID'
        elif self.paid_amount > 0:
            self.payment_status = 'PARTIALLY_PAID'
        elif self.payment_status != 'CANCELLED':
            self.payment_status = 'PENDING'

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            random_part = uuid.uuid4().hex[:4].upper()
            self.invoice_id = f"INV-{date.today().strftime('%y%m')}-{random_part}"
        super().save(*args, **kwargs)

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=200, help_text="e.g. Consultation, Blood Test, Medication")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.total = Decimal(str(self.unit_price)) * Decimal(str(self.quantity))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} ({self.quantity} x {self.unit_price} = {self.total})"

