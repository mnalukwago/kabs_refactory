from datetime import date, datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.mail import send_mail
from django.db.models import Count, F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    BranchForm,
    # ContactForm,
    CreditSaleForm,
    ProcurementForm,
    # ProductForm,
    SaleForm,
    SupplierForm,
)
from .models import (
    Branch,
    CreditSale,
    Procurement,
    # Product,
    Receipt,
    Sale,
    Supplier,
)


def index_view(request):
    return render(request, "index.html")


def home(request):
    return render(request, "home.html")
# LOGIN 

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UserProfile

def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.groups.filter(name="director").exists():
                return redirect("director_dashboard")

            elif user.groups.filter(name="manager").exists():
                try:
                    profile = UserProfile.objects.get(user=user)
                    branch = profile.branch.lower()
                    if branch == "matugga":
                        return redirect("manager_dashboard_matugga")
                    elif branch == "maganjo":
                        return redirect("manager_dashboard_maganjo")
                except UserProfile.DoesNotExist:
                    messages.error(request, "Manager profile not found.")
                    return redirect("login")

            elif user.groups.filter(name="sales_agent").exists():
                try:
                    profile = UserProfile.objects.get(user=user)
                    branch = profile.branch.lower()
                    if branch == "matugga":
                        return redirect("sales_agent_dashboard_matugga")
                    elif branch == "maganjo":
                        return redirect("sales_agent_dashboard_maganjo")
                except UserProfile.DoesNotExist:
                    messages.error(request, "Sales Agent profile not found.")
                    return redirect("login")

            else:
                messages.error(request, "Unauthorized role.")
                return redirect("login")
        else:
            messages.error(request, "Invalid username or password.")

    # Render login form on GET or failed POST
    form = AuthenticationForm()
    return render(request, "login.html", {"form": form, "title": "Login"})

#PROCUREMENT
# View for adding a new procurement
from django.shortcuts import render, redirect
from .forms import ProcurementForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def create_procurement(request):
    if request.method == "POST":
        form = ProcurementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('procurement_list')  # Adjust as needed
    else:
        form = ProcurementForm()

    return render(request, 'procurement_form.html', {'form': form})

from django.shortcuts import render
from .models import Procurement
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def procurement_list(request):
    procurements = Procurement.objects.order_by('-created_at')
    return render(request, 'procurement_list.html', {'procurements': procurements})


#SALES
from django.shortcuts import render, redirect
from .models import Sale
from .forms import SaleForm
from django.contrib.auth.decorators import login_required

@login_required
def sales_list(request):
    sales = Sale.objects.order_by('-date', '-time')
    return render(request, 'sales_list.html', {'sales': sales})

@login_required
def create_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales_list')
    else:
        form = SaleForm()
    return render(request, 'sale_form.html', {'form': form})


# CREDIT SALES
from django.shortcuts import render, redirect
from .forms import CreditSaleForm
from .models import CreditSale
from django.contrib.auth.decorators import login_required

# View to create a new credit sale
@login_required(login_url='login')
def create_credit_sale(request):
    if request.method == 'POST':
        form = CreditSaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('credit_sales_list')  # Update this with your actual URL name
    else:
        form = CreditSaleForm()
    
    return render(request, 'credit_sale_form.html', {'form': form})

# View to list all credit sales
@login_required(login_url='login')
def credit_sales_list(request):
    credit_sales = CreditSale.objects.all().order_by('-dispatch_date')
    return render(request, 'credit_sales_list.html', {'credit_sales': credit_sales})


# RECEIPT
from django.shortcuts import render, redirect, get_object_or_404
from .models import Receipt
from .forms import ReceiptForm

def receipt_list(request):
    receipts = Receipt.objects.all()
    return render(request, 'receipt_list.html', {'receipts': receipts})

def create_receipt(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('receipt_list')
    else:
        form = ReceiptForm()
    return render(request, 'create_receipt.html', {'form': form})

def receipt_detail(request, pk):
    receipt = get_object_or_404(Receipt, pk=pk)
    return render(request, 'receipt_detail.html', {'receipt': receipt})


# SUPPLIER
from django.shortcuts import render, get_object_or_404, redirect
from .models import Supplier
from .forms import SupplierForm

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})

def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'add_supplier.html', {'form': form})

def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'edit_supplier.html', {'form': form, 'supplier': supplier})

def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'delete_supplier.html', {'supplier': supplier})

