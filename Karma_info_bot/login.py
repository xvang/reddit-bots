
#The whole point of this file is that python27 uses "ConfigParser", and python34 uses "configparser"..... or something like that.
#This allows the script to run on all Python versions...I think...probably? At least 27 and 34. 
#The only difference between the try-except is the import statement. 
def login():

    try:
        import ConfigParser

        config = ConfigParser.ConfigParser()

        config.read('auth.ini')


        info = {}

        info['name'] = config.get('credentials', 'username')
        info['password'] = config.get('credentials', 'password')
        info['botname'] = config.get('credentials', 'botname')

        return info

    except:
        import configparser

        config = configparser.ConfigParser()
        
        config.read('auth.ini')
        
        info = {}

        info['name'] = config.get('credentials', 'username')
        info['password'] = config.get('credentials', 'password')
        info['botname'] = config.get('credentials', 'botname')

        return info        
