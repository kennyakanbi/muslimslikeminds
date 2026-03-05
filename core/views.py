from django.shortcuts import render, get_object_or_404
from .models import Teaching
from .models import Media
from .models import Event
from django.utils import timezone
from .models import CommunityPost
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.http import FileResponse, JsonResponse, HttpResponse
from pathlib import Path
from django.db.models import F
from urllib.parse import urlparse, parse_qs


def about(request):
    return render(request, 'core/about.html')


def home(request):
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(
        start_date__gte=today,
        is_published=True
    ).order_by('start_date')[:5]

    latest_teaching = Teaching.objects.order_by('-created_at')[:3]

    latest_media = Media.objects.filter(
        is_published=True
    ).order_by('-created_at')[:3]

    trending_media = Media.objects.filter(
        is_published=True
    ).order_by('-views', '-created_at')[:3]

    context = {
        'upcoming_events': upcoming_events,
        'latest_teaching': latest_teaching,
        'latest_media': latest_media,
        'trending_media': trending_media,
    }

    return render(request, 'core/home.html', context)


def teachings(request):
    teachings = Teaching.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'core/teachings.html', {
        'teachings': teachings
    })

def teaching_detail(request, id):
    teaching = Teaching.objects.get(id=id)  # or however you fetch your object
    return render(request, "core/teaching_detail.html", {"teaching": teaching})


def media(request):
    media_type = request.GET.get("type")

    queryset = Media.objects.all().order_by("-created_at")

    if media_type:
        queryset = queryset.filter(media_type=media_type)

    featured_media = Media.objects.filter(is_featured=True).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(queryset, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "featured_media": featured_media,
        "page_obj": page_obj,
        "selected_type": media_type,
    }

    return render(request, "core/media.html", context)


def media_detail(request, slug):
    media = get_object_or_404(Media, slug=slug, is_published=True)

    # Increase views
    Media.objects.filter(id=media.id).update(views=F('views') + 1)

    youtube_id = None

    if media.youtube_url:
        parsed_url = urlparse(media.youtube_url)

        if "youtube.com" in parsed_url.netloc:
            youtube_id = parse_qs(parsed_url.query).get("v")
            if youtube_id:
                youtube_id = youtube_id[0]

        elif "youtu.be" in parsed_url.netloc:
            youtube_id = parsed_url.path[1:]

    related_media = Media.objects.filter(
        media_type=media.media_type,
        is_published=True
    ).exclude(id=media.id)[:3]

    context = {
        "media": media,
        "youtube_id": youtube_id,
        "related_media": related_media
    }

    return render(request, "core/media_detail.html", context)


from django.shortcuts import render, get_object_or_404

def media_list(request):
    selected_type = request.GET.get('type')

    media_qs = Media.objects.filter(is_published=True)

    if selected_type:
        media_qs = media_qs.filter(media_type=selected_type)

    trending_media = Media.objects.filter(is_published=True).order_by('-views')[:5]

    context = {
        'media_list': media_qs.order_by('-created_at'),
        'selected_type': selected_type,
        'trending_media': trending_media,
    }
    return render(request, 'core/media_list.html', context)



def community(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if name and email and message:
            CommunityPost.objects.create(name=name, email=email, message=message)
            return redirect('core/community')

    posts = CommunityPost.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'core/community.html', {'posts': posts})


def events(request):
    # Get all published events, ordered by start_date
    events = Event.objects.filter(is_published=True).order_by('start_date')
    
    context = {
        'events': events
    }
    return render(request, 'core/events.html', context)


def event_detail(request, pk):
    # Get a single published event by primary key
    event = get_object_or_404(Event, pk=pk, is_published=True)
    context = {'event': event}
    return render(request, 'core/event_detail.html', context)


def serve_humanity(request):
    return render(request, 'core/serve_humanity.html')


def contact(request):
    return render(request, 'core/contact.html')

from django.http import FileResponse
def serve_video(request, filename):
    return FileResponse(open(f'media/{filename}', 'rb'), content_type='video/mp4')

from django.http import FileResponse, HttpResponse
from pathlib import Path

MEDIA_MAP = {
    "audio": ("media/sample.mp3", "audio/mpeg"),
    "video": ("media/sample.mp4", "video/mp4"),
}


MEDIA_FILES = {
    "audio": {
        "path": "media/sample.mp3",
        "content_type": "audio/mpeg",
    },
    "video": {
        "path": "media/sample.mp4",
        "content_type": "video/mp4",
    },
}

def media_view(request):
    media_type = request.GET.get("type")

    if media_type not in MEDIA_FILES:
        return HttpResponse("Invalid media type", status=400)

    media = MEDIA_FILES[media_type]
    file_path = Path(media["path"])

    if not file_path.exists():
        return HttpResponse("Media file not found", status=404)

    response = FileResponse(
        open(file_path, "rb"),
        content_type=media["content_type"],
    )
    response["Accept-Ranges"] = "bytes"
    return response

