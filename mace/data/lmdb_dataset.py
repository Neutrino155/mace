from mace.data.atomic_data import AtomicData
from mace.data.utils import Configuration
from fairchem.core.datasets import AseDBDataset
from torch.utils.data import Dataset
from mace.tools.utils import AtomicNumberTable

class LMDBDataset(Dataset):
    def __init__(self, file_path, r_max, z_table, **kwargs):
        dataset_paths = [
              file_path,
              # "/path/to/omat24/train/rattled-relax",
              # "train/rattled-1000-subsampled",
              # "/path/to/omat24/train/rattled-1000"
        ] 
        config_kwargs = {}
        super(LMDBDataset, self).__init__() # pylint: disable=super-with-arguments
        self.AseDB = AseDBDataset(config=dict(src=dataset_paths, **config_kwargs))
        self.r_max = r_max
        self.z_table = z_table

        self.kwargs = kwargs
        self.transform = kwargs['transform'] if 'transform' in kwargs else None

    def __len__(self):
        return len(self.AseDB)

    def __getitem__(self, index):
        try:
            atoms = self.AseDB.get_atoms(self.AseDB.ids[index])
        except:
            import ipdb; ipdb.set_trace()
            print(index)
            print(len(self.AseDB.ids))
            raise NotImplementedError
        config = Configuration(
            atomic_numbers=atoms.numbers,
            positions=atoms.positions,
            energy=atoms.get_potential_energy(),
            forces=atoms.get_forces(),
            stress=atoms.get_stress(),
            virials=None,
            dipole=None,
            charges=None,
            weight=1.0,
            head=None, # do not asign head according to h5
            energy_weight=1.0,
            forces_weight=1.0,
            stress_weight=1.0,
            virials_weight=1.0,
            config_type=None,
            pbc=atoms.pbc,
            cell=atoms.cell,
            alex_config_id=None,
        )
        if config.head is None:
            config.head = self.kwargs.get("head")
        try:
            atomic_data = AtomicData.from_config(
                    config,
                    z_table=self.z_table,
                    cutoff=self.r_max,
                    heads=self.kwargs.get("heads", ["Default"]),
            )
        except:
            import ipdb; ipdb.set_trace()

        if self.transform:
            atomic_data = self.transform(atomic_data)
        return atomic_data

if __name__ == "__main__":
    db = LMDBDataset(None, 5.0, AtomicNumberTable(range(1, 120)))
    print(db[0])

    from mace.tools import torch_geometric 
    loader = torch_geometric.dataloader.DataLoader(
        db, batch_size=128, num_workers=12, shuffle=False
    )
    for b in loader:
        print(b)
