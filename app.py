import random
import math
import numpy as np
import matplotlib.pyplot as plt

def random_palette(k=5):
    # return k random pastel-like colors
    return [(random.random(), random.random(), random.random()) for _ in range(k)]

def heart(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    """
    Generate coordinates for a wobbly heart shape.
    Uses the famous parametric equation for a heart.
    """
    t = np.linspace(0, 2*math.pi, points)

    # 1. 기본적인 하트 방정식 (Parametric equation)
    base_x = 16 * np.sin(t)**3
    base_y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)

    # 2. 하트 크기를 정규화하고 'r' (반지름/크기) 인자를 적용
    # 원본 방정식의 최대/최소값은 대략 -16 ~ +16 사이입니다. 16으로 나누어 정규화합니다.
    x_norm = base_x / 16.0
    y_norm = base_y / 16.0

    # 3. 'wobble' (울퉁불퉁함)을 위한 무작위 반지름 계수 생성
    wobble_factor = 1 + wobble*(np.random.rand(points)-0.5)

    # 4. 최종 좌표 계산: 중심(center) + (방향별 좌표 * 크기 * 울퉁불퉁함)
    # y_norm 앞에 -를 붙여 하트가 위를 향하도록 (포인트가 아래로 가도록) 수정
    x = center[0] + x_norm * r * wobble_factor
    y = center[1] + y_norm * r * wobble_factor

    return x, y

random.seed()  # different art each run
plt.figure(figsize=(7,10))
plt.axis('off')

# background
plt.gca().set_facecolor((0.98,0.98,0.97))

palette = random_palette(6)
n_layers = 8
for i in range(n_layers):
    cx, cy = random.random(), random.random()
    rr = random.uniform(0.15, 0.45)

    # === 여기를 수정했습니다 ===
    # x, y = blob(center=(cx, cy), r=rr, wobble=random.uniform(0.05,0.25))
    x, y = heart(center=(cx, cy), r=rr, wobble=random.uniform(0.05,0.25))
    # ========================

    color = random.choice(palette)
    alpha = random.uniform(0.25, 0.6)
    plt.fill(x, y, color=color, alpha=alpha, edgecolor=(0,0,0,0))

# simple typographic label
plt.text(0.05, 0.95, "Generative Poster", fontsize=18, weight='bold', transform=plt.gca().transAxes)
plt.text(0.05, 0.91, "Week 2 • Arts & Advanced Big Data", fontsize=11, transform=plt.gca().transAxes)

plt.xlim(0,1); plt.ylim(0,1)
plt.show()
