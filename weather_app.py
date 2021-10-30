from tkinter import *
from PIL import Image, ImageTk
import api
import requests
import math


class Weather:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("500x550+450+100")
        self.root.config(bg="#d1d1d1")

        # Icons
        self.search_icon = PhotoImage(file="assets/search.png")

        # Variable
        self.var_search = StringVar()

        title = Label(
            self.root,
            text="Weather App",
            font=("Rockwell", 30, "bold"),
            bg="#262626",
            fg="#fff",
        ).place(x=0, y=0, relwidth=1, height=60)
        lbl_city = Label(
            self.root,
            text="City Name",
            font=("Verdana", 15),
            bg="#033958",
            fg="#fff",
            anchor="w",
            padx=80,
        ).place(x=0, y=60, relwidth=1, height=40)
        txtarea = Entry(
            self.root,
            textvariable=self.var_search,
            font=("Verdana", 13),
            bg="lightyellow",
            fg="#262626",
        ).place(x=195, y=67, width=190, height=25)
        btn_search = Button(
            self.root,
            cursor="hand2",
            image=self.search_icon,
            bg="#033958",
            activebackground="#033958",
            bd=0,
            command=self.get_weather,
        ).place(x=390, y=67, width=25, height=25)

        # RESULTS
        self.lbl_city = Label(
            self.root,
            font=("Verdana", 15),
            bg="#d1d1d1",
            fg="green",
        )
        self.lbl_city.place(x=0, y=135, relwidth=1, height=25)

        self.lbl_icon = Label(
            self.root,
            font=("Verdana", 15),
            bg="#d1d1d1",
        )
        self.lbl_icon.place(x=0, y=200, relwidth=1, height=100)

        self.lbl_temp = Label(
            self.root,
            font=("Verdana", 20),
            bg="#d1d1d1",
            fg="#ad0000",
        )
        self.lbl_temp.place(x=0, y=350, relwidth=1, height=23)

        self.lbl_wind = Label(
            self.root,
            font=("Verdana", 20),
            bg="#d1d1d1",
            fg="#262626",
        )
        self.lbl_wind.place(x=0, y=420, relwidth=1, height=25)

        self.lbl_error = Label(
            self.root,
            font=("Verdana", 15),
            bg="#d1d1d1",
            fg="red",
        )
        self.lbl_error.place(x=0, y=450, relwidth=1, height=25)

        # FOOTER
        lbl_footer = Label(
            self.root,
            text="Made By - Lakshya Raikwal",
            font=("Futura", 15),
            bg="#004598",
            fg="white",
            pady=5,
        ).pack(side=BOTTOM, fill=X)

    def get_weather(self):
        api_key = api.api_key
        complete_url = f"http://api.openweathermap.org/data/2.5/weather?q={self.var_search.get()}&appid={api_key}"
        # cityname, countryname, icons, temperature_celcius, temperature_fahrenheit, wind

        if self.var_search.get() == "":
            self.lbl_city.config(text="")

            self.lbl_icon.config(image="")
            self.lbl_temp.config(text="")

            self.lbl_wind.config(text="")
            self.lbl_error.config(text="City Name Required!")

        else:
            result = requests.get(complete_url)
            if result:
                json = result.json()
                city_name = json["name"]
                country = json["sys"]["country"]
                icons = json["weather"][0]["icon"]
                temp_c = math.ceil(json["main"]["temp"] - 273.15)
                temp_f = math.ceil((json["main"]["temp"] - 273.15) * 9 / 5 + 32)
                wind = json["weather"][0]["main"]

                self.lbl_city.config(text=city_name + " , " + country)

                self.icon = Image.open(f"assets/icons/{icons}.png")
                self.icon = self.icon.resize((180, 180), Image.ANTIALIAS)
                self.icon = ImageTk.PhotoImage(self.icon)

                self.lbl_icon.config(image=self.icon)

                deg = "\N{DEGREE SIGN}"
                self.lbl_temp.config(
                    text=str(temp_c) + deg + "C | " + str(temp_f) + deg + " f"
                )

                self.lbl_wind.config(text=wind)

                self.lbl_error.config(text="")

                # print(city_name, country, icons, temp_c, temp_f, wind)

            else:
                self.lbl_city.config(text="")

                self.lbl_icon.config(image="")

                self.lbl_temp.config(text="")

                self.lbl_wind.config(text="")

                self.lbl_error.config(text="Invalid City Name")


root = Tk()
obj = Weather(root)
root.mainloop()
