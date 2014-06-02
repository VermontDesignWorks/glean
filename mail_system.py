## -- Time to Split -- ##
import sys
import random


from django.contrib.sites.models import Site
from django.core.mail import send_mail, send_mass_mail
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template.base import Template as T, Context
from django.utils.text import slugify

from functions import primary_source


def weave_template_and_body_and_glean(template, announcement, glean):
    site = Site.objects.get(pk=1)
    glean_link = "<a href='" + site.domain + str(
        reverse(
            'gleanevent:detailglean', args=(glean.id,))) + "'>Glean Info</a>"
    replace = {
        '{{custom}}': announcement.message,
        '{{glean.title}}': glean.title,
        '{{date}}': glean.date.strftime(
            '%A, %B %d') if glean.time_of_day == 'NA' else glean.date.strftime(
            '%A, %B %d') + ' ' + (
            'Morning' if glean.time_of_day == 'AM' else 'Afternoon'),
        '{{glean.description}}': glean.description,
        #'{{info}}': glean_link,
    }
    returnable = template.body
    for key, value in replace.iteritems():
        while returnable.find(key) != -1:
            try:
                start = returnable.find(key)
                finish = returnable.find(key)+len(key)
                returnable = returnable[:start] + value + returnable[finish:]
            except:  # in the case that the key ends the document
                start = returnable.find(key)
                finish = returnable.find(key)+len(key)
                returnable = returnable[:start] + value
    return returnable


def weave_unsubscribe(body, userprofile, announce):
    site = Site.objects.get(pk=1)
    returnable = body
    key = '{{unsubscribe}}'
    if userprofile.unsubscribe_key:
        value = userprofile.unsubscribe_key
    else:
        value = ''
        for i in range(29):
            value += random.choice('abcdefghijklmnopqrstuvwvyz')
        userprofile.unsubscribe_key = value
        userprofile.save()
    unsub_link = "<a href='" + site.domain + str(
        reverse('announce:unsubscribelink', args=(value,))
    )+"'>Click Here Unsubscribe</a> (if the link doesn't work,"
    " copy and paste the following address into your "
    "browser: " + site.domain + str(reverse(
        'announce:unsubscribelink', args=(value,)))

    glean_link = "<a href='" + site.domain + str(
        reverse('gleanevent:detailglean', args=(announce.glean.id,))
    ) + "'>Glean Time and Location Information</a>"
    raw_glean_link = site.domain+str(reverse('gleanevent:detailglean', args=(
        announce.glean.id,)))
    if announce.title:
        subject = announce.title
    else:
        subject = announce.glean.title

    date_entry = announce.glean.date.strftime('%A, %B %d')
    if announce.glean.time_of_day == "AM":
        date_entry += ' Morning'
    elif announce.glean.time_of_day == "PM":
        date_entry += ' Morning'

    replace = {
        '{{custom}}': announce.message,
        '{{glean.title}}': announce.glean.title,
        '{{glean.description}}': announce.glean.description,
        '{{info}}': glean_link,
        '{{date}}': date_entry,
        '{{raw_glean_link}}': raw_glean_link,
        '{{unsubscribe}}': unsub_link,
        '{{subject}}': subject,
    }
    returnable = announce.template.body
    for key, value in replace.iteritems():
        while returnable.find(key) != -1:
            try:
                start = returnable.find(key)
                finish = returnable.find(key)+len(key)
                returnable = returnable[:start] + value + returnable[finish:]
            except:  # in the case that the key ends the document
                start = returnable.find(key)
                finish = returnable.find(key)+len(key)
                returnable = returnable[:start] + value
    return returnable


def render_email(template, announcement, profile):
    site = Site.objects.get(pk=1)
    glean = announcement.glean
    glean_link = "<a href='{0}'>Glean Info</a>".format(glean.url)
    template = T(template.body)
    context = Context(
        {
            "custom": announcement.message,
            "glean": glean,
            'date': glean.date.strftime('%A, %B %d'),
            'info': glean_link,
            '{{raw_glean_link}}': glean_url,
            "unsubscribe_url": profile.unsubscribe_url,
            "unsubscribe": profile.stock_unsubscribe_link,
        }
    )
    body = str(template.render(context))
    return body


#== Mailing Logic ==#
def quick_mail(subject, text, recipient):
    msg = EmailMessage(
        subject,
        text,
        'no-reply@vermontgleaningcollective.org',
        [recipient]
    )
    msg.content_subtype = "html"
    msg.send()


def mail_from_source(body, announcement):
        mo = announcement.member_organization
        glean = announcement.glean

        from_address = slugify(
            unicode(mo)
        ) + "@vermontgleaningcollective.org"

        if announcement.title:
            subject = announcement.title
        else:
            subject = glean.title
        if mo.testing:
            for recipient in announcement.email_recipients.all():
                profile = recipient.profile
                text = weave_unsubscribe(
                    body,
                    profile,
                    announcement)
                if recipient not in glean.invited_volunteers.all():
                    glean.invited_volunteers.add(recipient)

            if mo.testing_email:
                msg = EmailMessage(
                    subject,
                    text,
                    from_address,
                    [mo.testing_email]
                )
                msg.content_subtype = "html"
                msg.send()

        else:
            for recipient in announcement.email_recipients.all():
                profile = recipient.profile
                text = weave_unsubscribe(body, profile, announcement)
                msg = EmailMessage(
                    subject,
                    text,
                    from_address,
                    [recipient.email]
                )
                msg.content_subtype = "html"
                msg.send()
                if recipient not in glean.invited_volunteers.all():
                    glean.invited_volunteers.add(recipient)
            for recipient in announcement.phone_recipients.all():
                if recipient not in glean.invited_volunteers.all():
                    glean.invited_volunteers.add(recipient)
        glean.save()
