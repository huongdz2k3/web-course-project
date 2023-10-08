# Available functions:
#    render - replacement for django render function
#    path - replacement for django path function. please use with * when replacing in urls.py
#    supported_languages - list that contains all available languages for this site
# Functions to be used in django templates:
#    languageReferences - create 'alternate' language references for SEO.
#        put it inside of the <head> section of the page in format {{languageReferences|safe}}
#    lang - current language. Used mostly in <html lang="{{lang}}">
#    languageMenu - adding language selection for your page. Format: {{languageMenu|safe}}
#    <<link variables>> - create linking to correct language link. 
#    usage:
#    for translated pages change {% url "my_page" %}
#    to name without quotes:     {% url my_page %}
supported_languages = ['en', 'vi']

def translation_dictionary(lang):
    if lang == 'en': return {
        'header_home':'''Home''',
        'header_about':'''About''',
        'header_contact_us':'''Contact''',
        'header_become_an_instructor':'''Become an Instructor''',
        'header_account':'''Account''',
        'header_enrolled_courses':'''Enrolled Courses''',
        'header_logout':'''Logout''',
        'header_welcome':'''Welcome''',
        'home_category':'''All Categories''',
        'home_featured_courses':'''Featured Courses''', 
        'home_featured_courses_des':'''Discover your perfect program in our courses''',
        'home_free': '''Free''',
        'about_story':'''Our Story''',
        'about_story_slogan': '''You can study anytime, anywhere flexibly''',
        'slogan': '''Technology Is Bringing A Massive Wave Of Evolution On Learning Things In Different Ways''',
        'view_courses': '''VIEW COURSES''',
        'trending_categories': '''Trending Categories''',
        'trending_categories_slogan': '''Check out the categories below for more information''',
        'browse_all': '''Browse All''',
        'upcoming_events': '''Upcoming Events''',
        'event_slogan': '''Join our rewarding events''',
        'top_rating_instructors': '''Top Rating Instructors''',
        'instructor_slogan': '''Opportunity to be guided by experts''',
        'latest_news': '''Latest News''',
        'news_slogan': '''Update the latest news''',
        'slogan1': '''Learn at your own pace''',
        'slogan1_content': '''''',
        'slogan2': '''Community of opportunities''',
        'slogan2_content': '''''',
        'footer_company': '''Company''',
        'footer_community': '''Community''',
        'table_of_content': '''Catalogue''',
        'topics': '''Topics''',
        'web_program': '''Web programming''',
        'mobile_program': '''Mobile app programming''',
        'embeded_program': '''Embedded programming''',
        'network_program': '''Network programming''',
        'machine_learning': '''Machine learning''',
        'support': '''Support''',
        'documentation': '''Documentation''',
        'forums': '''Forums''',
        'programmer': '''Programmer''',
        'home_description': 'Online learning refers to instruction that is delivered electronically through various multimedia and Internet platforms and applications. It is used interchangeably with other terms such as web-based learning, e-learning, computer-assisted instruction, and Internet-based learning.',
        'home_subscribe': 'Subscribe Our Newsletter',
        'subscribe': 'Subscribe',
        }
    if lang == 'vi': return {
        'header_home':'''Trang chủ''',
        'header_about':'''Về chúng tôi''',
        'header_contact_us':'''Liên hệ''',
        'header_become_an_instructor':'''Giảng viên''',
        'header_account':'''Tài khoản''',
        'header_enrolled_courses':'''Khóa học của tôi''',
        'header_logout':'''Đăng xuất''',
        'header_welcome':'''Xin chào''',
        'home_category':'''Thể loại''',
        'home_featured_courses':''' Khóa học nổi bật''',
        'home_featured_courses_des':'''Khám phá các chương trình chất lượng của chúng tôi''',
        'home_free': '''Miễn phí''',
        'about_story':'''Sứ mệnh''',
        'about_story_slogan': '''Bạn có thể học mọi lúc mọi nơi một cách linh hoạt''',
        'slogan': '''Công nghệ đang mang lại một làn sóng tiến hóa lơn trong lĩnh vực giáo dục theo những cách khác nhau''',
        'view_courses': '''TẤT CẢ KHÓA HỌC''',
        'trending_categories': '''Danh mục thịnh hành''',
        'trending_categories_slogan': '''Khám phá các thể loại dưới đây để vập nhật những kiến thức mới nhất''',
        'browse_all': '''Tất cả''',
        'upcoming_events': '''Sự kiện sắp tới''',
        'event_slogan': '''Tham gia vào các sự kiện bổ ích của chúng tôi''',
        'top_rating_instructors': '''Giảng viên hàng đầu''',
        'instructor_slogan': '''Cơ hội được hướng dẫn bởi các chuyên gia''',
        'latest_news': '''Tin tức mới nhất''',
        'news_slogan': '''Cập nhật những tin tức mới nhất''',
        'slogan1': '''Học theo tiến độ của riêng bạn''',
        'slogan1_content': '''''',
        'slogan2': '''Cộng đồng chia sẻ các cơ hội''',
        'slogan2_content': '''''',
        'footer_company': '''Tổ chức''',
        'footer_community': '''Cộng đồng''',
        'table_of_content': '''Mục lục''',
        'topics': '''Chủ đề''',
        'web_program': '''Lập trình web''',
        'mobile_program': '''Lập trình di động''',
        'embeded_program': '''Lập trình nhúng''',
        'network_program': '''Lập trình mạng''',
        'machine_learning': '''Học máy''',
        'support': '''Hỗ trợ''',
        'documentation': '''Tài liệu''',
        'forums': '''Diễn đàn''',
        'programmer': '''Lập trình viên''',
        'home_description': 'Học trực tuyến đề cập đến hướng dẫn được phân phối điện tử thông qua các ứng dụng và nền tảng đa phương tiện và Internet khác nhau. Nó được sử dụng thay thế cho các thuật ngữ khác như học tập dựa trên web, học tập điện tử, hướng dẫn có sự trợ giúp của máy tính và học tập dựa trên Internet.',
        'home_subscribe': 'Nhận thêm thông tin',
        'subscribe': 'Đăng ký ngay',
        }


