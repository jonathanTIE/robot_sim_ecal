from Trilateration_TDOA.POC_v1.tdoa_old import Station, Position, HEIGHT_SPK, trilateration_3d_tdoa

####DECODER SETTINGS ####



#### TDOA SETTINGS ####
station1 = Station(Position(0, 0, HEIGHT_SPK))
station2 = Station(Position(1.5, 2.0, HEIGHT_SPK))
station3 = Station(Position(3.0, 0, HEIGHT_SPK))

def process_tdoa(delay2, delay3):
    distance1 = 
    station4, distance4 = station1.gen_ghost_station(station1, distance1)
    station5, distance5 = station2.gen_ghost_station(station2, distance2)
    station6, distance6 = station3.gen_ghost_station(station3, distance3)
    trilateration_3d_tdoa([station1.pos.to_array(), station2.pos.to_array(), station3.pos.to_array(),
        station4.pos.to_array(), station5.pos.to_array(), station6.pos.to_array()], 
        [delay2, delay3, toa14, toa15, toa16])
