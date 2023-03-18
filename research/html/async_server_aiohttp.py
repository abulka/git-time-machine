import string
import random
import urllib.parse
import wx
import asyncio
from wxasync import AsyncBind, WxAsyncApp
import aiohttp
from aiohttp import web
import wxasync
import wx.html2  # modern supports css and javascript

import wx
import wx.html2


def generate_sentence():
    words = ["Lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit,", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua.", "Ut", "enim", "ad", "minim", "veniam,", "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea", "commodo",
             "consequat.", "Duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate", "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur.", "Excepteur", "sint", "occaecat", "cupidatat", "non", "proident,", "sunt", "in", "culpa", "qui", "officia", "deserunt", "mollit", "anim", "id", "est", "laborum."]
    sentence = ""
    for i in range(random.randint(5, 15)):
        sentence += words[random.randint(0, len(words)-1)] + " "
    return sentence[:-1] + "."


def lorem_paragraph():
    paragraph = ""
    for i in range(random.randint(3, 10)):
        paragraph += generate_sentence() + " "
    return paragraph[:-1]


class TestFrame(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title="Async Server Example")
        # make the frame big enough to see the browser
        self.SetSize((800, 600))

        # create a panel and sizer
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(sizer)

        # create a button
        self.button = wx.Button(panel, label="/")
        sizer.Add(self.button, 0, wx.ALL | wx.CENTER, 5)

        # create a button
        self.button_hello = wx.Button(panel, label="/hello")
        sizer.Add(self.button_hello, 0, wx.ALL | wx.CENTER, 5)

        # create an additional button
        self.button_html = wx.Button(panel, label="Load HTML")
        sizer.Add(self.button_html, 0, wx.ALL | wx.CENTER, 5)

        # another button to call randhtml
        self.button_randhtml = wx.Button(panel, label="Load Random HTML")
        sizer.Add(self.button_randhtml, 0, wx.ALL | wx.CENTER, 5)

        sizer2 = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer2, 1, wx.EXPAND)

        # create a text control to display the results
        self.text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        sizer2.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        # add web browser
        self.html = wx.html2.WebView.New(panel)
        sizer2.Add(self.html, 1, wx.EXPAND | wx.ALL, 5)

        # set the sizer for the panel
        panel.SetSizer(sizer)

        # make the browser the same size as the TextCtrl
        self.html.SetSize(self.text_ctrl.GetSize())

        # bind the button click event to a coroutine
        wxasync.AsyncBind(wx.EVT_BUTTON, self.on_button_click, self.button)
        wxasync.AsyncBind(
            wx.EVT_BUTTON, self.on_button_click_hello, self.button_hello)
        wxasync.AsyncBind(
            wx.EVT_BUTTON, self.on_button_click_html, self.button_html)
        wxasync.AsyncBind(
            wx.EVT_BUTTON, self.on_button_click_randhtml, self.button_randhtml)

    async def on_button_click(self, event):
        # use aiohttp to fetch some JSON data
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8080/') as response:
                data = await response.text()

        # update the text control with the data
        self.text_ctrl.SetValue(str(data))

    async def on_button_click_hello(self, event):
        # use aiohttp to fetch some JSON data
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8080/hello') as response:
                data = await response.text()

        # update the text control with the data
        self.text_ctrl.SetValue(str(data))

    async def on_button_click_html(self, event):
        # load a dummy HTML page
        # self.html.LoadURL("https://www.example.com")

        rand_word = ''.join(random.choices(string.ascii_lowercase, k=5))
        url = f"https://www.google.com/search?q={rand_word}"
        self.html.LoadURL(url)

    async def on_button_click_randhtml(self, event):
        self.html.LoadURL("http://localhost:8080/randhtml?num_paragraphs=5")


async def main():
    # start the aiohttp server
    async def handle(request):
        name = request.match_info.get('name', "Anonymous")
        text = "Hello, " + name
        return web.Response(text=text)

    async def randhtml(request):
        num_paragraphs = int(request.query.get('num_paragraphs', 1))
        html = "<html><body>"
        for i in range(num_paragraphs):
            html += f"<p> {i} " + lorem_paragraph() + "</p>"
        html += "</body></html>"
        return web.Response(text=html, content_type='text/html')

    app = web.Application()
    app.add_routes([
        web.get('/randhtml', randhtml),
        web.get('/', handle),
        web.get('/{name}', handle),
    ]
    )

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()

    # start the wxPython app
    app = WxAsyncApp()
    frame = TestFrame()
    frame.Show()
    app.SetTopWindow(frame)
    await app.MainLoop()

    # shutdown the server
    await runner.cleanup()

asyncio.run(main())
