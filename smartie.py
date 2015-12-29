import argparse, serial, time

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--backlight')
parser.add_argument('-c', '--contrast', type=int)
parser.add_argument('-l', '--line', type=int)
parser.add_argument('message', nargs='?')
args = parser.parse_args()

tty_path = '/dev/ttyUSB0'

lcd = serial.Serial(tty_path, 9600)
  # serial.EIGHTBITS,
  # serial.PARITY_NONE,
  # serial.STOPBITS_ONE,
  # timeout = 5,
  # rtscts = False)

  # lcd.open()
  # lcd.isOpen()

delay = 0.04

# Set custom char '0'
# ser.write(chr(0xFE)+chr(0x4E)+0+'0x15 0x15 0x15 0x15 0x15 0x15 0x1f 0')

def command(cmd):
  cmd_str = b''.join([b'\xFE'] + cmd)

  lcd.write(cmd_str)
  time.sleep(delay)

def backlight_on():
  command([b'\x42', b'\x00'])

def backlight_off():
  command([b'\x46'])

def set_contrast(amount):
  command([b'\x50', chr(amount).encode()])

def write_line(data, line=1):
  if line is None or line < 1 or line > 4:
    line = 1
  data = data.ljust(20)[:20]

  command([b'\x47', b'\x01', chr(line).encode(), data.encode()])


if args.backlight == 'on':
  backlight_on()
elif args.backlight == 'off':
  backlight_off()

if args.contrast:
  set_contrast(args.contrast)

if args.message:
  write_line(args.message, args.line)
