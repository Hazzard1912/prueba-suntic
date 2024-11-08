from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Document
from .forms import DocumentForm, ApproveDocumentForm

@login_required
def document_list(request):
    documents = Document.objects.filter(owner=request.user) | Document.objects.filter(approver=request.user)
    is_approver = request.user.groups.filter(name='Approvers').exists()
    return render(request, 'documents/document_list.html', {'documents': documents, 'is_approver': is_approver})

@login_required
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if document.owner != request.user and document.approver != request.user:
        return HttpResponseForbidden()
    return render(request, 'documents/document_detail.html', {'document': document})

@login_required
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user
            document.save()
            return redirect('documents:document_list')
    else:
        form = DocumentForm()
    return render(request, 'documents/document_form.html', {'form': form})

@login_required
def document_edit(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if document.owner != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('documents:document_list')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'documents/document_form.html', {'form': form})

@login_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if document.owner != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        document.delete()
        return redirect('documents:document_list')
    return render(request, 'documents/document_confirm_delete.html', {'document': document})

@login_required
def document_approve(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if document.approver != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ApproveDocumentForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            return redirect('documents:document_list')
    else:
        form = ApproveDocumentForm(instance=document)
    return render(request, 'documents/document_approve_form.html', {'form': form})

@login_required
def document_preview(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if document.owner != request.user and document.approver != request.user:
        return HttpResponseForbidden()
    return render(request, 'documents/document_preview.html', {'document': document})
