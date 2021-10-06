import copy
import cv2
import numpy
import os
import trimesh
from pyquaternion import Quaternion

os.environ["PYOPENGL_PLATFORM"] = "egl"
import pyrender


class Camera():
    def __init__(self, object_mesh_path, dt):

        # Sample time
        self.dt = dt

        # Mesh
        trimesh_mesh = trimesh.load(object_mesh_path)
        mesh = pyrender.Mesh.from_trimesh(trimesh_mesh)

        # Scene
        self.scene = pyrender.Scene(bg_color=[0.0, 0.0, 0.0])

        # Camera
        fx = 1066.8
        fy = 1067.5
        cx = 312.99
        cy = 241.31
        self.width = 640
        self.height = 480
        self.camera_transform_offset = Quaternion(axis = [1.0, 0.0, 0.0], angle = numpy.pi).transformation_matrix

        self.camera = pyrender.Node(camera = pyrender.IntrinsicsCamera(fx = fx, fy = fy, cx = cx, cy = cy))
        self.scene.add_node(self.camera)

        # Light
        self.light = pyrender.PointLight(intensity = 20.0)
        self.scene.add(self.light)

        # Object node
        self.mesh_node = pyrender.Node(mesh = mesh, matrix = numpy.eye(4))
        self.scene.add_node(self.mesh_node)

        # Initialize object pose
        self.object_transform = Quaternion(axis = [1.0, 1.0, 1.0], angle = numpy.pi / 2).transformation_matrix
        self.randomize_object()

        # Renderer
        self.renderer = pyrender.OffscreenRenderer(self.width, self.height)

        # Camera angles
        self.x_axis_angle = 0.0
        self.y_axis_angle = 0.0
        self.scene.set_pose(self.camera, self.eval_camera_pose())


    def eval_camera_pose(self):

        rot_x = Quaternion(axis = [1.0, 0.0, 0.0], angle = self.x_axis_angle).rotation_matrix
        rot_y = Quaternion(axis = [0.0, 1.0, 0.0], angle = self.y_axis_angle).rotation_matrix

        camera_pose = copy.copy(self.camera_transform_offset)
        camera_pose[0:3, 0:3] = numpy.dot(numpy.dot(camera_pose[0:3, 0:3], rot_x), rot_y)

        return camera_pose


    def move(self, x_dot, y_dot):

        self.x_axis_angle += x_dot * self.dt
        self.y_axis_angle += y_dot * self.dt

        # Update camera pose
        self.scene.set_pose(self.camera, self.eval_camera_pose())


    def rgb(self):

        # Render the scene
        render_rgb, render_depth = self.renderer.render(self.scene)

        render_rgb = cv2.cvtColor(render_rgb, cv2.COLOR_BGR2RGB)

        return render_rgb


    def randomize_object(self):

        # Randomize object position
        self.object_transform[0:3, 3] = [numpy.random.uniform(-0.25, 0.25), numpy.random.uniform(-0.15, 0.15), numpy.random.uniform(1.0, 1.2)]
        self.scene.set_pose(self.mesh_node, self.object_transform)
