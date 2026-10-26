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

## Shortest Route Extraction
This notebook is purely to algorithmically select the core routes on the itiner-e network between the node points used in the M2PRM model. It is included here only for clarity and reproducibility.

This script takes a network input and a points file and snaps the points to the network to ensure complete alignment, and runs simple Dijkstra’s Algorithms between each unique pair and extracts only the simplest route between these. All of the routes between every unique pair are then combined to produce a much reduced but complete network.

## Supplementary Data
[Appendix A- LMUV Shapefile and Data](https://zenodo.org/records/23557511?preview=1&token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjU0YjMxZTY3LWExYjYtNDFmMi1hNGE2LTQ2ZWU2MDM4NGVjNiIsImRhdGEiOnt9LCJyYW5kb20iOiI4NWYxZmIwZjBkYTZlNTk3MDE1ZmFhMmMwYmRmYzExNyJ9.6Sra0lGVax3u6iAl09EftdDBp6S2QGFVZu1P22Yen1Tm4N_2CzMbtkSIYvIJuylIS_MmsTzcR5ISuihtX_iGWg)

[Appendix B- 11 Cost Surfaces](https://zenodo.org/records/23668328?preview=1&token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6ImQxMGYxZWRlLTc4N2MtNGY4MS04MDI2LThiMjM5NjczYzE4MyIsImRhdGEiOnt9LCJyYW5kb20iOiIwMDQ0NGM4NTJkMzUxOGM0MTliZmY0MzVmNWViMDYyYSJ9.XepPY178_D0mW6KDxlYYkR_wmBC6jkFNeJioB24XzWExVq_j8_V9OP-KKn7M3D9wZNn9-nVLU3ZpVZ92Gdj6YQ)

[Appendix C- 11 Probabilistic Cost Corridors](https://zenodo.org/records/23666989?preview=1&token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6ImFlNDU5NTM4LWU5NzAtNDBmMi05NDNhLWVmODQ5YmExY2VjYiIsImRhdGEiOnt9LCJyYW5kb20iOiIzMTNiYzAwZmYyYTlkNjllZjljZTU0ZjQzNmZlZDUyNSJ9.hUehnto0YL0gzGb6gGjEacjLr7XkByz0tcKM-BAuduxiNoyqh0vgJZ6_qF9XI0CJaQSQZ4_bFp53DbKgf5MXCw)




## Acknowledgements
This study was part of the project OneWorld (PID2023-152402NB-I00) funded by Spanish Ministry of Science, Innovation and Universities.
McLean was funded through the Marie Skłodowska-Curie Actions project, R3NUrb- HORIZON-MSCA-2021-PF-01-101109605.

## Authors
Andrew McLean amclean@bsc.es
Héctor A. Orengo horengo@bsc.es
