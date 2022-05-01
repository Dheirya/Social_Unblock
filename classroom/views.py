from django.http import JsonResponse
from django.views.decorators.cache import cache_page, never_cache
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import WebVTTFormatter
from django.http import HttpResponse
from youtubesearchpython import *
from django.shortcuts import redirect
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import pytube
import json
import twint


def decodehash(string):
    arr = string.split(",")
    hash = ""
    for ele in arr:
        if ele.startswith('num'):
            hash = hash + ele.replace("num", "")
        elif ele == "0":
            hash = hash + " "
        else:
            hash = hash + chr(int(ele) + 96)
    return hash


@never_cache
def YoutubeSearchJSON(request):
    if request.method == 'GET':
        return render(request, 'classroom/index.html')


@cache_page(60 * 60 * 6)
def YoutubeAdvancedSearchJSON(request):
    if request.method == 'GET':
        if 'AcRP2W3NHNmEoQgzd9CN' in request.headers:
            if request.headers['AcRP2W3NHNmEoQgzd9CN'] == "seuMBIbvc33s4vKchgGY":
                query = decodehash(request.GET.get('q'))
                number = int(request.GET.get('number')) - 1
                if query:
                    if request.GET.get('minify'):
                        search = VideosSearch(query, limit=500)
                        for _ in range(number):
                            search.next()
                        return JsonResponse(search.result(), safe=False, json_dumps_params={'indent': 2})
                    else:
                        search = VideosSearch(query, limit=500)
                        for _ in range(number):
                            search.next()
                        return JsonResponse(search.result(), safe=False)
                else:
                    return JsonResponse([{'Error': 'No Query'}], safe=False)
            else:
                raise Exception('Error')
        else:
            raise Exception('Error')


@never_cache
def CacheBuster(request):
    if request.method == 'GET':
        return JsonResponse([{'Cache Buster': 'Yes'}], safe=False)


@never_cache
def YoutubeGetVideoSRC(request):
    if request.method == 'GET':
        try:
            yo_id = request.GET.get('id')
            if yo_id:
                youtube = pytube.YouTube('https://youtube.com/watch?v=' + yo_id)
                if request.GET.get('redirect'):
                    return redirect(youtube.streams.get_highest_resolution().url)
                else:
                    return JsonResponse([{'src': youtube.streams.get_highest_resolution().url}], safe=False)
            else:
                return JsonResponse([{'Error': 'No Query'}], safe=False)
        except:
            yo_id = request.GET.get('id')
            src = requests.get('https://socialunblockapi1.vercel.app/youtube/src/?id=' + yo_id)
            return HttpResponse('[{"src": "' + src.json()["src"] + '"}]', content_type='application/json')


@cache_page(60 * 60 * 24 * 30)
def YoutubeGetVideoTrack(request):
    if request.method == 'GET':
        yo_id = request.GET.get('id')
        if yo_id:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(yo_id)
                formatter = WebVTTFormatter()
                json_formatted = formatter.format_transcript(transcript)
                return HttpResponse(json_formatted, content_type="text/vtt")
            except:
                json_formatted = """WEBVTT

00:00:00.000 --> 00:00:00.001
Loading...
                """
                return HttpResponse(json_formatted, content_type="text/vtt")
        else:
            return JsonResponse([{'Error': 'No Query'}], safe=False)


@cache_page(60 * 60 * 24 * 7)
def GoogleSearchAPI(request):
    if request.method == 'GET':
        if 'AcRP2W3NHNmEoQgzd9CN' in request.headers:
            if request.headers['AcRP2W3NHNmEoQgzd9CN'] == "seuMBIbvc33s4vKchgGY":
                query = decodehash(request.GET.get('q'))
                if query:
                    search = requests.get('https://suggestqueries.google.com/complete/search?client=safari&ds=yt&q=' + query)
                    json_search = search.text
                    firstDelPos = json_search.find(',{"k"')
                    secondDelPos = json_search.find('"}')
                    stringAfterReplace = json_search.replace(json_search[firstDelPos + 1:secondDelPos], "").replace(',"}', '')
                    return JsonResponse(json.loads(stringAfterReplace), safe=False)
                else:
                    return JsonResponse([{'Error': 'No Query'}], safe=False)
            else:
                raise Exception('Error')
        else:
            raise Exception('Error')


@cache_page(60 * 60 * 6)
def TwitterDetailJSON(request):
    if request.method == 'GET':
        if 'AcRP2W3NHNmEoQgzd9CN' in request.headers:
            if request.headers['AcRP2W3NHNmEoQgzd9CN'] == "seuMBIbvc33s4vKchgGY":
                username = request.GET.get('username')
                id = request.GET.get('id')
                if username and id:
                    search = requests.get('https://publish.twitter.com/oembed?omit_script=true&url=https://twitter.com/' + username + '/status/' + id)
                    return JsonResponse(search.json(), safe=False)
                else:
                    return JsonResponse([{'Error': 'No Query'}], safe=False)
            else:
                raise Exception('Error')
        else:
            raise Exception('Error')


