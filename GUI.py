"""
    Title: UI/UX
    File Name: GUI.py
    Author: Devanshu Gupta
    Language: Python
    Date Modified: 30-07-2020
    ##########################################################################################################
    # Description:
    #       Authentication based GUI file to test basic functionalities of the Recommender system.
    #       Files necessary : login.txt, song_id, file2.csv
    #                                                         • Rate the experience
    ##########################################################################################################
"""
import tkinter as tk
from tkinter import messagebox
import Recommender_v1
import pandas as pd

no=0

class authenticate:
    def __init__(self,root):
        self.root=root
        self.root.title('User Authentication')
        self.root.protocol("WM_DELETE_WINDOW", self.exit_func)
        self.new = 0
        self.login()
        self.done=0

    def login(self):
        if self.new:
            self.frame.destroy()
        self.root.geometry('300x180')
        self.lab = tk.Label(self.root, text='         ').grid(row=0, column=0)
        self.lab = tk.Label(self.root, text='         ').grid(row=1, column=0)

        frame = tk.LabelFrame(self.root,text='Login')
        frame.grid(row=1,column=1)

        label=tk.Label(frame,text='Username')
        label.grid(row=0,column=0,pady=5)
        self.username=tk.Entry(frame)
        self.username.grid(row=0,column=1,columnspan=10,padx=20)
        label1=tk.Label(frame,text='Password')
        label1.grid(row=1, column=0,pady=5)
        self.password=tk.Entry(frame,show='*')
        self.password.grid(row=1,column=1,columnspan=10,padx=20)
        btn1 = tk.Button(frame,text='Login', command=self.login_user)
        btn1.grid(row=2, column=0,pady=5,padx=10)
        btn2 = tk.Button(frame, text='New User', command=self.new_user)
        btn2.grid(row=2, column=1,columnspan=10)

        self.label3=tk.Label(self.root,text=' \(^_^)/ ')
        self.label3.grid(row=2,column=1,padx=5,pady=5)

        login=open('login.txt').read()
        self.log=eval(login)


    def login_user(self):
        if self.username.get() in self.log.keys():
            if self.password.get()==self.log[self.username.get()]:
                self.user=self.username.get().strip()
                self.username.delete(0,tk.END)
                self.password.delete(0, tk.END)
                self.root.destroy()
                self.done=1
            else:
                self.label3.config(text='~( ˘ o ˘ ~)   (~ ˘ o ˘ )~ \n Password does not match!')
        else:
            self.label3.config(text='( ⚆ - ⚆)  \n Username does not exist!')

    def new_user(self):
        self.new=1
        self.root.geometry('340x210')
        self.frame = tk.LabelFrame(self.root, text='Welcome')
        self.frame.grid(row=1, column=1)

        label = tk.Label(self.frame, text='Username')
        label.grid(row=0, column=0, pady=5)
        self.username = tk.Entry(self.frame)
        self.username.grid(row=0, column=1, columnspan=10, padx=20)
        label1 = tk.Label(self.frame, text='Password')
        label1.grid(row=1, column=0, pady=5)
        self.password = tk.Entry(self.frame)
        self.password.grid(row=1, column=1, columnspan=10, padx=20)
        label1 = tk.Label(self.frame, text='Confirm Password')
        label1.grid(row=2, column=0, pady=5)
        self.confirmpassword = tk.Entry(self.frame)
        self.confirmpassword.grid(row=2, column=1, columnspan=10, padx=20,pady=10)

        btn2 = tk.Button(self.frame, text='Create User', command=self.create_user)
        btn2.grid(row=3, column=2, padx=5,pady=5, columnspan=10)
        btn2 = tk.Button(self.frame, text='Login', command=self.login)
        btn2.grid(row=3, column=0)

        self.label3 = tk.Label(self.root, text=' \(^_^)/ ')
        self.label3.grid(row=2, column=1, padx=5, pady=5)


    def create_user(self):
        if self.username.get().strip() in self.log.keys():
            self.label3.config(text=' Username Taken. ')
            return
        if self.username.get().strip() == '':
            self.label3.config(text= 'Username cannot be empty!')
            return
        if self.password.get().strip() == '':
            self.label3.config(text='Password cannot be empty!')

        else:
            if self.password.get().strip() == self.confirmpassword.get().strip():
                self.log[self.username.get().strip()] = self.password.get().strip()
                self.user=self.username.get().strip()
                with open('login.txt', 'w') as f:
                    f.write(str(self.log))
                f.close()
                self.label3.config(text='User Created.')
                songs = pd.read_csv('file2.csv')

                users=pd.read_csv('users.csv',index_col='username')
                users.loc[self.user]=0
                users.to_csv('users.csv')
                with open('rating.txt', 'r') as f1:
                    text = f1.read()
                rating = eval(text)
                f1.close()
                with open('rating.txt', 'w') as f2:
                    rating[self.user] = []
                    f2.write(str(rating))
                f2.close()
                self.root.destroy()
            else:
                self.label3.config(text='Password fields do not match!')

    def exit_func(self):
        global no
        if self.done:
            self.root.destroy()
        else:
            ans = tk.messagebox.askyesno('Close!','Do you want to quit?')
            if ans==True:
                self.root.destroy()
                no=1
            else:
                self.label3.config(text=' ')
                return

    def run(self):
        self.root.mainloop()
        return self.user


