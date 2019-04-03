# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from contacts.serializers import Contact, ContactSerializer
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from spam.serializers import Spam, SpamSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def search(request):
    q = request.query_params.get('q', None)

    if q is None:
        return Response({'error': 'Missing query'}, status.HTTP_400_BAD_REQUEST)

    results = []
    querysets = []

    if q.isdigit():
        print("Searching for phone ", q)
        try:
            user = CustomUser.objects.get(phone=q)

            results.append({
                'name': user.name,
                'phone': user.phone,
                'spam': 0,
            })

        except:
            print("User with phone", q, "not found ")

            user_startswith = CustomUser.objects.filter(
                phone__startswith=q).all()
            print("Users starting with", q, user_startswith.count())
            querysets.append(user_startswith)

            contact_startswith = Contact.objects.filter(
                phone__startswith=q).all()
            print("Contacts starting with", q, contact_startswith.count())
            querysets.append(contact_startswith)

            user_contains = CustomUser.objects.filter(
                phone__contains=q).exclude(phone__startswith=q).all()
            print("Users containing", q, user_contains.count())
            querysets.append(user_contains)

            contact_contains = Contact.objects.filter(
                phone__contains=q).exclude(phone__startswith=q).all()
            print("Contacts containing", q, contact_contains.count())
            querysets.append(contact_contains)

    else:
        print("Searching for Name ", q)
        try:
            user_startswith = CustomUser.objects.filter(
                name__startswith=q).all()

            print("Users starting with ", q, user_startswith.count())

            querysets.append(user_startswith)

            contact_startswith = Contact.objects.filter(
                name__startswith=q).all()
            print("Contacts starting with", q, contact_startswith.count())
            querysets.append(contact_startswith)

            user_contains = CustomUser.objects.filter(
                name__contains=q).exclude(name__startswith=q).all()
            print("Users containing", q, user_startswith.count())
            querysets.append(user_contains)

            contact_contains = Contact.objects.filter(
                name__contains=q).exclude(name__startswith=q).all()
            print("Contacts containing", q, contact_contains.count())
            querysets.append(contact_contains)

        except:
            pass

    for queryset in querysets:
        for obj in queryset:

            spam = 0
            spam_reports = Spam.objects.filter(
                phone=obj.phone, spam=True).count()
            if spam_reports > 0:
                print(spam_reports, "spam reports for", obj.phone)
                not_spam_reports = Spam.objects.filter(
                    phone=obj.phone, spam=False).count()

                if not_spam_reports > 0:
                    print(not_spam_reports, "not spam reports for", obj.phone)
                    spam = round(float(spam_reports) /
                                 (spam_reports + not_spam_reports), 2)
                elif spam_reports > 10:
                    spam = 1
                else:
                    spam = spam_reports * 0.2

                print("Spam likelyhood", spam)

            results.append({
                'name': obj.name,
                'phone': obj.phone,
                'spam': spam
            })

    return Response(results)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def detail(request):
    phone = request.query_params.get('phone', None)

    if phone is None:
        return Response({'error': 'Missing phone'}, status.HTTP_400_BAD_REQUEST)

    email = None

    try:
        obj = CustomUser.objects.get(phone=phone)

        print(obj)

        in_contacts = Contact.objects.filter(
            user=request.user, phone=phone).count()

        if in_contacts and obj.email:
            email = obj.email

    except:
        try:
            obj = Contact.objects.get(phone=phone)
        except:
            obj = None

    if obj is None:
        return Response({"error": "Not found"}, status.HTTP_404_NOT_FOUND)

    spam = 0
    spam_reports = Spam.objects.filter(
        phone=obj.phone, spam=True).count()
    if spam_reports > 0:
        print(spam_reports, "spam reports for", obj.phone)
        not_spam_reports = Spam.objects.filter(
            phone=obj.phone, spam=False).count()

        if not_spam_reports > 0:
            print(not_spam_reports, "not spam reports for", obj.phone)
            spam = round(float(spam_reports) /
                         (spam_reports + not_spam_reports), 2)
        elif spam_reports > 10:
            spam = 1
        else:
            spam = spam_reports * 0.2

        print("Spam likelyhood", spam)

    return Response({
        'name': obj.name,
        'phone': obj.phone,
        'spam': spam,
        'email': email
    })
