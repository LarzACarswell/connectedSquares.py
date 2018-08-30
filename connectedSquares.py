"""
Python 2.7 script that finds the largest number of connected squares in a grid. Sorry for the messy declarations! It's just a prototype.
Creates a "grid" of objects with x,y, and color attributes. Each cell is created with basic x,y, and color attributes.
Next, regions are created by recursively finding each cell with neighbors of the same color until no surrounding colors are matched
Finally, the region with the most members is highlighted.
Note that pygame is only used to display the grid and highlighted squares
"""
import pygame
from math import sqrt
sw,sh=700,700
visited=[]
size = [sw, sh]
screen = pygame.display.set_mode(size)
regions={}
class counter():
    def __init__(self):
        self.current=0
    def inc(self):
        self.current+=1
adder=counter()
class noise():                                                   #generates the "grid" by creating hei rows of length wid (it's just a list of lists)
    def __init__(self,wid,hei):
        self.width=wid
        self.height=hei
        self.colors=[(185,25,25),(25,185,25),(25,25,185)]        #red, green, blue
        self.pixels=[]                                           #this stores every [x,y,[color]]
    def generate(self):
        from random import randint
        for i in range(0,self.width):                            #this is our Y value
            self.pixels.append([])
            for j in range(0,self.height):                       #this is our X value
                color=self.colors[randint(0,len(self.colors)-1)] #random color
                position = [j*sw/self.width, i*sh/self.height]   #current square for drawing only
                size = [sw/self.width,sh/self.height]            #coef. for scaling
                s=pygame.display.get_surface()                   #new surface to fill the square
                r = pygame.Rect(position[0],position[1], size[0]+1,size[1]+1) #boundaries of the drawn square
                s.fill(color,r)                                  #fill in the boundaries
                self.pixels[i].append([j,i,list(color)])         #add this color to our list
                pygame.display.update()                          #update the surface to display the square
        return self.pixels

class cell():
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.color=color
        self.neighbors=[]                                                #every surrounding neighbor
        self.sameNeighbors=[]                                            #every neighbor with the same color

    def getNeighbors(self,cellList):
        for row in cellList[self.y-(self.y!=0):self.y+1+(self.y!=(len(cellList)-1))]: #abusing how Python treats booleans to find horizontal and vertical neighbors
            for loc in row[self.x-(self.x!=0):self.x+1+(self.x!=(len(row)-1))]: 
                if loc!=self:                                            #we don't want to compare ourself to ourself
                    d=sqrt((loc.x-self.x)**2+(loc.y-self.y)**2)          #we identify only the horizontal and vertical neighbors by their distance
                    if d<=1:
                        self.neighbors.append(loc)
                        if len(self.neighbors)==4:                       #dumb optimization technique, but no cell can have more than 4 neighbors (we exclude diagonals)
                            return
                    
    def checkNeighbors(self,depth=0):                             #identifies neighboring cells with matching colors
        visited.append([self.x,self.y])
        if len(self.neighbors)==0:                                #make sure the call getNeighbors before calling checkNeighbors
            print "cell [%s, %s, (%s)] did not have any neighbors set prior to this call"%(self.x,self.y,self.color)
        else:
            for n in self.neighbors:
                if [n.x,n.y] not in visited:
                    if n.color==self.color:
                        self.sameNeighbors.append(n)
                        if regions.has_key(adder.current):        #if our current region exists in the dictionary
                            if self not in regions[adder.current]:#add this object if we haven't already
                                regions[adder.current].append(self)
                            regions[adder.current].append(n)      #add the next object
                        else:                                     #create new region and add n to it
                            regions[adder.current]=[self,n]
                        n.checkNeighbors(depth+1)                 #check the next object's neighbors
                    else:
                        continue                                  #pass this object if its color is not the same as ours
                else:
                    continue                                      #pass this object if we've already visited it
            if len(regions)!=0:
                if regions.has_key(adder.current) and depth==0:
                    adder.inc()
            return
if __name__=="__main__":
    
    pygame.init()
    lengthSq=20                                                   #right now, our grid is a square matrix
                                                                  #create rows and columns with random colors
    canvas = noise(lengthSq,lengthSq) 
    pixls=canvas.generate()
    
    cells=[]                                                      #list of objects
    for i,row in enumerate(pixls):                                #iterate through each pixel. pixel = [x,y,[r,g,b]]
        cells.append([])                                          #Construct the list the same way we did with the pixels          
        for pixel in row:
            cells[i].append(cell(pixel[0],pixel[1],tuple(pixel[2]))) #add this cell's [x,y,color] to the list
    for row in cells:                                             #identify neighbors for each cell
        for c in row:
            c.getNeighbors(cells)
    for row in cells:                                             #identify matching colored neighboring cells
        for cel in row:
            cel.checkNeighbors()
    
    lengths={k:len(value) for k,value in regions.items()}         #dictionary containing the size of each region -> region:size
    for obj in regions[max(lengths, key=lengths.get)]:            #find the largest sized region and iterate over it
        
        pygame.draw.circle(screen, (255,255,0), [obj.x*sw/lengthSq+sw/(2*lengthSq),obj.y*sh/lengthSq+sh/(2*lengthSq)],sw/(2*lengthSq), sw/(2*lengthSq)) #highlight region
    pygame.display.update()
    raw_input("Done. Press Enter to exit.")
    pygame.quit()