class View:
    def __init__(self, root,username):
        self.root = root
        self.root.geometry('680x350')
        self.root.title('Recommender_GUI')
        self.root.protocol("WM_DELETE_WINDOW", self.exit_func)
        self.username = username

        label=tk.Label(root,text='Welcome')
        label.pack(padx=10,pady=10)

        self.all_songs=[]
        self.play_songs = []
        self.recommended_songs = []
        self.song_list()
        self.open_files()

    def song_list(self):
        Frame=tk.Frame(self.root)
        Frame.pack()

        searchFrame = tk.Frame(Frame)
        searchFrame.pack(side=tk.LEFT)
        self.slabel = tk.Text(searchFrame,height=8,width=20)

        scrollbar3 = tk.Scrollbar(searchFrame)
        scrollbar3.pack(side=tk.RIGHT,fill=tk.Y,padx=2)
        scrollbar3.config(command=self.slabel.yview)
        self.slabel.config(yscrollcommand=scrollbar3.set)
        self.slabel.pack(side=tk.BOTTOM,pady=10,padx=2)

        self.name_var = tk.StringVar
        self.search_bar = tk.Entry(searchFrame,text='enter artist or song',textvariable=self.name_var)
        self.search_bar.pack(side=tk.LEFT,expand=tk.YES)
        sbtn = tk.Button(searchFrame,text='Search',command=self.search)
        sbtn.pack(side=tk.LEFT)

        leftFrame=tk.Frame(Frame)
        leftFrame.pack(side=tk.LEFT)
        middleFrame = tk.Frame(Frame)
        middleFrame.pack(side=tk.LEFT)
        rightFrame = tk.Frame(Frame)
        rightFrame.pack(side=tk.LEFT)

        scrollbar = tk.Scrollbar(leftFrame)
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y,padx=5)
        scrollbar1 = tk.Scrollbar(middleFrame)
        scrollbar1.pack(side=tk.RIGHT,fill=tk.Y,padx=5)
        scrollbar2 = tk.Scrollbar(rightFrame)
        scrollbar2.pack(side=tk.RIGHT,fill=tk.Y,padx=5)


        self.label=tk.Label(leftFrame,text='All songs')
        self.label.pack()
        self.Lb = tk.Listbox(leftFrame,selectmode=tk.EXTENDED)
        self.Lb.pack()
        self.Lb.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.Lb.yview)

        btn = tk.Button(leftFrame, text='Remove', command= self.delete)
        btn.pack(side=tk.LEFT)
        btn = tk.Button(leftFrame, text='Add', command=self.add)
        btn.pack(side=tk.LEFT)

        self.label1 = tk.Label(middleFrame, text='Your playlist')
        self.label1.pack()
        self.Lb1=tk.Listbox(middleFrame,selectmode=tk.EXTENDED)
        self.Lb1.pack()
        self.Lb1.config(yscrollcommand=scrollbar.set)
        scrollbar1.config(command=self.Lb1.yview)

        btn1 = tk.Button(middleFrame, text='Save', command=self.save_playlist)
        btn1.pack(side=tk.LEFT)
        btn2 = tk.Button(middleFrame, text='Remove', command= self.remove)
        btn2.pack(side=tk.LEFT)
        btn_1 = tk.Button(middleFrame, text='Clear', command=self.clear)
        btn_1.pack(side=tk.LEFT)

        self.label2 = tk.Label(rightFrame, text='Recommended songs')
        self.label2.pack()
        self.Lb2 = tk.Listbox(rightFrame,selectmode=tk.EXTENDED)
        self.Lb2.pack()
        self.Lb2.config(yscrollcommand=scrollbar.set)
        scrollbar2.config(command=self.Lb2.yview)

        btn3 = tk.Button(rightFrame, text='Add',command=self.add_to_playlist)
        btn3.pack(side=tk.LEFT)
        btn4 = tk.Button(rightFrame, text='Recommend',command=self.recommend)
        btn4.pack(side=tk.LEFT)
        btn5 = tk.Button(rightFrame, text='Clear', command=self.clear_reco)
        btn5.pack(side=tk.LEFT)

    def open_files(self):
        with open('song_dict.txt') as song_dict:
            txt = song_dict.read()
        self.song_list = eval(txt)

        with open('rating.txt') as r:
            txt = r.read()
        self.rating = eval(txt)

        self.users=pd.read_csv('users.csv',index_col='username')
        self.df = pd.read_csv('file2.csv')
        print(self.users)

    def search(self):
        name = self.search_bar.get()
        name = name.lower().strip()
        if name=='':
            return
        self.Lb.delete(0, tk.END)

        name_ = name.replace(' ','_')

        for i in ['artist_1','artist_2','song']:
            df1 = self.df[self.df[i].str.contains(name) | self.df[i].str.contains(name_)]
            for ix,i in df1.iterrows():
                self.all_songs.append(i['song_id'])
                self.Lb.insert(tk.END,i['song'].replace('_',' '))
        if len(self.Lb.get(0,tk.END))==0:
            messagebox.showwarning('Not Found', 'We dont have them. Maybe try another name!')
            return

    def delete(self):
        s=self.Lb.curselection()
        s=sorted(s)
        for i in s[::-1]:
            self.all_songs.pop(i)
            self.Lb.delete(i)

    def remove(self):
        s = self.Lb1.curselection()
        s = sorted(s)
        for i in s[::-1]:
            self.play_songs.pop(i)
            self.Lb1.delete(i)

    def clear(self):
        self.Lb1.delete(0,tk.END)
        self.play_songs=[]

    def clear_reco(self):
        self.Lb2.delete(0,tk.END)
        self.recommended_songs=[]

    def add_to_playlist(self):
        playlist = list(self.Lb1.get(0,tk.END))
        selected_song = self.Lb2.curselection()
        selected_song = sorted(selected_song)
        artists=set()
        for i in selected_song:
            song = self.Lb2.get(i)
            if song not in playlist:
                self.play_songs.append(self.recommended_songs[i])
                self.Lb1.insert(tk.END,song)
        for i in selected_song[::-1]:
            self.Lb2.delete(i)
            self.recommended_songs.pop(i)
        print('Playlist:',self.play_songs)
        for i in self.play_songs:
            for j in self.df.iloc[i, 5:6]:
                if j=='0' or j==0:
                    continue
                j=j.replace('_',' ')
                artists.add(j)

        artists=set(artists)
        text='\n'.join(artists)

        self.slabel.delete('0.0',tk.END)

        self.slabel.insert(tk.INSERT,'Artists:\n')
        self.slabel.insert(tk.INSERT,text)

    def add(self):
        playlist = list(self.Lb1.get(0, tk.END))
        selected_song=self.Lb.curselection()
        selected_song = sorted(selected_song)
        flag=0
        artists=set()
        for i in selected_song:
            song = self.Lb.get(i)
            if str(song) not in playlist:
                self.Lb1.insert(tk.END,self.Lb.get(i))
                self.play_songs.append(self.all_songs[i])
            else:
                flag=1
        for i in selected_song[::-1]:
            self.Lb.delete(i)
            self.all_songs.pop(i)

        if flag:
            messagebox.showwarning("Warning", "Song already in list!")
        print('Playlist:',self.play_songs)
        for i in self.play_songs:
            for j in self.df.iloc[i, 5:6]:
                if j=='0' or j==0:
                    continue
                j=j.replace('_',' ')
                artists.add(j)

        artists=set(artists)
        text='\n'.join(artists)
        self.slabel.delete('0.0',tk.END)
        self.slabel.insert(tk.INSERT,'Artists:\n')
        self.slabel.insert(tk.INSERT,text)

    def recommend(self):
        playlist = self.Lb1.get(0,tk.END)
        playlist = list(playlist)
        if(len(playlist))<10:
            messagebox.showerror('Short','Select at least 10 songs')
            return
        current = self.recommended_songs
        self.rating[self.username].append(len(current))
        with open('rating.txt','w') as file:
            file.write(str(self.rating))

        playlist=playlist[-10:]
        recommendations = Recommender_v1.recommend(playlist,self.username)
        self.Lb2.delete(0,tk.END)
        self.recommended_songs=[]
        data = self.df.iloc[recommendations]

        for ix in range(data['song'].count()):
            if len(self.recommended_songs)>4:
                return
            i = data.iloc[ix]
            if i['song_id'] in self.play_songs:
                continue
            self.Lb2.insert(tk.END,i['song'].replace('_',' '))
            self.recommended_songs.append(i['song_id'])
        if len(self.recommended_songs)<5:
            tk.messagebox.showwarning('Warning!','Try different artists or songs.')

    def save_playlist(self):
        playlist = self.play_songs
        for i in playlist:
            self.users.loc[self.username][i] += 1
        self.users.to_csv('users.csv')

        
    def exit_func(self):
        result = messagebox.askyesno("(^_^)", "Do you want to quit?")
        if not result:
            return
        if len(self.play_songs)>9:
            ans=messagebox.askyesno('Save','Do you want to save playlist?')
            if ans:
                self.save_playlist()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


root1=tk.Tk()
obj1=authenticate(root1)
username=obj1.run()
if no==0:
    root = tk.Tk()
    obj = View(root,username)
    obj.run()