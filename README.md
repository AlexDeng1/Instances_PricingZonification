# Instances_ZonificationandPricing
This repository contains codes and data for generating instances in the article ''Zonification and Pricing: Formulations and Exact Solutions'' by J. Deng and G. Pantuso. The instance generator is written in Python, whose taken parameters have been thoroughly described in the article. This respository contains 4 folders. The [Input_data](./Input_data/) folder contains geographic data of carsharing stations and potential customers. The [Instance_generation](./Instance_generation/) folder contains codes that process the input data for generating instances. The [Instances](./Instances/) folder contains .csv files storing the information of potential customers and vehicles associated with generated instances. The [Results](./Results/) folder contains detailed computational results of individual instances.

# Input data
* [css_list.csv](/Input_data/css_list.csv): each row describes index, name, respective district, geographic coordinates (lat, lng) of a carsharing station.
* [css_distance_matrix.csv](/Input_data/css_distance_matrix.csv): each row presents distances and travel durations between two carsharing stations.
* [travellers_fromPOIs.csv](/Input_data/travellers_fromPOIs.csv): each row presents the geographic coordinates of each customer's origin and destination, as well as the coordinates of his/her nearset origin and destination carsharing stations.
* [trips_toModes.csv](/Input_data/trips_toModes.csv): each row describes the travel times of a customer by taking different transport modes.

# Instance generation
The [instance_generator.py](/Instance_generation/instance_generator.py) can be used to generate instances of different sizes, especially by controlling the following command line arguments.
* -nc the number of cutsomers
* -nv the number of vehicles
* -ns the number of carsharing stations
* -nz the number of zones
* -s the random seed number

# Instances
In this article we generated two sets of instances, which are small ones with 10 stations and larger ones with 20 stations. Corresponding data of these instances are stored in folders [small_instances](/Instances/small_instances/) and [large_instances](/Instances/larger_instances/), respectively. These .csv files collect information of randomly generated customers and randomly generated vehciles. In each .csv file, the columns used to store customers' data are as follows:
* traveller_id: the id of traveller
* cus_o: name of the nearest origin carsharing station
* cus_d: name of the nearest destination carsharing station
* highest_pl: the highest pricing level that is acceptable for the customer to choose carsharing service
* whether_request: takes value "Y" if the customer becomes a valid request, "N", otherwise

As for the vehicles, we merely store their initial locations after the rows of customers in each .csv file. 

Note that customer and vehicle data in each .csv file are used for instances with varying numbers of zones. As an example, [K400V100seed0](/Instances/larger_instances/K400V100seed0.csv) generated at random seed 0 is used for all instances with 400 customers, 100 vehicles and any number of zones ( i.e., S=3, 4, or 5), which correspond to instances K400V100S3seed0, K400V100S4seed0, K400V100S5seed0 in the article.

# Results
The [Results](/Results/) folder contains **computational performance data** of all small and larger instances, as well as **system performance data** of the tested instances in profit and econimic effect analysis part.
## Computational performance results
For small instances, we compare the solution times of instances reported by the solver through implementing different formulations, which are ''Original", "WF" and "CGLM" as discussed in the article. Solution times are also distiguished when no valid inequalities (i.e., No VIs) and different combinations of valid inequalities (i.e., VI1, VI2, and VI1&2) are implemented. Corresponding results are reported in [solver_small_3zones.csv](/Results/small_instances/solver_small_3zones.csv), [solver_small_4zones.csv](/Results/small_instances/solver_small_4zones.csv), and [solver_small_5zones.csv](/Results/small_instances/solver_small_5zones.csv) for small instances with 3, 4, and 5 zones, respectively.

Similar computational time results are reported when implementing Benders decomposition algorithm with or without additions of valid inequalities. Corresponding results are collected in [bd_small_3zones](/Results/small_instances/bd_small_3zones.csv), [bd_small_4zones](/Results/small_instances/bd_small_4zones.csv), and [bd_small_5zones](/Results/small_instances/bd_small_5zones.csv) data files for small instances with 3, 4, and 5 zones, respectively. 

For larger instances, we solve these instances by implementing the best performed "CGLM" formulation with the addition of VI1 and VI2. For each instance we compare the solution times and optimality gaps delivered by the solver and the BD algorithm. Corresponding results are shown in [larger_instance results](/Results/larger_instances/) folder.

## System performance results
For the system performance analysis and discussion, we report the following detailed results in individual-instance level.
* Carsharing system profits: reported in [profits_3zones](/Results/system_performance/Net_profits_3zones.csv), [profits_4zones](/Results/system_performance/Net_profits_4zones.csv), and [profits_5zones](/Results/system_performance/Net_profits_5zones.csv) data files.
* Service rates: reported in the[service_rates](/Results/system_performance/Service%20rates_3zones.csv) data file.
* Profits and costs for individual customers: results for all tested instances are collected in the [Individual profit & cost record](/Results/system_performance/Individual%20profit&cost%20record(zonification_granularity)/) folder.
