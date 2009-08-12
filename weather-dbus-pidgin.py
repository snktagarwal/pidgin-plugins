#The MIT License

#Copyright (c) 2009 Sanket Agarwal( mailto: snktagarwal@gmail.com )

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.



import dbus, gobject
from dbus.mainloop.glib import DBusGMainLoop

#set the basic variables
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")

#test it
#current_sm=purple.PurpleSavedstatusGetCurrent()
#print purple.PurpleSavedstatusGetMessage(current_sm)

def get_weather_report():
	""" To be called at fixed intervals of say 2-3 hours, the obtained information should be parsed into a final string to be passed to the status message update"""

	import urllib2
	from xml.dom import minidom
	
	#this stream is 'Jaipur' Specific, change the INXX0059 for local effects
	weather_stream=urllib2.urlopen('http://xoap.weather.com/weather/local/INXX0071?cc=*&link=xoap&dayf=5&prod=xoap&unit=m&par=1120014083&key=d5a6e28837a93517') 

	#parse the stream
	xml_weather_parse=minidom.parse(weather_stream)
	#find the required info by searching for the elements!
	
	

	#take the current condition, tag <cc>
	cc_tag=xml_weather_parse.getElementsByTagName('cc')
	cc_data=cc_tag[0] #Returns only one tag neways
	
	#The order of our data shall be, <lsup>, <obst>, <tmp>, <flik>, <wind><s>, <hmid>
	
	location_data=cc_data.getElementsByTagName('lsup')[0].childNodes[0].nodeValue
	place = cc_data.getElementsByTagName('obst')[0].childNodes[0].nodeValue
	
	temp = cc_data.getElementsByTagName('tmp')[0].childNodes[0].nodeValue
	
	feels_like = cc_data.getElementsByTagName('flik')[0].childNodes[0].nodeValue
	humidity = cc_data.getElementsByTagName('hmid')[0].childNodes[0].nodeValue
	weather_list=[location_data, place, temp, feels_like, humidity]
	return weather_list
	
	


def set_sm_to_weather():
	current_sm=purple.PurpleSavedstatusGetCurrent()
	
	#format the message to be printed
	
	weather_list=get_weather_report()
	report="WEATHER ONLINE\nPLACE: "+ str(weather_list[1])+"\nDETAILS AS PER: "+ str(weather_list[0])+"\nTEMPRATURE: "+ str(weather_list[2])+" deg cel\nFEELS LIKE: "+ str(weather_list[3])+" deg cel\nHUMIDITY: "+str(weather_list[4])+"%"
	
	#Add the PLUGIN INFORMATION
	
	report+="\n\n\n\n\n\n\n\nThis is a DBUS Script in Python, it fetches information from weather.com\nAuthor: Sanket Agarwal\nEMAIL: snktagarwal@gmail.com\n Code: http://maillist-cse.iitkgp.ernet.in/kgp/cab/8/"
	
	purple.PurpleSavedstatusSetMessage(current_sm,report)
	purple.PurpleSavedstatusActivate(current_sm)

if __name__ == '__main__':
	import time
	while(True):
		set_sm_to_weather()
		time.sleep(1800)
		print "here we go"
	
