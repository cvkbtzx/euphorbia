#-*- coding:utf-8 -*-

## License: Public domain


import euphorbia


#------------------------------------------------------------------------------

class HelloWorld(euphorbia.Plugin):
    """Test plugin."""
    
    def __init__(self):
        euphorbia.Plugin.__init__(self)
    
    def activate(self):
        print "Hello!"
        print "This is the application's main instance:", self.app
    
    def deactivate(self):
        print "Bye!"


#------------------------------------------------------------------------------


