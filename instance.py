import re
from datarec import information as info

class instance:
    def __init__(self, inputstring) -> None:
        self.input = inputstring
        self.identity = self.identify()
        self.result = self.catchinfo()
        if self.result != None:
            if self.identity['type'] in ['arxiv', 'doi']:
                self.message = instance.arxivdoiTextFormat(self.result, self.input)
            elif self.identity['type'] == 'youtube':
                self.message = instance.videoTextFormat(self.result)
            elif self.identity['type'] == 'quantamag':
                self.message = instance.quantamagTextFormat(self.result, self.input)
            else: 
                pass
        else:
            self.message = None
        
        
    def identify(self):
        # Regular expressions for each identifier/link pattern
        arxivIdentifier = r'\d{4}\.\d{4,5}(v\d+)?$'
        doiIdentifier   = r'10\.\d{4,9}/[-._;()/:A-Z0-9]+'
        arxivLink       = r'(?:https?://)?(?:www\.)?arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5}(v\d+)?)$'
        doiLink         = r'(?:https?://)?(?:www\.)?doi\.org/(\d{2}\.\d{4,9}/[-._;()/:A-Z0-9]+)$'
        youtubeVideo    = r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[A-Za-z0-9_-]+'
        quantaLink      = r'(?:https?://)?(?:www\.)?quantamagazine\.org/[-._;()/:A-Za-z0-9]+'
        youtubeshortlink = r'https?://youtu\.be/([A-Za-z0-9_-]+)'
        
        
        # Checking patterns using regex
        if re.match(arxivIdentifier, self.input):
            return {'input': self.input,
                    'type': 'arxiv'}
        
        elif re.match(doiIdentifier, self.input):
            return {'input': self.input,
                    'type': 'doi'}
        
        elif re.match(arxivLink, self.input):
            identifier = re.match(arxivLink, self.input).group(1)
            return {'input': identifier,
                    'type': "arxiv"}
        
        elif re.match(doiLink, self.input):
            identifier = re.match(doiLink, self.input).group(1)
            return {'input': identifier,
                    'type': "doi"}
        
        elif re.match(youtubeVideo, self.input):
            return {'input': self.input,
                    'type': 'youtube'}
        
        elif re.match(quantaLink, self.input):
            return {'input': self.input,
                    'type': 'quantamag'}
        elif re.match(youtubeshortlink, self.input):
            youtube_prefix = "https://www.youtube.com/watch?v="
            video_id = self.input.split("/")[-1]
            full_link = youtube_prefix + video_id
            return {'input': full_link, 
                    'type': 'youtube'}
        else:
            return {'input': self.input,
                    'type': "unknown"}
    def catchinfo(self):
        if self.identity['type'] == 'arxiv':
            self.result  = info.getArXiv(self.identity['input'])
        elif self.identity['type'] == 'doi':
            self.result  =info.getDOI(self.identity['input'])
        elif self.identity['type'] == 'youtube':
            self.result  =info.getYouTube(self.input)
        elif self.identity['type'] == 'quantamag':
            self.result  = info.getquanta(self.input)
        else:
            self.result = None
        return self.result
    @staticmethod
    def arxivdoiTextFormat(texts, link):
        textmessage = f"📄  *{texts['title']}*\n\n👤 {texts['authors']}\n\n🔗 {link}\n \n\n📌 {texts['subject']}\n\n📅 {texts['publishdate']}\n\n🪐@UTPhysicsArticles"
        return textmessage
    @staticmethod
    def videoTextFormat(video):
        textmessage = f"🎥  {video['title']}\n\n👤 {video['channel']}\n\n🔗 {video}\n\n🪐@UTPhysicsArticles"
        return textmessage
    @staticmethod
    def quantamagTextFormat(post, link):
        textmessage = f"📄  *{post['title']}*\n\n🔗 {link}\n\n▫️ {post['desc']}\n\n🪐@UTPhysicsArticles"
        return [textmessage, post['img']]

if __name__ == '__main__':
    while True:
        userinput = input("please give me a link:")
        user = instance(userinput)
        print(user.identity)
        print(user.result)