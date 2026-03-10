import io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
import pandas as pd

from apps.profiles.models import Profile
from apps.matchmaking.models import Interest
from apps.interactions.models import Favorite
from apps.moderation.models import ExportLog
from apps.core.decorators import admin_required

User = get_user_model()


@login_required
def home_view(request):
    """Browse all profiles with search / filter."""
    queryset = Profile.objects.select_related('user').exclude(user=request.user)

    try:
        user_gender = request.user.profile.gender.lower()
        if user_gender in ('m', 'male'):
            queryset = queryset.filter(gender__in=['F', 'female'])
        elif user_gender in ('f', 'female'):
            queryset = queryset.filter(gender__in=['M', 'male'])
    except Profile.DoesNotExist:
        pass

    q          = request.GET.get('q', '')
    gender     = request.GET.get('gender', '')
    min_age    = request.GET.get('min_age', '')
    max_age    = request.GET.get('max_age', '')
    location   = request.GET.get('location', '')
    occupation = request.GET.get('occupation', '')
    education  = request.GET.get('education', '')
    religion   = request.GET.get('religion', '')

    if q:
        queryset = queryset.filter(
            Q(name__icontains=q) |
            Q(occupation__icontains=q) |
            Q(location__icontains=q) |
            Q(education__icontains=q)
        )
    if gender:
        queryset = queryset.filter(gender__iexact=gender)
    if min_age:
        try:
            queryset = queryset.filter(age__gte=int(min_age))
        except ValueError:
            pass
    if max_age:
        try:
            queryset = queryset.filter(age__lte=int(max_age))
        except ValueError:
            pass
    if location:
        queryset = queryset.filter(location__icontains=location)
    if occupation:
        queryset = queryset.filter(occupation__icontains=occupation)
    if education:
        queryset = queryset.filter(education__icontains=education)
    if religion:
        queryset = queryset.filter(religion__iexact=religion)

    queryset = queryset.order_by('-created_at')

    paginator = Paginator(queryset, 12)
    page_number = request.GET.get('page', 1)
    profiles = paginator.get_page(page_number)

    favorited_ids = set(
        Favorite.objects.filter(user=request.user).values_list('profile_id', flat=True)
    )

    sent_accepted_ids = set()
    sent_pending_ids = set()
    for interest in Interest.objects.filter(sender=request.user).select_related('receiver__profile'):
        try:
            pid = interest.receiver.profile.id
            if interest.status == 'accepted':
                sent_accepted_ids.add(pid)
            else:
                sent_pending_ids.add(pid)
        except Profile.DoesNotExist:
            pass

    filters_active = any([gender, min_age, max_age, location, occupation, education, religion])

    return render(request, 'profiles/home.html', {
        'profiles': profiles,
        'favorited_ids': favorited_ids,
        'sent_accepted_ids': sent_accepted_ids,
        'sent_pending_ids': sent_pending_ids,
        'filters_active': filters_active,
        'filters': {
            'q': q, 'gender': gender, 'min_age': min_age,
            'max_age': max_age, 'location': location,
            'occupation': occupation, 'education': education,
            'religion': religion,
        },
    })


@login_required
def profile_detail_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    is_own = profile.user == request.user

    interest = Interest.objects.filter(
        Q(sender=request.user, receiver=profile.user) |
        Q(sender=profile.user, receiver=request.user)
    ).first()

    can_view_contact = bool(interest and interest.status == 'accepted')
    is_favorited = Favorite.objects.filter(user=request.user, profile=profile).exists()

    return render(request, 'profiles/detail.html', {
        'profile': profile,
        'is_own': is_own,
        'interest': interest,
        'can_view_contact': can_view_contact,
        'is_favorited': is_favorited,
    })


@login_required
def edit_profile_view(request):
    user = request.user
    profile = getattr(user, 'profile', None)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name  = request.POST.get('last_name', '').strip()
        user.email      = request.POST.get('email', '').strip()
        user.save()

        if profile is None:
            profile = Profile(user=user, age=18, mobile_number='', location='', gender='male')

        full_name = f"{user.first_name} {user.last_name}".strip()
        if full_name:
            profile.name = full_name

        profile.location              = request.POST.get('location', '').strip()
        profile.occupation            = request.POST.get('occupation', '').strip()
        profile.education             = request.POST.get('education', '').strip()
        profile.about                 = request.POST.get('bio', '').strip()
        profile.desired_partner_traits = request.POST.get('desired_partner_traits', '').strip()

        height_str = request.POST.get('height', '')
        if height_str:
            try:
                profile.height = float(height_str)
            except ValueError:
                pass

        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            if photo.size > 5 * 1024 * 1024:
                messages.error(request, 'Photo must be less than 5 MB.')
                return redirect('profiles:edit_profile')
            profile.photo = photo

        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profiles:edit_profile')

    return render(request, 'profiles/edit.html', {
        'user': user,
        'profile': profile,
    })


@admin_required
def export_pdf_view(request):
    profiles     = Profile.objects.select_related('user').all()
    record_count = profiles.count()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30
    )
    elements = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title', parent=styles['Heading1'],
        fontSize=20, textColor=colors.HexColor('#c0392b'),
        spaceAfter=20, alignment=TA_CENTER
    )

    elements.append(Paragraph("PerfectPair – Profiles Export", title_style))
    elements.append(Paragraph(
        f"Generated: {timezone.now().strftime('%Y-%m-%d %H:%M')} UTC", styles['Normal']
    ))
    elements.append(Paragraph(f"Total records: {record_count}", styles['Normal']))
    elements.append(Spacer(1, 0.3 * inch))

    table_data = [['Name', 'Gender', 'Age', 'Location', 'Occupation', 'Mobile']]
    for p in profiles:
        table_data.append([
            (p.name or '')[:25],
            p.gender.capitalize(),
            str(p.age),
            (p.location or '')[:25],
            (p.occupation or '')[:20],
            p.mobile_number,
        ])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1,  0), colors.HexColor('#c0392b')),
        ('TEXTCOLOR',     (0, 0), (-1,  0), colors.whitesmoke),
        ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME',      (0, 0), (-1,  0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1,  0), 10),
        ('BOTTOMPADDING', (0, 0), (-1,  0), 10),
        ('BACKGROUND',    (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR',     (0, 1), (-1, -1), colors.black),
        ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',      (0, 1), (-1, -1), 8),
        ('GRID',          (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    doc.build(elements)

    pdf_data  = buffer.getvalue()
    buffer.close()
    file_name = f"profiles_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    ExportLog.objects.create(
        admin=request.user, file_type='pdf',
        file_name=file_name, export_type='profiles',
        record_count=record_count,
    )

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response


@admin_required
def export_excel_view(request):
    profiles     = Profile.objects.select_related('user').all()
    record_count = profiles.count()

    data_list = []
    for p in profiles:
        data_list.append({
            'ID':         p.id,
            'Name':       p.name,
            'Username':   p.user.username,
            'Email':      p.user.email,
            'Gender':     p.gender,
            'Age':        p.age,
            'Location':   p.location,
            'Occupation': p.occupation,
            'Education':  p.education,
            'Height':     float(p.height) if p.height else None,
            'Mobile':     p.mobile_number,
            'Created':    p.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

    df = pd.DataFrame(data_list)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Profiles')
    excel_data = buffer.getvalue()
    buffer.close()

    file_name = f"profiles_{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    ExportLog.objects.create(
        admin=request.user, file_type='excel',
        file_name=file_name, export_type='profiles',
        record_count=record_count,
    )

    response = HttpResponse(
        excel_data,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response
