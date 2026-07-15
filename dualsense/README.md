# dualsense

PS5 DualSense コントローラーを ROS2 ノードとして扱うパッケージ。
コントローラー入力を `custom_messages/Gamepad` としてパブリッシュし、
LED・バイブレーション・アダプティブトリガーをサブスクライブで制御する。

## トピック

| 種別 | トピック名 | 型 |
|------|-----------|-----|
| Publish | `/gamepad/p{player}` | `custom_messages/msg/Gamepad` |
| Subscribe | `/dualsense/feedback` | `custom_messages/msg/DualSenseFeedback` |

## ボタンマッピング

| DualSense | `Gamepad` フィールド |
|-----------|---------------------|
| Cross (✕) | `a` |
| Circle (○) | `b` |
| Square (□) | `x` |
| Triangle (△) | `y` |
| L1 | `lb` |
| R1 | `rb` |
| L2 (閾値超え) | `lt` (bool) |
| R2 (閾値超え) | `rt` (bool) |
| L2 アナログ | `l2` (0.0〜1.0) |
| R2 アナログ | `r2` (0.0〜1.0) |
| 十字キー上 | `up` |
| 十字キー右 | `right` |
| 十字キー下 | `down` |
| 十字キー左 | `left` |
| Create | `back` |
| Options | `start` |
| PS ボタン | `power` |
| L3 (左スティック押し込み) | `ls` |
| R3 (右スティック押し込み) | `rs` |
| 左スティック X | `lx` (-1.0〜1.0) |
| 左スティック Y | `ly` (-1.0〜1.0) |
| 右スティック X | `rx` (-1.0〜1.0) |
| 右スティック Y | `ry` (-1.0〜1.0) |

## パラメータ

| パラメータ | デフォルト | 説明 |
|-----------|-----------|------|
| `publish_rate` | `100.0` | パブリッシュ周波数 (Hz) |
| `player` | `1` | トピック番号 (`/gamepad/p1` など) |
| `l2_threshold` | `20` | `lt` (bool) 判定しきい値 (0-255) |
| `r2_threshold` | `20` | `rt` (bool) 判定しきい値 (0-255) |
| `stick_deadzone` | `8` | スティックのデッドゾーン (0-128) |

## 起動

```bash
ros2 launch dualsense dualsense.launch.py
```

パラメータを変更する場合：

```bash
ros2 launch dualsense dualsense.launch.py publish_rate:=50.0 player:=2
```

---

## 入力の確認

```bash
# Gamepad トピックをリアルタイム表示
ros2 topic echo /gamepad/p1

# 周波数確認
ros2 topic hz /gamepad/p1
```

---

## フィードバックのテスト

ノードが起動している状態で以下のコマンドを別ターミナルから実行する。

### LED カラー変更

```bash
# 赤
ros2 topic pub --once /dualsense/feedback custom_messages/msg/DualSenseFeedback \
  '{led_r: 255, led_g: 0, led_b: 0}'

# 緑
ros2 topic pub --once /dualsense/feedback custom_messages/msg/DualSenseFeedback \
  '{led_r: 0, led_g: 255, led_b: 0}'

# 青
ros2 topic pub --once /dualsense/feedback custom_messages/msg/DualSenseFeedback \
  '{led_r: 0, led_g: 0, led_b: 255}'

# 消灯
ros2 topic pub --once /dualsense/feedback custom_messages/msg/DualSenseFeedback \
  '{led_r: 0, led_g: 0, led_b: 0}'
```

### バイブレーション

```bash
# 左モーター（弱め）
ros2 topic pub --once /dualsense/feedback custom_messages/msg/DualSenseFeedback \
  '{rumble_left: 100, rumble_right: 0}'

# 右モーター（弱め）
ros2 topic pub --once /dualsense/feedback custom_messages/msg/DualSenseFeedback \
  '{rumble_left: 0, rumble_right: 100}'

# 両方（強め）
ros2 topic pub --once /dualsense/feedback custom_messages/msg/DualSenseFeedback \
  '{rumble_left: 200, rumble_right: 200}'

# バイブ停止
ros2 topic pub --once /dualsense/feedback custom_messages/msg/DualSenseFeedback \
  '{rumble_left: 0, rumble_right: 0}'
```

### アダプティブトリガー

`trigger_l_mode` / `trigger_r_mode` の値：

| 値 | モード | 説明 |
|----|--------|------|
| `0` | Off | 抵抗なし（デフォルト） |
| `1` | Rigid | 固定の抵抗感 |
| `2` | Pulse_A | パルス振動 |

`trigger_l_force` / `trigger_r_force` は抵抗の強さ (0-255)。

```bash
# 両トリガーを硬くする（Rigid, 最大強度）
ros2 topic pub --once /dualsense/feedback custom_messages/msg/DualSenseFeedback \
  '{trigger_l_mode: 1, trigger_l_force: 255, trigger_r_mode: 1, trigger_r_force: 255}'

# 両トリガーをパルスにする
ros2 topic pub --once /dualsense/feedback custom_messages/msg/DualSenseFeedback \
  '{trigger_l_mode: 2, trigger_l_force: 128, trigger_r_mode: 2, trigger_r_force: 128}'

# トリガー解除
ros2 topic pub --once /dualsense/feedback custom_messages/msg/DualSenseFeedback \
  '{trigger_l_mode: 0, trigger_l_force: 0, trigger_r_mode: 0, trigger_r_force: 0}'
```

### 全部まとめて送る例

```bash
# 赤LED + 両バイブ + 右トリガー硬め
ros2 topic pub --once /dualsense/feedback custom_messages/msg/DualSenseFeedback \
  '{led_r: 255, led_g: 0, led_b: 0, rumble_left: 100, rumble_right: 100, trigger_r_mode: 1, trigger_r_force: 200}'
```

### 全リセット

```bash
ros2 topic pub --once /dualsense/feedback custom_messages/msg/DualSenseFeedback \
  '{led_r: 0, led_g: 0, led_b: 0, rumble_left: 0, rumble_right: 0, trigger_l_mode: 0, trigger_l_force: 0, trigger_r_mode: 0, trigger_r_force: 0}'
```
