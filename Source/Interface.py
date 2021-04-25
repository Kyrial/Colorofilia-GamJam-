from tkinter import *
import tkinter.font as tkFont
import random
from math import *
import time
from terrain import *
import pygame.mixer






#####CLASS INTERFACE#####



class interface:

    def __init__(self, fen ):
        self.fenetre = fen
        self.fenetre.title('Colorofilia')

        self.largeur=1080
        self.hauteur=648
        self.tailleCase=72



       
    
##    def creerCanvas(self):
##        
##        self.canvas = Canvas(self.fenetre,  width=600, height=600,
##                             borderwidth=5,background="white")
##        self.canvas['scrollregion'] = (-25,-25,575,575)
##
##
##
##        self.canvas.grid(column =2, row=2) # columnspan=2)



    #def frameJeu(self):
        



    def cacherFrame(self):
        self.frameMenu.grid_forget()
        self.frameDialog.grid_forget()
        self.frameEnv.grid_forget()
        self.framePrincipalMenu.grid_forget()
        self.frameCombat.grid_forget()

    def frameInit(self):

        ##frame principal
        #frame menu
        self.framePrincipalMenu = Frame(self.fenetre,
                                    borderwidth=0,width = self.largeur,height =self.hauteur,  relief=GROOVE)
        self.framePrincipalMenu.grid(column=2, row=0)

        #frame environement
        self.frameEnv = Frame(self.fenetre,
                                    borderwidth=0,width = self.largeur,height =self.hauteur,  relief=GROOVE)
        self.frameEnv.grid(column=2, row=0)


        ####frame du beauceau inferieur
        ##frame du menu
        self.frameMenu = Frame(self.fenetre,
                                    borderwidth=2,width = self.largeur,height =self.hauteur/4,  relief=GROOVE)
        self.frameMenu.grid(column=2, row=1)

        ##frame des dialogues
        self.frameDialog = Frame(self.fenetre,
                                    borderwidth=2,width = self.largeur,height =self.hauteur/4,  relief=GROOVE)     
        self.frameDialog.grid(column=2, row=1)

        

        ##frame combat
        self.frameCombat = Frame(self.fenetre,
                                   borderwidth=2,width = self.largeur,height =self.hauteur/4,  relief=GROOVE)
        self.frameCombat.grid(column=2, row=1)


        ##on cache les frames:
        self.cacherFrame();
        

    def changeZone(self,direction):
        #print(self.carteCourrante)
        temp = list(self.carteCourrante)

        x, y = self.canvasEnv.coords(self.perso)
        
        if direction =="droite":
            self.canvasEnv.coords(self.perso,2*self.tailleCase,y)
            #self.canvasEnv.move(self.perso,-13 *self.tailleCase,0)
            self.plateau.positionP[0] = 1
            
            temp[2]=str(int(temp[2])+1)     
            
        elif direction =="gauche":
            self.canvasEnv.coords(self.perso,14*self.tailleCase,y)
            #self.canvasEnv.move(self.perso,13*self.tailleCase,0)
            self.plateau.positionP[0] = 15
            
            temp[2]=str(int(temp[2])-1)     
            
        elif direction =="haut":
            self.canvasEnv.coords(self.perso,x,8*self.tailleCase)
            #self.canvasEnv.move(self.perso,0,6*self.tailleCase)
            self.plateau.positionP[1] = 8
            
            temp[0]=str(int(temp[0])-1)     
            
        elif direction =="bas":
            self.canvasEnv.coords(self.perso,x,2*self.tailleCase)
            #self.canvasEnv.move(self.perso,0,-6*self.tailleCase)
            self.plateau.positionP[1] = 1
            
            temp[0]=str(int(temp[0])+1)     
            
        temp="".join(temp)        
        self.carteCourrante=temp
    
        #print(self.carteCourrante)
        
        if self.carteCourrante == "1-1":
            #cinématique"
            print("BOSS")
            self.chargeCarte()
            
            self.placeBoss()
            self.cinematique("denouement")
            
        else:
            self.chargeCarte()

    def placeBoss(self):
        #self.imageCinema = PhotoImage(file="plante1.png")
        self.imageFleur = PhotoImage(file="fleur.png")
        self.imgPlante = self.canvasEnv.create_image(self.largeur/2+10,self.hauteur/2, image=self.imageFleur,tag="monstre")
        #=self.canvasEnv.create_image(self.largeur/2,self.hauteur/2, image=self.imageCinema, tag="monstre")

       
        self.canvasEnv.tag_raise("monstre")
        

        #self.canvasEnv.tag_raise("personnage")




         
        
    def chargeCarte(self):
        ##destroy peu etre l'encien canvas
        self.fontEnv = PhotoImage(file="decor_"+self.carteCourrante+".png")
        self.canvasEnv.create_image(self.largeur/2,self.hauteur/2, image=self.fontEnv)

        self.canvasEnv.tag_raise("personnage")
        
        #self.plateau.positionP=[2,2]
        
       
    def initEnv(self):
        self.frameEnv.grid(column=2, row=0)
        self.frameEnv.grid_propagate(0)
        self.canvasEnv = Canvas(self.frameEnv,width=self.largeur, height=self.hauteur)
        self.canvasEnv.grid(column=2, row=0)
        self.fontEnv = PhotoImage(file="decor_0-0.png")
        self.canvasEnv.create_image(self.largeur/2,self.hauteur/2, image=self.fontEnv)

        self.personnage = PhotoImage(file="personnage.png")
        
        self.perso = self.canvasEnv.create_image(5*self.tailleCase,5*self.tailleCase,image=self.personnage,tag='personnage')#,anchor='s')

        self.carteCourrante="0-0"
        self.plateau = terrain()

        self.plateau.positionP=[5,5]

        
        
    def attenteEvent(self):

        
        self.fenetre.bind("<Button-1>", self.directionClique)



        
    def move(self,x,y,item,noSleep=False):
        if item == self.perso:
            self.plateau.positionP[0] = self.plateau.positionP[0]+x
            self.plateau.positionP[1] = self.plateau.positionP[1]+y
        fps=16
        for i in range(0,fps):
            
            #self.canvasEnv.move(self.perso, -1,0)
            self.canvasEnv.move(item,x*(self.tailleCase//fps),y*(self.tailleCase//fps))
            self.canvasEnv.update_idletasks()
            #self.canvasEnv.update()
            if not(noSleep):
                time.sleep(0.01)

    def verifPosition(self,x,y):

      
        ###ATTENTION, PLATEAU MATRICE X Y inversé !!!
        #print("position ",self.plateau.positionP[0],"  ",self.plateau.positionP[1])
        #print("destination ",self.plateau.positionP[0]+x,"  ",self.plateau.positionP[1]+y)
        value=(self.plateau.matrice[self.carteCourrante]
               [self.plateau.positionP[1]+y]
               [self.plateau.positionP[0]+x])
        #print(value)
        #if value==1:
       #     self.plateau.matrice[self.carteCourrante][self.plateau.positionP[1]+x][self.plateau.positionP[0]+y] = 5
       # for i in (self.plateau.matrice[self.carteCourrante]):
       #     print(i)
        
        if value==0:
            return True
        elif value==1:
            return False

        elif value==8:
            print("changement de carte gauche")
            self.changeZone("droite")
            return False
        elif value==9:
            print("changement de carte gauche")
            self.changeZone("gauche")
            return False
        elif value==6:
            print("changement de carte gauche")
            self.changeZone("haut")
            return False
        elif value==7:
            print("changement de carte gauche")
            self.changeZone("bas")
            return False
            
        
        
    def directionClique(self, event):
        x = self.canvasEnv.canvasx (event.x)
        y = self.canvasEnv.canvasy (event.y)

        #print("coords x, y:", x, " ", y)
        coords = self.canvasEnv.coords(self.perso)
        #print("coords :",self.canvasEnv.coords(self.perso))
        if( (y-coords[1]) < 0 and abs(y-coords[1]) > abs(x-coords[0])):                
            #print("haut")
            if self.verifPosition(0,-1):
                self.move(0,-1,self.perso)

        elif( (y-coords[1]) >= 0 and abs(y-coords[1]) > abs(x-coords[0])):               
            #print("bas")
            if self.verifPosition(0,1):
                self.move(0,1,self.perso)
        elif( (x-coords[0]) >= 0 and abs(x-coords[0]) > abs(y-coords[1])):              
            #print("droite")
            if self.verifPosition(1,0):
                self.move(1,0,self.perso)
        elif( (x-coords[0]) < 0 and abs(x-coords[0]) > abs(y-coords[1])):
            #print("gauche")
            if self.verifPosition(-1,0):
                self.move(-1,0,self.perso)
        


    def menu(self):
        #création des differente frame
        self.frameInit()
        
        ##musique
        pygame.mixer.init()
        pygame.mixer.music.load("intro.mp3")   # chargement de la musique
        pygame.mixer.music.play(loops=-1)
        

        #frame self.framePrincipalMenu
        ##canvas: image menu
        self.framePrincipalMenu.grid(column=2, row=0)
        self.framePrincipalMenu.grid_propagate(0)
        
        
        self.canvasM = Canvas(self.framePrincipalMenu,width=self.largeur, height=self.hauteur)

        self.imageMenu = PhotoImage(file="imageMenu.png")
        self.canvasM.create_image(self.largeur/2,self.hauteur/2, image=self.imageMenu)#.pack()
        
        self.canvasM.grid(column=2, row=0)
        ##ajouter: musique


        ## frame: bouton menu

        self.frameMenu.grid(column=2, row=1)
        self.frameMenu.grid_propagate(0)

        #Coloroflia
           #"Coloroflia \n Un monde Sans Couleur"
        #police=tkFont.Font(family='Comic', size=26, weight='bold')
        #Label(self.frameMenu,text="j ",height=2,width=30).grid()
        
        self.boutonCommencer=Button(self.frameMenu, text="Nouvelle partie",command=self.newGame ).pack(padx=10, pady=10)
       
    def newGame(self):
        #pygame.mixer.music.stop()
        pygame.mixer.init()
        pygame.mixer.music.load("worldTheme.mp3")   # chargement de la musique
        pygame.mixer.music.play(loops=-1)
        self.canvasM.destroy()
        #self.frameMenu.destroy()
        self.cacherFrame()

        self.initEnv()
        #self.canvas = Canvas(self.fenetre,width=self.largeur, height=self.hauteur)
        #self.canvas.grid(column=2, row=0)
        
       # self.image = [PhotoImage(file="test.gif")],format = 'gif -index %i' % (i)) for i in range(2)]
    


       
     #  self.image = PhotoImage(file="test.gif")],format = 'gif -index 0';
       # self.image = PhotoImage(file="test.gif")],format = 'gif -index 1';
        #self.canvas.create_image(self.largeur/2,self.hauteur/2, image=self.frames)
        
        self.dialogue("intro")
        self.boutonCommencer=Button(self.frameMenu, text="Nouvelle partie",command=self.newGame ).pack(padx=10, pady=10)
        









    def cinematique(self, indice):
        ##si intro faire bouger plante colorer
        if indice == "intro":
            self.imageCinema = PhotoImage(file="plante1.png")

            self.ImgCinema = self.canvasEnv.create_image(self.largeur-self.largeur/2.8,
                                                         self.hauteur+self.tailleCase,
                                                         image=self.imageCinema,tag='cinema')
            
            for i in range(0,9):
                self.move(0,-1.1,self.ImgCinema)
            
            
            self.dialogue("intro2")
        elif indice == "intro2":
            for i in range(0,5):
                self.move(1.5,0,self.ImgCinema)
            self.canvasEnv.delete(self.ImgCinema)
            self.dialogue("intro3")

        elif indice == "denouement":
            self.imageCinema = PhotoImage(file="plante1.png")

            self.ImgCinema = self.canvasEnv.create_image(self.largeur-self.largeur/3.5,
                                                         -self.tailleCase,
                                                         image=self.imageCinema,tag=("cinema","monstre"))

            x, y = self.canvasEnv.coords(self.perso)
        
            self.canvasEnv.coords(self.perso,self.tailleCase*7,-self.tailleCase)
            #self.canvasEnv.move(self.perso,-13 *self.tailleCase,self.tailleCase*5)
            self.plateau.positionP[1] = -2
            self.plateau.positionP[0] = 7


            for i in range(0,6):
                self.move(0,1,self.ImgCinema)
            time.sleep(0.8)

            for i in range(0,3):
                self.move(0,1,self.perso)
                self.plateau.positionP[1] = self.plateau.positionP[1]+1
            self.dialogue("denouement2")
        elif indice == ("denouement2"):
            for i in range(0,5):
                self.move(-0.1,0.2,self.ImgCinema,noSleep=True)
                self.move(0.1,0,self.imgPlante,noSleep=True)
                self.move(-0.6,0.6,self.perso,noSleep=True)
                
                
                time.sleep(0.02)
            self.barreCombat()
            


    def finCombat(self):
            #self.narrat.unbind("<Button-1>",)
           # self.phrase1.unbind("<Button-1>",)
            #self.phrase2.unbind("<Button-1>",)
           # self.phrase3.unbind("<Button-1>",)
        
            self.narrateur.destroy()
            self.choix1.destroy()
            self.choix2.destroy()
            self.choix3.destroy()
            self.frameCombat.grid_forget()

            pygame.mixer.init()
            pygame.mixer.music.load("victoryBattle.mp3")   # chargement de la musique
            pygame.mixer.music.play(loops=-1)
           

        


    def actionCombat(self,indice, nbp,narrat, phrase1, phrase2, phrase3):
        #print(indice)
        nbp[0] = indice
        #print( combat[indice][0][1])
        if combat[indice][0][1] == "PERDU":
            pygame.mixer.music.stop()
            print("perdu")
            self.finCombat()

            self.frameCombat.grid_forget()
            self.dialogue("perdu")
        elif combat[indice][0][1] == "GAGNER":
            #self.fontEnv = PhotoImage(file="decor_"+self.carteCourrante+".png")
            self.fontEnv = PhotoImage(file="decor_1-1Color.png")
            self.canvasEnv.create_image(self.largeur/2,self.hauteur/2, image=self.fontEnv)


            x, y = self.canvasEnv.coords(self.perso)
            self.personnage = PhotoImage(file="perso1Color.png")
            self.perso = self.canvasEnv.create_image(x,y,image=self.personnage,tag='personnage')#,anchor='s')


            self.canvasEnv.tag_raise("personnage")
            pygame.mixer.music.stop()
            print("gagner")
            self.finCombat()
            self.dialogue("gagner")
        else:    
            narrat.set(combat[indice][0][0])
            phrase1.set(combat[indice][1][0])
            phrase2.set(combat[indice][2][0])
            phrase3.set(combat[indice][3][0])
        
      
    
    def barreCombat(self):

        pygame.mixer.init()
        pygame.mixer.music.load("battleTheme.mp3")   # chargement de la musique
        pygame.mixer.music.play(loops=-1)

       
        self.frameDialog.grid_forget()
        self.frameCombat.grid(column=2, row=1)
        self.frameCombat.grid_propagate(0)
        #self.boutonCommencer=Button(self.frameMenu, textvariable="Attaquer",command=self.newGame ).pack(padx=10, pady=10)
        #combat["debut"]        

        nbp=["debut"]
        
        narrat = StringVar()
        phrase1 = StringVar()
        phrase2 = StringVar()
        phrase3 = StringVar()
       # phrase.set(dialog[indice][nbP[0]])
        narrat.set(combat["debut"][0][0])
        phrase1.set(combat["debut"][1][0])
        phrase2.set(combat["debut"][2][0])
        phrase3.set(combat["debut"][3][0])
        self.narrateur=Label(self.frameCombat,textvariable=narrat,font=('Time','18'))#,
                        #activebackground= "black", activeforeground ="white")
        self.narrateur.grid(column=1, row = 0)

        self.choix1=Label(self.frameCombat,textvariable=phrase1,font=('Time','16'))
        self.choix2=Label(self.frameCombat,textvariable=phrase2,font=('Time','16'))
        self.choix3=Label(self.frameCombat,textvariable=phrase3,font=('Time','16'))

        self.choix1.grid(column=1, row = 1)
        self.choix2.grid(column=1, row = 2)
        self.choix3.grid(column=1, row = 3)

        #combat[nbp[0]][1][1]
        self.choix1.bind("<Button-1>", lambda e:self.actionCombat(indice = combat[nbp[0]][1][1],nbp = nbp,
                                                                  narrat = narrat, phrase1 = phrase1,
                                                                  phrase2 = phrase2, phrase3 = phrase3))
        self.choix2.bind("<Button-1>", lambda e:self.actionCombat(indice = combat[nbp[0]][2][1],nbp = nbp,
                                                                  narrat = narrat, phrase1 = phrase1,
                                                                  phrase2 = phrase2, phrase3 = phrase3))
        self.choix3.bind("<Button-1>", lambda e:self.actionCombat(indice = combat[nbp[0]][3][1],nbp = nbp,
                                                                  narrat = narrat, phrase1 = phrase1,
                                                                  phrase2 = phrase2, phrase3 = phrase3))
        #self.choix2.bind("<Button-1>", self.test)
        #self.choix3.bind("<Button-1>", self.test)
                         #lambda e:self.avanceDialog(nbp=nbP,indice=indice,phrase=phrase)) 
        

           
                
            
            


    def avanceDialog(self,nbp,indice,phrase):
        
        nbp[0]=nbp[0]+1
        #print(nbp[0])
        if len(dialog[indice])<=nbp[0]:
            #print("stoop")
            self.phrase.destroy()
            self.fenetre.unbind("<Button-1>",)
            self.frameDialog.grid_forget()
            if indice in ("intro","intro2","denouement2") :
                self.cinematique(indice)
    
            
            elif indice in ("gagner","perdu"):
                pygame.mixer.music.stop()
                if indice == "perdu":
                    self.newGame()
                #self.attenteEvent()
            else:
                ##appel fonction suite
                self.attenteEvent()

        else:
            phrase.set(dialog[indice][nbp[0]])

        
        
        
##        if not hasattr(avanceDialog, 'c'):
##            avanceDialog.c=0
##        if reset == True:
##                avanceDialog.c=0
##        else:
##            avanceDial og.c=avanceDialog.c+1
            
        
        
            
        
        

    def dialogue(self,indice):
        
        
        nbP=[0]
        #f.frame.grid_forget()
        #f.frameDialog.grid_forget()
        
        #print("miaou")
        self.frameDialog.grid(column=2, row=1)
        self.frameDialog.grid_propagate(0)

        phrase = StringVar()
        phrase.set(dialog[indice][nbP[0]])
        
#        dialog["intro"][0]
        self.phrase=Label(self.frameDialog,textvariable=phrase,font=('Time','27'))
        self.phrase.grid()
        
       
        self.fenetre.bind("<Button-1>", lambda e:self.avanceDialog(nbp=nbP,indice=indice,phrase=phrase)) 
        

        
        

            
        
        

  
dialog={}
dialog["intro"]=("mais... que c'est-il passé ?...","où suis-je ?... ",
                 "ah ? mais je reconnais c'est ma maison ?","Mais pourquoi je ne perçois aucune couleur ?","uniquement des nuances de noir et blanc, \n ou sont les passé les couleurs ? ")

dialog["intro2"]=("c'était quoi ça ? j'ai vu un truc bougé","on aurais dit une plante")
dialog["intro3"]=("mais ??! c'était coloré ! pas comme le reste", "et une plante qui marche ? c'est anodin ça",
                  " je devrais peut etre le suivre, j'en apprendrais plus","d'ailleurs je ne sais meme pas ce qu'il se passe et \n je me lance dans une quête invraissenblable",
                  " si ça se trouve je suis en train de dormir ?",
                  "bref pour le moment je suis là, donc avançons !")

dialog["denouement2"]=("c'est quoi ça ?!","serais-se se monstre le responsable de tout ceci ?","si je le bat peut etre que les couleur reviendront")

dialog["perdu"]=("ahh... j'ai .. perdu.."," c'est pas possible", "tout cela en vaint")

dialog["gagner"]=("ah ? j'ai gagné !","je m'en croyais pas capable"," et les couleur revienne j'ai reussi !","FIN")


combat={}
combat["debut"]=(("les plantes se mettent en position de combat","SUITE"),
                 ("se mettre en position offensive", 2),
                 ("se mettre en position defensive",5),
                 ("faire une roulade pour se placé sur le flanc de l'enemie", 10))

combat[2]=(("une racine jaillit du sol, vous parez et la tranche d'un coup rapide ","SUITE"),
                 ("courir vers l'enemie", 11),
                 ("rester en position",16),
                 ("lancée son épee pour décapiter la grosse fleur", 15))

combat[5]=(("une racine jaillit du sol et vous fouette violament, vous vous ressaisissez","SUITE"),
                 ("courir vers l'enemie", 11),
                 ("rester en position",16),
                 ("lancée son épee pour décapiter la grosse fleur", 15))


combat[10]=(("Vous esquivez de justesse une racine sortant du sol et vous vous mettez hors de sa portée","SUITE"),
                 ("courir vers l'enemie", 11),
                 ("rester en position",16),
                 ("lancée son épee pour tentez de décapiter la grosse fleur", 15))


combat[11]=(("la petite plante vous barre la route","SUITE"),
                 ("l'empaller a l'aide de son épée", 17),
                 ("tenter de le taillader",12),
                 ("se mettre en garde", 18))



combat[12]=(("vous réussissez votre coup, la fleur prépare quelque chose mais est hors de portée","SUITE"),
                 ("lancée son épee pour tentez de décapiter la grosse fleur", 13),
                 ("se mettre en garde",18),
                 ("courrir pour l'arreter", 16))

combat[13]=(("Vous réussissez votre coup et avez terrasser c'est deux monstre","GAGNER"),)


combat[18]=(("vous ne voyez pas la racine derrière vous bous balayer, vous tombez incosciant", "PERDU"),)

combat[17]=(("votre épée se coince dans le corps du monstre, une liane vous balaye et tombez inconsciant", "PERDU"),)

combat[16]=(("la Fleur libère des spore, il est trop tard pour l'arreter, vous vous evanouissez", "PERDU"),)

combat[15]=(("vous réussissez votre coup mais n'avez plus d'épée","PERDU"),)


f=interface(Tk())
#f.creerCanvas()


f.menu()
#pygame.mixer.init()
#pygame.mixer.music.load("intro.mp3")   # chargement de la musique
#pygame.mixer.music.play(loops=-1)#, fade_ms=0)

#son = pygame.mixer.Sound("intro.mp3")
#son.play()



f.fenetre.mainloop()




