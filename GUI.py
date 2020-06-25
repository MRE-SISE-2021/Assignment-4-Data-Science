from tkinter import *
from tkinter import filedialog
import KMeansClustering
from tkinter import messagebox
import tkinter.font as tkFont


class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)
        # reference to the master widget, which is the tk window
        self.master = master
        # with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("K Means Clustering GUI")

        # allowing the widget to take the full space of the root window
        self.grid()

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        self.bool = False  # must do pre process first
        # create the file object)
        file = Menu(menu)

        # command it runs on event is client_exit
        file.add_command(label="Exit", command=self.client_exit)

        # added "file" to our menu
        menu.add_cascade(label="File", menu=file)

        vcmd = (self.master.register(self.check), '%s')
        Label(self.master, text="Enter Path").grid(row=0)
        self.labelBrowse = Entry(self.master, bd=5, width=70, validate="key", validatecommand=vcmd)
        self.frame1 = Frame(self.master)
        self.buttonBrowse = Button(self.master, text="Browse", command=lambda: self.fileDialog())
        self.labelBrowse.grid(row=0, column=1, columnspan=2)
        self.buttonBrowse.grid(row=0, column=3)

        """
        2 labels for Number of clusters k And Number of runs
        """
        Label(self.master, text="Number of clusters k").grid(row=1)
        Label(self.master, text="Number of runs").grid(row=2)
        self.e1 = Entry(self.master)
        self.e2 = Entry(self.master)
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)

        self.processBtn = Button(self.master, text="pre-process", command=lambda: self.preProcessFunc())
        self.clusterBtn = Button(self.master, text="cluster", command=lambda: self.kmeansModel())
        self.processBtn.grid(row=5, column=1)
        self.clusterBtn.grid(row=5, column=2)

        self.preprocess = None

    def showImg(self):
        fontStyle = tkFont.Font(family="Lucida Grande", size=20)
        Label(text="The output is", font=fontStyle).grid(row=6, column=2)
        img = PhotoImage(file=r"country_map.png")
        img1 = img.subsample(2, 2)
        Label(self.master, image=img1).grid(row=7, column=0,
                                            columnspan=2, rowspan=2, padx=5, pady=5)

        secondimg = PhotoImage(file=r"k-means_scatter.png")
        img2 = secondimg.subsample(2, 2)
        Label(self.master, image=img2).grid(row=7, column=5,
                                            columnspan=2, rowspan=2, padx=5, pady=5)

        mainloop()

    def client_exit(self):
        exit()

    def check(self, new_text):
        if not new_text:
            return True

    def fileDialog(self):
        f = filedialog.askopenfilename()
        self.labelBrowse.delete(0, END)
        self.labelBrowse.insert(0, f)
        print(self.labelBrowse.get())

    def preProcessFunc(self):
        # create preprocess
        print("Got The Data")

        path = self.labelBrowse.get()
        if path == "":
            messagebox.showinfo("Error", "You have to input path ")
        else:
            if path.endswith(".xlsx"):
                self.bool = True
                self.preprocess = KMeansClustering.Preprocess(path)
                # clean_na
                self.preprocess.clean_na()
                # normalize
                self.preprocess.standardization()
                # aggregate by country
                self.preprocess.aggregate_by_country()
                messagebox.showinfo("Pre-processing", "Preprocessing completed successfully!")
            else:
                messagebox.showinfo("Error", "You should Enter Path And Ends with xlsx !")

    def kmeansModel(self):
        print("build the model and Get Visualization")
        print("Number of clusters k : ", self.e1.get())
        print("Number of runs : ", self.e2.get())
        if self.e1.get() == "" or self.e2.get() == "":
            messagebox.showinfo("Error", "One of the parameters is missing ")
        else:
            if self.bool:
                if int(self.e1.get()) > 2 and int(self.e1.get()) < 165:
                    clustering = KMeansClustering.Clustering(self.preprocess.data_frame)
                    clustering.activate_k_means_algorithm(int(self.e1.get()), int(self.e2.get()))
                    clustering.create_scatter_generosity_social_support()
                    clustering.create_country_map()
                    messagebox.showinfo("clustering", "Clustering completed successfully!")
                    self.showImg()
                else:
                    messagebox.showinfo("clustering", "The K is wrong")

            else:
                messagebox.showinfo("Error", "Must first do pre-processing ")


root = Tk()
root.geometry("1000x600")
# creation of an instance
app = Window(root)
root.mainloop()
