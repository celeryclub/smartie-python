import argparse, serial, time, unicodedata

TTY_PATH = '/dev/ttyUSB0'
DELAY = 0.04

class Smartie(object):
  def __init__(self, path=TTY_PATH):
    self.lcd = serial.Serial(path, 9600)

    # Set custom char '0'
    # ser.write(chr(0xFE)+chr(0x4E)+0+'0x15 0x15 0x15 0x15 0x15 0x15 0x1f 0')

  def command(self, cmd):
    cmd_str = b''.join([b'\xFE'] + cmd)

    self.lcd.write(cmd_str)
    time.sleep(DELAY)

  def backlight_on(self):
    self.command([b'\x42', b'\x00'])

  def backlight_off(self):
    self.command([b'\x46'])

  def set_contrast(self, amount):
    self.command([b'\x50', chr(amount).encode()])

  def write_line(self, data, line=1):
    if line is None or line < 1 or line > 4:
      line = 1

    data = unicode(data)
    data = unicodedata.normalize('NFKD', data)
    data = data.encode('ascii', 'ignore')
    data = data.ljust(20)[:20]

    self.command([b'\x47', b'\x01', chr(line).encode(), data])

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-b', '--backlight')
  parser.add_argument('-c', '--contrast', type=int)
  parser.add_argument('-l', '--line', type=int)
  parser.add_argument('message', nargs='?')
  args = parser.parse_args()

  smartie = Smartie()

  if args.backlight == 'on':
    smartie.backlight_on()
  elif args.backlight == 'off':
    smartie.backlight_off()

  if args.contrast:
    smartie.set_contrast(args.contrast)

  if args.message:
    smartie.write_line(args.message, args.line)
