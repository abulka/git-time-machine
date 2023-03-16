import wx.html

class MyFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title='Scrolling Text')

        self.html = wx.html.HtmlWindow(self)
        self.html.SetPage('<html><body><p>Some long text...Wandered of days might basked loathed scorching, to that finds nor evil dwelt the one will. Open of that to sorrow sins the power will had. Lines of men far mine ah, all concubines that where that sea but rhyme her venerable, long from one in ne long that consecrate he. Did climes befell he sun since strange know, now dear would were fabled not sadness misery, awake true partings suits the joyless of rake. And childe where could present florid dear the, that flow though shades given save. Lyres though for none fame and but of heralds, to bacchanals saw had ere to, change neer that land glee the crime. Their in little aisle and fountain come men sacred and. Can whom it from in know would brow not not, gild happy mirth condole alas, since fall suffice he that. His then would shameless strength most fly. Him condemned vulgar nor bliss. To from nor left formed in, strength where but to sullen but his talethis, save mine a rake was waste spent sun. Strength their hall departed the to of his.  hall sing the that, he one a companie wight and not like they of, in for. Sadipscing lorem erat sea tempor vero no invidunt sea et, ea accusam kasd sanctus eos est. Sed vero aliquyam clita sit, et labore elitr diam aliquyam kasd duo, sit est accusam sit duo erat erat sed kasd. Sea stet ea amet kasd ipsum vero magna, consetetur eirmod erat accusam et et erat elitr. Stet ipsum eirmod sadipscing accusam diam diam, vero erat tempor eos dolor takimata ipsum eos, eirmod diam sanctus et tempor dolore no kasd, voluptua sanctus et sadipscing erat nonumy consetetur accusam sadipscing, rebum lorem et ipsum at dolore magna, et rebum amet nonumy sadipscing sed sadipscing ipsum ipsum, sit takimata rebum rebum ipsum invidunt. Diam ipsum elitr takimata et sadipscing duo aliquyam. Eos gubergren et vero lorem nonumy diam lorem et, est voluptua diam et diam accusam sadipscing. Dolore erat invidunt ea amet ipsum et, dolore duo consetetur lorem nonumy sit nonumy. Kasd sit rebum aliquyam aliquyam takimata ea. Nonumy gubergren dolor amet takimata, clita sea duo lorem ut stet diam et diam kasd, dolor est kasd rebum dolor kasd et aliquyam, dolore at et invidunt duo, nonumy dolor ipsum et aliquyam dolores, ipsum consetetur sit sed amet elitr, accusam aliquyam et sadipscing est elitr at et.Magna vero at consetetur sit consetetur rebum tempor eirmod, et stet diam est sadipscing dolores stet dolor duo. Dolor lorem. </p></body></html>')
        self.html.Scroll(0, 5)  # Scroll to position (0, 500)

        self.Show()

app = wx.App()
frame = MyFrame(None)
app.MainLoop()
