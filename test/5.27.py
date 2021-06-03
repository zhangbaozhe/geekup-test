import serial

serial_6 = serial.Serial('/dev/cu.wchusbserial1440', 9600, timeout=0.1)

while True:
    if serial_6.in_waiting:
        readbuf = serial_6.read(serial_6.in_waiting)
        readbuf_str = str(readbuf)
        angle = ''
        for i in readbuf_str:
            if i.isdigit() or i == '.':
                angle += i
        angle = float(angle)
        print(angle)



        serial_6.write(bytes('adds', encoding='utf-8'))

    


            
