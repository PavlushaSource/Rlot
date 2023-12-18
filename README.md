# Rlot 

A utility for testing the performance of different RAID arrays of kernel space and user space

## Features
- Support for testing any of your mounted block devices
- Support for automatic launch of Mdadm RAID implementation _(kernel space)_
- Support for SPDK RAID implemepython3 -m pip install -r requirements.txtntations. __Important__: The file for the description of the SPDK RAID device is not generated automatically

## TO-DO
1. Implement support for more than just IOPs graphs.
2. Write an automatic generation .JSON file for SPDK RAID
3. Add more RAID array implementations such as ZFS and others

---
## Get started

### Installation
```
git clone https://github.com/PavlushaSource/Rlot.git
cd Rlot
```
### Prerequisites
**Source requirements**
```
python3 -m pip install -r requirements.txt
```
**MDADM is a utility for testing the performance RAID from kernel space**
```
sudo apt update
sudo apt install mdadm
```
**SPDK RAID arrays for testing the performance of RAID implementations from user space**
1. Download and build [SPDK_FIO](https://github.com/spdk/spdk/tree/master/examples/bdev/fio_plugin)
2. Download [SPDK](https://github.com/spdk/spdk)
3. Build SPDK
   ```
   python3 -m venv venv-spdk
   source venv-spdk/bin/activate
   sudo scripts/setup.sh
   sudo scripts/pkgdep.sh
   sudo ./configure --with-fio=/path/to/fio/repo
   sudo make
   ```
## Usage
All examples of configuration files are located in ./templates
### Configuration file

<table>
<tr>
<th> Bdev </th>
<th> Mdadm </th>
<th> SPDK </th>
</tr>
<tr>
<td>

```
[global]
ioengine=libaio
invalidate=1
ramp_time=5
size=4K
iodepth = 32
numjobs = 1
runtime = 120
bs = 4K
rw = write, read
dev = /dev/sdb
```

</td>
<td>

```
[global]
ioengine=libaio
iodepth = 1
numjobs = 1
rw = write, read, randread, randwrite

[raid]
dev = /dev/sdb, /dev/sdc, /dev/sdd
number_realization = 0
```

</td>

<td>

```
[global]
ioengine=spdk_bdev
ramp_time=5
rw = write

[spdk]
dev = /dev/sdb, /dev/sdc, /dev/sdd
number_realization = 0
spdk_json_conf = None
```
  
</td>
</tr>
</table>

Some of them can be __omitted__, then the parameters will be taken from the file `./resources/default_<name>.ini`
#### Parameters that cannot be skipped
- `ioengine`
- `dev`
- `number_realization` _(for every RAID)_
- `spdk_json_conf` _(for SPDK. Example [here](https://github.com/spdk/spdk/blob/master/examples/bdev/fio_plugin/bdev.json))_
### Running
```
python3 -m rlot_app <path_to_conf_file.ini> <optional_param_path_to_output_graph_folder>
```
## Output
<img src=https://github.com/PavlushaSource/Rlot/blob/feat/bdev/resources/read_graph_iops-11-12-2023-17-32-52.png alt="" width="500">
<figcaption>IOPs graph output</figcaption>

## License
This project is licensed under the terms of the GPL-3.0 license. See the [LICENSE](https://www.gnu.org/licenses/gpl-3.0.html) for more information.
