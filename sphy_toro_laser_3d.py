# -*- coding: utf-8 -*-
"""
========================================================================
 SPHY 120-QUBIT CLIFFORD TORUS 3D LASER GEODESIC VISUALIZER (py5)
 Autor: Deywe Okabe (Harpia Quantum)
 Descrição: Renderiza o Toro de Clifford em 3D com 120 qubits ativos 
            representados como feixes de laser orbitando as geodésicas 
            moduladas pela razão áurea (phi) e constante de estrutura fina.
========================================================================
"""

import py5
import math

# Constantes Físico-Matemáticas SPHY
PHI = 1.618033988749895
ALPHA = 1.0 / 137.035999084
LAMBDA_SPHY = PHI / ALPHA

NUM_QUBITS = 120
R_MAJOR = 180.0  # Raio maior do toro
R_MINOR = 60.0   # Raio menor do toro

angle_offset = 0.0

def setup():
    py5.size(1000, 800, py5.P3D)
    py5.smooth(8)
    py5.color_mode(py5.RGB, 255)
    print("=== SPHY Toro 3D Visualizer Iniciado ===")

def draw():
    global angle_offset
    py5.background(10, 10, 15)
    
    # Configuração da Câmera 3D Órbita suave
    py5.lights()
    py5.ambient_light(50, 50, 70)
    py5.directional_light(255, 255, 255, 0.5, 0.5, -1.0)
    
    py5.translate(py5.width / 2.0, py5.height / 2.0, -100)
    py5.rotate_x(py5.frame_count * 0.005 + 0.5)
    py5.rotate_y(py5.frame_count * 0.008)
    
    # 1. Renderização da Malha do Toro de Clifford (Wireframe / Superfície Geométrica)
    py5.stroke(40, 120, 200, 60)
    py5.no_fill()
    
    step_u = 40
    step_v = 30
    
    for i in range(step_u):
        u1 = (i / float(step_u)) * 2 * math.pi
        u2 = ((i + 1) / float(step_u)) * 2 * math.pi
        
        py5.begin_shape(py5.QUAD_STRIP)
        for j in range(step_v + 1):
            v = (j / float(step_v)) * 2 * math.pi
            
            # Coordenadas paramétricas do Toro
            for u in [u1, u2]:
                x = (R_MAJOR + R_MINOR * math.cos(v)) * math.cos(u)
                y = (R_MAJOR + R_MINOR * math.cos(v)) * math.sin(u)
                z = R_MINOR * math.sin(v)
                py5.vertex(x, y, z)
        py5.end_shape()

    # 2. Renderização dos 120 Qubits como Lasers orbitando a Geodésica (Razão Áurea)
    angle_offset += 0.02
    d_theta = 2.0 * math.pi / NUM_QUBITS

    for i in range(NUM_QUBITS):
        theta = i * d_theta
        # Geodésica modulada pela razão áurea e lambda SPHY
        phi_geo = LAMBDA_SPHY * (theta + angle_offset * 0.1)
        
        # Posição do Qubit no Toro
        cx = (R_MAJOR + R_MINOR * math.cos(phi_geo)) * math.cos(theta)
        cy = (R_MAJOR + R_MINOR * math.cos(phi_geo)) * math.sin(theta)
        cz = R_MINOR * math.sin(phi_geo)
        
        # Desenha o núcleo do Qubit (Esfera de Laser Brilhante)
        py5.push_matrix()
        py5.translate(cx, cy, cz)
        py5.no_stroke()
        py5.fill(0, 255, 180, 220)
        py5.sphere(3.5)
        py5.pop_matrix()
        
        # Desenha o feixe de laser conectando à geodésica seguinte
        if i < NUM_QUBITS - 1:
            next_theta = (i + 1) * d_theta
            next_phi = LAMBDA_SPHY * (next_theta + angle_offset * 0.1)
            nx = (R_MAJOR + R_MINOR * math.cos(next_phi)) * math.cos(next_theta)
            ny = (R_MAJOR + R_MINOR * math.cos(next_phi)) * math.sin(next_theta)
            nz = R_MINOR * math.sin(next_phi)
            
            py5.stroke(0, 255, 200, 150)
            py5.stroke_weight(1.5)
            py5.line(cx, cy, cz, nx, ny, nz)

if __name__ == "__main__":
    py5.run_sketch()
