#!/usr/bin/env python3
 
#sys.exit(1) > Relais-Parameter fehlerhaft
#sys.exit(2) > falsches Betriebssystem
#sys.exit(3) > unzulässiges Kommando
#sys.exit(4) > serielle Schnittstelle fehlerhaft
#sys.exit(5) > Karte falsch angesprochen

 
import argparse
import serial
import textwrap
import sys
from sys import platform
from argparse import ArgumentParser, HelpFormatter
import serial.tools.list_ports


#https://stackoverflow.com/questions/3853722/how-to-insert-newlines-on-argparse-help-text
class RawFormatter(HelpFormatter):
    def _fill_text(self, text, width, indent):
        text = textwrap.dedent(text)          # Strip the indent from the original python definition that plagues most of us.
        text = textwrap.indent(text, indent)  # Apply any requested indent.
        text = text.splitlines()              # Make a list of lines
        text = [textwrap.fill(line, width) for line in text] # Wrap each line 
        text = "\n".join(text)                # Join the lines again
        return text

msg_info = '''Dieses Programm ist nur für mich zum Lernen ;)
Das Programm schaltet die Relais einer Conrad-Relais-Platine (Bestell-Nr. 197730) entsprechend des Parameters.

(c) Broken Leg Enterprises 05.07.2021


'''
msg_help = "Zeigt diese Hilfe an."
msg_bin= "binäre Darstellung der Relais; 00000001 = Relais 1; 00000011 = Relais 2+1; 10101010 = Relais 8+6+4+2 usw."
msg_command = "3 = alle Relais schalten; 6 = Relais einschalten ohne Änderung der restlichen Ausgänge; 7 = Relais ausschalten ohne Änderung der restlichen Ausgänge; 8 = Wechseln des Schaltzustands ohne Änderung der restlichen Ausgänge"

#parser = argparse.ArgumentParser(exit_on_error=False, description = msg_info, add_help=False, prefix_chars='-/', formatter_class=RawFormatter)
#unter Windows würde der Schrägstrich als Parameter-Trenner funktionieren, unter Linux wird der Pfad zur seriellen Schnittstelle angegeben und ich falle mit einem Fehler raus
parser = argparse.ArgumentParser(exit_on_error=False, description = msg_info, add_help=False, prefix_chars='-', formatter_class=RawFormatter)
parser.add_argument("-p",
#                    "--port",
#                    "/p",
#                    "/port",
                    dest='port',
                    help = "serielle Schnittstelle z.B. COM1",
                    required=True
                    )
parser.add_argument("-c",
#                    "--command", 
#                    "/c",
#                    "/command",
                    dest='command',
                    type=str,
                    help = msg_command,
                    required=True
                    )
parser.add_argument("-b",
#                    "--bin", 
#                    "/b",
#                    "/bin",
                    dest='bin',
                    type=str,
                    help = msg_bin,
                    required=True
                    )
parser.add_argument("-k",
#                    "--karte", 
#                    "/k",
#                    "/karte", 
                    dest='karte',
                    type=str,
                    help = "Nummer der Relais-Karte bei mehreren zusammengeschalteten Karten",
                    required=False
                    )
parser.add_argument('-h',
                    '--help',
#                    '/h',
#                    '/help',
#                    '/?',
                    action='help',
                    default=argparse.SUPPRESS,
                    help=msg_help
                    )


args = parser.parse_args()

#print('Quiet mode is %r.' % args.quiet)
#print('Verbose mode is %r.' % args.verbose)
#print('serielle Schnittstelle ist %r' % args.port)
#print('bin ist %r' % args.bin)
#print('Kartennummer: %r' % args.karte)


#Relais-Parameter auswerten
if args.bin == None:
    print ('\r\nEs wurden keine Relais-Parameter angegeben. \r\nBitte rufen Sie die Hilfe mit dem Parameter -h auf.\r\n')
    sys.exit(1)
elif len(args.bin) < 8:
    print ('\r\nDer Wert für die Relais-Anzahl ist zu kurz. \r\nBitte rufen Sie die Hilfe mit dem Parameter -h auf.\r\n')
    sys.exit(1)
elif len(args.bin) > 8:
    print ('\r\nDer Wert für die Relais-Anzahl ist zu lang. \r\nBitte rufen Sie die Hilfe mit dem Parameter -h auf.\r\n')
    sys.exit(1)
