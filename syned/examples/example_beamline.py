
from syned.storage_ring.electron_beam import ElectronBeam
from syned.storage_ring.magnetic_structures.undulator import Undulator

from syned.storage_ring.light_source import LightSource

if __name__ == "__main__":



    src1 = ElectronBeam.initialize_as_pencil_beam(energy_in_GeV=6.0,current=0.2)
    src2 = Undulator()
    src = LightSource("test",src1,src2)

    for key in src1.keys():
        print(key,src1.to_dictionary()[key])








    for key in src2.keys():
        print(key,src2.to_dictionary()[key])



    print(src1.keys())
    print(src2.keys())

    print(src1.info())
    print(src2.info())

    print("==================== Beamline Info: ==================")
    print(src.info())


    src2.set_value_from_key_name("K_horizontal",33)

    print(src.info())
    assert (33,src2.get_value_from_key_name("K_horizontal"))

    src1.dump_json("tmp_src1.json")
    src2.dump_json("tmp_src2.json")
