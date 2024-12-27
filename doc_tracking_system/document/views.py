from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Document, DocumentStatus
from .forms import DocumentForm, DocumentSearchForm


@login_required
def dashboard(request):
    department = request.user.userprofile.department

    # Status counts for the logged-in user's department
    pending_count = DocumentStatus.objects.filter(
        department=department, status='Pending'
    ).count()
    in_process_count = DocumentStatus.objects.filter(
        department=department, status='In Process'
    ).count()
    forwarded_count = DocumentStatus.objects.filter(
        department=department, status='Forwarded'
    ).count()
    returned_count = DocumentStatus.objects.filter(
        department=department, status='Returned'
    ).count()

    # Recent activities
    recent_activities = DocumentStatus.objects.filter(
        department=department
    ).order_by('-timestamp')[:10]

    context = {
        'pending_count': pending_count,
        'in_process_count': in_process_count,
        'forwarded_count': forwarded_count,
        'returned_count': returned_count,
        'recent_activities': recent_activities,
    }

    return render(request, 'document/dashboard.html', context)

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.created_by = request.user
            document.save()
            # Create initial status
            DocumentStatus.objects.create(
                document=document,
                department=request.user.userprofile.department,
                status='In Process'
            )
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'document/upload.html', {'form': form})

@login_required
def document_list(request):
    form = DocumentSearchForm(request.GET or None)
    documents = Document.objects.filter(forwarded_to=request.user.userprofile.department)

    if form.is_valid():
        if form.cleaned_data['title']:
            documents = documents.filter(title__icontains=form.cleaned_data['title'])
        if form.cleaned_data['category']:
            documents = documents.filter(category__icontains=form.cleaned_data['category'])
        if form.cleaned_data['status']:
            documents = documents.filter(status__icontains=form.cleaned_data['status'])

    return render(request, 'document/list.html', {'form': form,'documents': documents})

@login_required
def forward_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        forwarded_to = request.POST.get('forwarded_to')
        document.forwarded_to_id = forwarded_to
        document.save()
        # Update status
        DocumentStatus.objects.create(
            document=document,
            department_id=forwarded_to,
            status='Pending'
        )
        return redirect('document_list')
    return render(request, 'document/forward.html', {'document': document})

@login_required
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return render(request, 'document/detail.html', {'document': document})
