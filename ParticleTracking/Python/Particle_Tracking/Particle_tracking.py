# -*- coding: utf-8 -*-
"""
Contributors : Lars Kool
Affiliations : Laboratoire Physique et Méchanique des Milieux Hétérogènes
(PMMH), ESPCI, Paris, France
               
This project has received funding from the European Union’s Horizon 2020
research and innovation programme under the Marie Skłodowska-Curie grant
agreement No. 813162
More info on this programme: https://caliper-itn.org/
"""

from track_particles import track_particles

datapath = r'E:\Lars\Oscillatory Compression\20201103 Creep\test\Preprocessed\V1'
dataFormat = 'pkl'
minLength = 2
search_range = 25

track_particles(datapath, dataFormat, minLength, search_range)