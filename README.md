# MODUS

The 'MOdèle de Déplacements Urbains et Suburbains' is used to model travel in the Ile de France Region of France. 

It is a four step travel demand model that estimates travel demand according to the following schema: 

![Modèle4étapes](https://user-images.githubusercontent.com/61752640/154925037-200f35e1-79c1-4ca1-acc6-edf54744171e.png)

Travel demand is estimated by answering four successive questions:
1. Who travels? (Trip generation) - The number of trips generated and attracted by each zone is estimated, based on the socio-économic characteristics of the zone.
2. Where do they go? (Trip distribution) - A gravity model is used to estimate the destination choices as a function of the generalized cost of travel.
3. What mode is used? (Modal choice) - The number of trips choosing each of the available modes can be selected based on the generalized cost of travel with that mode, by applying random utility theory.
4. What route is used? (Route selection) - The number of users on each potential route is estimated such that for each user there is no alternative route to their destination that would allow them to reduce their travel costs. 

## Input Data
1. The volume and spatial distribution of population and employment in Ile de France. This is used to define the zoning used in the model.
![1024px-ZonageMODUS](https://user-images.githubusercontent.com/61752640/154927777-0c04cb97-72f3-412c-aac2-3229a9514e5f.png)

2. The transport supply. This is in the form of the spatial layout of the public transport routes, the road network, the travel times, the frequency along public transport lines, etc.
3. Travel behaviour information. This is obtained through household travel surveys, which are used to calibrate the various sub-models of the four step model. 

## Outputs
1. General travel characteristics for the situation under consideration. These are mainly the trip volumes, modal shares, spatial distribution of mobility, etc.
2. The traffic on different routes and public transport lines, and the associated level of service.

## Structure of the Model
The structure of the model is as shown below:

![image](https://user-images.githubusercontent.com/61752640/154929787-a7e32311-7be9-495b-bdee-4b76287ea8b5.png)
