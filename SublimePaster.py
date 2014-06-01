import urllib.parse
import urllib.request

import sublime
import sublime_plugin

API_KEY = "cb6d789cca854a88c2442509c89adf6e"


class PasterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        content = ""
        for sel in self.view.sel():
            sublime.status_message(str(sel))
            content += self.view.substr(sel)

        sublime.status_message("Creating Paste!")
        
        syntax = self.view.settings().get('syntax')
        syntax = syntax.split("/")[-1].split(".")[0]
        print (syntax)

        self.paste(content, syntax)

    def paste(self, content, syntax):
        url = 'http://pastebin.com/api/api_post.php'
        values = {
                  'api_dev_key': API_KEY,
                  'api_paste_code': content,
                  'api_option': 'paste',
                  # 'api_paste_format': syntax
            }

        data = urllib.parse.urlencode(values).encode('utf-8')
        req = urllib.request.Request(url, data)
        try:
            response = urllib.request.urlopen(req)
            paste_url = response.read().decode('utf-8')
        except urllib.error.URLError as e:
            pass

        sublime.set_clipboard(paste_url)
        sublime.message_dialog("Paste link copied to Clipboard")
