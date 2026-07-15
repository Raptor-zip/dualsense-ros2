# dualsense-ros2 インストール

## 動作環境

- Ubuntu 22.04 LTS
- ROS 2 Humble

## 1. システムライブラリ

```bash
sudo apt install -y libhidapi-hidraw0 libhidapi-libusb0
# Bluetooth 接続で使う場合
sudo apt install -y bluez
```

## 2. Python パッケージ（pydualsense）

`dualsense_node` は `pydualsense` に依存する。ワークスペースの Python 環境へ入れる。

```bash
# uv を使う場合（推奨）
uv venv --python 3.10
uv pip install pydualsense

# もしくは pip
pip install pydualsense
```

## 3. udev ルール（一般ユーザーから HID デバイスへアクセスするために必要）

```bash
sudo tee /etc/udev/rules.d/70-dualsense.rules << 'EOF'
# Sony DualSense (PS5) - USB
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="054c", ATTRS{idProduct}=="0ce6", MODE="0666"
# Sony DualSense Edge (PS5) - USB
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="054c", ATTRS{idProduct}=="0df2", MODE="0666"
EOF

sudo udevadm control --reload-rules
sudo udevadm trigger
```

設定後、コントローラを一度抜いて再接続する。

## 4. ビルド

```bash
colcon build --packages-select custom_messages dualsense
source install/setup.bash
ros2 launch dualsense dualsense.launch.py
```

## トラブルシューティング

- `pydualsense` の `init()` でデバイスが見つからない → udev ルールを再確認し、
  コントローラを再接続する。Bluetooth の場合は先にペアリングしておく。
- `hidapi` 関連の import エラー → `libhidapi-hidraw0 libhidapi-libusb0` を入れ直す。
