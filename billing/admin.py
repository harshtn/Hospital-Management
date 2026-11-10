from django.contrib import admin
from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'patient', 'total_amount', 'paid_amount', 'payment_status', 'payment_method', 'issue_date')
    list_filter = ('payment_status', 'payment_method', 'issue_date')
    search_fields = ('invoice_id', 'patient__first_name', 'patient__last_name', 'patient__patient_id')
    readonly_fields = ('invoice_id', 'created_at', 'updated_at')
    inlines = [InvoiceItemInline]
