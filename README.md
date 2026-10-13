# ROS 2 Lab Exercises for Mobile Robotics

A set of four new ROS 2 (Kilted) lab exercises for the Mobile Robotics course: workspaces and packages, publishers and subscribers, LiDAR processing with TF frames, and 2D/3D mapping with SLAM Toolbox and OctoMap on a simulated TurtleBot3. I wrote the lab handouts and the accompanying example and solution packages. The final versions published on the course website were reviewed and edited by the course's teaching assistant Tarik Pozderac.

> **Note:** Apart from this summary, everything in this project is written in Bosnian: the rest of this README, the source code, the comments and the technical documentation.

> **Napomena:** Izvorni kod, komentari i tehnička dokumentacija za ovaj projekat su napisani na bosanskom jeziku.

## O projektu

Laboratorijske vježbe pripremljene su za predmet **Mobilna robotika** na Elektrotehničkom fakultetu Univerziteta u Sarajevu (akademska 2025/2026. godina). Cilj vježbi je upoznati studente s radom u ROS 2 okruženju na primjeru simuliranog robota TurtleBot3 u simulatoru Gazebo.

Autorica sam uputa za vježbe i pratećih ROS 2 paketa u ovom repozitoriju. Konačne verzije uputa objavljene na stranici predmeta pregledao je i dopunio asistent na predmetu, pa se mogu razlikovati od verzija u ovom repozitoriju.

## Sadržaj vježbi

| Vježba | Tema | Paketi |
|---|---|---|
| **LV1** | Instalacija ROS 2, radni prostor (*workspace*), *overlay* i *underlay*, kreiranje paketa, prvi čvor, publisher i subscriber, launch datoteke | `moj_paket`, `cpp_pubsub` |
| **LV2** | Turtlesim, osnovne ROS 2 komande (čvorovi, teme, servisi, akcije), Gazebo i TurtleBot3, upravljanje robotom na osnovu odometrije | `cpp_pubsub` |
| **LV3** | Rad s LiDAR podacima (`sensor_msgs/LaserScan`), pronalazak najbliže prepreke, statičke TF transformacije i vlastiti koordinatni okviri | `lidar_vjezba` |
| **LV4** | 2D mapiranje sa SLAM Toolboxom, 3D mapiranje s OctoMapom i bojenje oblaka tačaka po visini | `vjezba4` |

### Opis paketa

- **`moj_paket`** (LV1): minimalni C++ čvor kreiran naredbom `ros2 pkg create`.
- **`cpp_pubsub`** (LV1): čvor `listener` prima poruke tipa `geometry_msgs/Twist` na temi `topic`, udvostručuje linearne, a mijenja predznak ugaonih komponenti i rezultat objavljuje na temi `novi_topic`. Launch datoteka pokreće TurtleBot3 (model `waffle`) u praznom Gazebo svijetu i RViz.
- **`cpp_pubsub`** (LV2): proširena verzija u kojoj `listener` čita odometriju (`/odom`), iz kvaterniona računa ugao zakretanja robota i proporcionalnim zakonom upravljanja šalje komande brzine (`/cmd_vel`, `TwistStamped`) kako bi robot stigao u zadanu tačku (3, 3).
- **`lidar_vjezba`** (LV3):
  - `lidar_pubsub` pronalazi najbližu tačku iz LiDAR skeniranja i objavljuje je kao `PointStamped` na temi `/najbliza_tacka`;
  - `moj_scan_pubsub` ponovo objavljuje skeniranje u vlastitom koordinatnom okviru `moj_laser` na temi `/moj_scan`;
  - launch datoteka dodaje statičke transformacije `odom → moj_base_link → moj_laser`.
- **`vjezba4`** (LV4):
  - `moj_mapping.launch.py` pokreće SLAM Toolbox kao *lifecycle* čvor;
  - `moj_octomap.launch.py` povezuje čvor `scan_to_cloud` (pretvara `LaserScan` u `PointCloud2`), `octomap_server` i čvor `colorize_cloud` (boji centre ćelija OctoMape prema visini);
  - paket sadrži i dodatne launch datoteke za RTAB-Map s mostovima prema Gazebo kamerama i za prikaz u RViz-u.

## Struktura repozitorija

```
.
├── LV1/
│   ├── Laboratorijska_vježba_1.pdf
│   └── LV1 kodovi/
│       ├── moj_paket/
│       └── cpp_pubsub/
├── LV2/
│   ├── Laboratorijska_vježba_2.pdf
│   └── LV2 kodovi/cpp_pubsub/
├── LV3/
│   ├── Laboratorijska_vježba_3.pdf
│   └── LV3 kodovi/lidar_vjezba/
└── LV4/
    ├── Laboratorijska_vježba_4.pdf
    └── LV4 kodovi/vjezba4/
```

## Pokretanje

**Preduslovi:** Ubuntu 24.04 (Noble) i ROS 2 Kilted, instaliran prema [zvaničnim uputama](https://docs.ros.org/en/kilted/Installation/Ubuntu-Install-Debs.html), te paketi za simulaciju i mapiranje:

```bash
sudo apt install ros-kilted-turtlesim \
                 ros-kilted-turtlebot3 ros-kilted-turtlebot3-simulations ros-kilted-turtlebot3-teleop \
                 ros-kilted-slam-toolbox \
                 ros-kilted-octomap-server ros-kilted-octomap-msgs ros-kilted-octomap-ros \
                 ros-kilted-laser-geometry
```

### Izgradnja paketa

Svaka vježba ima vlastitu verziju paketa, pa se u radni prostor kopiraju paketi samo one vježbe koja se radi. Paket `cpp_pubsub` postoji u verzijama za LV1 i LV2 s istim imenom.

```bash
mkdir -p ~/ros2_ws/src
cp -r "LV3/LV3 kodovi/lidar_vjezba" ~/ros2_ws/src/
cd ~/ros2_ws
source /opt/ros/kilted/setup.bash
colcon build
source install/setup.bash
```

### Primjeri pokretanja

```bash
# LV1 i LV2: simulacija i čvor
ros2 launch cpp_pubsub moj_launch.launch.py
ros2 run cpp_pubsub listener

# LV3: TurtleBot3 u svijetu s preprekama i obrada LiDAR podataka
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
ros2 run lidar_vjezba lidar_pubsub
ros2 launch lidar_vjezba moj_laser_scanner.launch.py

# LV4: 2D i 3D mapiranje
ros2 launch vjezba4 moj_mapping.launch.py
ros2 launch vjezba4 moj_octomap.launch.py
```

Detaljan postupak, očekivani ispisi i zadaci za studente nalaze se u PDF uputama za svaku vježbu.

## Autor

- **Autorica uputa i koda:** Berina Biberović
- **Predmet:** Mobilna robotika, Elektrotehnički fakultet, Univerzitet u Sarajevu
- **Predmetni profesor:** prof. dr Jasmin Velagić
- **Predmetni asistent:** Tarik Pozderac
