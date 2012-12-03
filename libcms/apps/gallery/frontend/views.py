# -*- encoding: utf-8 -*-
from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from guardian.decorators import permission_required_or_403

from ..models import Album, AlbumImage



def index(request):
    albums = Album.objects.filter(public=True)
    avatars = AlbumImage.objects.filter(as_avatar=True)
    avatars_dict = {}
    for avatar in avatars:
        avatars_dict[avatar.album_id] = avatar

    for album in albums:
        if album.id in avatars_dict:
            album.avatar = avatars_dict[album.id]
    return render(request, 'gallery/frontend/albums_list.html', {
        'albums': albums
    })


def album_view(request, id):

    album = get_object_or_404(Album, id=id)
    album_images = AlbumImage.objects.filter(album=album)

    return render(request, 'gallery/frontend/album_view.html', {
        'album': album,
        'album_images': album_images,
    })