elif len(args.bin) == 8:
    # print ('genau richtig')
    bin_list_string=list(args.bin)
    bin_list_int = list(map(int, bin_list_string))
    # print('Liste 1:', bin_list_int)
    # print ('Count for 0 : ', bin_list_int.count(0))
    # print ('Count for 1 : ', bin_list_int.count(1))
    list_anzahl = bin_list_int.count(0) + bin_list_int.count(1)
    if list_anzahl == 8:
        # if bin_list_int[0] == 0:
            # print ('Relais 8 = Nicht Umschalten')
        # else:
            # print ('Relais 8 = Umschalten')
        # if bin_list_int[1] == 0:
            # print ('Relais 7 = Nicht Umschalten')
        # else:
            # print ('Relais 7 = Umschalten')
        # if bin_list_int[2] == 0:
            # print ('Relais 6 = Nicht Umschalten')
        # else:
            # print ('Relais 6 = Umschalten')
        # if bin_list_int[3] == 0:
            # print ('Relais 5 = Nicht Umschalten')
        # else:
            # print ('Relais 5 = Umschalten')
        # if bin_list_int[4] == 0:
            # print ('Relais 4 = Nicht Umschalten')
        # else:
            # print ('Relais 4 = Umschalten')
        # if bin_list_int[5] == 0:
            # print ('Relais 3 = Nicht Umschalten')
        # else:
            # print ('Relais 3 = Umschalten')
        # if bin_list_int[6] == 0:
            # print ('Relais 2 = Nicht Umschalten')
        # else:
            # print ('Relais 2 = Umschalten')
        # if bin_list_int[7] == 0:
            # print ('Relais 1 = Nicht Umschalten')
        # else:
            # print ('Relais 1 = Umschalten')
        bin_daten_int = bin_list_int[0]*128 + bin_list_int[1]*64 + bin_list_int[2]*32 + bin_list_int[3]*16 + bin_list_int[4]*8 + bin_list_int[5]*4 + bin_list_int[6]*2 + bin_list_int[7]*1
#        print('Daten-Wort:', bin_daten_int)
    else:
        print ('\r\nDa scheinen falsche Zeiche drin zu sein ;) \r\nBitte rufen Sie die Hilfe mit dem Parameter -h auf.\r\n')

#COM-Schnittstelle auswerten
if args.port == None:
    print ('\r\nEs wurde keine serielle Schnittstelle angegeben.\r\nBitte rufen Sie die Hilfe mit dem Parameter -h auf.\r\n')
    sys.exit(4)
else:
    port_list = sorted([comport.device for comport in serial.tools.list_ports.comports()])
#    print(port_list)
    if port_list.count(args.port) == 1:
        port_string = args.port
    else:
        print('\r\nDiese serielle Schnittstelle ist nicht im System vorhanden.\r\nBitte nutzen Sie eine der folgenden Schnittstellen: ', port_list, '\r\n')
        sys.exit(4)

#Kartennummer auslesen
if args.karte == None:
    print ('\r\nEs wurde keine Karte angegeben. \r\nIch gehe daher von nur einer Karte aus.\r\n')
    karte_int = 1
elif args.karte.isdigit():
        karte_int = int(args.karte)
else:
    print('\r\nDer Parameter für die Karte muss eine positive Zahl sein.\r\nBitte rufen Sie die Hilfe mit dem Parameter -h auf.\r\n')
    sys.exit(5)

#3 = alle Relais schalten
#6 = Relais einschalten ohne Änderung der restlichen Ausgänge
#7 = Relais ausschalten ohne Änderung der restlichen Ausgänge
#8 = Wechseln des Schaltzustands ohne Änderung der restlichen Ausgänge

if args.command == None:
    print ('\r\nEs wurde kein Befehl angegeben. \r\nBitte rufen Sie die Hilfe mit dem Parameter -h auf.\r\n')
elif args.command.isdigit():
    if args.command == '3':
#        print(3)
        command_int = 3
    elif args.command == '6':
#        print(6)
        command_int = 6
    elif args.command == '7':
#        print(7)
        command_int = 7
    elif args.command == '8':
#        print(8)
        command_int = 8
    else:
        print ('\r\nDieses Kommando wird nicht unterstützt. \r\nBitte rufen Sie die Hilfe mit dem Parameter -h auf.\r\n')
        sys.exit(3)
else:
    print('\r\nDer Parameter für das Kommando muss eine positive Zahl sein.\r\nBitte rufen Sie die Hilfe mit dem Parameter -h auf.\r\n')
    sys.exit(3)

#Checksumme des Setup-Frame berechnen
check_setup_int = 1 ^ karte_int ^ 1
setup_array = [1, karte_int, 1, check_setup_int]
setup_bytearray = bytearray(setup_array)


#Checksumme des Daten-Frame berechnen
check_frame_int = command_int ^ karte_int ^ bin_daten_int
frame_array = [command_int, karte_int, bin_daten_int, check_frame_int]
frame_bytearray = bytearray(frame_array)


ser = serial.Serial()

if platform == "linux" or platform == "linux2":
    ser.port = port_string
elif platform == "darwin":
    print("\r\nDieses Betriebssystem wird zur Zeit nicht unterstützt.\r\n")
    sys.exit(2)
elif platform == "win32":
    ser.port = port_string
ser.timeout = 0
ser.bytesize = 8
ser.parity = 'N'
ser.stopbits = 1
ser.xonxoff = False
ser.rtscts = False
ser.baudrate = 19200

#Setup der Karte
ser.open()
ser.write(setup_bytearray)
ser.close()

#schreiben des Befehls an die Karte
#wenn beide kurz hintereinander geschickt werden, reagiert die Karte nicht
ser.open()
ser.write(frame_bytearray)
ser.close()



