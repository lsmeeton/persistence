'''
Created on 17 Dec 2013

@author: lewis
'''
__metaclass__ = type
class ConnectedComponent(object):
    '''
    Class for defining connected components for persistence diagrams
    Initiates four class attributes:
    
    birth: Energy at which connected component is born
    death: Energy at which connected component dies
    eatenby: Connected component which current connected component is eaten by
    contents: List of minima indices contained in connected component
    '''


    def __init__(self, birth, min_id):
        '''
        Constructor
        '''
        self.birth = birth
        self.death = None
        self.eatenby = None
        self.contents = [min_id]
        self.size = 1
        
    def AddContents(self,m):
        '''
        Takes as argument list of minima indices, m, and adds them to contents
        '''
        self.contents.append(m)
        
if __name__ == '__main__':
    cc = ConnectedComponent(birth=0, min_id=1)
    print cc.__dict__