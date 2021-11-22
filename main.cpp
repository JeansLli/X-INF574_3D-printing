#include <igl/opengl/glfw/Viewer.h>
#include <igl/readOBJ.h>
#include <iostream>
#include <ostream>

using namespace Eigen;

MatrixXd V1; // vertex coordinates of the input mesh
MatrixXi F1; // incidence relations between faces and edges
RowVector3d rotation_axis(1., 0., 0.); // rotation axis

// ------------ main program ----------------
int main(int argc, char *argv[]) {
  igl::readOBJ("/home/theo/Documents/ecole_polytechnique/geometry_representation_shapes/project/X-INF574_3D-printing/data/bunny.obj", V1, F1); // Load an input mesh in OFF format

  // input mesh
  std::cout << "Vertices: " << V1.rows() << std::endl;
  std::cout << "Faces:    " << F1.rows() << std::endl;

  igl::opengl::glfw::Viewer viewer;
  //viewer.callback_key_down = &key_down;
  //viewer.callback_pre_draw = &pre_draw;
  viewer.data().set_mesh(V1, F1);
  viewer.core().is_animating = true; // animation is active

  //draw_bounding_box(viewer, V1);
  viewer.launch();
}