from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q

from .models import Category, Item, Message
from .forms import SignUpForm, ItemForm, EditItemForm, ContactForm, MessageForm


def index(request):
    """Home page displaying latest unsold items and category list."""
    items = Item.objects.filter(is_sold=False)[:6]
    categories = Category.objects.all()
    return render(request, 'core/index.html', {
        'items': items,
        'categories': categories,
    })


def contact(request):
    """Contact page with Django Form validation and flash success messages."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})


def signup_view(request):
    """User registration view using Django's UserCreationForm."""
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}.')
            return redirect('index')
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {'form': form})


def browse(request):
    """Browse and search items with category filtering."""
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', 0)

    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()

    try:
        category_id = int(category_id)
    except (ValueError, TypeError):
        category_id = 0

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'core/browse.html', {
        'items': items,
        'categories': categories,
        'query': query,
        'category_id': category_id,
    })


def detail(request, pk):
    """Item detail page showing seller info, actions, and message form."""
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[:3]
    form = MessageForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = item.seller
            msg.item = item
            msg.save()
            messages.success(request, 'Message sent to seller!')
            return redirect('conversation_detail', item_pk=item.pk, user_pk=item.seller.pk)

    return render(request, 'core/detail.html', {
        'item': item,
        'related_items': related_items,
        'form': form,
    })


@login_required
def new_item(request):
    """Create a new item listing (seller = logged in user)."""
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            messages.success(request, 'Item listed successfully!')
            return redirect('detail', pk=item.pk)
    else:
        form = ItemForm()

    return render(request, 'core/form.html', {
        'form': form,
        'title': 'New Item',
    })


@login_required
def edit_item(request, pk):
    """Edit an existing item listing (restricted to seller)."""
    item = get_object_or_404(Item, pk=pk, seller=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('detail', pk=item.pk)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'core/form.html', {
        'form': form,
        'title': 'Edit Item',
        'item': item,
    })


@login_required
def delete_item(request, pk):
    """Delete an item listing (restricted to seller)."""
    item = get_object_or_404(Item, pk=pk, seller=request.user)
    item.delete()
    messages.success(request, 'Item deleted successfully.')
    return redirect('browse')


@login_required
def inbox(request):
    """View listing active conversations grouped by (item, other user)."""
    user_messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('item', 'sender', 'receiver')

    # Group messages into unique conversations (item, other_user)
    conversations_map = {}
    for msg in user_messages:
        other_user = msg.receiver if msg.sender == request.user else msg.sender
        key = (msg.item.pk, other_user.pk)
        if key not in conversations_map:
            conversations_map[key] = {
                'item': msg.item,
                'other_user': other_user,
                'last_message': msg,
                'unread_count': 0,
            }
        # Update unread count if message was sent to request.user and is unread
        if msg.receiver == request.user and not msg.is_read:
            conversations_map[key]['unread_count'] += 1

    conversations = list(conversations_map.values())

    return render(request, 'core/inbox.html', {
        'conversations': conversations,
    })


@login_required
def conversation_detail(request, item_pk, user_pk):
    """View showing message history for a specific item and user."""
    item = get_object_or_404(Item, pk=item_pk)
    other_user = get_object_or_404(User, pk=user_pk)

    conversation_messages = Message.objects.filter(
        item=item
    ).filter(
        (Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user))
    ).order_by('timestamp')

    # Mark incoming unread messages as read
    Message.objects.filter(
        item=item, sender=other_user, receiver=request.user, is_read=False
    ).update(is_read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = other_user
            msg.item = item
            msg.save()
            return redirect('conversation_detail', item_pk=item.pk, user_pk=other_user.pk)
    else:
        form = MessageForm()

    return render(request, 'core/conversation.html', {
        'item': item,
        'other_user': other_user,
        'messages_list': conversation_messages,
        'form': form,
    })