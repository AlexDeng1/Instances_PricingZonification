import argparse
import math

def get_args():
    parser = argparse.ArgumentParser(description='Generate instances...')

    # instance args
    parser.add_argument('-i', '--name_of_instance', type=str, default='k400-v200')
    parser.add_argument('-s', '--seed_number', type=int, default=3)
    parser.add_argument('-seeds', '--seed_numbers', type=list, default=[0, 1, 2, 3, 9])
    parser.add_argument('-nc', '--num_of_customers', type=int, default=100)
    parser.add_argument('-nv', '--num_of_vehicles', type=int, default=25)
    parser.add_argument('-ns', '--num_of_selected_css', type=int, default=20)
    parser.add_argument('-nz', '--number_of_zones', type=int, default=5)

    # problem args
    parser.add_argument('--cs_min_fee', type=float, default=0.3)
    parser.add_argument('--pricing_levels', type=dict, default={0: -2, 1: -1, 2: 0, 3: 1, 4: 2})

    # parameters in mode selection
    # waiting and/walking time
    parser.add_argument('--taxi_wt', type=tuple, default=(4, 8))
    parser.add_argument('--wwt_public', type=tuple, default=(4, 12))
    parser.add_argument('--taxi_fee', type=float, default=3.89)
    parser.add_argument('--taxi_min_fee', type=float, default=2.55)
    parser.add_argument('--public_ticket', type=float, default=3.22)

    # preference parameters in utility functions
    parser.add_argument('--mu_sv', type=float, default=math.log(17.43))
    parser.add_argument('--mu_others', type=float, default=math.log(18.94))
    parser.add_argument('--mu_ww', type=float, default=math.log(70.45))
    parser.add_argument('--sd_sv', type=float, default=0.4)
    parser.add_argument('--sd_others', type=float, default=0.4)
    parser.add_argument('--sd_ww', type=float, default=0.4)

    # file path args
    parser.add_argument('--storage_data_path', type=str, default="../Instances/", help='Path to data.')

    args = parser.parse_args()

    return args