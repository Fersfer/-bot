from multiprocessing import freeze_support

from ultralytics import YOLO

def print_metrics(metrics, name):
    print(f"🔍 {name}")
    for k, v in metrics.items():
        print(f"{k:30}: {v:.4f}")
    print("-" * 40)

def compare_models():
    new_model_path = r"D:\mob_detector\mob_detector\yolov8n_mob2\weights\best.pt"
    old_model_path = r"D:\mob_detector\mob_detector\yolov8n_mob22\weights\best.pt"
    data_yaml = "data.yaml"
    img_size = 512

# === ЗАВАНТАЖЕННЯ МОДЕЛЕЙ ===
    new_model = YOLO(new_model_path)
    old_model = YOLO(old_model_path)

# === ВАЛІДАЦІЯ МОДЕЛЕЙ ===
    metrics1 = new_model.val(data=data_yaml, imgsz=img_size, split="val", verbose=False)
    metrics2 = old_model.val(data=data_yaml, imgsz=img_size, split="val", verbose=False)

# === ЗБІР МЕТРИК ===
    m1 = metrics1.results_dict
    m2 = metrics2.results_dict

    print_metrics(m1, "Model 1")
    print_metrics(m2, "Model 2")

    # Дістаємо ключ, якщо є:
    key = "metrics/mAP50-95(B)"  # ← тут правильна назва
    if key not in m1 or key not in m2:
        print(f"❌ Помилка: ключ '{key}' не знайдений у результатах.")
        return



    better = "Model 1 ✅" if m1[key] > m2[key] else "Model 2 ✅"

# === ФОРМУВАННЯ ЗВІТУ ===
    report = f"""
📊 COMPARISON REPORT

🔹 New Model: {new_model_path}
mAP50-95: {m1['metrics/mAP50-95']:.4f}
mAP50   : {m1['metrics/mAP50']:.4f}
Precision: {m1['metrics/precision']:.4f}
Recall   : {m1['metrics/recall']:.4f}

🔸 Old Model: {old_model_path}
mAP50-95: {m2['metrics/mAP50-95']:.4f}
mAP50   : {m2['metrics/mAP50']:.4f}
Precision: {m2['metrics/precision']:.4f}
Recall   : {m2['metrics/recall']:.4f}

✅ BEST MODEL: {'New Model ✅' if m1['metrics/mAP50-95'] > m2['metrics/mAP50-95'] else 'Old Model ✅'}
"""

# === ЗБЕРЕЖЕННЯ У ФАЙЛ ===
    with open("compare_report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    print(report)  # Показати вивід тут же

if __name__ == "__main__":
    freeze_support()
    compare_models()
