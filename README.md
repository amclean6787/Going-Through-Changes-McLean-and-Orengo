# Going Through Changes: The Impact of Seasonal Multifactor Costs for Modelling Past Mobility and Understanding Roman Urbanism
Andrew McLean and Héctor A. Orengo

This repository contains the source code for the paper submitted to the Journal of Archaeological Science.

## Cost Surface Generation
The cost surfaces are generated using GEE and openly accessible data. The script is ready to run and can be adjusted depending on user preference.

## Probabilistic Cost Corridor Model Generation
The Probabilistic Cost Corridor Model is generated through GRASS GIS called in a Jupyter notebook. The script must be run for each scenario individually and requires a point shapefile with the node sites and a cost surface raster. This takes two main steps.

### 1- Cost Corridor Generation and Normalisation
Here a cumulative cost surface (using r.cost) is generated for each of the defined node sites. The script is setup to run these in parallel. Each individual pair of node sites is then averaged, to produce a corridor between them. These are then normalised to values between 1-1000, before they can be merged.

### 2- Merging
With so many large rasters, a slightly more complex means of merging was utilised to combined all corridors. However, if a smaller case study is being used, a standard minimum cell stats merge can be used. Here, only individual pairs of corridors are merged in rounds, until only one final merged raster remains. Again, this is set up to be run in parallel.

The end result is a single raster for the Probabilistic Cost Corridor model.

## Small Scale Network Generation Loop
This script is purely to create a simple Probabilistic Cost Corridor Network between the 31 node sites for demonstration of the impact of multi factor multitemporal costs on route costs. It is included here only for clarity and reproducibility, and is not intended to be used to create a full network.

This loop skeletonises the Probabilistic Cost Corridor and ensures the node sites are all directly connected. It then uses the appropriate cost surface to apply costs to this skeletonised network. Cumulative cost surfaces from each node site are then generated across the network and the costs at every other node site sampled and added to a cost matrix. Producing 11 cost matrices where every unique route between node sites has a cost.

## Supplementary Data
Appendix A- 11 Cost Surfaces

Appendix B- 11 Probabilistic Cost Corridors

Appendix C- LMUV Shapefile and Data

Appendix D- Cost Matrices

## Acknowledgements
This study was part of the project OneWorld (PID2023-152402NB-I00) funded by Spanish Ministry of Science, Innovation and Universities.
McLean was funded through the Marie Skłodowska-Curie Actions project, R3NUrb- HORIZON-MSCA-2021-PF-01-101109605.

## Authors
Andrew McLean amclean@bsc.es
Héctor A. Orengo horengo@bsc.es
