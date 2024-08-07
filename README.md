# HQ PCB

### Get PCB quotations within KiCad and order with a single click

HQ PCB plugin will help you:

- Extract key manufacturing parameters from your design
- Get real-time quotations from HQ PCB within KiCad
- Generate Gerber files and upload them to HQ PCB along with your personal board settings

Once the upload is complete, you can use the HQ DFM Gerber Viewer to double check your manufacturing files, adjust board parameters then add it to your HQ PCB cart directly.
![NextPCB Plugin](https://github.com/SYSUeric66/kicad-amf-plugin/blob/8318782634b7f8237bd4a650c37e4031e876e3a0/docs/amf.gif)

## Features

### Automatic parameter extraction

When launching the plugin, the following parameters will be extracted from your KiCad design:

- Layer count
- Board size (x,y)
- Board thickness
- Minimum trace width/spacing
- Minimum drill hole size

_Note: These parameters cannot be edited from the plugin as they are extracted directly from your KiCad design._

### Real-time quotations completely within KiCad

Click the "Update Price" button to get the latest pricing and lead time for your boards from HQ PCB.

You can modify other parameters (E.g. solder mask color, board quantity, etc.) at any time and re-quote the price with a click of a button. All the options are synced with [NextPCB](https://www.nextpcb.com/).

_Note: Some combinations are restricted (E.g. white silkscreen cannot be chosen with white solder mask)._

### One-click Gerber generation and sync to the order page

Click the "Place Order" button to generate Gerber and NC drill files and upload them straight to HQ PCB's order page along with your board parameters.

Everything is in sync, so no additional adjustments are required. Of course, you are free to change the settings on the website and then proceed to order.

The following regions are supported:

- China mainland [HQPCB](https://www.hqpcb.com/quote/)
- For regions out of China, please use NextPCB plugin. The features are identical.

## Installation

Download the latest release ZIP file from **reserved for package** then within KiCad, open the "Plugin and Content Manager" from the main window. Finally, install the ZIP file using "Install from File..." at the bottom of the window.
![image](https://github.com/HubertHQH/HQ-NextPCB/assets/125419974/97ef0ca3-380e-4f6f-a14b-6960271118fc)


## NextPCB

NextPCB is the overseas version of HQ PCB, supporting orders in Japan, Europe and U.S.A.

- Europe and the U.S.A : [NextPCB](https://www.nextpcb.com/pcb-quote)
- Japan:[JP.NextPCB](https://jp.nextpcb.com/pcb-quote#/pcb-quote/)

## HQ DFM

HQ DFM One-click analysis of over 20 design risk issues including open circuits, disconnected traces, line spacing, and width.
[华秋DFM](https://dfm.hqpcb.com/)
you can use the HQ DFM Gerber Viewer to double check your manufacturing files, adjust board parameters 


### About HQ PCB

HQ PCB specializes in reliable multilayer PCB manufacture and assembly, and like KiCad, our goal is to enable engineers to build tomorrow's electronics. HQ PCB is working with KiCad to provide smart tools to simplify the progression from design to physical product. With 3 major factories catering to prototyping, mass production and PCB assembly, and over 15 years of engineering expertise, HQ PCB believes our industrial experience will prove invaluable to KiCad users and the PCB design community.

We are a [KiCad Platinum Sponsor](https://www.nextpcb.com/blog/kicad-nextpcb-platinum-sponsorship).

## Credits
This project contains copies or makes use of other works. These works and their respective license and terms are:

[Bouni's kicad-jlcpcb-tools](https://github.com/Bouni/kicad-jlcpcb-tools) is under [MIT License](https://github.com/theacodes/kicanvas/blob/main/LICENSE.md)