#PRODUCE
from django.shortcuts import render, get_object_or_404, redirect
from .models import Produce
from .forms import ProduceForm

def produce_list(request):
    produces = Produce.objects.all()
    return render(request, 'produce_list.html', {'produces': produces})

def add_produce(request):
    if request.method == 'POST':
        form = ProduceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produce_list')
    else:
        form = ProduceForm()
    return render(request, 'add_produce.html', {'form': form})

def edit_produce(request, pk):
    produce = get_object_or_404(Produce, pk=pk)
    if request.method == 'POST':
        form = ProduceForm(request.POST, instance=produce)
        if form.is_valid():
            form.save()
            return redirect('produce_list')
    else:
        form = ProduceForm(instance=produce)
    return render(request, 'edit_produce.html', {'form': form})

def delete_produce(request, pk):
    produce = get_object_or_404(Produce, pk=pk)
    if request.method == 'POST':
        produce.delete()
        return redirect('produce_list')
    return render(request, 'delete_produce.html', {'produce': produce})

#BRANCH
from django.shortcuts import render, get_object_or_404, redirect
from .models import Branch
from .forms import BranchForm

def branch_list(request):
    branches = Branch.objects.all()
    return render(request, 'branch_list.html', {'branches': branches})

def add_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('branch_list')
    else:
        form = BranchForm()
    return render(request, 'add_branch.html', {'form': form})

