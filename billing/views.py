from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from decimal import Decimal
from .models import Invoice
from .forms import InvoiceForm, InvoiceItemFormSet

def invoice_list(request):
    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '').strip()

    invoices = Invoice.objects.select_related('patient', 'appointment').all()

    if search_query:
        invoices = invoices.filter(
            Q(invoice_id__icontains=search_query) |
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query) |
            Q(patient__patient_id__icontains=search_query)
        )

    if status_filter:
        invoices = invoices.filter(payment_status=status_filter)

    paginator = Paginator(invoices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    statuses = Invoice.PAYMENT_STATUS_CHOICES

    return render(request, 'billing/invoice_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'statuses': statuses,
        'total_count': invoices.count()
    })

def invoice_detail(request, pk):
    invoice = get_object_or_404(
        Invoice.objects.select_related('patient', 'appointment').prefetch_related('items'),
        pk=pk
    )
    return render(request, 'billing/invoice_detail.html', {'invoice': invoice})

def invoice_print(request, pk):
    invoice = get_object_or_404(
        Invoice.objects.select_related('patient', 'appointment').prefetch_related('items'),
        pk=pk
    )
    return render(request, 'billing/invoice_print.html', {'invoice': invoice})

def invoice_create(request):
    initial = {}
    if 'patient_id' in request.GET:
        initial['patient'] = request.GET.get('patient_id')
    if 'appointment_id' in request.GET:
        initial['appointment'] = request.GET.get('appointment_id')

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.save()
            formset.instance = invoice
            formset.save()
            # Calculate totals
            invoice.calculate_totals()
            invoice.save()
            messages.success(request, f"Invoice {invoice.invoice_id} generated successfully.")
            return redirect('invoice_detail', pk=invoice.pk)
        else:
            messages.error(request, "Failed to create invoice. Please check line items and fields.")
    else:
        form = InvoiceForm(initial=initial)
        formset = InvoiceItemFormSet()

    return render(request, 'billing/invoice_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Create New Patient Invoice'
    })

def invoice_update(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceItemFormSet(request.POST, instance=invoice)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            invoice.calculate_totals()
            invoice.save()
            messages.success(request, f"Invoice {invoice.invoice_id} updated successfully.")
            return redirect('invoice_detail', pk=invoice.pk)
        else:
            messages.error(request, "Please check form entries.")
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSet(instance=invoice)

    return render(request, 'billing/invoice_form.html', {
        'form': form,
        'formset': formset,
        'title': f"Edit Invoice #{invoice.invoice_id}",
        'invoice': invoice
    })

def invoice_mark_paid(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.paid_amount = invoice.total_amount
    invoice.payment_status = 'PAID'
    invoice.save()
    messages.success(request, f"Invoice {invoice.invoice_id} marked as Paid in Full.")
    return redirect('invoice_detail', pk=pk)

