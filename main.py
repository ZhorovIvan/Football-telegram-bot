import configparser as cp

config = cp.ConfigParser()
config.read('config.ini')

print(config['TELEGRAM']['token'] == '1918073988:AAHaAem6Y4U_bko3SESMTxa8wvgjy51X2r4')