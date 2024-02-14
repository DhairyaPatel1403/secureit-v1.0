

import tkinter as tk

class PatternPassword(tk.Canvas):

    def __init__(self, show_pattern=False, show_numbers=False, max_length=9):

        super().__init__()

        if 1 < max_length > 9:
            #print('[*] Not aloud more than 9 as max_length')
            raise Exception('[*] Max length must be between 1 and 9')

        self.config(bg='grey', width=300, height=300)
        self.bind_all("<B1-Motion>", self.ShowInfo)
        self.bind_all("<ButtonPress-1>", self.ShowInfo)


        self.show_pattern = show_pattern
        self.show_numbers = show_numbers
        self.max_length = max_length

        self.pattern = tk.StringVar()
        self.pattern.set('Pattern Password: ')
        self.current_widget = None
        self.activeStub = tk.PhotoImage(file='stubActive.png')
        self.click_num = 0
        self.x1, self.y1, self.x2, self.y2 = None, None, None, None
        self.lines = []
        self.points = []

        self.SetupStubs()

    def AddLine(self, event):

        self.delete(self.lines[0])
        del self.lines[0]
        line = self.create_line(self.points, fill="white", arrow=tk.LAST, width=3)
        self.lines.append(line)

    def DrawLine(self, event, middleBounds):
       
        if self.click_num==0:
           self.x1=middleBounds[0]
           self.y1=middleBounds[1]
           self.click_num=1
           self.points.append(self.x1)
           self.points.append(self.y1)
        else:
           self.x2=middleBounds[0]
           self.y2=middleBounds[1]
           self.points.append(self.x2)
           self.points.append(self.y2)
           if len(self.lines) == 1:
               self.AddLine(event)
               return
           
           line = self.create_line(self.x1,self.y1,self.x2,self.y2, fill="white", width=3, arrow=tk.LAST, smooth=1, splinesteps=12)
           self.lines.append(line)

    def AddToPattern(self, number):

        self.pattern.set(f'Pattern Password: {self.pattern.get()[18:]}{str(number)}')

        if(number==475369821):
            print("Hi")

    def ActivateStub(self, number):

        self.itemconfig(self.stubs[number-1], image=self.activeStub)

    def ShowInfo(self, event):

        for stubNumber in list(self.stubs.values()):

            bound = self.bbox(stubNumber)
            x = [bound[0], bound[2]]
            y = [bound[1], bound[3]]
            middleBoundX = sum(x) / len(x)
            middleBoundY = sum(y) / len(y)
            middleBounds = [middleBoundX, middleBoundY]
            
            if bound[0] < event.x < bound[2] and bound[1] < event.y < bound[3]:

                widget = stubNumber     

                if self.current_widget != widget:
                    self.current_widget = widget
                    if len(self.pattern.get()) < (18+self.max_length) and str(self.current_widget) not in self.pattern.get()[18:]:
                        self.AddToPattern(self.current_widget)
                        self.ActivateStub(self.current_widget)
                        if self.show_pattern:
                            self.DrawLine(event, middleBounds)
                    
    def SetupStubs(self):

        x=20
        y=20

        self.stub = tk.PhotoImage(file='stub.png')
        self.stubs = {}

        for stubNum in range(9):

            stubButtonID = self.create_image(x,y,anchor=tk.NW,image=self.stub)

            x += 100

            if x == 320:
                y += 100
                x = 20

            self.stubs.update({stubNum: stubButtonID})
        
        if self.show_numbers:
            x=20
            y=20
            for stubNum in range(9):
                self.create_text(x+34, y+34, text=stubNum+1, fill="white", font=('Helvetica 15 bold'))
                x += 100

                if x == 320:
                    y += 100
                    x = 20

    def ClearPattern(self):

        self.pattern.set('Pattern Password: ')
        for stub in list(self.stubs.values()):
            #stub.config(image=self.stub)
            self.itemconfig(stub, image=self.stub)
        for line in self.lines:
            self.delete(line)
        self.click_num = 0
        self.points = []


if __name__ == '__main__':

    main = tk.Tk()
    main.geometry('500x500')
    main.config(bg='grey')

    title = tk.Label(main, text='Pattern Password', bg=main['bg'], fg='white', font=('Verdana Pro Light', 32, 'underline'))
    title.pack(fill=tk.X, pady=20)

    pattern = PatternPassword(show_pattern=True, show_numbers=False, max_length=9)
    pattern.pack()

    controlFrame = tk.Frame(main, bg='grey')
    controlFrame.pack_propagate(False)
    controlFrame.pack(padx=(50,0), pady=20, ipady=40, fill=tk.X, expand=1)

    passLabel = tk.Label(controlFrame, textvariable=pattern.pattern, font=('Verdana Pro Light', 18), bg='grey', fg='white')
    passLabel.pack(side=tk.LEFT)

    clearPattern = tk.Button(controlFrame, text='Clear', font=('Arial', 20), bg='grey', activebackground='grey', fg='white', activeforeground='white', bd=0, highlightthickness=0, command=pattern.ClearPattern)
    clearPattern.pack(side=tk.LEFT, padx=(20,0), ipadx=20, ipady=3)

    main.mainloop()


