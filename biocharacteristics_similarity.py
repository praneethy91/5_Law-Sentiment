import configparser
import numpy as np
import os
import pickle as pck
import pandas as pd
import utils

# Reading values of the configuration file
config = configparser.ConfigParser()
config.read('config.ini')
case_similarities_dir = config['directories']['case_level_similarities']
vote_level_dataset = config['directories']['vote_level_dataset']
circuit_year_to_case_file = config['directories']['circuit_year_to_case_dataset']
bio_weighted_avg_file = config['directories']['biocharacteristics_weighted_avg']
bio_unweighted_avg_file = config['directories']['biocharacteristics_unweighted_avg']

case_data_df_iterator = pd.read_stata(vote_level_dataset, iterator=True, chunksize=1000)
bio_columns = ['x_dem', 'x_republican', 'x_instate_ba', 'x_elev', 'x_unity',
               'x_aba', 'x_crossa', 'x_pfedjdge', 'x_pindreg1', 'x_plawprof',
               'x_pscab', 'x_pcab', 'x_pusa', 'x_pssenate', 'x_paag', 'x_psp',
               'x_pslc', 'x_pssc', 'x_pshouse', 'x_psg', 'x_psgo', 'x_psenate',
               'x_psatty', 'x_pprivate', 'x_pmayor', 'x_plocct', 'x_phouse',
               'x_pgov', 'x_pda', 'x_pcc', 'x_pccoun', 'x_pausa', 'x_pasatty',
               'x_pag', 'x_pada', 'x_pgovt', 'x_llm_sjd', 'x_protestant',
               'x_evangelical', 'x_mainline', 'x_noreligion', 'x_catholic',
               'x_jewish', 'x_black', 'x_nonwhite', 'x_female', 'x_jd_public',
               'x_ba_public', 'x_b10s', 'x_b20s', 'x_b30s', 'x_b40s', 'x_b50s',
               'x_pbank', 'x_pmag', 'x_ageon40s', 'x_ageon50s', 'x_ageon60s',
               'x_ageon40orless', 'x_ageon70ormore', 'x_pago']

with open(circuit_year_to_case_file, 'rb') as f:
    ckt_case_map  = pck.load(f)

bio_weighted_dict = {}
bio_unweighted_dict = {}

bio_weighted_num_dict = {}
bio_unweighted_num_dict = {}

for (ckt, year), case_df in ckt_case_map.items():
    ckt = int(ckt)
    year = int(year)
    if year >= 1964:
        bio_weighted_dict[(ckt, year)] = {}
        bio_unweighted_dict[(ckt, year)] = {}
        bio_weighted_num_dict[(ckt, year)] = {}
        bio_unweighted_num_dict[(ckt, year)] = {}
        for bio_column in bio_columns:
            bio_weighted_dict[(ckt, year)][bio_column] = np.zeros(40, dtype=np.float64)
            bio_unweighted_dict[(ckt, year)][bio_column] = np.zeros(40, dtype=np.float64)
            bio_unweighted_num_dict[(ckt, year)][bio_column] = np.zeros(40, dtype=np.float64)
            bio_weighted_num_dict[(ckt, year)][bio_column] = np.zeros(40, dtype=np.float64)

chunk = 1
for case_data_df_chunk in case_data_df_iterator:
    for index, row in case_data_df_chunk.iterrows():
        ckt = row['Circuit']
        year = row['year']
        if(~ np.isfinite(ckt) or ~ np.isfinite(year)):
            continue
        year = int(row['year'])
        case = row['caseid']
        case_path = os.path.join(case_similarities_dir, str(year), (case.upper() + '-maj.p'))
        if os.path.isfile(case_path) and year >= 1964:
            with open(case_path, mode='rb') as f:
                case_similarity = pck.load(f)
                case_similarity = utils.normalize_similarity(case_similarity)
            for column in bio_columns:
                value = np.float64(row[column])
                if (~ np.isfinite(value)):
                    continue
                if np.min(case_similarity) <= 0.0:
                     print('Dangerous')
                bio_weighted_dict[(ckt, year)][column] = np.add(bio_weighted_dict[(ckt, year)][column], (value * case_similarity))
                bio_unweighted_dict[(ckt, year)][column] = np.add(bio_unweighted_dict[(ckt, year)][column], (value * np.ones(40, dtype=np.float64)))
                bio_weighted_num_dict[(ckt, year)][column] = np.add(bio_weighted_num_dict[(ckt, year)][column], case_similarity)
                bio_unweighted_num_dict[(ckt, year)][column] = np.add(bio_unweighted_num_dict[(ckt, year)][column], np.ones(40, dtype=np.float64))
    print('Chunk: ' + str(chunk))
    chunk += 1
    if chunk > 20:
        break

for (ckt, year), ls in ckt_case_map.items():
    ckt = int(ckt)
    year = int(year)
    if year >= 1964:
        for bio_column in bio_columns:
            if np.sum(bio_unweighted_num_dict[(ckt, year)][bio_column]) == 0.0:
                print('no valid bio characteristic for: Circuit:{0}, year:{1}, bio_column:{2}'.format(ckt, year, bio_column))
                continue
            bio_weighted_dict[(ckt, year)][bio_column] = np.divide(bio_weighted_dict[(ckt, year)][bio_column], bio_weighted_num_dict[(ckt, year)][bio_column])
            bio_unweighted_dict[(ckt, year)][bio_column] = np.divide(bio_unweighted_dict[(ckt, year)][bio_column], bio_unweighted_num_dict[(ckt, year)][bio_column])

# dump bio averages dictionary
for (ckt, year), trs in ckt_case_map.items():
    ckt = int(ckt)
    year = int(year)
    if year >= 1964:
        for bio_column in bio_columns:
            if np.min(bio_unweighted_dict[(ckt, year)][bio_column]) < 0.0 or np.max(bio_unweighted_dict[(ckt, year)][bio_column]) > 1.0:
                print('unweighted dictionary not between 0 and 1: Circuit:{0}, year:{1}, bio_column:{2}'.format(ckt, year, bio_column))
            if np.min(bio_weighted_dict[(ckt, year)][bio_column]) < 0.0 or bio_weighted_dict[(ckt, year)][bio_column] > 1.0:
                print('weighted dictionary not between 0 and 1: Circuit:{0}, year:{1}, bio_column:{2}'.format(ckt, year, bio_column))
        os.makedirs('data\\bioaverage\\' + str(ckt) + '_' + str(year), exist_ok=True)
        pck.dump(bio_weighted_dict[(ckt, year)], open('data\\bioaverage\\' + str(ckt) + '_' + str(year) + '\\bio_weighted_dict.pkl', 'wb'))
        pck.dump(bio_unweighted_dict[(ckt, year)], open('data\\bioaverage\\' + str(ckt) + '_' + str(year) + '\\bio_unweighted_dict.pkl', 'wb'))

# load bio averages dictionary
# for (ckt, year), gkhv in ckt_case_map.items():
#     ckt = int(ckt)
#     year = int(year)
#     if year >= 1964:
#         bio_weighted_dict = pck.load(open('data\\bioaverage\\' + str(ckt) + '_' + str(year) + '\\bio_weighted_dict.pkl', 'rb'))
#         bio_unweighted_dict = pck.load(open('data\\bioaverage\\' + str(ckt) + '_' + str(year) + '\\bio_unweighted_dict.pkl', 'rb'))
#         for bio_column in bio_columns:
#             print(bio_unweighted_dict[bio_column])