import pandas as pd
import numpy as np

class mode_selection:
    def __init__(self, cs_stations: list, travellers_df: pd.DataFrame, num_of_selected_travellers: int,
                 mu_sv: float, sd_sv: float, mu_others: float, sd_others: float, mu_w: float, sd_w: float,
                 wwt_public: tuple, taxi_wt: tuple, num_of_selected_stations: int, trips_df: pd.DataFrame, seed):
        '''
        :param p:
        :param wwt_min: minimal walking/waiting time of public transit
        :param wwt_max: maximal walking/waiting time of public transit use [wwt_min, wwt_max] to generate random walking/waiting time
        :param seed: different seed values are used to generate varying instances under the same setting
                     (i.e., the same customer numbers and css quantities)
        '''

        self.cs_stations = cs_stations
        self.travellers_df = travellers_df
        self.trips_df = trips_df
        self.mu_sv = mu_sv
        self.sd_sv = sd_sv
        self.mu_others = mu_others
        self.sd_others = sd_others
        self.mu_w = mu_w
        self.sd_w = sd_w
        # walking/waiting time of public transit, taxi modes
        self.wwt_public = wwt_public
        self.taxi_wt = taxi_wt
        self.num_of_selected_stations = num_of_selected_stations
        self.num_of_selected_travellers = num_of_selected_travellers
        self.seed = seed

    def selected_data(self):
        # formalize the data structure of selected css/travellers to "string"
        # otherwise it will cause some incompatible problems of reading indices
        np.random.seed(self.seed)
        selected_css_str_list = []
        selected_travellers_str_list = []

        selected_cs_stations = list(np.random.choice(np.array(self.cs_stations), self.num_of_selected_stations, replace=False))
        for css in selected_cs_stations:
            selected_css_str_list.append(str(css))

        full_travellers = []

        for i in range(len(self.travellers_df)):
            traveller_id = self.travellers_df.iloc[i]['traveller_id']
            css_o = self.travellers_df.iloc[i]['css_o']
            css_d = self.travellers_df.iloc[i]['css_d']

            if css_o in selected_css_str_list and css_d in selected_css_str_list:
                full_travellers.append(traveller_id)

        np.random.seed(self.seed)
        selected_travellers = list(np.random.choice(np.array(full_travellers), self.num_of_selected_travellers, replace=False))
        for traveller in selected_travellers:
            selected_travellers_str_list.append(str(traveller))

        return selected_css_str_list, selected_travellers_str_list

    def vot_dict_generator(self, selected_travellers: list):
        # vot unit: Euro/hour
        np.random.seed(self.seed)
        vot_sv = np.random.lognormal(self.mu_sv, self.sd_sv, len(selected_travellers))
        vot_others = np.random.lognormal(self.mu_others, self.sd_others, len(selected_travellers))
        vot_ww = np.random.lognormal(self.mu_w, self.sd_w, len(selected_travellers))

        return vot_sv, vot_others, vot_ww

    def unit_transfer_to_min(self, duration):
        travel_time_min = 0
        if len(duration.split(' ')) == 2:
            travel_time_min = float(duration.split(' ')[0])
        elif len(duration.split(' ')) == 4:
            travel_time_min = float(duration.split(' ')[0] * 60 + duration.split(' ')[2])
        return travel_time_min

    def cs_customer_generator(self, selected_travellers: list, vot_sv: dict, vot_others: dict, vot_ww: dict,
                              cs_pick_up_fee: dict, cs_min_fee: float, public_ticket, taxi_fee):

        '''
        :param selected_travellers:
        :param dict_vot:
        :return: dictionary of requests
        {'r0': ('traveller_1', 'l1'), 'r1': ('traveller_2', 'l1'), ...},...,}
        '''

        Dict_requests = {}  # initialize the dictionary of all requests
        request_no = 0
        np.random.seed(self.seed)
        wwt_public = list(np.random.uniform(self.wwt_public[0], self.wwt_public[1], len(selected_travellers)))
        wt_taxi = list(np.random.uniform(self.taxi_wt[0], self.taxi_wt[1], len(selected_travellers)))

        """
        # compute the utilities of different transport modes for each traveller
        """
        for i in range(len(selected_travellers)):
            traveller_idx = selected_travellers[i]
            df_idx = self.trips_df[self.trips_df['traveller_id'] == traveller_idx].index.tolist()[0]

            # transfer the travel time in hour into travel time in minute
            public_time_in_min = self.unit_transfer_to_min(self.trips_df.iloc[df_idx]['public_duration'])
            cs_time_in_min = self.unit_transfer_to_min(self.trips_df.iloc[df_idx]['cs_duration'])
            taxi_time_in_min = self.unit_transfer_to_min(self.trips_df.iloc[df_idx]['taxi_duration'])
            wt_css_in_min = float(self.trips_df.iloc[df_idx]['wt_css'])

            # calculate travel costs of each transport mode
            # calculate the cs travel costs for each pick_up level and store in cs_costs dictionary
            cs_costs = {}
            for level in cs_pick_up_fee.keys():
                cs_cost_at_level = cs_pick_up_fee[level] + cs_min_fee * cs_time_in_min + \
                                   vot_sv[i] / 60 * (cs_time_in_min) + vot_ww[i] / 60 * wt_css_in_min
                cs_costs[level] = cs_cost_at_level

            # travel costs
            public_cost = public_ticket + vot_others[i] / 60 * (public_time_in_min - wwt_public[i]) + \
                          vot_ww[i] / 60 * wwt_public[i]
            taxi_cost = taxi_fee + vot_others[i] / 60 * taxi_time_in_min + vot_ww[i] / 60 * wt_taxi[i]

            highest_pricing_level = 0
            pricing_list = list(cs_pick_up_fee.keys())
            pricing_list.reverse()

            min_travel_cost = min(public_cost, taxi_cost)
            for level in pricing_list:
                current_level_fee = cs_costs[level]
                if current_level_fee <= min_travel_cost:
                    # min_travel_cost = current_level_fee
                    highest_pricing_level = level
                    # print(traveller_idx, 'cs is selected at pricing level', level)
                    break

            if highest_pricing_level != 0:
                Dict_requests[traveller_idx] = ('r' + str(request_no), highest_pricing_level)
                request_no = request_no + 1

        return Dict_requests





