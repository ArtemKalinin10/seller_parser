import time
from datetime import timedelta
import datetime
import re
import json
import undetected_chromedriver as uc
from undetected_chromedriver import By


class Seller:
    def __init__(self):
        
        self.MONTHS = {
            "января": 1,
            "февраля": 2,
            "марта": 3,
            "апреля": 4,
            "мая": 5,
            "июня": 6,
            "июля": 7,
            "августа": 8,
            "сентября": 9,
            "октября": 10,
            "ноября": 11,
            "декабря": 12
        }
        
        self.links = {0: [{'link': 'https://www.avito.ru/krasnodar/odezhda_obuv_aksessuary/dzhinsy_camp_david_true_religion_type_7937476736?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7937476736', 'time': datetime.datetime(2026, 2, 1, 21, 29), 'price': '3500'},
                          {'link': 'https://www.avito.ru/volgograd/odezhda_obuv_aksessuary/dzhinsy_true_religion_klesh_24_bootcut_7959900016?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7959900016', 'time': datetime.datetime(2026, 2, 1, 21, 26), 'price': '4000'},
                          {'link': 'https://www.avito.ru/sankt-peterburg/odezhda_obuv_aksessuary/dzhinsy_true_religion_original_7887355779?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7887355779', 'time': datetime.datetime(2026, 2, 1, 20, 38), 'price': '6999'},
                          {'link': 'https://www.avito.ru/sankt-peterburg/odezhda_obuv_aksessuary/dzhinsy_true_religion_7896092308?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7896092308', 'time': datetime.datetime(2026, 2, 1, 20, 15), 'price': '1750'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_muzhskie_true_religion_joey_klesh_original_7967325761?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7967325761', 'time': datetime.datetime(2026, 2, 1, 20, 11), 'price': '10999'},
                          {'link': 'https://www.avito.ru/sankt-peterburg/odezhda_obuv_aksessuary/dzhinsy_true_religion_7914146194?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7914146194', 'time': datetime.datetime(2026, 2, 1, 19, 33), 'price': '5000'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_true_religion_arhivnye_7887556550?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7887556550', 'time': datetime.datetime(2026, 2, 1, 19, 27), 'price': '7990'},
                          {'link': 'https://www.avito.ru/velikiy_novgorod/odezhda_obuv_aksessuary/dzhinsy_archive_double_you_7906758165?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7906758165','time': datetime.datetime(2026, 2, 1, 21, 32), 'price': '2260'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/muzhskie_golubye_dzhinsy_route_one_original_7852089253?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7852089253', 'time': datetime.datetime(2026, 2, 1, 21, 12), 'price': '3490'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_shirokie_balenciaga_type_7941259753?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7941259753', 'time': datetime.datetime(2026, 2, 1, 21, 9), 'price': '1990'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_off_street_7906997611?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7906997611', 'time': datetime.datetime(2026, 2, 1, 21, 5), 'price': '5990'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/levis_premium_501_original_31x32_original_7860691727?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7860691727', 'time': datetime.datetime(2026, 2, 1, 21, 3), 'price': '9990'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_type_acne_studios_x_jaded_london_7899562223?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7899562223', 'time': datetime.datetime(2026, 2, 1, 21, 3), 'price': '2600'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_archive_type_7859964329?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7859964329', 'time': datetime.datetime(2026, 2, 1, 21, 2), 'price': '2815'},
                          {'link': 'https://www.avito.ru/sankt-peterburg/odezhda_obuv_aksessuary/dzhinsy_levis_501_lmn_original_novye_7936329178?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7936329178', 'time': datetime.datetime(2026, 2, 1, 20, 56), 'price': '3499'},
                          {'link': 'https://www.avito.ru/rybinsk/odezhda_obuv_aksessuary/dzhinsy_shirokie_type_balenciaga_acne_zak_7895960511?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7895960511', 'time': datetime.datetime(2026, 2, 1, 20, 48), 'price': '2790'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_shirokie_balenciaga_type_archive_8013413119?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 8013413119', 'time': datetime.datetime(2026, 2, 1, 20, 28), 'price': '2990'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_shirokie_vetemets_type_7847528974?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7847528974', 'time': datetime.datetime(2026, 2, 1, 20, 24), 'price': '1990'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_jaded_london_original_7929081885?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7929081885', 'time': datetime.datetime(2026, 2, 1, 20, 24), 'price': '3899'},
                          {'link': 'https://www.avito.ru/rostov-na-donu/odezhda_obuv_aksessuary/dzhinsy_fcniubi_kak_polar_big_boy_empyre_7967652530?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7967652530', 'time': datetime.datetime(2026, 2, 1, 20, 15), 'price': '1300'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/levis_505-4891_made_in_u.s.a._33x30_vintazh_1996g_7860212484?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7860212484', 'time': datetime.datetime(2026, 2, 1, 20, 0), 'price': '26500'},
                          {'link': 'https://www.avito.ru/krasnodar/odezhda_obuv_aksessuary/dzhinsy_turetskie_kachestvennye_muzhskip_demisezonnye_7958861860?context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7958861860', 'time': datetime.datetime(2026, 2, 1, 20, 9), 'price': '4700'},
                          {'link': 'https://www.avito.ru/sankt-peterburg/odezhda_obuv_aksessuary/dzhinsy_tom_tailor_3234_7937058641?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7937058641', 'time': datetime.datetime(2026, 2, 1, 19, 44), 'price': '1799'},
                          {'link': 'https://www.avito.ru/rybinsk/odezhda_obuv_aksessuary/dzhinsy_klesh_type_zara_flared_kak_u_gabanny_zak_7896412229?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7896412229', 'time': datetime.datetime(2026, 2, 1, 19, 26), 'price': '2990'},
                          {'link': 'https://www.avito.ru/sankt-peterburg/odezhda_obuv_aksessuary/dzhinsy_levis_501_3436_7936237676?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7936237676', 'time': datetime.datetime(2026, 2, 1, 19, 17), 'price': '3000'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_slimfit_chernye_amiri_type_7852275516?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7852275516', 'time': datetime.datetime(2026, 2, 1, 19, 5), 'price': '1490'},
                          {'link': 'https://www.avito.ru/sankt-peterburg/odezhda_obuv_aksessuary/dzhinsy_cash_on_delivery_by_joker_3334_7937621342?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7937621342', 'time': datetime.datetime(2026, 2, 1, 19, 2), 'price': '1999'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_sakura_y2k_7899615364?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7899615364', 'time': datetime.datetime(2026, 2, 1, 19, 2), 'price': '2990'},
                          {'link': 'https://www.avito.ru/pskov/odezhda_obuv_aksessuary/dzhinsy_levis_514_7915732857?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7915732857', 'time': datetime.datetime(2026, 2, 1, 18, 50), 'price': '1990'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_no_faith_studios_cargo_tripp_nyc_opium_7869929992?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7869929992', 'time': datetime.datetime(2026, 2, 1, 18, 43), 'price': '3280'},
                          {'link': 'https://www.avito.ru/nizhniy_tagil/odezhda_obuv_aksessuary/dzhinsy_germ._brend_esprit_8013738585?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 8013738585', 'time': datetime.datetime(2026, 2, 1, 18, 41), 'price': '1100'},
                          {'link': 'https://www.avito.ru/sankt-peterburg/odezhda_obuv_aksessuary/dzhinsy_alessandro_salvarini_3632_7937536736?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7937536736', 'time': datetime.datetime(2026, 2, 1, 18, 29), 'price': '1799'},
                          {'link': 'https://www.avito.ru/chelyabinsk/odezhda_obuv_aksessuary/dzhinsy_muzhskie_7900188205?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7900188205', 'time': datetime.datetime(2026, 2, 1, 18, 28), 'price': '2000'},
                          {'link': 'https://www.avito.ru/moskva_zelenograd/odezhda_obuv_aksessuary/muzhskie_dzhinsy_diesel_viker_2832_7937236274?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7937236274', 'time': datetime.datetime(2026, 2, 1, 18, 28), 'price': '5434'},
                          {'link': 'https://www.avito.ru/nizhniy_novgorod/odezhda_obuv_aksessuary/dzhinsy_soul_star_l_50-52_7887459699?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7887459699', 'time': datetime.datetime(2026, 2, 1, 18, 13), 'price': '2600'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_celine_7816418055?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7816418055', 'time': datetime.datetime(2026, 2, 1, 18, 10), 'price': '11900'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_rick_owens_bolans_bootcut_faded_mineral_7869690116?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7869690116', 'time': datetime.datetime(2026, 2, 1, 18, 9), 'price': '5990'}, 
                          {'link': 'https://www.avito.ru/sankt-peterburg/odezhda_obuv_aksessuary/dzhinsy_burberry_flared_jeans_7899402450?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7899402450', 'time': datetime.datetime(2026, 2, 1, 18, 5), 'price': '3700'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_rick_owens_bolans_bootcut_leather_mainline_7869738060?slocation=621540&context=H4sIAAAAAAAA_wF_AID_YTo0OntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czozOiJzcmMiO3M6MTA6ImJyb2FkbWF0Y2giO3M6MTE6IndpZGdldFRpdGxlIjtOO3M6MToieCI7czozMToiYzAxYXdhcmhsNHVsZDBoYXlyMjRnaml6d2RjOGg5NCI7fQAC77d_AAAA', 'id': '№ 7869738060', 'time': datetime.datetime(2026, 2, 1, 18, 5), 'price': '5990'},
                          {'link': 'https://www.avito.ru/vidnoe/odezhda_obuv_aksessuary/dzhinsy_true_religion_7896169584?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7896169584', 'time': datetime.datetime(2026, 2, 1, 19, 8), 'price': '4395'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_true_religion_straight_swag_7899561793?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7899561793', 'time': datetime.datetime(2026, 2, 1, 18, 45), 'price': '11350'},
                          {'link': 'https://www.avito.ru/voronezh/odezhda_obuv_aksessuary/dzhinsy_true_religion_ricky_relaxed_straight_belye_7886172658?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7886172658', 'time': datetime.datetime(2026, 2, 1, 18, 31), 'price': '4500'},
                          {'link': 'https://www.avito.ru/irkutsk/odezhda_obuv_aksessuary/dzhinsy_true_religion_7929779462?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7929779462', 'time': datetime.datetime(2026, 2, 1, 18, 2), 'price': '5494'},
                          {'link': 'https://www.avito.ru/vyshniy_volochek/odezhda_obuv_aksessuary/dzhinsy_true_religion_7967384178?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7967384178', 'time': datetime.datetime(2026, 2, 1, 17, 57), 'price': '799'},
                          {'link': 'https://www.avito.ru/balashiha/odezhda_obuv_aksessuary/dzhinsy_true_religion_big_t_7893341982?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7893341982', 'time': datetime.datetime(2026, 2, 1, 17, 51), 'price': '6500'},
                          {'link': 'https://www.avito.ru/petrozavodsk/odezhda_obuv_aksessuary/dzhinsy_true_religion_bootcut_usa_7816739370?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7816739370', 'time': datetime.datetime(2026, 2, 1, 17, 16), 'price': '8500'}, 
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_true_religion_straight_chain_logo_7955447513?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7955447513', 'time': datetime.datetime(2026, 2, 1, 17, 6), 'price': '8800'}, 
                          {'link': 'https://www.avito.ru/izhevsk/odezhda_obuv_aksessuary/dzhinsy_true_religion_billy_super_qt_redkie_7929842984?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7929842984', 'time': datetime.datetime(2026, 2, 1, 17, 3), 'price': '5800'},
                          {'link': 'https://www.avito.ru/rybinsk/odezhda_obuv_aksessuary/dzhinsy_true_religion_kak_u_slatt_savage_7898474682?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7898474682', 'time': datetime.datetime(2026, 2, 1, 17, 2), 'price': '6557'},
                          {'link': 'https://www.avito.ru/chelyabinsk/odezhda_obuv_aksessuary/dzhinsy_true_religion_ricky_fit_7929805785?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7929805785', 'time': datetime.datetime(2026, 2, 1, 16, 41), 'price': '3500'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_true_religion_7966932141?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7966932141', 'time': datetime.datetime(2026, 2, 1, 16, 41), 'price': '5990'}, 
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/true_religion_jennie_mid_rise_sn_skinny_7886793131?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7886793131', 'time': datetime.datetime(2026, 2, 1, 16, 24), 'price': '7650'},
                          {'link': 'https://www.avito.ru/shadrinsk/odezhda_obuv_aksessuary/dzhinsy_true_religion_7955471764?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7955471764', 'time': datetime.datetime(2026, 2, 1, 16, 18), 'price': '2500'}, 
                          {'link': 'https://www.avito.ru/perm/odezhda_obuv_aksessuary/dzhinsy_true_religion_chernye_7915914714?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7915914714', 'time': datetime.datetime(2026, 2, 1, 16, 4), 'price': '1990'},
                          {'link': 'https://www.avito.ru/saratov/odezhda_obuv_aksessuary/dzhinsy_true_religion_7957918080?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7957918080', 'time': datetime.datetime(2026, 2, 1, 15, 52), 'price': '4945'}, 
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_laguna_beach_7895993263?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7895993263', 'time': datetime.datetime(2026, 2, 1, 15, 49), 'price': '10500'},
                          {'link': 'https://www.avito.ru/simferopol/odezhda_obuv_aksessuary/dzhinsy_true_religion_7858780357?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7858780357', 'time': datetime.datetime(2026, 2, 1, 15, 42), 'price': '1500'}, 
                          {'link': 'https://www.avito.ru/kurovskoe/odezhda_obuv_aksessuary/dzhinsy_true_religion_belye_7867439605?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7867439605', 'time': datetime.datetime(2026, 2, 1, 15, 31), 'price': '4000'},
                          {'link': 'https://www.avito.ru/nahodka/odezhda_obuv_aksessuary/dzhinsy_true_religion_baggy_jeans_7955848043?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7955848043', 'time': datetime.datetime(2026, 2, 1, 15, 29), 'price': '3490'},
                          {'link': 'https://www.avito.ru/ryazan/odezhda_obuv_aksessuary/dzhinsy_true_religion_7936688570?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7936688570', 'time': datetime.datetime(2026, 2, 1, 14, 40), 'price': '3296'}, 
                          {'link': 'https://www.avito.ru/surgut/odezhda_obuv_aksessuary/true_religion_ricky_34_7906447945?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7906447945', 'time': datetime.datetime(2026, 2, 1, 14, 8), 'price': '6000'}, 
                          {'link': 'https://www.avito.ru/samara/odezhda_obuv_aksessuary/dzhinsy_true_religion_ricky_relaxed_straight_7955457000?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7955457000', 'time': datetime.datetime(2026, 2, 1, 13, 58), 'price': '7300'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_true_religion_7936341146?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7936341146', 'time': datetime.datetime(2026, 2, 1, 12, 36), 'price': '7500'},
                          {'link': 'https://www.avito.ru/kazan/odezhda_obuv_aksessuary/dzhinsy_true_religion_original_8013888799?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 8013888799', 'time': datetime.datetime(2026, 2, 1, 12, 24), 'price': '4000'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_true_religion_flared_7915691373?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7915691373', 'time': datetime.datetime(2026, 2, 1, 12, 27), 'price': '13000'},
                          {'link': 'https://www.avito.ru/nefteyugansk/odezhda_obuv_aksessuary/dzhinsy_true_religion_34_original_7955830583?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7955830583', 'time': datetime.datetime(2026, 2, 1, 12, 1), 'price': '7000'}, 
                          {'link': 'https://www.avito.ru/tolyatti/odezhda_obuv_aksessuary/dzhinsy_true_religion_shirokie_7915848908?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7915848908', 'time': datetime.datetime(2026, 2, 1, 11, 57), 'price': '5500'},
                          {'link': 'https://www.avito.ru/barnaul/odezhda_obuv_aksessuary/dzhinsy_true_religion_original_7847724938?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7847724938', 'time': datetime.datetime(2026, 2, 1, 11, 41), 'price': '4400'}, 
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_true_religion_7914053535?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7914053535', 'time': datetime.datetime(2026, 2, 1, 11, 35), 'price': '7000'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_true_religion_billy_bigt_original_7869729767?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7869729767', 'time': datetime.datetime(2026, 2, 1, 11, 9), 'price': '5692'},
                          {'link': 'https://www.avito.ru/kaluga/odezhda_obuv_aksessuary/dzhinsy_cipobaxx_7847471604?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7847471604', 'time': datetime.datetime(2026, 2, 1, 11, 1), 'price': '4000'},
                          {'link': 'https://www.avito.ru/omsk/odezhda_obuv_aksessuary/dzhinsy_true_religion_klesh_original_7906825001?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7906825001', 'time': datetime.datetime(2026, 2, 1, 10, 39), 'price': '4615'}, 
                          {'link': 'https://www.avito.ru/omsk/odezhda_obuv_aksessuary/dzhinsy_true_religion_7888194373?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7888194373', 'time': datetime.datetime(2026, 2, 1, 10, 35), 'price': '9450'}, 
                          {'link': 'https://www.avito.ru/omsk/odezhda_obuv_aksessuary/dzhinsy_true_religion_ricky_super_t_7888397540?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7888397540', 'time': datetime.datetime(2026, 2, 1, 10, 32), 'price': '8500'}, 
                          {'link': 'https://www.avito.ru/vladivostok/odezhda_obuv_aksessuary/true_religion_ricky_7941463611?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7941463611', 'time': datetime.datetime(2026, 2, 1, 10, 13), 'price': '1900'}, 
                          {'link': 'https://www.avito.ru/kursk/odezhda_obuv_aksessuary/dzhinsy_true_religion_slim_fit_7895996627?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7895996627', 'time': datetime.datetime(2026, 2, 1, 5, 41), 'price': '1690'}, 
                          {'link': 'https://www.avito.ru/petrozavodsk/odezhda_obuv_aksessuary/true_religion_jeans_camo_7915491661?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7915491661', 'time': datetime.datetime(2026, 2, 1, 5, 30), 'price': '9990'},
                          {'link': 'https://www.avito.ru/novopetrovskoe/odezhda_obuv_aksessuary/dzhinsy_true_religion_7905997640?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7905997640', 'time': datetime.datetime(2026, 2, 1, 4, 34), 'price': '6557'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_true_religion_type_archive_japan_7896031872?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7896031872', 'time': datetime.datetime(2026, 2, 1, 4, 8), 'price': '6666'},
                          {'link': 'https://www.avito.ru/egorevsk/odezhda_obuv_aksessuary/dzhinsy_true_religion_muzhskie_7914447108?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7914447108', 'time': datetime.datetime(2026, 2, 1, 3, 41), 'price': '7000'},
                          {'link': 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dzhinsy_true_religion_29_7893868654?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7893868654', 'time': datetime.datetime(2026, 2, 1, 3, 20), 'price': '2700'},
                          {'link': 'https://www.avito.ru/sankt-peterburg/odezhda_obuv_aksessuary/dzhinsy_true_religion_7914121365?slocation=621540&context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNcjdkZkZEdVNXMFJtaGlUIjt9FFIvUj8AAAA', 'id': '№ 7914121365', 'time': datetime.datetime(2026, 2, 1, 3, 4), 'price': '3500'}]}
        
        with open("clothes.json", 'r', encoding="utf-8") as file:
            data = json.load(file)
            res = {i: item for i, item in enumerate(data)}
        self.res = res
        
        
        options = uc.ChromeOptions()

        #options.add_argument("--headless=new")  # важно: new
        options.page_load_strategy = 'eager' 
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")

        self.driver = uc.Chrome(
            version_main=144,
            options=options
        )
    
    def __get_source__(self, id: int):
        self.driver.get(self.res[id]["path"])
        time.sleep(3)
        try:
            self.driver.find_element(By.CSS_SELECTOR, '[data-marker="page-title/text"]')
        except Exception:
            self.__get_source__(id)
        else:
            print(f"все окей для ссылки {id}")
            time.sleep(1)
    
    def __scroll_to_bottom__(self, pause=0.5, step=1200, max_scrolls=50):
        last_height = self.driver.execute_script("return window.pageYOffset + window.innerHeight")
        total_height = self.driver.execute_script("return document.body.scrollHeight")

        scrolls = 0
        while last_height < total_height and scrolls < max_scrolls:
            self.driver.execute_script(f"window.scrollBy(0, {step});")
            time.sleep(pause)

            last_height = self.driver.execute_script("return window.pageYOffset + window.innerHeight")
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            scrolls += 1
            
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        
    def __converting_time__(self, date_str: str) -> datetime:
        now = datetime.datetime.now()
        
        date_str = date_str.lower().strip()
        
        if "сегодня" in date_str:
            time_part = re.search(r'(\d{1,2}:\d{2})', date_str).group(1)
            hour, minute = map(int, time_part.split(":"))
            return datetime.datetime(now.year, now.month, now.day, hour, minute)
        
        elif "вчера" in date_str:
            time_part = re.search(r'(\d{1,2}:\d{2})', date_str).group(1)
            hour, minute = map(int, time_part.split(":"))
            yesterday = now - timedelta(days=1)
            return datetime.datetime(yesterday.year, yesterday.month, yesterday.day, hour, minute)
        
        else:
            # формат '29 января в 21:33'
            day, month_str, time_part = re.search(r'(\d{1,2}) (\w+) в (\d{1,2}:\d{2})', date_str).groups()
            day = int(day)
            month = self.MONTHS[month_str]
            hour, minute = map(int, time_part.split(":"))
            # Если месяц позже текущего, значит это прошлый год
            year = now.year if month <= now.month else now.year - 1
            return datetime.datetime(year, month, day, hour, minute)
        
    
    def __scrap_cloth__(self, link: str) -> list:
        self.driver.get(link)
        time.sleep(2)
        price = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="item-view/item-price"]').get_attribute("content")
        time_ = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="item-view/item-date"]').text
        cloth_id = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="item-view/item-id"]').text
        return [time_, price, cloth_id]
    
    def __scrap_links__(self, id: int):
        items = self.driver.find_elements(By.CSS_SELECTOR, '[data-marker="item"]')
        links = []
        for item in items:
            links.append(item.find_element(By.CSS_SELECTOR, '[data-marker="item-photo-sliderLink"]').get_attribute("href"))
        
        links_per_cource = self.links.get(id, [])
        add_flag = True if links_per_cource else False
        res_links = []
        
        for link in links:
            time_, price, cloth_id = self.__scrap_cloth__(link)
            converted_time = (datetime.datetime.now() - self.__converting_time__(time_)).days
            time_ = self.__converting_time__(time_)
            if converted_time <= 7:
                if add_flag is False:
                    links_per_cource.append({"link": link, "id": cloth_id, "time": time_, "price": price})
                elif add_flag:
                    if time_ < links_per_cource[0]["time"] and cloth_id not in [i["id"] for i in links_per_cource]: 
                        res_links.append({"link": link, "id": cloth_id, "time": time_, "price": price})
                    else:
                        break
            else:
                break
            
        if add_flag is False:
            res_links = links_per_cource
        elif add_flag:
            for el in res_links[::-1]:
                links_per_cource.insert(0, el)
        self.links[id] = links_per_cource
        print(res_links)
    
    def scrap(self):
        self.__get_source__(0)
        self.__scroll_to_bottom__()
        self.__scrap_links__(0)
    
    

if __name__ == "__main__":
    seller = Seller()
    seller.scrap()

#обращаюсь в бд к последней шмотке и запоминаю ее дату
#позже и больше чем неделя дальше не смотрю
#как только все шмотки просмотрел обновляю бд