def detectLanguage(request):
    languageDetected = supported_languages[0]
    pagePath = request.path
    if pagePath[-1] == '/': pagePath=pagePath[:-1]
    pagePath = pagePath.split('?')[0]
    pagePath = pagePath.split('#')[0]
    lastPath = pagePath.split('/')[-1]
    if lastPath in supported_languages[1:]:
        languageDetected = lastPath
    return languageDetected


def translated(requestOrLang,TranslateVariable):
    if requestOrLang in supported_languages:
        lang=requestOrLang
    else:
        lang = detectLanguage(requestOrLang)
    return translation_dictionary(lang)[TranslateVariable]


def localizeLink(request, link):
    lang=detectLanguage(request)
    if lang == supported_languages[0]: return link
    index1 = link.find('#')
    index2 = link.find('?')
    if index1 == -1 and index2 == -1: smallest_index = len(link)
    elif index1 == -1: smallest_index = index2
    elif index2 == -1: smallest_index = index1
    else: smallest_index = min(index1, index2)
    path = link[:smallest_index]
    if path[-1] == '/': path=path[:-1]
    return path+'/'+lang+link[smallest_index:]


from django.shortcuts import redirect as org_redirect
def redirect(request, to, *args, permanent=False, **kwargs):
    lang=detectLanguage(request)
    if lang in supported_languages[1:]:
        to=to+'_'+lang
    return org_redirect(to, *args, permanent=permanent, **kwargs)


from django.urls import path as org_path
def path(route, view, kwargs=None, name=None):
    if route == '':
        return [org_path('', view, kwargs, name),org_path('vi', view, kwargs, name+'_vi'),]
    if route[-1] == '/': route=route[:-1]
    return [org_path(route, view, kwargs, name),org_path(route+'/vi', view, kwargs, name+'_vi'),]


