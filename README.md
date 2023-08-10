# HQ NextPCB Active Manufacturing
### Quote your board in KiCad and make your order with single click

Active manufacturing plugin will help you:
- Extract key manufacturing parameters from your design
- Get real time quotation from NextPCB within KiCad
- Generate gerber files and send it to NextPCB with your personal setting

Once the upload is complete, you can use HQ Gerber Viewer double check your files, adjust manufacturing parameters or add it to cart directly.

## Features
### Automatic parameter extraction
When launching the plugin, below parameters will be extracted from PCB:
- Layer count
- Board size(x,y)
- Board thickness
- Min trace width/clearance
- Min drilled hole
  
*Note: These parameters can not be edited as it is directly extracted from board.*

### Real time quotation Within KiCad
When you click "Update Price" button, plugin will show you the price and leading time for your board.

You can modify your requirement(Eg. silkscreen/solder mask color, board quantity etc) any time and re-quote the price by clicking the button. All the parameters are aligned with the setting on [NextPCB](https://www.nextpcb.com/).

*Note: Some combinations are restricted(Eg. white silkscreen should not match white soldermask).*

### Gerber generatation and sync to [NextPCB](https://www.nextpcb.com/) website with single click
When you click "Place Order" button, plugin will generate gerber/NC drill files at backend and post the gerber files to website along with your manufacturing setting.

So everything is in sync, no additional manual adjustments required. Of course, you are free to change the settings on the website and then make the real order.

## Installation
Download the latest release ZIP file from **reserved for package**, within KiCad open the "Plugin and Content Manager" from the main window. Install the ZIP file using "Install from File..." a the bottom of the window.
![image](https://github.com/HubertHQH/HQ-NextPCB/assets/125419974/97ef0ca3-380e-4f6f-a14b-6960271118fc)

### About HQ NextPCB
HQ NextPCB specializes in reliable multilayer PCB manufacture and assembly, and like KiCad, our goal is to enable engineers to build tomorrow's electronics. NextPCB is working with KiCad to provide smart tools to simplify the progression from design to physical product. With 3 major factories catering to prototyping, mass production and PCB assembly, and over 15 years of engineering expertise, NextPCB believes our industrial experience will prove invaluable to KiCad users and the PCB design community.

We are [KiCad Platinum Sponsor](https://www.nextpcb.com/blog/kicad-nextpcb-platinum-sponsorship).
