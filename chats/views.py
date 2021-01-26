from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import FriendRequest, Friend, ChatThread, SentRequest


@login_required()
def chat(request):
    user = request.user
    friends_thread = user.outbox.all()

    pk = request.GET.get('pk')
    print(pk)

    context = {
        'friends': friends_thread,
    }
    return render(request, 'chat.html', context)


@login_required()
def chat_message(request, id):
    user = request.user
    thread = ChatThread.objects.get(id=id)

    obj = Friend.objects.get(user=user)

    friend = thread.friend
    if friend in obj.friend.all():
        messages = thread.chatmessage_set.all()
        friends_thread = user.outbox.all()

        context = {
            'friend': friend,
            'thread': thread,
            'messages': messages,
            'friends': friends_thread,
        }

        return render(request, 'chat_message.html', context)


@login_required()
def search_for_friends(request):
    user = request.user
    friends_list = []
    request_sent_list = []
    user_friend_request_list = []

    if request.method == 'POST':
        username = request.POST['search']
        if username.isalpha():
            matches = User.objects.filter(username__startswith=username)

            # Check if a search match is in a user's friend list
            if bool(Friend.objects.all().filter(user=user)):
                user_friend_list_obj = Friend.objects.get(user=user)
                friends_list += list(user_friend_list_obj.friend.all())

            else:
                friends_list += []

            # check if a search match has already been sent a request
            if bool(SentRequest.objects.all().filter(user=user)):
                user_sent_request_obj = SentRequest.objects.get(user=user)
                request_sent_list += list(user_sent_request_obj.friend.all())

            else:
                request_sent_list += []

            # check if a search match sent the user a request
            if bool(FriendRequest.objects.all().filter(user=user)):
                user_friend_request_list_obj = FriendRequest.objects.get(user=user)
                user_friend_request_list += list(user_friend_request_list_obj.friend.all())

            else:
                user_friend_request_list += []

            context = {
                'matches': matches,
                'friends_list': friends_list,
                'request_sent_list': request_sent_list,
                'user_friend_request_list': user_friend_request_list,
            }

            return render(request, 'search_results.html', context)

    return redirect('chat')

@login_required()
def accept_request(request, id):
    friend = User.objects.get(id=id)
    user = request.user

    # User adds friend to friend's list
    if bool(Friend.objects.all().filter(user=user)):
        user_friend_obj = Friend.objects.get(user=user)
        user_friend_obj.friend.add(friend)
    else:
        obj = Friend.objects.create(user=user)
        obj.friend.add(friend)

    # Friend adds user to friend's list
    if bool(Friend.objects.all().filter(user=friend)):
        friend_friend_obj = Friend.objects.get(user=friend)
        friend_friend_obj.friend.add(user)
    else:
        obj = Friend.objects.create(user=friend)
        obj.friend.add(user)

    # A Chat Thread is created
    ChatThread.objects.create(user=user, friend=friend)
    ChatThread.objects.create(user=friend, friend=user)

    # friend is removed from user friend request list
    if bool(FriendRequest.objects.all().filter(user=user)):
        user_friend_request_list_obj = FriendRequest.objects.get(user=user)
        user_friend_request_list_obj.friend.remove(friend)
    else:
        obj = FriendRequest.objects.get(user=user)
        obj.friend.remove(friend)

    # user is removed from friend's sent request list
    if bool(SentRequest.objects.all().filter(user=friend)):
        friend_sent_request_list_obj = SentRequest.objects.get(user=friend)
        friend_sent_request_list_obj.friend.remove(user)
    else:
        obj = SentRequest.objects.get(user=friend)
        obj.friend.remove(user)


    return redirect('friends')

def delete_thread(request, id):
    # Chat Thread id is taken since is was passed from the template
    friend = User.objects.get(id=id)

    user = request.user

    # Friend is removed from User's friend's list
    obj1 = Friend.objects.get(user=user)
    obj1.friend.remove(friend)

    # User is removed from Friend's friend's list
    obj2 = Friend.objects.get(user=friend)
    obj2.friend.remove(user)

    # Unfortunately for now the chat thread will be deleted

    # Chat thread get's deleted
    user.outbox.get(friend=friend).delete()
    friend.outbox.get(friend=user).delete()

    return redirect('friends')


@login_required()
def friends(request):
    user = request.user
    friends_thread = user.outbox.all()
    friend_requests_list = []
    friends_list = []
    if bool(FriendRequest.objects.all().filter(user=user)):
        friend_requests_obj = FriendRequest.objects.get(user=user)
        for friend_request in list(friend_requests_obj.friend.all()):
            friend_requests_list.append(friend_request)

    else:
        friend_requests_list += []

    if bool(Friend.objects.all().filter(user=user)):
        friend_obj = Friend.objects.get(user=user)
        for friend in list(friend_obj.friend.all()):
            friends_list.append(friend)

    else:
        friends_list += []


    context = {
        'user': user,
        'friends_requests': friend_requests,
        'friends': friends_list,
        'friend_requests_list': friend_requests_list,
    }
    return render(request, 'friends.html', context)

@login_required()
def send_a_friend_request(request, id):
    friend = User.objects.get(pk=id)
    user = request.user

    if bool(SentRequest.objects.all().filter(user=user)):
        user_sent_request_obj = SentRequest.objects.get(user=user)
        user_sent_request_obj.friend.add(friend)
    else:
        obj = SentRequest.objects.create(user=user)
        obj.friend.add(friend)

    if bool(FriendRequest.objects.all().filter(user=friend)):
        friend_friend_request_obj = FriendRequest.objects.get(user=friend)
        friend_friend_request_obj.friend.add(user)
    else:
        obj = FriendRequest.objects.create(user=friend)
        obj.friend.add(user)

    return redirect('search_for_friends')









