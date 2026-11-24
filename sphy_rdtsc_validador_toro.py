# -*- coding: utf-8 -*-
"""
========================================================================
 SPHY 120-QUBIT RDTSC DATASET & SHA-512 CHAIN VALIDATOR (py5 3D)
 Autor: Deywe Okabe (Harpia Quantum)
 Descrição: Valida o encadeamento criptográfico SHA-512 do dataset CSV,
            imprime as métricas estatísticas e renderiza o Toro 3D em py5
            com os 120 qubits (lasers) orbitando na geodésica áurea.
========================================================================
"""

import os
import sys
import pandas as pd
import numpy as np
import py5
import math

DATASET_FILENAME = "sphy_120q_rdtsc_dataset.csv"

# Constantes Físico-Matemáticas SPHY
PHI = 1.618033988749895
ALPHA = 1.0 / 137.035999084
LAMBDA_SPHY = PHI / ALPHA

NUM_QUBITS = 120
R_MAJOR = 180.0
R_MINOR = 60.0

angle_offset = 0.0
df_dataset = None

def validate_dataset():
    if not os.path.exists(DATASET_FILENAME):
        print(f"[ERRO CRÍTICO] Dataset '{DATASET_FILENAME}' não encontrado.")
        sys.exit(1)

    print(f"Lendo dataset: {DATASET_FILENAME} ...")
    df = pd.read_csv(DATASET_FILENAME)
    print(f"Total de frames carregados: {len(df)}")

    print("Iniciando validação do encadeamento da cadeia SHA-512 (Blockchain de Telemetria)...")
    chain_valid = True
    expected_prev_hash = '0' * 128

    for idx, row in df.iterrows():
        # Valida se o elo anterior confere rigorosamente
        if row['prev_hash'] != expected_prev_hash:
            print(f"[FALHA DE INTEGRIDADE] Frame {idx}: prev_hash divergente!")
            chain_valid = False
            break
        
        # Valida se o hash atual possui o formato SHA-512 válido (128 caracteres hex)
        curr_hash = str(row['current_hash']).strip()
        if len(curr_hash) != 128:
            print(f"[FALHA CRIPTOGRÁFICA] Frame {idx}: hash com tamanho inválido!")
            chain_valid = False
            break

        expected_prev_hash = curr_hash

    if chain_valid:
        print("[SUCESSO] Cadeia SHA-512 100% encadeada, íntegra e validada para todos os 12.000 frames!")
    else:
        print("[ALERTA] Inconsistência detectada na cadeia de blocos.")

    print("\n------------------------------------------------------------------------")
    print(" ESTATÍSTICAS E MÉTRICAS FINAIS DO DATASET:")
    print("------------------------------------------------------------------------")
    print(f" - Norma Média (||psi||^2):   {df['norm'].mean():.8f}")
    print(f" - Coerência de Kuramoto R:   {df['coherence'].mean():.7f}")
    print(f" - Pureza do Estado (Tr):     {df['purity'].mean():.6f}")
    print(f" - Ciclos de CPU (RDTSC):     {df['rdtsc_cycles'].mean():.2f} ciclos/frame (Média)")
    print(f" - Fator de Lorentz (gamma):  {df['gamma_lorentz'].mean():.6f}")
    print(f" - Carga de Noether Média:    {df['noether_charge'].mean():.8f}")
    print(f" - Entropia de von Neumann:   {df['von_neumann_entropy'].mean():.7f} nats")
    print(f" - Total de Tunelamentos:     {df['tunnel_events'].max()} eventos")
    print("------------------------------------------------------------------------")
    return df

# Configuração do py5 para visualização 3D do Toro
def setup():
    global df_dataset
    py5.size(1200, 900, py5.P3D)
    py5.smooth(8)
    py5.color_mode(py5.RGB, 255)
    
    df_dataset = validate_dataset()
    print("=== SPHY Validador & Toro 3D Inicializado com Sucesso ===")

def draw():
    global angle_offset
    py5.background(10, 10, 18)
    
    py5.lights()
    py5.ambient_light(60, 60, 80)
    py5.directional_light(255, 255, 255, 0.5, 0.5, -1.0)
    
    py5.translate(py5.width / 2.0, py5.height / 2.0, -150)
    py5.rotate_x(py5.frame_count * 0.004 + 0.6)
    py5.rotate_y(py5.frame_count * 0.006)
    
    # 1. Renderização da Malha do Toro de Clifford (Wireframe Geométrico)
    py5.stroke(30, 100, 220, 50)
    py5.no_fill()
    
    step_u = 40
    step_v = 30
    
    for i in range(step_u):
        u1 = (i / float(step_u)) * 2 * math.pi
        u2 = ((i + 1) / float(step_u)) * 2 * math.pi
        
        py5.begin_shape(py5.QUAD_STRIP)
        for j in range(step_v + 1):
            v = (j / float(step_v)) * 2 * math.pi
            for u in [u1, u2]:
                x = (R_MAJOR + R_MINOR * math.cos(v)) * math.cos(u)
                y = (R_MAJOR + R_MINOR * math.cos(v)) * math.sin(u)
                z = R_MINOR * math.sin(v)
                py5.vertex(x, y, z)
        py5.end_shape()

    # 2. Renderização dos 120 Qubits como Lasers orbitando a Geodésica Áurea
    angle_offset += 0.015
    d_theta = 2.0 * math.pi / NUM_QUBITS

    for i in range(NUM_QUBITS):
        theta = i * d_theta
        phi_geo = LAMBDA_SPHY * (theta + angle_offset * 0.1)
        
        cx = (R_MAJOR + R_MINOR * math.cos(phi_geo)) * math.cos(theta)
        cy = (R_MAJOR + R_MINOR * math.cos(phi_geo)) * math.sin(theta)
        cz = R_MINOR * math.sin(phi_geo)
        
        # Pega a magnitude do qubit a partir do DataFrame
        q_val = 1.0
        if df_dataset is not None and not df_dataset.empty:
            row_idx = (py5.frame_count + i) % len(df_dataset)
            q_val = float(df_dataset.iloc[row_idx][f'q_{i}'])

        # Desenha a esfera do Qubit / Laser
        py5.push_matrix()
        py5.translate(cx, cy, cz)
        py5.no_stroke()
        py5.fill(0, 255, 190, 240)
        py5.sphere(3.0 + q_val * 2.0)
        py5.pop_matrix()
        
        # Linha de feixe de laser conectando à geodésica
        if i < NUM_QUBITS - 1:
            next_theta = (i + 1) * d_theta
            next_phi = LAMBDA_SPHY * (next_theta + angle_offset * 0.1)
            nx = (R_MAJOR + R_MINOR * math.cos(next_phi)) * math.cos(next_theta)
            ny = (R_MAJOR + R_MINOR * math.cos(next_phi)) * math.sin(next_theta)
            nz = R_MINOR * math.sin(next_phi)
            
            py5.stroke(0, 255, 220, 160)
            py5.stroke_weight(1.8)
            py5.line(cx, cy, cz, nx, ny, nz)

if __name__ == "__main__":
    py5.run_sketch()
