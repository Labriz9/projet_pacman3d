#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from collision import cont_to_disc
from cpe3d import Object3D
from labyrinth import laby_matrice
import pyglet
import random
import time

music = pyglet.media.load('star_mode.mp3')

def music_start():
    player = music.play()
    player.play()

class ViewerGL:
    def __init__(self):
        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(1200, 1200, 'OpenGL', None, None)
        # paramétrage de la fonction de gestion des évènements
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        glfw.set_cursor_pos_callback(self.window, self.cursor_pos_callback)
        glfw.set_key_callback(self.window, self.key_callback)
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.objs = [] #liste des objets affichés
        self.text = [] #liste des textes affichés
        self.touch = {}
        self.mouse = [0.0,0.0]
        self.List_points = [] #liste des points affichés
        self.List_pomme = [] #liste des pommes affichés
        self.List_fantome = [] #liste des fantomes affichés
        self.point_orig = 0 #position d'origine du premier point
        self.pomme_orig = 0 #position d'origine de la première pomme
        self.fantome_orig = 0 #position d'origine du premier fantôme
        self.obj_remove = 0 #nombre d'objets enlevés
        self.win = False
        self.lose = False
        self.score = 0
        self.score_per_point = 100
        self.vie = 3
        self.fps_view = True
        self.deplacement = [[0,0,0.25], [0,0,-0.25], [0.25,0,0], [-0.25,0,0]] # Gestion aléatoire du déplacement des ennemis
        self.temps_deplacement = 0 # Temps pour gérer le changement de direction de déplacement
        
    def run(self):
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.update_key()
            self.update_fantome()
            self.update_camera(self.objs[0].program)
            self.lose_life()
            self.end_game_win()
            self.message_final()
            for i in range(len(self.objs)):
                GL.glUseProgram(self.objs[i].program)
                if isinstance(self.objs[i], Object3D):
                    self.objs[i].draw()
                    
            for obj in self.text:
                GL.glUseProgram(obj.program)
                if isinstance(obj, Object3D):
                    self.update_camera(obj.program)
                obj.draw()
            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
        
    def cursor_pos_callback(self, win, xpos, ypos):
        delta_xpos, delta_ypos = xpos - self.mouse[0], ypos - self.mouse[1]
        self.mouse = [xpos,ypos]
        self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += delta_xpos*0.002
        if -800 <= ypos <= 800 :
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += delta_ypos*0.002

    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
        self.touch[key] = action
    
    def lose_life(self):
        x_pos, z_pos = self.cam.transformation.translation[0], self.cam.transformation.translation[2]
        x_pos_mat, z_pos_mat = cont_to_disc(x_pos, z_pos)
        for fantome in self.List_fantome :
            position_matrice_x, position_matrice_z = cont_to_disc(self.objs[fantome[0]].transformation.translation[0],self.objs[fantome[0]].transformation.translation[2])
            if x_pos_mat == position_matrice_x and z_pos_mat == position_matrice_z :
                self.vie -= 1
                self.text[3].value = "Vie:" + str(self.vie)
                self.cam.transformation.rotation_center.x = 0
                self.cam.transformation.rotation_center.z = 0
                self.cam.transformation.translation.x = 0
                self.cam.transformation.translation.z = 0
            if self.vie == 0:
                self.lose = True
                break
                
    
    def end_game_win(self):
        if self.List_points == []:
            self.win = True

    def message_final(self):
        if self.win:
            self.text[0].value = ""
            self.text[1].value = ""
            self.text[2].value = "YOU WON"
        elif self.lose:
            self.text[0].value = ""
            self.text[1].value = ""
            self.text[2].value = "YOU LOSE"

    def return_score(self):
        return self.score
    
    def add_object(self, obj):
        self.objs.append(obj)

    def set_camera(self, cam):
        self.cam = cam

    def add_points(self, p): #ajoute les informations du point de la liste
        self.List_points.append(p)
    def set_list_point(self): #initialise la position du premier point dans la liste d'objets affichés
        self.point_orig = self.List_points[0][0]

    def add_pomme(self, p): #ajoute les informations de la pomme de la liste
        self.List_pomme.append(p)
    def set_list_pomme(self): #initialise la position de la première pomme dans la liste d'objets affichés
        self.pomme_orig = self.List_pomme[0][0]

    def add_fantome(self, p): #ajoute les informations du fantome de la liste
        self.List_fantome.append(p)

    def set_list_fantome(self): #initialise la position du fantome dans la liste d'objets affichés
        self.fantome_orig = self.List_fantome[0][0]

    def update_camera(self, prog):
        GL.glUseProgram(prog)
        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "translation_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : translation_view")
        # Modifie la variable pour le programme courant
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_center_view")
        # Modifie la variable pour le programme courant
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(-self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)
    
        loc = GL.glGetUniformLocation(prog, "projection")
        if (loc == -1) :
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)

    def update_key(self):
        # Update joueur
        x_pos, z_pos = self.cam.transformation.translation[0], self.cam.transformation.translation[2] #position de la cam en réel
        x_pos_mat, z_pos_mat = cont_to_disc(x_pos, z_pos) #position de la cam dans la matrice
        angle = pyrr.euler.create(0.0,0.0,self.cam.transformation.rotation_euler[pyrr.euler.index().yaw])
        if laby_matrice[z_pos_mat][x_pos_mat] == 2: #test si on est sur un point
            laby_matrice[z_pos_mat][x_pos_mat] = 0 #actualise la map
            index_list_point = 0
            indice_point_trouve = False
            while not indice_point_trouve:
                point_obj, point_i, point_j = self.List_points[index_list_point]
                if point_i == z_pos_mat and point_j == x_pos_mat: 
                    indice_point_trouve = True
                else:
                    index_list_point += 1
            self.objs.pop(self.point_orig + index_list_point) #enleve le pomme de la liste d'affichage
            self.List_points.pop(index_list_point) 
            self.obj_remove += 1
            self.score += self.score_per_point
            self.text[0].value = "Score:" + str(self.score)
            self.text[1].value = "Points restants: " + str(len(self.List_points))
        
        if laby_matrice[z_pos_mat][x_pos_mat] == 3: #test si on est sur une pomme
            laby_matrice[z_pos_mat][x_pos_mat] = 0 #actualise la map
            index_list_pomme = 0
            indice_pomme_trouve = False
            while not indice_pomme_trouve:
                pomme_obj, pomme_i, pomme_j = self.List_pomme[index_list_pomme]
                if pomme_i == z_pos_mat and pomme_j == x_pos_mat: 
                    indice_pomme_trouve = True
                else:
                    index_list_pomme += 1
            self.objs.pop(self.pomme_orig + index_list_pomme - self.obj_remove) #enleve la pomme de la liste d'affichage
            self.List_pomme.pop(index_list_pomme) 
            #music_start()


        if x_pos_mat == 0 and z_pos_mat == 14: #sortie gauche du labyrinthe
            self.cam.transformation.rotation_center.x = 26
            self.cam.transformation.rotation_center.z = -18
            self.cam.transformation.translation.x = 26
            self.cam.transformation.translation.z = -18
            
        if x_pos_mat == 27 and z_pos_mat == 14: #sortie droite du labyrinthe   
            self.cam.transformation.rotation_center.x = -26
            self.cam.transformation.rotation_center.z = -18
            self.cam.transformation.translation.x = -26
            self.cam.transformation.translation.z = -18
            
        if self.fps_view:
            if glfw.KEY_W in self.touch and self.touch[glfw.KEY_W] > 0: #avancer
                test_collision_x0 = self.cam.transformation.translation + \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(angle), pyrr.Vector3([0, 0, -0.5]))
                test_collision_x1 = self.cam.transformation.translation + \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(angle), pyrr.Vector3([0, 0, -0.25])) 
                position_matrice_x, position_matrice_z = cont_to_disc(test_collision_x0[0], test_collision_x0[2])
                if not(laby_matrice[position_matrice_z][position_matrice_x] == 1):  #si il n'y a pas de collision
                    self.cam.transformation.rotation_center = test_collision_x1
                    self.cam.transformation.translation = test_collision_x1
            
            if glfw.KEY_S in self.touch and self.touch[glfw.KEY_S] > 0: #reculer
                test_collision_x0 = self.cam.transformation.translation + \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(angle), pyrr.Vector3([0, 0, 0.5]))
                test_collision_x1 = self.cam.transformation.translation + \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(angle), pyrr.Vector3([0, 0, 0.25]))
                position_matrice_x, position_matrice_z = cont_to_disc(test_collision_x0[0], test_collision_x0[2])
                if not(laby_matrice[position_matrice_z][position_matrice_x] == 1):  #si il n'y a pas de collision
                    self.cam.transformation.rotation_center = test_collision_x1
                    self.cam.transformation.translation = test_collision_x1
            
            if glfw.KEY_A in self.touch and self.touch[glfw.KEY_A] > 0: #deplacer à gauche
                test_collision_z0 = self.cam.transformation.translation + \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(angle), pyrr.Vector3([-0.5, 0, 0]))
                test_collision_z1 = self.cam.transformation.translation + \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(angle), pyrr.Vector3([-0.25, 0, 0]))
                position_matrice_x, position_matrice_z = cont_to_disc(test_collision_z0[0], test_collision_z0[2])
                if not(laby_matrice[position_matrice_z][position_matrice_x] == 1):  #si il n'y a pas de collision
                    self.cam.transformation.rotation_center = test_collision_z1
                    self.cam.transformation.translation = test_collision_z1
            
            if glfw.KEY_D in self.touch and self.touch[glfw.KEY_D] > 0: #déplacer à droite
                test_collision_z0 = self.cam.transformation.translation + \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(angle), pyrr.Vector3([0.5, 0, 0]))
                test_collision_z1 = self.cam.transformation.translation + \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(angle), pyrr.Vector3([0.25, 0, 0]))
                position_matrice_x, position_matrice_z = cont_to_disc(test_collision_z0[0], test_collision_z0[2])
                if not(laby_matrice[position_matrice_z][position_matrice_x] == 1):  #si il n'y a pas de collision
                    self.cam.transformation.rotation_center = test_collision_z1
                    self.cam.transformation.translation = test_collision_z1

        if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE]:
            self.cam.transformation.translation.y = 10
            self.fps_view = False

        if glfw.KEY_LEFT_CONTROL in self.touch and self.touch[glfw.KEY_LEFT_CONTROL]:
            self.cam.transformation.translation.y = 2
            self.fps_view = True
            
        if glfw.KEY_R in self.touch and self.touch[glfw.KEY_R]:
            self.deplacement = [random.choice([[0,0,0.25], [0,0,-0.25], [0.25,0,0], [-0.25,0,0]]) for i in range(4)]
            

    def update_fantome(self):
        # Déplacement
        if time.time() - self.temps_deplacement > 7: # change de direction au bout de 7sec
            self.temps_deplacement = time.time()
            self.deplacement = [random.choice([[0,0,0.25], [0,0,-0.25], [0.25,0,0], [-0.25,0,0]]) for i in range(4)]
        for i in range(4):
            fantome = (self.List_fantome)[i]
            test_collision_x0 = self.objs[fantome[0]].transformation.translation + np.asarray(self.deplacement[i]) * 2
            test_collision_x1 = self.objs[fantome[0]].transformation.translation + self.deplacement[i]
            position_matrice_x, position_matrice_z = cont_to_disc(test_collision_x0[0], test_collision_x0[2])
            
            # Sortie du labyrinthe
            if position_matrice_x == 0 and position_matrice_z == 14: #sortie gauche du labyrinthe
                self.objs[fantome[0]].transformation.rotation_center.x = 26
                self.objs[fantome[0]].transformation.rotation_center.z = -18
                self.objs[fantome[0]].transformation.translation.x = 26
                self.objs[fantome[0]].transformation.translation.z = -18
                
            elif position_matrice_x == 27 and position_matrice_z == 14: #sortie droite du labyrinthe   
                self.objs[fantome[0]].transformation.rotation_center.x = -26
                self.objs[fantome[0]].transformation.rotation_center.z = -18
                self.objs[fantome[0]].transformation.translation.x = -26
                self.objs[fantome[0]].transformation.translation.z = -18
                
            # Deplacement normal
            elif not(laby_matrice[position_matrice_z][position_matrice_x] == 1):  #si il n'y a pas de collision
                self.objs[fantome[0]].transformation.rotation_center = test_collision_x1
                self.objs[fantome[0]].transformation.translation = test_collision_x1
            else : 
                self.deplacement[i] = random.choice([[0,0,0.25], [0,0,-0.25], [0.25,0,0], [-0.25,0,0]])
                
                
            
        
