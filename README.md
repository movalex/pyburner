# pyBurner
This small python script helps rerender frames of the failed render server with Autodesk Backburner.
## Description
Sometimes when you render a 3dMax animation on multiple servers, if one server fails, you have to re-render only failed frames which was assinged to that server.
In this case you have to manually choose those frames and add them to render queue.
This little script automates this task, so you have to just export job file from backburner and then choose failed server. The result of the program run is a .bat file, which, when executed, adds new job to the Backburber queue with all failed frames.

`settings.ini` file has options for:
* 3dMax Version (year)
* Render Priority
* Computer name with working render manager
* Path to the folder with the 3dMax scene

The contents of the output file is following:
`"C:\Program Files\Autodesk\3ds Max {year}\3dsmaxcmd.exe" "{path-to-max-file}.max" -frames:{comma separated frame numbers} -submit: {Backburner manager ip-address} -jobname: {job_name}_{server_name} -priority:{1-100}`

## Usage
1. Go to Backburner Queue Monitor and export report file to the Desktop by right clicking the job name
2. Launch the script and load that file by pressing <CTRL+O> or file->open
3. You will be provided with the list of servers involved in the render job. Choose one server that failed.
4. Click 'run' button (or press Space button), and choose .max scene you want to rerender. Defauls path to look .max files for is C:/%userprofile%/Documents/. You can override this in `config.ini` file in `path` option. For network path just use regular UNC (`\\computername\sharedFolder\resource`) path.
5. If the `open result` checkbutton is checked, the folder with .bat file will be opened. 
6. When you run this .bat file, new job should appear in Backburner monitor. Job name is inherited from original job plus failed server name (Ex: `neon_v09_render1`)    
7 Since the script does not currently support several server submission, in case you have more than one server failed, just repeat steps 2-5. It is really fast after all.