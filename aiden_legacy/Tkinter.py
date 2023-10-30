# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 13:25:28 2023

@author: ahuss
"""

#things to install prior to running code googlemap and numpy libraries
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
# import ttkbootstrap as ttk # install later
import googlemaps
import requests
import numpy as np

#Google authentication process
API_KEY = 'AIzaSyCfXPRg8mKI7m9N0XxyKNmMRVcaIqKkIK0'
url = "https://maps.googleapis.com/maps/api/staticmap?"

#Local image file location. Comment out my local path and add yours underneath
file_path = 'C:\\Users\\ahuss\\.spyder-py3\\testimage_new.png'
#file_path =

#Adjust this later on for the gps code using Serial or I2C libraries
lat = [0.0]
long = [0.0]
GPS_array = np.zeros((1000,2))


#Creates string for Google API connection
center = ['center='+str(lat[0])+','+str(long[0])]

#function for converting lat and long pixel values
#this will only work with high zoom values (5 or greater)
def convertGPS(x, y):
    parallelMult = np.cos(lat[0] * np.pi / 180)
    degPerPixelX = 360 / np.power(2, current_zoom_value.get() + 8)
    degPerPixelY = 360 / np.power(2, current_zoom_value.get() + 8) * parallelMult
    pointLat = lat[0] - degPerPixelY * (y - 600/2)
    pointLong = long[0] + degPerPixelX * (x - 600/2)
    return (pointLat, pointLong)

#function to retrieve the current value of a slider
def get_value():
    return'{:.0f}'.format(current_zoom_value.get())
    
#function to get the pixel information for the sub_window
pixel_info = None
def get_pixel(event):
    global pixel_info
    x = event.x
    y = event.y
    data_written = False
    for i in range(len(GPS_array)):
        if GPS_array[i,0]==0 and GPS_array[i,1]==0 and y<=600:
            (GPS_array[i,0], GPS_array[i,1]) = convertGPS(x, y)
            data_written = True
            print(GPS_array[i])
        if (GPS_array[i,0], GPS_array[i,1]) == convertGPS(x, y) and data_written==True:
            break
        
    

#function for when the slider is moved to change display value
def zoom_slider_changed(event):
    zoom_value.configure(text = get_value())
    
#function for calling gps location
def get_gps():
    r = requests.get(url+center[0]+'&zoom='+str(zoom_value.cget('text'))+'&size=600x600&scale=1&markers=color:red%7Clabel:Start%7C'+str(lat[0])+','+str(long[0])+\
                     '&maptype=hybrid&key='+API_KEY+'&sensor=false')
    #Saves map image to local drive
    f = open(file_path,'wb')
    f.write(r.content)
    f.close()
    current_new_location = ImageTk.PhotoImage(Image.open(file_path))
    photo.configure(image = current_new_location)
    photo.image=current_new_location
    
def open_location_image():
    #Create a sub window when button is clicked
    sub_window = tk.Toplevel()
    sub_window.title('GPS Location')
    sub_window.geometry('600x780')
    #Return pixel information using the left mouse button
    sub_window.bind('<Button-1>', get_pixel)
    #Create image of location into sub_window
    location_photo = ttk.Label(master=sub_window, image=photo.image)
    location_photo.pack(side='top', anchor='nw')
    #Create exit button to close window
    close_button = ttk.Button(master=sub_window, text='Close', command=sub_window.destroy)
    close_button.pack(side='top', anchor='n', pady=50)
    sub_window.mainloop()

def submit_gps():
    try:
        lat[0]=(float(lat_var.get()))
        long[0]=(float(long_var.get()))
        center[0] = 'center='+str(lat[0])+','+str(long[0])
        lat_var.set("")
        long_var.set("")
    except Exception as ex:
        print(ex)
    
#Window for widgets
main_window = tk.Tk()
main_window.title('User Interface')
main_window.geometry('1920x980')


#Frame style initialization used to help visualize the location of the frames
#frame_style = ttk.Style()
#frame_style.configure('TFrame', background='blue')

#Frame for option widgets
window_one = ttk.Frame(master=main_window, width=1020, height=980, style='TFrame')
window_one.pack(side='left',anchor='nw')

#Widgets for the slider in main window
zoom_label = ttk.Label(master=window_one, text='Zoom', font='Calibri 16 bold underline')
zoom_label.pack(side='top', anchor='n', padx=20)
#Widget for zoom slider
current_zoom_value = tk.DoubleVar()
zoom_slider = ttk.Scale(master=window_one, from_=1, to=20, length=325,
                        orient='horizontal', command=zoom_slider_changed, variable = current_zoom_value)
zoom_slider.set(1)
zoom_slider.pack(side='top', anchor='n', padx=10)
#Widget for displaying the slider bars value
zoom_value = ttk.Label(master=window_one, text=get_value(), font='Calibri 16')
zoom_value.pack(side='top', anchor='n', padx=20)

#Widget for dropdown label
path_label = ttk.Label(master=window_one, text='Select path profile', font='Calibri 16 bold underline')
path_label.pack(side='top', anchor='n', padx=10, pady=(10,0))
#Widget for dropdown selection menu
path_selected = tk.StringVar()
path_profile = ttk.OptionMenu(window_one, path_selected, "- Select -", 'Direct', 'Least distance travelled', 'Smooth')
path_profile.config(width=50)
path_profile.pack(side='top', anchor='n', padx=10, pady=10)

#Widget for latitude and longitude entry
entry_label = ttk.Label(master=window_one, text='GPS location', font='Calibri 16 bold underline')
entry_label.pack(side='top', anchor='n', padx=20)
#Create latitude widgets
lat_var = tk.StringVar()
lat_label = ttk.Label(master=window_one, text='Latitude:', font='Calibri 16')
lat_label.pack(side='top', anchor='n',padx=10, pady=10)
lat_entry = ttk.Entry(master=window_one, textvariable = lat_var, font='Calibri 16')
lat_entry.pack(side='top', anchor='n', padx=10)
#create longitude widgets
long_var = tk.StringVar()
long_label = ttk.Label(master=window_one, text='Longitude:', font='Calibri 16')
long_label.pack(side='top', anchor='n', padx=10, pady=10)
long_entry = ttk.Entry(master=window_one, textvariable = long_var, font='Calibri 16')
long_entry.pack(side='top', anchor='n', padx=10)
#submit lat and long values widget
submit_button = ttk.Button(master=window_one, text='Submit', command=submit_gps)
submit_button.pack(side='top', anchor='n', padx=20)


#widget for display window of location
current_location = ImageTk.PhotoImage(Image.open(file_path))
window_two = ttk.Frame(master=main_window, width=900, height=1080)
window_two.pack(side='right', anchor='n', padx=10)

#Widget for labeling current location
location_label = ttk.Label(master=window_two, text='Current location', font='Calibri 16 bold underline')
location_label.pack(side='top', anchor='n')

#Widget for selecting gps location spots
select_gps = ttk.Button(master=window_two, text='Select GPS points', command=open_location_image)
select_gps.pack(side='top', anchor='n')

#widget for displaying location image
photo = ttk.Label(master=window_two, image=current_location)
photo.pack(side='top',anchor='n',pady=10)
photo.configure(image = current_location)
photo.image = current_location

#widget to refresh location image
refresh_button = ttk.Button(master=window_two, text='Refresh', command=get_gps)
refresh_button.pack(side='bottom',anchor='s', pady=10)

#input_frame = ttk.Frame(master = window)
entry_int = tk.IntVar()
#entry = ttk.Entry(master = input_frame, textvariable = entry_int)
#button = ttk.Button(master = input_frame, text = 'Whatever', command = convert)
#entry.grid(row=0,column=0)
#button.grid(row=0,column=1)
#input_frame.grid(row=1,column=0)

output_string = tk.StringVar()
#output_label = ttk.Label(master = window, text = 'Output', font = 'Calibri 24', textvariable = output_string)
#output_label.grid(row=2,column=0)


main_window.mainloop()