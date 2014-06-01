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

        name = self.view.file_name().split("/")[-1]
        syntax = self.view.settings().get('syntax')
        syntax = syntax.split("/")[-1].split(".")[0]
        print (syntax)

        self.paste(content, name, syntax)

    def paste(self, content, name, syntax):
        url = 'http://pastebin.com/api/api_post.php'
        values = {
                  'api_dev_key': API_KEY,
                  'api_paste_code': content,
                  'api_option': 'paste',
                  'api_paste_format': syntax
            }
        if name is not None: values['api_paste_name'] = name

        data = urllib.parse.urlencode(values).encode('utf-8')
        req = urllib.request.Request(url, data)
        try:
            response = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                sublime.error_message(
                    'SublimePaster failed to reach a server, reason: '+e.reason)
            elif hasattr(e, 'code'):
                sublime.error_message(
                    'Server sent an error: '+e.code)
        else:
            paste_url = response.read().decode('utf-8')
            sublime.set_clipboard(paste_url)
            sublime.status_message("Paste link copied to Clipboard")

        