def langRef(path_ref):
    last=path_ref.split('/')[-1]
    if last in supported_languages:
        path_ref=path_ref[:-len(last)-1]
    result='<link rel="alternate" hreflang="en" href="'+addLinks(path_ref,'')+'" />\n'
    result+='<link rel="alternate" hreflang="vi" href="'+addLinks(path_ref,'vi')+'" />\n'
    result+='<link rel="alternate" hreflang="x-default" href="'+addLinks(path_ref,'')+'" />\n'
    return result


from django.urls import get_resolver
def translatedLinks(lang):
    names=[]
    for i in get_resolver().url_patterns:
        if hasattr(i, 'name'):
            if i.name:
                names.append(i.name)
    result = {}
    if lang == supported_languages[0]:
        for i in names:
            if i[-3:] not in ['_vi'] and names.count(i+'_vi'):
                result.update({i:i})
        return result
    for i in names:
        if names.count(i+'_'+lang):
            result.update({i:i+'_'+lang})
    return result


def languageMenu(request, lang):
    path = request.path
    remainder = request.get_full_path()[len(path):]
    selected = [' ', ' ']
    selected[supported_languages.index(lang)]=' selected '
    if supported_languages.index(lang):
        path=path[:-3]
    result = '<select id="languageMenu" class="form-select form-select-sm" aria-label=".form-select-sm example" style="width:150px; " onchange="window.location = this.value;">'
    if path == '/': path = ''
    if path =='':
        result += '<option'+selected[0]+'value="/'+remainder+'">English</option>'
    else:
        result += '<option'+selected[0]+'value="' + path + remainder +'">English</option>'
    result += '<option'+selected[1]+'value="' + path +'/vi'+remainder+'">Tiếng Việt</option>'
    result += '</select>'
    return result


from django.shortcuts import render as org_render
def render(request, template_name, context=None, *args, **kwargs):
    lang=detectLanguage(request)
    if context == None:
        context={}
    return org_render(request, template_name, {**context,
                                                **translation_dictionary(lang),
                                                'lang':lang,
                                                'languageReferences':langRef(request.build_absolute_uri()),
                                                'languageMenu':languageMenu(request, lang),
                                                'candyLink':translatedLinks(lang),
                                                }, *args, **kwargs)


def addLinks(*args):
    result=''
    for i in args:
        if result and result[-1]=='/':result=result[:-1]
        if i and i[-1]=='/':i=i[:-1]
        if i and i[0]=='/':i=i[1:]
        if result and i: result+='/'
        result+=i
    return result


def provideSitemap(request, add_pages=[], remove_pages=[], remove_paths=[]):
    from django.http import HttpResponse
    result='<?xml version="1.0" encoding="UTF-8"?>'+'\n'
    result+='<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+'\n'
    domain= request.build_absolute_uri()
    domain=domain.split('/')[0]+'//'+domain.split('/')[2]+'/'
    paths = []
    for i in get_resolver().url_patterns:
        if str(type(i))=="<class 'django.urls.resolvers.URLPattern'>":
            try:
                route=i.pattern._route
                route=route.split('<')[0]
                if not route == 'sitemap.xml':
                    if 'robots.txt' not in route:
                        paths.append(addLinks(domain,route))
            except: pass
    paths+=add_pages
    paths=list(dict.fromkeys(paths))
    for route in paths:
        removed_path = False
        for removal in remove_paths:
            if route[:len(removal)] == removal: removed_path = True
        if not removed_path and route not in remove_pages:
            result+='<url>'+'\n'
            result+='<loc>'+route+'</loc>'+'\n'
            result+='</url>'+'\n'
    result+='</urlset>'
    result= result.encode('utf-8')
    return HttpResponse(result, content_type='application/xml; charset=utf-8')


def sitemap(add_pages=[], remove_pages=[], remove_paths=[]):
    return [org_path('sitemap.xml', provideSitemap,{'add_pages' :add_pages,'remove_pages': remove_pages, 'remove_paths': remove_paths})]