@cache_page(60 * 60 * 6)
def YoutubeVideoDetailJSON(request):
    if request.method == 'GET':
        if 'AcRP2W3NHNmEoQgzd9CN' in request.headers:
            if request.headers['AcRP2W3NHNmEoQgzd9CN'] == "seuMBIbvc33s4vKchgGY":
                youtube_id = request.GET.get('id')
                if youtube_id:
                    if request.GET.get('minify'):
                        try:
                            videoInfo = Video.getInfo('https://youtu.be/' + youtube_id, mode=ResultMode.json)
                            return JsonResponse(videoInfo, safe=False, json_dumps_params={'indent': 2})
                        except:
                            return JsonResponse([{'Error': 'No Comments'}], safe=False)
                    else:
                        try:
                            videoInfo = Video.getInfo('https://youtu.be/' + youtube_id, mode=ResultMode.json)
                            return JsonResponse(videoInfo, safe=False)
                        except:
                            return JsonResponse([{'Error': 'No Comments'}], safe=False)
                else:
                    return JsonResponse([{'Error': 'No Query'}], safe=False)
            else:
                raise Exception('Error')
        else:
            raise Exception('Error')


@cache_page(60 * 60 * 24 * 14)
def YoutubeCommentsSearchJSON(request):
    if request.method == 'GET':
        if 'AcRP2W3NHNmEoQgzd9CN' in request.headers:
            if request.headers['AcRP2W3NHNmEoQgzd9CN'] == "seuMBIbvc33s4vKchgGY":
                youtube_id = request.GET.get('id')
                if youtube_id:
                    if request.GET.get('minify'):
                        try:
                            comments = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?key={yourkey}&textFormat=plainText&part=snippet&maxResults=75&order=relevance&videoId=' + youtube_id)
                            return JsonResponse(comments.json(), safe=False, json_dumps_params={'indent': 2})
                        except:
                            return JsonResponse([{'Error': 'No Comments'}], safe=False)
                    else:
                        try:
                            comments = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?key={yourkey}&textFormat=plainText&part=snippet&maxResults=75&order=relevance&videoId=' + youtube_id)
                            return JsonResponse(comments.json(), safe=False)
                        except:
                            return JsonResponse([{'Error': 'No Comments'}], safe=False)
                else:
                    return JsonResponse([{'Error': 'No Query'}], safe=False)
            else:
                raise Exception('Error')
        else:
            raise Exception('Error')


@cache_page(60 * 60 * 24)
def TwitterSearchJSON(request):
    if request.method == 'GET':
        if 'AcRP2W3NHNmEoQgzd9CN' in request.headers:
            if request.headers['AcRP2W3NHNmEoQgzd9CN'] == "seuMBIbvc33s4vKchgGY":
                query = decodehash(request.GET.get('q'))
                c = twint.Config()
                c.Search = query
                c.Limit = 125
                c.Pandas = True
                c.Popular_tweets = True
                likes = request.GET.get('likes')
                if not likes:
                    c.Min_likes = 100
                twint.run.Search(c)
                df = twint.storage.panda.Tweets_df
                djson = df.to_json(orient='table')
                return HttpResponse(djson, content_type='application/json')
            else:
                raise Exception('Error')
        else:
            raise Exception('Error')


@cache_page(60 * 60 * 24 * 30)
def URLJSON(request):
    if request.method == 'GET':
        if 'AcRP2W3NHNmEoQgzd9CN' in request.headers:
            if request.headers['AcRP2W3NHNmEoQgzd9CN'] == "seuMBIbvc33s4vKchgGY":
                query = request.GET.get('id')
                try:
                    response = requests.get(query, headers={"User-Agent": "Googlebot"})
                    soup = BeautifulSoup(response.text, "html.parser")
                    metas = soup.find_all('meta', {"name": "description"})
                    title = soup.find_all('title')
                    do = False
                    ix = False
                    for m in metas:
                        if m.get('name') == 'description':
                            if do is False:
                                do = True
                                desc = m.get('content')
                                url_desc = desc
                        else:
                            if do is False:
                                do = True
                                url_desc = ""
                    for t in title:
                        if ix is False:
                            ix = True
                            url_title = t.string
                    return JsonResponse({"data": {"title": url_title, "description": url_desc}}, safe=False)
                except:
                    return JsonResponse({'error': 'error'}, safe=False)
            else:
                raise Exception('Error')
        else:
            raise Exception('Error')
