# dualsense-ros2

PS5 DualSense コントローラを ROS 2 (Humble) から使うための最小構成パッケージ群。

`pydualsense` でコントローラの入力を読み取り、`custom_messages/Gamepad` として
publish する。LED・振動・アダプティブトリガへのフィードバックにも対応する。

`custom_messages` は DualSense 用の 2 メッセージ（`Gamepad` / `DualSenseFeedback`）
のみを含む最小構成。他プロジェクトから git submodule で参照して使うことを想定している。

## パッケージ

| パッケージ | 種別 | 内容 |
|---|---|---|
| `custom_messages` | ament_cmake | `Gamepad.msg` / `DualSenseFeedback.msg` の定義 |
| `dualsense` | ament_python | `dualsense_node`（入力publish + フィードバックsubscribe） |

## トピック

| 方向 | トピック | 型 | QoS |
|---|---|---|---|
| publish | `/gamepad/p{player}` | `custom_messages/Gamepad` | BEST_EFFORT, depth 10 |
| subscribe | `/dualsense/feedback` | `custom_messages/DualSenseFeedback` | default |

`player` パラメータ（既定 1）でトピック名の末尾が決まる。複数台つなぐときに使う。

### `Gamepad` メッセージ

ボタンは `bool`（a/b/x/y, 十字, lb/rb/lt/rt, back/start/power, ls/rs）、
スティックは `float32 lx/ly/rx/ry`（−1.0〜1.0, デッドゾーン処理済み）、
アナログトリガは `float32 l2/r2`（0.0〜1.0）。

`a=×, b=○, x=□, y=△`（DualSenseの物理ボタン → Xbox配列名でのマッピング）。

## パラメータ

| 名前 | 既定 | 説明 |
|---|---|---|
| `publish_rate` | 100.0 | publish周波数 [Hz] |
| `player` | 1 | トピック `/gamepad/p{player}` の番号 |
| `l2_threshold` | 20 | `lt` を true にする L2 生値のしきい値 |
| `r2_threshold` | 20 | `rt` を true にする R2 生値のしきい値 |
| `stick_deadzone` | 8 | スティックのデッドゾーン（生値, ±128中心） |

## ビルドと起動

colcon ワークスペースの `src/` 以下にこのリポジトリを置いてビルドする。

```bash
# 依存は INSTALL.md を参照（libhidapi / pydualsense / udev ルール）
colcon build --packages-select custom_messages dualsense
source install/setup.bash
ros2 launch dualsense dualsense.launch.py
```

DualSense を USB または Bluetooth で接続してから起動する。

## ライセンス

Apache-2.0。
