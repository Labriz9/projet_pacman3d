from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr
from viewerGL import laby_matrice
import pyglet

def main():
    music = pyglet.media.load('pacman.mp3')
    #player = music.play()
    #player.play()

    viewer = ViewerGL()

    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y = 2
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')

    decalage_z = 23
    decalage_x = 13.5
# Load fantômes

    m = Mesh.load_obj('stegosaurus.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([4, 4, 4, 1]))
    vao = m.load_to_gpu()
    for i in range(4):
        texture = glutils.load_texture('fantome'+str(i+1)+'.jpg')
        tr = Transformation3D()
        tr.translation.y = -np.amin(m.vertices, axis=0)[1]
        tr.translation.z = -24
        tr.translation.x = 2*i - 2
        tr.rotation_center.z = 0.2
        o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
        viewer.add_object(o)
        viewer.add_fantome([len(viewer.objs) - 1, 20, 12 + i])
    viewer.set_list_fantome()

# Load murs
    m = Mesh.load_obj('cube.obj')
    m.normalize()
    vao = m.load_to_gpu()
    texture = glutils.load_texture('cube_tex1.png')
    for i in range(len(laby_matrice)):  # itère sur les lignes
        for j in range(len(laby_matrice[0])):  # itère sur les colonnes
            if laby_matrice[i][j] == 1 :
                tr = Transformation3D()
                tr.translation.y = -np.amin(m.vertices, axis=0)[1]
                tr.translation.z = 2*i - 2*decalage_z
                tr.translation.x = 2*j - 2*decalage_x
                tr.rotation_center.z = 0.2
                o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
                viewer.add_object(o)

# Load points
    m = Mesh.load_obj('sphere.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([0.1, 0.1, 0.1, 1]))
    vao = m.load_to_gpu()
    texture = glutils.load_texture('point.jpg')
    for i in range(len(laby_matrice)):  # itère sur les lignes
        for j in range(len(laby_matrice[0])):  # itère sur les colonnes
            if laby_matrice[i][j] == 2 :
                tr = Transformation3D()
                tr.translation.y = -np.amin(m.vertices, axis=0)[1] + 0.5
                tr.translation.z = 2*i - 2*decalage_z
                tr.translation.x = 2*j - 2*decalage_x
                tr.rotation_center.z = 0.2
                o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
                viewer.add_object(o)
                viewer.add_points([len(viewer.objs) - 1, i, j])
    viewer.set_list_point()

# Load pommes
    m = Mesh.load_obj('sphere.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([0.25, 0.25, 0.25, 1]))
    vao = m.load_to_gpu()
    texture = glutils.load_texture('pomme.jpg')
    for i in range(len(laby_matrice)):  # itère sur les lignes
        for j in range(len(laby_matrice[0])):  # itère sur les colonnes
            if laby_matrice[i][j] == 3 :
                tr = Transformation3D()
                tr.translation.y = -np.amin(m.vertices, axis=0)[1] + 0.5
                tr.translation.z = 2*i - 2*decalage_z
                tr.translation.x = 2*j - 2*decalage_x
                tr.rotation_center.z = 0.2
                o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
                viewer.add_object(o)
                viewer.add_pomme([len(viewer.objs) - 1, i, j])
    viewer.set_list_pomme()


    m = Mesh()
    p0, p1, p2, p3 = [-28, 0, -47], [28, 0, -47], [28, 0, 15], [-28, 0, 15]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [10, 0], [10, 10], [0, 10]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('blackstone.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    vao = Text.initalize_geometry()
    texture = glutils.load_texture('fontB.jpg')
    o = Text('Score:0', np.array([-1, 0.7], np.float32), np.array([0.5, 0.9], np.float32), vao, 2, programGUI_id, texture)
    viewer.text.append(o)
    o = Text('Points restants: 0', np.array([-0.95, 0.45], np.float32), np.array([0.9, 0.65], np.float32), vao, 2, programGUI_id, texture)
    viewer.text.append(o)
    o = Text('', np.array([-0.4, -0.1], np.float32), np.array([0.6, 0.1], np.float32), vao, 2, programGUI_id, texture)
    viewer.text.append(o)
    o = Text('Vie:3', np.array([-0.95, -0.9], np.float32), np.array([0.3, -0.7], np.float32), vao, 2, programGUI_id, texture)
    viewer.text.append(o)
    
    viewer.run()

if __name__ == '__main__':
    main()