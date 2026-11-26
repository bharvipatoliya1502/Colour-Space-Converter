import numpy as np
from PIL import Image
from math_engine.matrix import matrix_null_space, matrix_rank, matrix_multiply
from math_engine.converter import (GRAYSCALE_MATRIX, grayscale_projection_matrix,
    grayscale_null_space, same_gray_demo, convert_image_to_grayscale, RGB_TO_YIQ)
def test_nullspace_grayscale_basis():
    basis=matrix_null_space(GRAYSCALE_MATRIX)
    assert len(basis)==2
    for v in basis: assert abs(sum(GRAYSCALE_MATRIX[0][i]*v[i] for i in range(3)))<1e-9
def test_nullspace_full_rank_empty():
    assert matrix_null_space([[1,0],[0,1]])==[]
def test_nullspace_zero_matrix_standard_basis_and_numpy():
    a=[[0,0,0],[0,0,0]]
    basis=matrix_null_space(a)
    assert len(basis)==3
    assert len(basis)==3-np.linalg.matrix_rank(np.array(a))
    for v in basis: np.testing.assert_allclose(np.array(a)@v,0,atol=1e-10)
def test_nullspace_numpy_dimension():
    a=[[1,2,3],[2,4,6]]
    basis=matrix_null_space(a)
    assert len(basis)==3-np.linalg.matrix_rank(np.array(a))
    for v in basis: np.testing.assert_allclose(np.array(a)@v,0,atol=1e-9)
def test_projection_idempotent_and_rank():
    m=np.array(grayscale_projection_matrix())
    np.testing.assert_allclose(m@m,m,atol=1e-10)
    assert matrix_rank(m.tolist())==1
    np.testing.assert_allclose(m,np.outer([1,1,1],GRAYSCALE_MATRIX[0]))
def test_same_gray_demo_valid():
    d=same_gray_demo()
    assert d["rgb1"]!=d["rgb2"]
    assert all(0<=x<=255 for x in d["rgb2"])
    assert abs(d["gray1"]-d["gray2"])<1e-9
def test_grayscale_pixel_matrix_path():
    im=Image.new("RGB",(1,1),(200,100,50))
    assert convert_image_to_grayscale(im).getpixel((0,0))==int(round(float((np.array(GRAYSCALE_MATRIX)@np.array([[200],[100],[50]]))[0,0])))


def test_grayscale_null_space_api_returns_two_valid_vectors():
    basis=grayscale_null_space()
    assert len(basis)==2
    for vector in basis:
        np.testing.assert_allclose(np.asarray(GRAYSCALE_MATRIX)@np.asarray(vector),[0.0],atol=1e-10)

def test_same_gray_demo_edge_colour_and_numpy_gray_reference():
    demo=same_gray_demo((255, 255, 0))
    assert demo["rgb1"] != demo["rgb2"]
    assert all(0 <= value <= 255 for value in demo["rgb2"])
    g=np.asarray(GRAYSCALE_MATRIX)
    np.testing.assert_allclose((g@np.asarray(demo["rgb1"]))[0],(g@np.asarray(demo["rgb2"]))[0],atol=1e-9)
