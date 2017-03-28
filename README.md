# pyburner
Small python script which helps re-render frames of the certain render server with Autodesk Backburner.

Sometimes when you render a 3dMax animation on multiple servers, if one server fails, you have to re-render only failed frames which was assinged to that server.
In this case you have to manually choose those frames and add them to render queue.
This little script automates this task, so you have to just export job file from backburner and then choose failed server. The result of the program run is a .bat file, which, when executed, adds new job to the Backburber queue with all failed frames.

`settings.ini` file has options for:
* 3dMax Version (year)
* Render Priority
* Render Server name
* Path to the folder with the 3dMax scene



# todo
* implement tkSimpleSialog.py for preferences [(_link_)](http://effbot.org/tkinterbook/tkinter-dialog-windows.htm)
* write full description
