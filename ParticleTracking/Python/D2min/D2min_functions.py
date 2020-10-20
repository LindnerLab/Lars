# -*- coding: utf-8 -*-
"""
Functions used to calculate D2min of ensembles of particles.

Dependencies:
    - Pandas
    - Numpy

@author: Lars Kool
"""
import numpy as np
import pandas as pd

def distance(x1, x2, y1, y2):
    """
    Euclidian distance between two points with coordinates [x1[i],y1[i]] and
    [x2[i],y2[i]]

    Parameters
    ----------
    x1 : Float
        x-coordinate of point 1.
    x2 : Float
        x-coordinate of point 2.
    y1 : Float
        y-coordinate of point 1.
    y2 : Float
        y-coordinate of point 2.

    Returns
    -------
    distance : Float
        Euclidian distance between the two points

    """
    distance = np.sqrt(np.square(x1 - x2) + np.square(y1 - y2))
    return distance

def distance_to_neighbors(xy_particle, xy_neighbors):
    """
    Euclidian distance between a reference point (xy_particle [x,y]) and a
    list of n other points (xy_neighbors [[x1,y1],[x2,y2],...,[x_n, y_n]])

    Parameters
    ----------
    xy_particle : 1-by-2 array of floats
        Coordinates of the reference point [x,y].
    xy_neighbors : n-by-2 array of floats
        Coordinatees of n other points, where the column indicates x/y
        (col=0 -> x, col=1 -> y) and the row indicates the point.

    Returns
    -------
    distance : n-by-1 numpy array of floats
        Euclidian distance between the reference point and the other points,.

    """
    distance = np.sqrt(np.square(xy_neighbors[:, 0] - xy_particle[0])
                       + np.square(xy_neighbors[:, 1] - xy_particle[1]))
    return distance

def neighboring_particles(xy_particles, cutoff):
    """
    Determines which particles are within the cutoff distance of each particle.

    Parameters
    ----------
    xy_particles : n-by-2 numpy array of floats
        Coordinatees of n particles, where the column indicates x/y
        (col=0 -> x, col=1 -> y) and the row indicates the particle index.
    cutoff : float
        Maximum distance for which two particles can be considered neighbors.

    Returns
    -------
    neighbors : list of lists of ints
        Lists of lists of indices of neighoring particles, where
        len(neighbors[i]) will give the number of neighbors of particle i, and
        xy_particles[neighbors[i],:] will give a list of xy-coordinates of the
        particles that neighbor particle i.

    """
    nParticles = xy_particles.shape[0]
    neighbors = [[] for i in range(nParticles)]
    for i in range(nParticles):
        distances = distance_to_neighbors(xy_particles[i, :],
                                          xy_particles[i+1:, :])
        neighbors_particle = distances < cutoff
        idx = [j+i+1 for j, x in enumerate(neighbors_particle) if x == True]
        neighbors[i] = neighbors[i]+idx
        for j in idx:
            neighbors[j] = neighbors[j]+[i]
    return neighbors

def d2min_particle(xy_particle, xy_particle_next,
                   xy_neighbors, xy_neighbors_next, avg_distance = 1):
    """
    Determines a measure of the non-affine displacement of a particle with
    respect to its neighboring particles. First, the affine transformation is
    determined by mapping the neighboring particles (xy_neighbors) to their
    positions after displacement (xy_neighbors_next) using a best-fit linear
    combination of affine transformations. This best-fit transfomation is then
    applied to the reference particle (xy_particle). Then, the distances
    between the reference particle and its neighbors, after displacement and
    after transformation, are determined. D2min is the average squared
    difference between the interparticle distance after displacement and
    after transformation.
    
    More info on affine transformations: en.Wikipedia.org/Affine_transformation
    More info on D2min: Falk, Langer (1998) Dynamics of viscoplastic
                        deformation in amorphous solids, PRE


    Parameters
    ----------
    xy_particle : 1-by-2 array of floats
        [x,y] position of the reference particle before displacement.
    xy_particle_next : 1-by-2 array of floats
        [x,y] position of the reference particle after displacement.
    xy_neighbors : n-by-2 array of floats
        [x,y] position of neighboring particles before displacement, where
        the row-index indicates the particle index.
    xy_neighbors_next : TYPE
        [x,y] position of neighboring particles before displacement, where
        the row-index indicates the particle index.
    avg_distance : float, optional
        Average distance between the particles (r of first peak of g(r)). Used
        to make D2min dimensionless. The default is 1.

    Returns
    -------
    d2min : float
        Measure of the non-affine displacement of the reference particle
        (xy_particle), with respect to its neighbors (xy_neighbors). The D2min
        is non-dimensionalized using the typical interparticle spacing
        (avg_distance)

    """
    if xy_neighbors.size > 0:
        nNeighbors = xy_neighbors.shape[0]
        xy_particle = np.append(xy_particle,
                                np.ones([1, 1])).reshape([1, 3], order='F')
        xy_particle_next = np.append(xy_particle_next, np.ones([1, 1])
                                     ).reshape([1, 3], order='F')
        xy_neighbors = np.append(xy_neighbors.transpose(), np.ones([nNeighbors, 1])
                                 ).reshape([nNeighbors, 3], order='F')
        xy_neighbors_next = np.append(xy_neighbors_next.transpose(),
                                      np.ones([nNeighbors, 1])
                                      ).reshape([nNeighbors, 3], order='F')
        
        try:
            M = np.linalg.lstsq(xy_neighbors, xy_neighbors_next, rcond=None)
            xy_neighbors_transformed = np.dot(M[0].transpose(),
                                              xy_neighbors.transpose()).transpose()
            xy_particle_transformed = np.dot(M[0].transpose(),
                                             xy_particle.transpose()).transpose()
            
            Rij_next = np.linalg.norm(xy_neighbors_next-xy_particle_next,
                                      ord=2, axis=1) # R_ij(t+dt)
            Rij_transformed = np.linalg.norm(xy_neighbors_transformed
                                             -xy_particle_transformed,
                                             ord=2, axis=1) # M*R_ij(t)
            d2min = np.sum(np.square(Rij_next-Rij_transformed))/(nNeighbors*avg_distance**2)
        except:
            d2min = float('NaN')
    else:
        d2min = float('NaN')
    return d2min

if __name__ == '__main__':
    pass