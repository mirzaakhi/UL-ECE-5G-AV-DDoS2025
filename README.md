# UL-ECE-5G-AV-DDoS2025

This repository contains the simulation script and raw datasets associated with the proposed UL-ECE-5G-AV-DDoS2025 dataset from our ongoing research. The data is generated using the CARLA simulator to emulate autonomous vehicle (AV) behavior under normal and attack conditions in a 5G-enabled environment. 


## ⚠️ Note on Final Dataset

The final processed dataset (`UL-ECE-5G-AV-DDoS2025.csv`) excludes samples labeled as `Hijacked` under `Attack_Type`.

This decision is made to focus the model training on detecting and differentiating between `Normal` and `DDoS Attack` scenarios.


## 📁 Repository Structure 
```
UL-ECE-5G-AV-DDoS2025/
├── UL-ECE-5G-AV-DDoS2025.csv                     # Final processed dataset without Hijacked attack samples, used for training the proposed model
├── initial_raw_av_DDoSattack_dataset.csv         # Initial raw dataset used to generate the final processed dataset
├── regenerated_raw_av_DDoSattack_dataset.csv     # Raw dataset regenerated using the simulation script
├── av_attack_dataset_generator_carla.py          # CARLA-based simulation script for generating raw dataset
└── README.md                                     # Project description and usage instructions
```

## 📊 Dataset Structure

Each sample in the dataset includes the following 14 features:
```python
["Timestamp", "Latitude", "Longitude", "Speed", "Acceleration",
"Throttle", "Steering", "Brake",
"Network_Latency", "Packet_Loss", "Throughput", "Jitter", "Bandwidth_Utilization",
"Attack_Type"]
```
- **Attack_Type** includes: `Normal`, `DDoS Attack`, and `Hijacked`

## 🧪 Reproducibility

To ensure reproducibility, the simulation script includes:
- Fixed sample count: **5000 samples**
- Fixed random seed: `random.seed(42)`  
- Output: `regenerated_raw_av_DDoSattack_dataset.csv`

## ⚙️ Requirements

- Python 3.7
- CARLA 0.9.14
- CARLA Python API (Ensure `.egg` is available in PYTHONPATH)

## 📝 Citation

If you use this dataset or script, please cite the Zenodo record associated with this research work.

## 📄 License

This project is released under the [MIT License](LICENSE) or [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (choose the one applicable).


