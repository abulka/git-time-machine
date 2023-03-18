import wx
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
import asyncio
import time
import wxasync
import asyncio
import aiohttp

class TestFrame(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title="Async Server Example")
        
        # create a panel and sizer
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        
        # create a button
        self.button = wx.Button(panel, label="Get Data")
        sizer.Add(self.button, 0, wx.ALL | wx.CENTER, 5)
        
        # create a text control to display the results
        self.text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        sizer.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        
        # bind the button click event to a coroutine
        wxasync.AsyncBind(wx.EVT_BUTTON, self.on_button_click, self.button)

    async def on_button_click(self, event):
        # use aiohttp to fetch some JSON data
        async with aiohttp.ClientSession() as session:
            async with session.get('https://jsonplaceholder.typicode.com/posts/1') as response:
                data = await response.json()
                
        # update the text control with the data
        self.text_ctrl.SetValue(str(data))

async def main():            
    app = WxAsyncApp()
    frame = TestFrame()
    frame.Show()
    app.SetTopWindow(frame)
    await app.MainLoop()


asyncio.run(main())