def edit_branch(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            return redirect('branch_list')
    else:
        form = BranchForm(instance=branch)
    return render(request, 'edit_branch.html', {'form': form})

def delete_branch(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    if request.method == 'POST':
        branch.delete()
        return redirect('branch_list')
    return render(request, 'delete_branch.html', {'branch': branch})


# DIRECTOR
from .models import Sale, Procurement, CreditSale  # Ensure all these models exist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required(login_url='login')
def director_dashboard(request):
    if request.user.groups.filter(name="director").exists():
        total_sales = Sale.objects.all().count()
        total_credit_sales = Sale.objects.filter(payment_type='credit').count() 
        total_procurements = Procurement.objects.all().count()
        # total_stock = Stock.objects.all().count()

        context = {
            "total_sales": total_sales,
            "total_credit_sales": total_credit_sales,
            "total_procurements": total_procurements,
            # "total_stock": total_stock
        }
        return render(request, "director_dashboard.html", context)
    else:
        return redirect("login")


# MANAGER_MATUGGA
from django.shortcuts import render
from .models import Sale, Produce  # Assuming models are imported

def manager_dashboard_matugga(request):
    total_sales = Sale.objects.filter(branch_name="Matugga").aggregate(Sum('amount_paid'))['amount_paid__sum']
    total_credit_sales = Sale.objects.filter(branch_name="Matugga", payment_type="credit").aggregate(Sum('amount_paid'))['amount_paid__sum']
    total_procurements = Produce.objects.aggregate(Sum('quantity_in_kg'))['quantity_in_kg__sum']
    total_stock = Produce.objects.filter(produce_type="Stock").aggregate(Sum('quantity_in_kg'))['quantity_in_kg__sum']
    sales_overview = Sale.objects.filter(branch_name="Matugga")
    stock_overview = Produce.objects.all()

    context = {
        'total_sales': total_sales,
        'total_credit_sales': total_credit_sales,
        'total_procurements': total_procurements,
        'total_stock': total_stock,
        'sales_overview': sales_overview,
        'stock_overview': stock_overview,
    }

    return render(request, 'manager_dashboard_matugga.html', context)

#MANAGER MAGANJO
from django.shortcuts import render
from django.db.models import Sum
from .models import Sale, Produce

def manager_dashboard_maganjo(request):
    total_sales = Sale.objects.filter(branch_name="Maganjo").aggregate(Sum('amount_paid'))['amount_paid__sum']
    total_credit_sales = Sale.objects.filter(branch_name="Maganjo", payment_type="credit").aggregate(Sum('amount_paid'))['amount_paid__sum']
    total_procurements = Produce.objects.aggregate(Sum('quantity_in_kg'))['quantity_in_kg__sum']
    total_stock = Produce.objects.filter(produce_type="Stock").aggregate(Sum('quantity_in_kg'))['quantity_in_kg__sum']
    
    sales_overview = Sale.objects.filter(branch_name="Maganjo")
    stock_overview = Produce.objects.all()

    context = {
        'total_sales': total_sales,
        'total_credit_sales': total_credit_sales,
        'total_procurements': total_procurements,
        'total_stock': total_stock,
        'sales_overview': sales_overview,
        'stock_overview': stock_overview,
    }

    return render(request, 'manager_dashboard_maganjo.html', context)

# SALESAGENT MATUGGA
from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Sale, CreditSale

@login_required
def sales_agent_dashboard_matugga(request):
    branch = "Matugga"
    agent = request.user  # Assumes user is a sales agent

    # Total confirmed sales
    total_sales = Sale.objects.filter(branch_name=branch, sales_agent=agent).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    total_tonnage = Sale.objects.filter(branch_name=branch, sales_agent=agent).aggregate(Sum('tonnage_kg'))['tonnage_kg__sum'] or 0

    # Recent confirmed sales
    recent_sales = Sale.objects.filter(branch_name=branch, sales_agent=agent).order_by('-date')[:10]

    # Pending credit sales (amount_due > 0)
    pending_credit_sales = CreditSale.objects.filter(
        branch_name=branch,
        sales_agent=agent,
        amount_due__gt=0
    ).order_by('-dispatch_date')[:10]

    pending_credit_total = pending_credit_sales.aggregate(Sum('amount_due'))['amount_due__sum'] or 0

    context = {
        'branch': branch,
        'total_sales': total_sales,
        'total_tonnage': total_tonnage,
        'recent_sales': recent_sales,
        'pending_credit_sales': pending_credit_sales,
        'pending_credit_total': pending_credit_total,
    }

    return render(request, 'sales_agent_dashboard_matugga.html', context)

# SALESAGENT MAGANJO
from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Sale, CreditSale

@login_required
def sales_agent_dashboard_maganjo(request):
    branch = "Maganjo"
    agent = request.user  # Assumes user is a sales agent

    # Total confirmed sales
    total_sales = Sale.objects.filter(branch_name=branch, sales_agent=agent).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    total_tonnage = Sale.objects.filter(branch_name=branch, sales_agent=agent).aggregate(Sum('tonnage_kg'))['tonnage_kg__sum'] or 0

    # Recent confirmed sales
    recent_sales = Sale.objects.filter(branch_name=branch, sales_agent=agent).order_by('-date')[:10]

    # Pending credit sales (amount_due > 0)
    pending_credit_sales = CreditSale.objects.filter(
        branch_name=branch,
        sales_agent=agent,
        amount_due__gt=0
    ).order_by('-dispatch_date')[:10]

    pending_credit_total = pending_credit_sales.aggregate(Sum('amount_due'))['amount_due__sum'] or 0

    context = {
        'branch': branch,
        'total_sales': total_sales,
        'total_tonnage': total_tonnage,
        'recent_sales': recent_sales,
        'pending_credit_sales': pending_credit_sales,
        'pending_credit_total': pending_credit_total,
    }

    return render(request, 'sales_agent_dashboard_maganjo.html', context)



def daily_sales_report(request):
    # Get today's date
    today = timezone.now().date()

    # Filter sales by today's date and group by branch
    branches = Sale.objects.filter(date=today).values("branch_name").distinct()

    # Prepare a dictionary to store sales per branch
    branch_sales = {}
    for branch in branches:
        sales = Sale.objects.filter(date=today, branch_name=branch["branch_name"])
        branch_sales[branch["branch_name"]] = sales

    return render(
        request,
        "daily_sales_report.html",
        {"branch_sales": branch_sales, "today": today},
    )


def stock_page(request):
    search_query = request.GET.get("search", "")
    if search_query:
        stock_items = Procurement.objects.filter(produce_name__icontains=search_query)
    else:
        stock_items = Procurement.objects.all()
    return render(
        request,
        "stock_page.html",
        {"stock_items": stock_items, "search_query": search_query},
    )


from django.shortcuts import render, redirect

# from .forms import CustomSignupForm


def signup(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # redirect to your login page
    else:
        form = CustomSignupForm()
    return render(request, "signup.html", {"form": form})


# def credit_list(request):
#     credits = CreditSale.objects.all()
#     return render(request, "credit_list.html", {"credits": credits})


def is_director(user):
    return user.is_superuser  # Only superusers can access the director dashboard




def maganjo_sales_report(request):
    today = timezone.now().date()
    maganjo_sales = Sale.objects.filter(branch_name="Maganjo", date=today)
    return render(
        request, "maganjo_sales_report.html", {"sales": maganjo_sales, "today": today}
    )
from django.db.models import Sum
from django.shortcuts import render
from .models import Sale, Procurement

def branch_comparison_dashboard(request):
    branches = ["Matugga", "Maganjo"]
    branch_data = {}

    for branch in branches:
        # Fetch all data per branch
        branch_sales = Sale.objects.filter(branch_name=branch)
        branch_procurement = Procurement.objects.filter(branch_name=branch)
        branch_credit = CreditList.objects.filter(branch_name=branch)

        # Calculate totals for each branch
        total_sales_kg = branch_sales.aggregate(total=Sum("tonnage_kg"))["total"] or 0
        total_sales_amount = branch_sales.aggregate(total=Sum("amount_paid"))["total"] or 0
        total_procurement_kg = branch_procurement.aggregate(total=Sum("tonnage_kg"))["total"] or 0
        total_credit_kg = branch_credit.aggregate(total=Sum("tonnage_kg"))["total"] or 0
        total_credit_due = branch_credit.aggregate(total=Sum("amount_due"))["total"] or 0

        # Store data
        branch_data[branch] = {
            "sales": branch_sales,
            "procurements": branch_procurement,
            "credits": branch_credit,
            "total_sales_kg": total_sales_kg,
            "total_sales_amount": total_sales_amount,
            "total_procurement_kg": total_procurement_kg,
            "total_credit_kg": total_credit_kg,
            "total_credit_due": total_credit_due,
        }

    return render(request, "branch_comparison_dashboard.html", {"branch_data": branch_data})
def credit_recovery_report(request):
    credit_records = CreditList.objects.all().order_by("-due_date")
    return render(
        request, "credit_recovery_report.html", {"credit_records": credit_records}
    )



@login_required
def sales_agent_dashboard_matugga(request):
    today = timezone.now().date()
    this_month = today.month

    # Today's Cash Sales
    todays_sales = Sale.objects.filter(branch_name="Matugga", date=today)
    todays_sales_kg = todays_sales.aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    todays_sales_amount = todays_sales.aggregate(amount=Sum("amount_paid"))["amount"] or 0

    # Today's Credit Sales
    todays_credit = CreditSale.objects.filter(branch_name="Matugga", dispatch_date=today)
    todays_credit_kg = todays_credit.aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    todays_credit_amount = todays_credit.aggregate(amount=Sum("amount_due"))["amount"] or 0

    # Monthly Cash Sales
    monthly_sales = Sale.objects.filter(branch_name="Matugga", date__month=this_month)
    monthly_sales_kg = monthly_sales.aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    monthly_sales_amount = monthly_sales.aggregate(amount=Sum("amount_paid"))["amount"] or 0

    # Monthly Credit Sales
    monthly_credit = CreditSale.objects.filter(branch_name="Matugga", dispatch_date__month=this_month)
    monthly_credit_kg = monthly_credit.aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    monthly_credit_amount = monthly_credit.aggregate(amount=Sum("amount_due"))["amount"] or 0

    context = {
        "todays_sales_kg": todays_sales_kg,
        "todays_sales_amount": todays_sales_amount,
        "todays_credit_kg": todays_credit_kg,
        "todays_credit_amount": todays_credit_amount,
        "monthly_sales_kg": monthly_sales_kg,
        "monthly_sales_amount": monthly_sales_amount,
        "monthly_credit_kg": monthly_credit_kg,
        "monthly_credit_amount": monthly_credit_amount,
    }

    return render(request, "sales_agent_dashboard_matugga.html", context)

from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Sale, CreditSale

@login_required
def sales_agent_dashboard_maganjo(request):
    today = timezone.now().date()
    this_month = today.month

    # Today's Cash Sales for Maganjo
    todays_sales = Sale.objects.filter(branch_name="Maganjo", date=today)
    todays_sales_kg = todays_sales.aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    todays_sales_amount = todays_sales.aggregate(amount=Sum("amount_paid"))["amount"] or 0

    # Today's Credit Sales for Maganjo
    todays_credit = CreditSale.objects.filter(branch_name="Maganjo", dispatch_date=today)
    todays_credit_kg = todays_credit.aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    todays_credit_amount = todays_credit.aggregate(amount=Sum("amount_due"))["amount"] or 0

    # Monthly Cash Sales for Maganjo
    monthly_sales = Sale.objects.filter(branch_name="Maganjo", date__month=this_month)
    monthly_sales_kg = monthly_sales.aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    monthly_sales_amount = monthly_sales.aggregate(amount=Sum("amount_paid"))["amount"] or 0

    # Monthly Credit Sales for Maganjo
    monthly_credit = CreditSale.objects.filter(branch_name="Maganjo", dispatch_date__month=this_month)
    monthly_credit_kg = monthly_credit.aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    monthly_credit_amount = monthly_credit.aggregate(amount=Sum("amount_due"))["amount"] or 0

    context = {
        "todays_sales_kg": todays_sales_kg,
        "todays_sales_amount": todays_sales_amount,
        "todays_credit_kg": todays_credit_kg,
        "todays_credit_amount": todays_credit_amount,
        "monthly_sales_kg": monthly_sales_kg,
        "monthly_sales_amount": monthly_sales_amount,
        "monthly_credit_kg": monthly_credit_kg,
        "monthly_credit_amount": monthly_credit_amount,
    }

    return render(request, "sales_agent_dashboard_maganjo.html", context)

def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, "sale_detail.html", {"sale": sale})


# RECEIPT
from django.shortcuts import render, redirect, get_object_or_404
from .models import Receipt
from .forms import ReceiptForm

def receipt_list(request):
    receipts = Receipt.objects.all()
    return render(request, 'receipt_list.html', {'receipts': receipts})

def create_receipt(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('receipt_list')
    else:
        form = ReceiptForm()
    return render(request, 'create_receipt.html', {'form': form})

def receipt_detail(request, pk):
    receipt = get_object_or_404(Receipt, pk=pk)
    return render(request, 'receipt_detail.html', {'receipt': receipt})


# # MANAGER_MATUGGA
# from django.shortcuts import render
# from .models import Sale, Produce  # Assuming models are imported

# def manager_dashboard_matugga(request):
#     total_sales = Sale.objects.filter(branch_name="Matugga").aggregate(Sum('amount_paid'))['amount_paid__sum']
#     total_credit_sales = Sale.objects.filter(branch_name="Matugga", payment_type="credit").aggregate(Sum('amount_paid'))['amount_paid__sum']
#     total_procurements = Produce.objects.aggregate(Sum('quantity_in_kg'))['quantity_in_kg__sum']
#     total_stock = Produce.objects.filter(produce_type="Stock").aggregate(Sum('quantity_in_kg'))['quantity_in_kg__sum']
#     sales_overview = Sale.objects.filter(branch_name="Matugga")
#     stock_overview = Produce.objects.all()

#     context = {
#         'total_sales': total_sales,
#         'total_credit_sales': total_credit_sales,
#         'total_procurements': total_procurements,
#         'total_stock': total_stock,
#         'sales_overview': sales_overview,
#         'stock_overview': stock_overview,
#     }

#     return render(request, 'manager_dashboard_matugga.html', context)

# #MANAGER MAGANJO
# from django.shortcuts import render
# from django.db.models import Sum
# from .models import Sale, Produce

# def manager_dashboard_maganjo(request):
#     total_sales = Sale.objects.filter(branch_name="Maganjo").aggregate(Sum('amount_paid'))['amount_paid__sum']
#     total_credit_sales = Sale.objects.filter(branch_name="Maganjo", payment_type="credit").aggregate(Sum('amount_paid'))['amount_paid__sum']
#     total_procurements = Produce.objects.aggregate(Sum('quantity_in_kg'))['quantity_in_kg__sum']   
#     total_stock = Produce.objects.filter(produce_type="Stock").aggregate(Sum('quantity_in_kg'))['quantity_in_kg__sum']
#     sales_overview = Sale.objects.filter(branch_name="Maganjo")
    
#     stock_overview = Produce.objects.all()

#     context = {
#         'total_sales': total_sales,
#         'total_credit_sales': total_credit_sales,
#         'total_procurements': total_procurements,
#         'total_stock': total_stock,
#         'sales_overview': sales_overview,
#         'stock_overview': stock_overview,
#     }

#     return render(request, 'manager_dashboard_maganjo.html', context)
    

def sales_by_branch(request, branch_name):
    sales = Sale.objects.filter(branch_name=branch_name)
    return render(
        request, "sales_by_branch.html", {"sales": sales, "branch_name": branch_name}
    )

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

# def Login(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)

#             # Role-based redirection
#             if user.groups.filter(name="director").exists():
#                 return redirect("director_dashboard")

#             elif user.groups.filter(name="manager").exists():
#                 if hasattr(user, "branch"):
#                     if user.branch.lower() == "matugga":
#                         return redirect("manager_dashboard_matugga")
#                     elif user.branch.lower() == "maganjo":
#                         return redirect("manager_dashboard_maganjo")
#                 else:
#                     messages.error(request, "Manager branch not specified.")
#                     return redirect("login")

#             elif user.groups.filter(name="sales_agent").exists():
#                 if hasattr(user, "branch"):
#                     if user.branch.lower() == "matugga":
#                         return redirect("sales_agent_dashboard_matugga")
#                     elif user.branch.lower() == "maganjo":
#                         return redirect("sales_agent_dashboard_maganjo")
#                 else:
#                     messages.error(request, "Sales Agent branch not specified.")
#                     return redirect("login")

#             else:
#                 messages.error(request, "Unauthorized role.")
#                 return redirect("login")

#         else:
#             messages.error(request, "Invalid username or password.")

#     # For GET or after failed POST
#     form = AuthenticationForm()
#     return render(request, "login.html", {"form": form, "title": "Login"})






def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})

from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import render
from .models import Sale

def matugga_daily_sales_report(request):
    today = timezone.now().date()

    # Get cash and credit sales separately
    cash_sales = Sale.objects.filter(branch_name='Matugga', date=today, payment_type='cash')
    credit_sales = Sale.objects.filter(branch_name='Matugga', date=today, payment_type='credit')

    # Calculate totals
    total_cash_kg = cash_sales.aggregate(total=Sum('tonnage_kg'))['total'] or 0
    total_cash_amount = cash_sales.aggregate(total=Sum('amount_paid'))['total'] or 0
    total_credit_kg = credit_sales.aggregate(total=Sum('tonnage_kg'))['total'] or 0
    total_credit_amount = credit_sales.aggregate(total=Sum('amount_due'))['total'] or 0

    # Fix total_sales_kg and total_sales_amount by summing both
    total_sales_kg = total_cash_kg + total_credit_kg
    total_sales_amount = total_cash_amount + total_credit_amount

    # Pass everything to the template
    context = {
        'cash_sales': cash_sales,
        'credit_sales': credit_sales,
        'total_cash_kg': total_cash_kg,
        'total_cash_amount': total_cash_amount,
        'total_credit_kg': total_credit_kg,
        'total_credit_amount': total_credit_amount,
        'total_sales_kg': total_sales_kg,  # Correctly calculated total
        'total_sales_amount': total_sales_amount,  # Correctly calculated total
        'today': today,
    }
    return render(request, 'matugga_daily_sales_report.html', context)
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import render
from .models import Sale

def maganjo_daily_sales_report(request):
    today = timezone.now().date()

    # Separate cash and credit sales for Maganjo
    cash_sales = Sale.objects.filter(branch_name='Maganjo', date=today, payment_type='cash')
    credit_sales = Sale.objects.filter(branch_name='Maganjo', date=today, payment_type='credit')

    # Debugging: Check if sales exist
    if not credit_sales.exists():
        print("No credit sales found!")

    # Aggregate totals for cash and credit sales
    total_cash_kg = cash_sales.aggregate(total=Sum('tonnage_kg'))['total'] or 0
    total_cash_amount = cash_sales.aggregate(total=Sum('amount_paid'))['total'] or 0
    total_credit_kg = credit_sales.aggregate(total=Sum('tonnage_kg'))['total'] or 0
    total_credit_amount = credit_sales.aggregate(total=Sum('amount_due'))['total'] or 0

    # Compute total sales
    total_sales_kg = total_cash_kg + total_credit_kg
    total_sales_amount = total_cash_amount + total_credit_amount

    # Pass the updated data to the template
    context = {
        'cash_sales': cash_sales,
        'credit_sales': credit_sales,
        'total_cash_kg': total_cash_kg,
        'total_cash_amount': total_cash_amount,
        'total_credit_kg': total_credit_kg,  # Ensure credit kg is passed
        'total_credit_amount': total_credit_amount,
        'total_sales_kg': total_sales_kg,
        'total_sales_amount': total_sales_amount,
        'today': today,
    }
    return render(request, 'maganjo_daily_sales_report.html', context)
